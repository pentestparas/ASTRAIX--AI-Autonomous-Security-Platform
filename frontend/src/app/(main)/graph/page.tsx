"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import ReactFlow, {
  Background,
  BackgroundVariant,
  Controls,
  MiniMap,
  type Node,
  type Edge,
  type NodeProps,
} from "reactflow";
import dagre from "dagre";
import { apiClient } from "@/services/api";
import { LayoutGrid, MoveHorizontal, Orbit, RotateCw } from "lucide-react";

const GROUP_META: Record<string, { label: string; color: string; glyph: string }> = {
  target: { label: "Target", color: "#38bdf8", glyph: "◆" },
  port: { label: "Port", color: "#818cf8", glyph: "▣" },
  service: { label: "Service", color: "#34d399", glyph: "⬡" },
  finding: { label: "Finding", color: "#f87171", glyph: "●" },
  tool: { label: "Tool", color: "#fbbf24", glyph: "★" },
};

const SEVERITY_COLORS: Record<string, string> = {
  critical: "#f87171",
  high: "#fb923c",
  medium: "#facc15",
  low: "#4ade80",
  info: "#94a3b8",
};

const GROUP_WIDTH: Record<string, number> = { target: 150, port: 120, service: 130, finding: 84, tool: 110 };

type GraphNodeData = {
  label: string;
  group: string;
  severity?: string;
  info: string;
};

function GraphNode({ data }: NodeProps) {
  const meta = GROUP_META[data.group] || GROUP_META.finding;
  const sevColor = data.severity ? SEVERITY_COLORS[data.severity.toLowerCase()] : null;
  const isFinding = data.group === "finding";
  const color = isFinding ? sevColor || meta.color : meta.color;
  const width = GROUP_WIDTH[data.group] || 84;

  return (
    <div
      className="flex items-center gap-2 rounded-lg border bg-card/95 px-2 py-1.5 backdrop-blur transition-colors hover:border-primary/50"
      style={{
        width,
        borderColor: `${color}66`,
        boxShadow: `0 0 14px -4px ${color}40, inset 0 1px 0 hsl(210 40% 98% / 0.04)`,
      }}
    >
      <span
        className="flex items-center justify-center w-5 h-5 rounded-md text-[10px] font-bold flex-shrink-0"
        style={{ background: `${color}22`, color }}
      >
        {meta.glyph}
      </span>
      <span
        className="text-[11px] font-medium truncate"
        style={{ color: "#e2e8f0", textShadow: "0 1px 2px rgba(0,0,0,0.8)" }}
        title={data.label}
      >
        {data.label}
      </span>
    </div>
  );
}

const nodeTypes = { graphNode: GraphNode };

type RawNode = { id: string; label: string; group: string; severity: string; title: string };
type RawEdge = { from: string; to: string; label: string };
type LayoutMode = "lr" | "tb" | "radial";

function edgeColor(e: RawEdge): string {
  if (e.to === "finding" || e.label === "finding") return "#f87171";
  if (e.from === "tool") return "#fbbf24";
  return "#64748b";
}

function layoutDagre(rawNodes: RawNode[], rawEdges: RawEdge[], rankdir: "LR" | "TB") {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({
    rankdir,
    nodesep: 18,
    ranksep: 90,
    marginx: 40,
    marginy: 40,
  });
  rawNodes.forEach((n) => {
    g.setNode(n.id, { width: GROUP_WIDTH[n.group] || 84, height: 34 });
  });
  rawEdges.forEach((e) => {
    if (!g.hasNode(e.from) || !g.hasNode(e.to)) return;
    g.setEdge(e.from, e.to);
  });
  dagre.layout(g);

  const positions = new Map<string, { x: number; y: number }>();
  rawNodes.forEach((n) => {
    const layout = g.node(n.id);
    if (!layout) return;
    positions.set(n.id, { x: layout.x - (GROUP_WIDTH[n.group] || 84) / 2, y: layout.y - 17 });
  });
  return positions;
}

function layoutRadial(rawNodes: RawNode[], rawEdges: RawEdge[]) {
  const order = ["target", "port", "service", "tool", "finding"];
  const radii: Record<string, number> = { target: 0, port: 150, service: 270, tool: 360, finding: 450 };
  const positions = new Map<string, { x: number; y: number }>();
  const counts: Record<string, number> = {};
  rawNodes.forEach((n) => {
    counts[n.group] = (counts[n.group] || 0) + 1;
  });
  const cursor: Record<string, number> = {};
  rawNodes.forEach((n) => {
    const r = radii[n.group] ?? 300;
    const total = counts[n.group] || 1;
    const idx = cursor[n.group] || 0;
    cursor[n.group] = idx + 1;
    if (r === 0) {
      positions.set(n.id, { x: -60, y: -17 });
      return;
    }
    const angle = (idx / total) * Math.PI * 2 - Math.PI / 2;
    positions.set(n.id, { x: Math.cos(angle) * r - (GROUP_WIDTH[n.group] || 84) / 2, y: Math.sin(angle) * r - 17 });
  });
  return positions;
}

function computeLayout(rawNodes: RawNode[], rawEdges: RawEdge[], mode: LayoutMode) {
  if (mode === "radial") return layoutRadial(rawNodes, rawEdges);
  return layoutDagre(rawNodes, rawEdges, mode === "lr" ? "LR" : "TB");
}

export default function GraphPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [layoutMode, setLayoutMode] = useState<LayoutMode>("lr");
  const [selectedNode, setSelectedNode] = useState<{ id: string; label: string; info: string } | null>(null);
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);
  const [stats, setStats] = useState({ targets: 0, ports: 0, findings: 0, services: 0 });

  const buildGraph = useMemo(
    () => async (rawNodes: RawNode[], rawEdges: RawEdge[]) => {
      const layout = computeLayout(rawNodes, rawEdges, layoutMode);
      setNodes(
        rawNodes.map((n) => {
          const gw = GROUP_WIDTH[n.group] || 84;
          return {
            id: n.id,
            type: "graphNode",
            position: layout.get(n.id) || { x: Math.random() * 800, y: Math.random() * 500 },
            style: { width: gw, height: 34 },
            data: { label: n.label, group: n.group, severity: n.severity, info: n.title || "" } as GraphNodeData,
          };
        })
      );
      setEdges(
        rawEdges.map((e) => ({
          id: `${e.from}->${e.to}`,
          source: e.from,
          target: e.to,
          type: "smoothstep",
          animated: true,
          label: e.label || undefined,
          style: { stroke: edgeColor(e), strokeWidth: 1.4 },
          labelStyle: { fill: "#94a3b8", fontSize: 9 },
          labelBgStyle: { fill: "#0f172a", fillOpacity: 0.8, stroke: "#1e293b", strokeWidth: 1 },
        }))
      );
    },
    [layoutMode]
  );

  const dataRef = useRef<{ nodes: RawNode[]; edges: RawEdge[] } | null>(null);

  useEffect(() => {
    let mounted = true;

    async function initGraph() {
      try {
        const res = await apiClient.get<{ nodes: any[]; edges: any[] }>("/graph");
        if (!mounted) return;
        const rawNodes: RawNode[] = res.data?.nodes || [];
        const rawEdges: RawEdge[] = res.data?.edges || [];

        if (!rawNodes.length) {
          setLoading(false);
          setError("No graph data available. Run a scan first.");
          return;
        }

        dataRef.current = { nodes: rawNodes, edges: rawEdges };
        setStats({
          targets: rawNodes.filter((n) => n.group === "target").length,
          ports: rawNodes.filter((n) => n.group === "port").length,
          findings: rawNodes.filter((n) => n.group === "finding").length,
          services: rawNodes.filter((n) => n.group === "service").length,
        });
        await buildGraph(rawNodes, rawEdges);
        setLoading(false);
      } catch (e: any) {
        if (mounted) {
          setError(e?.message || "Failed to load graph data");
          setLoading(false);
        }
      }
    }

    initGraph();

    return () => {
      mounted = false;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function changeLayout(mode: LayoutMode) {
    setLayoutMode(mode);
  }

  useEffect(() => {
    if (dataRef.current) {
      void buildGraph(dataRef.current.nodes, dataRef.current.edges);
    }
  }, [buildGraph]);

  const selectedInfo = useMemo(() => selectedNode, [selectedNode]);

  const layoutOptions: { id: LayoutMode; label: string; icon: typeof MoveHorizontal }[] = [
    { id: "lr", label: "Left → Right", icon: MoveHorizontal },
    { id: "tb", label: "Top → Bottom", icon: LayoutGrid },
    { id: "radial", label: "Radial", icon: Orbit },
  ];

  return (
    <div className="h-[calc(100vh-3rem)] flex flex-col">
      <div className="flex items-center justify-between mb-4 gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Attack Surface Graph</h1>
          <p className="text-muted-foreground text-sm mt-1">Neo4j knowledge graph visualization of scan results</p>
        </div>
        <div className="flex items-center gap-3">
          <div className="flex p-1 gap-1 bg-secondary/60 border border-border rounded-lg">
            {layoutOptions.map((opt) => (
              <button
                key={opt.id}
                onClick={() => changeLayout(opt.id)}
                className={`flex items-center gap-1.5 px-2.5 py-1.5 rounded-md text-xs font-medium transition-colors ${
                  layoutMode === opt.id
                    ? "bg-primary/15 text-primary border border-primary/30"
                    : "text-muted-foreground hover:text-foreground border border-transparent"
                }`}
              >
                <opt.icon className="w-3.5 h-3.5" />
                {opt.label}
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            <StatBadge label="targets" count={stats.targets} />
            <StatBadge label="ports" count={stats.ports} />
            <StatBadge label="services" count={stats.services} />
            <StatBadge label="findings" count={stats.findings} />
          </div>
        </div>
      </div>

      <div className="flex-1 flex gap-4 min-h-0">
        <div ref={containerRef} className="flex-1 glass-card overflow-hidden relative">
          {loading && (
            <div className="absolute inset-0 flex items-center justify-center bg-card/80 z-10">
              <div className="flex flex-col items-center gap-3">
                <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
                <p className="text-sm text-muted-foreground">Loading attack surface graph...</p>
              </div>
            </div>
          )}
          {error && (
            <div className="absolute inset-0 flex items-center justify-center bg-card/80 z-10">
              <div className="text-center max-w-md">
                <p className="text-muted-foreground">{error}</p>
              </div>
            </div>
          )}
          {!loading && !error && (
            <ReactFlow
              key={layoutMode}
              nodes={nodes}
              edges={edges}
              nodeTypes={nodeTypes}
              fitView
              fitViewOptions={{ padding: 0.14, maxZoom: 1.3 }}
              minZoom={0.03}
              nodesDraggable
              nodesConnectable={false}
              proOptions={{ hideAttribution: true }}
              defaultEdgeOptions={{ type: "smoothstep" }}
              onNodeClick={(_event, node) => {
                const data = node.data as GraphNodeData;
                setSelectedNode({ id: node.id, label: data.label, info: data.info });
              }}
              onPaneClick={() => setSelectedNode(null)}
              style={{ background: "transparent" }}
            >
              <Background variant={BackgroundVariant.Dots} color="#334155" gap={22} size={1.2} />
              <MiniMap
                pannable
                zoomable
                nodeColor={(n) => {
                  const d = n.data as GraphNodeData;
                  if (!d) return "#334155";
                  if (d.group === "finding") return SEVERITY_COLORS[d.severity?.toLowerCase() || "info"] || "#f87171";
                  return GROUP_META[d.group]?.color || "#334155";
                }}
                className="!bg-card/90 !border-border"
              />
              <Controls className="!bg-card !border-border [&>button]:!bg-card [&>button]:!text-foreground [&>button]:hover:!bg-accent" />
            </ReactFlow>
          )}
        </div>

        {selectedInfo && (
          <div className="w-72 glass-card rounded-xl p-4 overflow-y-auto">
            <h3 className="font-semibold text-sm mb-3">Node Detail</h3>
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-xs text-muted-foreground block">Label</span>
                <p className="font-medium">{selectedInfo.label}</p>
              </div>
              <div>
                <span className="text-xs text-muted-foreground block">ID</span>
                <p className="font-mono text-xs truncate">{selectedInfo.id}</p>
              </div>
              {selectedInfo.info && (
                <div>
                  <span className="text-xs text-muted-foreground block">Details</span>
                  <div className="text-xs mt-1 leading-relaxed" dangerouslySetInnerHTML={{ __html: selectedInfo.info }} />
                </div>
              )}
            </div>
          </div>
        )}

        <Legend />
      </div>
    </div>
  );
}

function StatBadge({ label, count }: { label: string; count: number }) {
  return (
    <div className="flex items-center gap-1.5 px-3 py-1.5 bg-secondary/60 border border-border rounded-lg">
      <span className="text-sm font-semibold">{count}</span>
      <span className="text-xs text-muted-foreground">{label}</span>
    </div>
  );
}

function Legend() {
  return (
    <div className="w-56 bg-card border rounded-xl p-4 space-y-3 overflow-y-auto">
      <h3 className="font-semibold text-sm">Legend</h3>
      {Object.entries(GROUP_META).map(([group, meta]) => (
        <div key={group} className="flex items-center gap-2 text-sm">
          <span
            className="w-4 h-4 rounded flex items-center justify-center text-[10px] font-bold flex-shrink-0"
            style={{ background: `${meta.color}22`, color: meta.color }}
          >
            {meta.glyph}
          </span>
          <span className="capitalize">{meta.label}</span>
        </div>
      ))}
      <div className="pt-3 border-t mt-3">
        <h4 className="text-xs font-medium text-muted-foreground mb-2">Finding Severity</h4>
        {Object.entries(SEVERITY_COLORS).map(([sev, color]) => (
          <div key={sev} className="flex items-center gap-2 text-xs mb-1">
            <div className="w-3 h-3 rounded-full" style={{ background: color }} />
            <span className="capitalize">{sev}</span>
          </div>
        ))}
      </div>
      <div className="pt-3 border-t text-xs text-muted-foreground">
        <p>Drag to pan · Scroll to zoom · Click a node for details</p>
        <p className="mt-1">Animated edges trace attack paths · findings color by severity</p>
      </div>
    </div>
  );
}