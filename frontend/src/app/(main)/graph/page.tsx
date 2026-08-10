"use client";

import { useEffect, useMemo, useRef, useState } from "react";
import ReactFlow, {
  Background,
  Controls,
  type Node,
  type Edge,
  type NodeProps,
} from "reactflow";
import dagre from "dagre";
import { apiClient } from "@/services/api";

const GROUP_STYLES: Record<string, { shape: string; color: { background: string; border: string }; width: number }> = {
  target: { shape: "diamond", color: { background: "#1a3a5c", border: "#0f2440" }, width: 130 },
  port: { shape: "box", color: { background: "#475569", border: "#334155" }, width: 120 },
  service: { shape: "ellipse", color: { background: "#16a34a", border: "#15803d" }, width: 120 },
  finding: { shape: "dot", color: { background: "#dc2626", border: "#b91c1c" }, width: 64 },
  tool: { shape: "star", color: { background: "#f59e0b", border: "#d97706" }, width: 72 },
};

const SEVERITY_COLORS: Record<string, string> = {
  critical: "#dc2626",
  high: "#ea580c",
  medium: "#ca8a04",
  low: "#65a30d",
  info: "#6b7280",
};

const SHAPE_CLIP: Record<string, string> = {
  diamond: "polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)",
  box: "polygon(0% 0%, 100% 0%, 100% 100%, 0% 100%)",
  ellipse: "polygon(0% 15%, 15% 0%, 85% 0%, 100% 15%, 100% 85%, 85% 100%, 15% 100%, 0% 85%)",
  dot: "polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)",
  star: "polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)",
};

type GraphNodeData = {
  label: string;
  group: string;
  severity?: string;
  info: string;
};

function GraphNode({ data }: NodeProps) {
  const gs = GROUP_STYLES[data.group] || GROUP_STYLES.finding;
  const sevColor = data.severity ? SEVERITY_COLORS[data.severity.toLowerCase()] : null;
  const bg = sevColor || gs.color.background;
  const clip = SHAPE_CLIP[gs.shape] || SHAPE_CLIP.box;
  const isDot = gs.shape === "dot";
  return (
    <div style={{ display: "flex", flexDirection: isDot ? "column" : "row", alignItems: "center", gap: 6, width: gs.width }}>
      <div
        style={{
          clipPath: clip,
          background: bg,
          border: data.group === "finding" ? "none" : undefined,
          boxShadow: "0 0 4px rgba(15, 36, 64, 0.6)",
          flexShrink: 0,
          ...(isDot
            ? { width: 14, height: 14, margin: "0 auto" }
            : { width: 16 + Math.min(gs.width, 130) * 0.28, height: 22 }),
        }}
      />
      {!isDot && (
        <span
          style={{
            color: "#e2e8f0",
            fontSize: data.group === "target" ? 12 : 10,
            fontWeight: data.group === "target" ? 700 : 400,
            lineHeight: 1.2,
            overflow: "hidden",
            textOverflow: "ellipsis",
            whiteSpace: "nowrap",
            maxWidth: gs.width - 34,
            textShadow: "0 1px 2px rgba(0,0,0,0.8)",
          }}
          title={data.label}
        >
          {data.label}
        </span>
      )}
      {isDot && (
        <span style={{ color: "#e2e8f0", fontSize: 9, textAlign: "center" }}>{data.label}</span>
      )}
    </div>
  );
}

const nodeTypes = { graphNode: GraphNode };

type RawNode = { id: string; label: string; group: string; severity: string; title: string };
type RawEdge = { from: string; to: string; label: string };

const GROUP_HEIGHT: Record<string, number> = { target: 44, port: 40, service: 40, finding: 34, tool: 40 };

function computeLayout(rawNodes: RawNode[], rawEdges: RawEdge[]) {
  const g = new dagre.graphlib.Graph();
  g.setDefaultEdgeLabel(() => ({}));
  g.setGraph({
    rankdir: "LR",
    nodesep: 14,
    ranksep: 100,
    marginx: 30,
    marginy: 30,
  });

  rawNodes.forEach((n) => {
    const gw = GROUP_STYLES[n.group]?.width ?? 90;
    const gh = GROUP_HEIGHT[n.group] ?? 40;
    g.setNode(n.id, { width: gw, height: gh });
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
    const gw = GROUP_STYLES[n.group]?.width ?? 90;
    const gh = GROUP_HEIGHT[n.group] ?? 40;
    positions.set(n.id, { x: layout.x - gw / 2, y: layout.y - gh / 2 });
  });
  return positions;
}

export default function GraphPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({ targets: 0, ports: 0, findings: 0, services: 0 });
  const [selectedNode, setSelectedNode] = useState<{ id: string; label: string; info: string } | null>(null);
  const [nodes, setNodes] = useState<Node[]>([]);
  const [edges, setEdges] = useState<Edge[]>([]);

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

        const layout = computeLayout(rawNodes, rawEdges);

        setNodes(
          rawNodes.map((n) => {
            const gw = GROUP_STYLES[n.group]?.width ?? 90;
            const gh = GROUP_HEIGHT[n.group] ?? 40;
            return {
              id: n.id,
              type: "graphNode",
              position: layout.get(n.id) || { x: Math.random() * 800, y: Math.random() * 600 },
              style: { width: gw, height: gh },
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
            label: e.label || undefined,
            style: { stroke: "#475569", strokeWidth: 1 },
            labelStyle: { fill: "#94a3b8", fontSize: 9 },
            labelBgStyle: { fill: "#0f172a", fillOpacity: 0.75, stroke: "#1e293b", strokeWidth: 1 },
          }))
        );

        setStats({
          targets: rawNodes.filter((n) => n.group === "target").length,
          ports: rawNodes.filter((n) => n.group === "port").length,
          findings: rawNodes.filter((n) => n.group === "finding").length,
          services: rawNodes.filter((n) => n.group === "service").length,
        });
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
  }, []);

  const selectedInfo = useMemo(() => selectedNode, [selectedNode]);

  return (
    <div className="h-[calc(100vh-3rem)] flex flex-col">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Attack Surface Graph</h1>
          <p className="text-muted-foreground text-sm mt-1">Neo4j knowledge graph visualization of scan results</p>
        </div>
        <div className="flex gap-3">
          <StatBadge label="targets" count={stats.targets} />
          <StatBadge label="ports" count={stats.ports} />
          <StatBadge label="services" count={stats.services} />
          <StatBadge label="findings" count={stats.findings} />
        </div>
      </div>

      <div className="flex-1 flex gap-4 min-h-0">
        <div ref={containerRef} className="flex-1 bg-card border rounded-xl overflow-hidden relative" style={{ backgroundColor: "#0f172a" }}>
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
              nodes={nodes}
              edges={edges}
              nodeTypes={nodeTypes}
              fitView
              fitViewOptions={{ padding: 0.12, maxZoom: 1.2 }}
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
              style={{ backgroundColor: "#0f172a" }}
            >
              <Background color="#1e293b" gap={24} />
              <Controls />
            </ReactFlow>
          )}
        </div>

        {selectedInfo && (
          <div className="w-72 bg-card border rounded-xl p-4 overflow-y-auto">
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
    <div className="flex items-center gap-1.5 px-3 py-1.5 bg-muted rounded-lg">
      <span className="text-sm font-semibold">{count}</span>
      <span className="text-xs text-muted-foreground">{label}</span>
    </div>
  );
}

function Legend() {
  return (
    <div className="w-56 bg-card border rounded-xl p-4 space-y-3 overflow-y-auto">
      <h3 className="font-semibold text-sm">Legend</h3>
      {Object.entries(GROUP_STYLES).map(([group, style]) => (
        <div key={group} className="flex items-center gap-2 text-sm">
          <div
            className="w-4 h-4 rounded-sm flex-shrink-0"
            style={{ background: style.color.background, clipPath: "polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)" }}
          />
          <span className="capitalize">{group}</span>
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
        <p className="mt-1">Findings color by severity: critical→high→medium→low→info</p>
      </div>
    </div>
  );
}