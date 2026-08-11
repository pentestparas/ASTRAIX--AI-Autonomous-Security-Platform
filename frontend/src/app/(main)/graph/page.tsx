"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
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
import {
  forceSimulation,
  forceLink,
  forceManyBody,
  forceCenter,
  forceCollide,
  forceX,
  forceY,
} from "d3-force";
import { apiClient, projectsApi, assessmentsApi, findingsApi } from "@/services/api";
import {
  LayoutGrid,
  MoveHorizontal,
  Orbit,
  RotateCw,
  CircleDot,
  ShieldAlert,
  Layers,
  Waypoints,
} from "lucide-react";

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

const SEVERITY_RANK: Record<string, number> = {
  critical: 4,
  high: 3,
  medium: 2,
  low: 1,
  info: 0,
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
type LayoutMode = "lr" | "tb" | "radial" | "force";
type Scope = { kind: "graph" } | { kind: "project"; id: string } | { kind: "scan"; id: string };

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

const GROUP_ANCHORS: Record<string, [number, number]> = {
  target: [0, 0],
  port: [-80, -140],
  service: [160, -60],
  tool: [-180, 160],
  finding: [150, 200],
};

function layoutForce(rawNodes: RawNode[], rawEdges: RawEdge[]) {
  interface SimNode extends d3.SimulationNodeDatum {
    id: string;
    group: string;
    width: number;
  }

  const simNodes: SimNode[] = rawNodes.map((n) => ({
    id: n.id,
    group: n.group,
    width: GROUP_WIDTH[n.group] || 84,
    x: (Math.random() - 0.5) * 900,
    y: (Math.random() - 0.5) * 600,
  }));

  const simLinks = rawEdges
    .filter((e) => rawNodes.some((n) => n.id === e.from) && rawNodes.some((n) => n.id === e.to))
    .map((e) => ({ source: e.from, target: e.to }));

  const simulation = forceSimulation<SimNode>(simNodes)
    .force("link", forceLink<SimNode, { source: string; target: string }>(simLinks).id((d) => d.id).distance(120).strength(0.55))
    .force("charge", forceManyBody<SimNode>().strength(-420))
    .force("center", forceCenter(0, 0))
    .force(
      "x",
      forceX<SimNode>((d) => (GROUP_ANCHORS[d.group] || [0, 0])[0]).strength(0.06)
    )
    .force(
      "y",
      forceY<SimNode>((d) => (GROUP_ANCHORS[d.group] || [0, 0])[1]).strength(0.06)
    )
    .force("collide", forceCollide<SimNode>((d) => Math.sqrt(Math.pow(d.width / 2, 2) + 17 * 17) + 10))
    .stop();

  for (let i = 0; i < 400 && simulation.alpha() > 0.005; i++) {
    simulation.tick();
  }

  const positions = new Map<string, { x: number; y: number }>();
  simNodes.forEach((n) => {
    positions.set(n.id, { x: (n.x ?? 0) - n.width / 2, y: (n.y ?? 0) - 17 });
  });
  return positions;
}

function computeLayout(rawNodes: RawNode[], rawEdges: RawEdge[], mode: LayoutMode) {
  if (mode === "force") return layoutForce(rawNodes, rawEdges);
  if (mode === "radial") return layoutRadial(rawNodes, rawEdges);
  return layoutDagre(rawNodes, rawEdges, mode === "lr" ? "LR" : "TB");
}

type GroupedFinding = {
  title: string;
  count: number;
  severity: string;
  tools: string[];
  items: Record<string, any>[];
};

function groupFindings(findings: Record<string, any>[]): GroupedFinding[] {
  const byTitle = new Map<string, Record<string, any>[]>();
  findings.forEach((f) => {
    const key = String(f.title || "Unnamed finding");
    if (!byTitle.has(key)) byTitle.set(key, []);
    byTitle.get(key)!.push(f);
  });
  return [...byTitle.entries()].map(([title, items]) => {
    let severity = "info";
    items.forEach((f) => {
      const s = String(f.severity || "info").toLowerCase();
      if (SEVERITY_RANK[s] > SEVERITY_RANK[severity]) severity = s;
    });
    const tools = new Set<string>();
    items.forEach((f) => {
      const t = f.tool_name || (f.details && f.details.tool) || f.plugin_id || "";
      if (t) tools.add(String(t).replace(/^vapt\//, ""));
    });
    return { title, count: items.length, severity, tools: [...tools], items };
  });
}

function fetchAllFindings(params: Record<string, unknown>): Promise<Record<string, any>[]> {
  const PAGE = 200;
  return new Promise(async (resolve, reject) => {
    const all: Record<string, any>[] = [];
    let page = 1;
    try {
      for (;;) {
        const res: any = await findingsApi.list({ page, page_size: PAGE, ...params });
        const items = res?.data?.items || [];
        const total = res?.data?.total || items.length;
        all.push(...items);
        if (all.length >= total || items.length < PAGE) break;
        page += 1;
      }
      resolve(all);
    } catch (e) {
      reject(e);
    }
  });
}

function bubbleSize(count: number): number {
  return Math.min(170, Math.max(64, 52 + count * 9));
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

  // --- Scope / bubble view state ---
  const [projects, setProjects] = useState<any[]>([]);
  const [assessments, setAssessments] = useState<any[]>([]);
  const [scope, setScope] = useState<Scope>({ kind: "graph" });
  const [scopeLabel, setScopeLabel] = useState("Knowledge Graph");
  const [bubbles, setBubbles] = useState<GroupedFinding[]>([]);
  const [selectedGroup, setSelectedGroup] = useState<GroupedFinding | null>(null);
  const [bubbleLoading, setBubbleLoading] = useState(false);
  const [bubbleError, setBubbleError] = useState("");
  const [scopeLoaded, setScopeLoaded] = useState(false);

  const bubbleMode = scope.kind !== "graph";

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

  // Load projects + their scans for the scope dropdown
  useEffect(() => {
    const orgId = localStorage.getItem("organization_id");
    if (!orgId || scopeLoaded) return;
    setScopeLoaded(true);
    (async () => {
      try {
        const projectsRes: any = await projectsApi.list(orgId);
        const projectsList = Array.isArray(projectsRes)
          ? projectsRes
          : projectsRes?.data?.items || projectsRes?.data || [];
        setProjects(Array.isArray(projectsList) ? projectsList : []);
        const assessmentsRes: any = await assessmentsApi.list({ organization_id: orgId, limit: 200 });
        setAssessments((assessmentsRes?.data?.items || []).slice());
      } catch {
        // dropdown stays empty; bubble view reports its own error
      }
    })();
  }, [scopeLoaded]);

  // Fetch findings for the selected scope and group into bubbles
  useEffect(() => {
    setSelectedGroup(null);
    setBubbleError("");
    if (scope.kind === "graph") {
      setBubbles([]);
      return;
    }
    let cancelled = false;
    setBubbleLoading(true);
    (async () => {
      try {
        const params =
          scope.kind === "project"
            ? { project_id: scope.id }
            : { assessment_id: scope.id };
        const findings = await fetchAllFindings(params);
        if (cancelled) return;
        setBubbles(groupFindings(findings));
      } catch (e: any) {
        if (!cancelled) setBubbleError(e?.message || "Failed to load findings");
      } finally {
        if (!cancelled) setBubbleLoading(false);
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [scope]);

  function changeLayout(mode: LayoutMode) {
    setLayoutMode(mode);
  }

  useEffect(() => {
    if (dataRef.current) {
      void buildGraph(dataRef.current.nodes, dataRef.current.edges);
    }
  }, [buildGraph]);

  function handleScopeChange(value: string) {
    if (!value || value === "graph") {
      setScope({ kind: "graph" });
      setScopeLabel("Knowledge Graph");
      return;
    }
    if (value.startsWith("scan:")) {
      const id = value.slice(5);
      const a = assessments.find((x) => x.id === id);
      setScope({ kind: "scan", id });
      setScopeLabel(`${a?.asset?.name || a?.asset_name || "Scan"} · ${a?.asset?.identifier || "scan"}`);
      return;
    }
    const id = value.slice("project:".length);
    const p = projects.find((x) => x.id === id);
    setScope({ kind: "project", id });
    setScopeLabel(p?.name || "Project");
  }

  const bubbleSummary = useMemo(() => {
    const bySeverity: Record<string, number> = {};
    let total = 0;
    bubbles.forEach((g) => {
      bySeverity[g.severity] = (bySeverity[g.severity] || 0) + 1;
      total += g.count;
    });
    return { bySeverity, total };
  }, [bubbles]);

  const layoutOptions: { id: LayoutMode; label: string; icon: typeof MoveHorizontal }[] = [
    { id: "lr", label: "Left → Right", icon: MoveHorizontal },
    { id: "tb", label: "Top → Bottom", icon: LayoutGrid },
    { id: "radial", label: "Radial", icon: Orbit },
    { id: "force", label: "Force", icon: Waypoints },
  ];

  return (
    <div className="h-[calc(100vh-3rem)] flex flex-col">
      <div className="flex items-center justify-between mb-4 gap-4 flex-wrap">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Attack Surface Graph</h1>
          <p className="text-muted-foreground text-sm mt-1">
            {bubbleMode
              ? `Vulnerability bubbles for ${scopeLabel}`
              : "Neo4j knowledge graph visualization of scan results"}
          </p>
        </div>
        <div className="flex items-center gap-3 flex-wrap">
          <div className="relative">
            <select
              value={
                scope.kind === "graph" ? "graph" : scope.kind === "project" ? `project:${scope.id}` : `scan:${scope.id}`
              }
              onChange={(e) => handleScopeChange(e.target.value)}
              className="h-9 pl-3 pr-8 rounded-lg bg-secondary/60 border border-border text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-primary/40 appearance-none cursor-pointer"
            >
              <option value="graph">Knowledge Graph</option>
              <optgroup label="Projects">
                {projects.map((p) => (
                  <option key={`project:${p.id}`} value={`project:${p.id}`}>
                    {p.name}
                  </option>
                ))}
              </optgroup>
              <optgroup label="Scans">
                {assessments.map((a) => (
                  <option key={`scan:${a.id}`} value={`scan:${a.id}`}>
                    {a.asset?.name || a.asset_name || "Scan"} ·{" "}
                    {a.started_at ? new Date(a.started_at).toLocaleDateString() : "—"}
                  </option>
                ))}
              </optgroup>
            </select>
            <Layers className="w-3.5 h-3.5 text-muted-foreground absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>

          {!bubbleMode && (
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
          )}

          {bubbleMode && (
            <div className="flex items-center gap-1.5 px-3 py-1.5 bg-secondary/60 border border-border rounded-lg text-xs text-muted-foreground">
              <CircleDot className="w-3.5 h-3.5 text-primary" />
              Bubbles view
            </div>
          )}

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
          {bubbleMode ? (
            <BubbleView
              loading={bubbleLoading}
              error={bubbleError}
              groups={bubbles}
              selectedTitle={selectedGroup?.title || null}
              onSelect={setSelectedGroup}
            />
          ) : (
            <>
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
                      if (d.group === "finding")
                        return SEVERITY_COLORS[d.severity?.toLowerCase() || "info"] || "#f87171";
                      return GROUP_META[d.group]?.color || "#334155";
                    }}
                    className="!bg-card/90 !border-border"
                  />
                  <Controls className="!bg-card !border-border [&>button]:!bg-card [&>button]:!text-foreground [&>button]:hover:!bg-accent" />
                </ReactFlow>
              )}
            </>
          )}
        </div>

        {bubbleMode ? (
          <BubbleDetailPane group={selectedGroup} summary={bubbleSummary} totalGroups={bubbles.length} />
        ) : selectedNode ? (
          <div className="w-72 glass-card rounded-xl p-4 overflow-y-auto">
            <h3 className="font-semibold text-sm mb-3">Node Detail</h3>
            <div className="space-y-2 text-sm">
              <div>
                <span className="text-xs text-muted-foreground block">Label</span>
                <p className="font-medium">{selectedNode.label}</p>
              </div>
              <div>
                <span className="text-xs text-muted-foreground block">ID</span>
                <p className="font-mono text-xs truncate">{selectedNode.id}</p>
              </div>
              {selectedNode.info && (
                <div>
                  <span className="text-xs text-muted-foreground block">Details</span>
                  <div
                    className="text-xs mt-1 leading-relaxed"
                    dangerouslySetInnerHTML={{ __html: selectedNode.info }}
                  />
                </div>
              )}
            </div>
          </div>
        ) : (
          <Legend />
        )}
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
        <p className="mt-1">Select a project or scan above to view vulnerability bubbles</p>
      </div>
    </div>
  );
}

function BubbleView({
  loading,
  error,
  groups,
  selectedTitle,
  onSelect,
}: {
  loading: boolean;
  error: string;
  groups: GroupedFinding[];
  selectedTitle: string | null;
  onSelect: (g: GroupedFinding | null) => void;
}) {
  const [now, setNow] = useState(Date.now());
  useEffect(() => {
    const id = window.setInterval(() => setNow(Date.now()), 5000);
    return () => window.clearInterval(id);
  }, []);

  if (loading) {
    return (
      <div className="absolute inset-0 flex items-center justify-center bg-card/80 z-10">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 border-primary border-t-transparent rounded-full animate-spin" />
          <p className="text-sm text-muted-foreground">Loading vulnerability bubbles...</p>
        </div>
      </div>
    );
  }
  if (error) {
    return (
      <div className="absolute inset-0 flex items-center justify-center bg-card/80 z-10">
        <div className="text-center max-w-md px-6">
          <p className="text-muted-foreground">{error}</p>
        </div>
      </div>
    );
  }
  if (groups.length === 0) {
    return (
      <div className="absolute inset-0 flex items-center justify-center bg-card/80 z-10">
        <div className="text-center max-w-md px-6">
          <ShieldAlert className="w-12 h-12 mx-auto mb-4 opacity-40 text-muted-foreground" />
          <p className="text-muted-foreground">No vulnerabilities found for this selection.</p>
          <p className="text-sm text-muted-foreground mt-1">Run a scan against this project first.</p>
        </div>
      </div>
    );
  }
  return (
    <div className="absolute inset-0 overflow-y-auto">
      <div className="flex flex-wrap items-center justify-center content-start gap-6 p-8 min-h-full">
        {groups.map((g) => {
          const color = SEVERITY_COLORS[g.severity] || "#94a3b8";
          const size = bubbleSize(g.count);
          const selected = selectedTitle === g.title;
          return (
            <button
              key={g.title}
              onClick={() => onSelect(selected ? null : g)}
              className={`flex flex-col items-center gap-2 p-2 rounded-xl border transition-all hover:scale-[1.03] ${
                selected ? "border-primary/70 bg-primary/10" : "border-transparent"
              }`}
            >
              <span
                className="flex flex-col items-center justify-center rounded-full text-white font-bold shadow-lg"
                style={{
                  width: size,
                  height: size,
                  background: `radial-gradient(circle at 32% 28%, ${color}cc, ${color}55 68%, ${color}22)`,
                  border: `2px solid ${color}`,
                  boxShadow: `0 6px 24px -8px ${color}aa, inset 0 1px 0 rgba(255,255,255,0.25)`,
                }}
                title={`${g.title} (${g.count})`}
              >
                <span className="text-2xl leading-none drop-shadow">{g.count}</span>
                <span className="text-[10px] uppercase tracking-wider opacity-90">bugs</span>
              </span>
              <span className="max-w-44 text-center text-xs font-medium leading-tight line-clamp-2 text-foreground">
                {g.title}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
}

function BubbleDetailPane({
  group,
  summary,
  totalGroups,
}: {
  group: GroupedFinding | null;
  summary: { bySeverity: Record<string, number>; total: number };
  totalGroups: number;
}) {
  if (group) {
    return (
      <div className="w-80 flex flex-col glass-card rounded-xl overflow-hidden">
        <div className="p-4 border-b border-border/60">
          <div className="flex items-start justify-between gap-2">
            <h3 className="font-semibold text-sm leading-snug">{group.title}</h3>
            <Badge pill color={SEVERITY_COLORS[group.severity]}>
              {group.severity.toUpperCase()}
            </Badge>
          </div>
          <p className="text-xs text-muted-foreground mt-1.5">
            {group.count} occurrence{group.count > 1 ? "s" : ""} ·{" "}
            {group.tools.length ? `via ${group.tools.join(", ")}` : "various tools"}
          </p>
        </div>
        <div className="flex-1 overflow-y-auto p-3 space-y-2">
          {group.items.map((f, i) => (
            <details key={f.id || i} className="rounded-lg border border-border/70 bg-card/60 group/details">
              <summary className="flex items-center gap-2 px-2.5 py-2 cursor-pointer text-xs list-none">
                <span
                  className="w-2 h-2 rounded-full flex-shrink-0"
                  style={{ background: SEVERITY_COLORS[String(f.severity || "info").toLowerCase()] || "#94a3b8" }}
                />
                <span className="font-mono truncate flex-1">
                  {f.host || f.target || (f.details && f.details.target) || "—"}
                  {f.port ? `:${f.port}` : ""}
                  {f.path ? f.path : ""}
                </span>
                <span className="text-[10px] text-muted-foreground">
                  {f.tool_name || (f.details && f.details.tool) || "tool"}
                </span>
              </summary>
              <div className="px-3 pb-3 pt-1 text-xs space-y-2">
                {f.description && <p className="text-muted-foreground leading-relaxed">{f.description}</p>}
                {(f.cve || f.cwe) && (
                  <div className="flex flex-wrap gap-1">
                    {(Array.isArray(f.cve) ? f.cve : f.cve ? [f.cve] : [])
                      .filter(Boolean)
                      .slice(0, 4)
                      .map((c: string) => (
                        <span key={c} className="px-1.5 py-0.5 rounded bg-blue-500/10 border border-blue-500/30 text-blue-300 font-mono">
                          {c}
                        </span>
                      ))}
                    {(Array.isArray(f.cwe) ? f.cwe : f.cwe ? [f.cwe] : [])
                      .filter(Boolean)
                      .slice(0, 4)
                      .map((c: string) => (
                        <span key={c} className="px-1.5 py-0.5 rounded bg-purple-500/10 border border-purple-500/30 text-purple-300 font-mono">
                          {c}
                        </span>
                      ))}
                  </div>
                )}
                {f.remediation && (
                  <div>
                    <p className="text-[10px] uppercase tracking-wider text-muted-foreground mb-0.5">Remediation</p>
                    <p className="text-muted-foreground leading-relaxed">{f.remediation}</p>
                  </div>
                )}
              </div>
            </details>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="w-80 glass-card rounded-xl p-4 overflow-y-auto">
      <h3 className="font-semibold text-sm mb-3">Summary</h3>
      {totalGroups === 0 ? (
        <p className="text-sm text-muted-foreground">
          Select a project or scan from the dropdown to see vulnerabilities as bubbles.
        </p>
      ) : (
        <div className="space-y-2">
          <div className="text-sm">
            <span className="font-bold">{summary.total}</span>{" "}
            <span className="text-muted-foreground">total findings · {totalGroups} unique bugs</span>
          </div>
          {Object.keys(SEVERITY_COLORS).map((sev) => {
            const n = summary.bySeverity[sev] || 0;
            if (n === 0) return null;
            return (
              <div key={sev} className="flex items-center gap-2 text-xs">
                <div className="w-3 h-3 rounded-full" style={{ background: SEVERITY_COLORS[sev] }} />
                <span className="capitalize flex-1">{sev}</span>
                <span className="font-semibold">{n}</span>
              </div>
            );
          })}
          <p className="pt-3 border-t border-border/60 text-xs text-muted-foreground">
            Click a bubble to inspect every occurrence of that vulnerability.
          </p>
        </div>
      )}
    </div>
  );
}

function Badge({ children, color, pill }: { children: React.ReactNode; color: string; pill?: boolean }) {
  return (
    <span
      className={`px-2 py-0.5 text-[10px] font-semibold ${pill ? "rounded-full" : "rounded-md"} flex-shrink-0`}
      style={{ background: `${color}22`, color, border: `1px solid ${color}55` }}
    >
      {children}
    </span>
  );
}