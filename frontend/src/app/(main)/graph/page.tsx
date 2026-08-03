"use client";

import { useEffect, useRef, useState } from "react";
import { apiClient } from "@/services/api";

const GROUP_STYLES: Record<string, { shape: string; color: { background: string; border: string }; size: number }> = {
  target: { shape: "diamond", color: { background: "#1a3a5c", border: "#0f2440" }, size: 30 },
  port: { shape: "box", color: { background: "#475569", border: "#334155" }, size: 20 },
  service: { shape: "ellipse", color: { background: "#16a34a", border: "#15803d" }, size: 25 },
  finding: { shape: "dot", color: { background: "#dc2626", border: "#b91c1c" }, size: 18 },
  tool: { shape: "star", color: { background: "#f59e0b", border: "#d97706" }, size: 20 },
};

const SEVERITY_COLORS: Record<string, string> = {
  critical: "#dc2626",
  high: "#ea580c",
  medium: "#ca8a04",
  low: "#65a30d",
  info: "#6b7280",
};

function getNodeStyle(n: any) {
  const gs = GROUP_STYLES[n.group] || GROUP_STYLES.finding;
  const sevColor = n.severity ? SEVERITY_COLORS[n.severity.toLowerCase()] : null;
  return {
    ...gs,
    color: sevColor ? { background: sevColor, border: "#1e293b" } : gs.color,
  };
}

export default function GraphPage() {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [stats, setStats] = useState({ targets: 0, ports: 0, findings: 0, services: 0 });
  const [selectedNode, setSelectedNode] = useState<{ id: string; label: string; info: string } | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    let network: any = null;
    let mounted = true;

    async function initGraph() {
      try {
        const res = await apiClient.get<{ nodes: any[]; edges: any[] }>("/graph");
        if (!mounted) return;
        const rawNodes: any[] = res.data?.nodes || [];
        const rawEdges: any[] = res.data?.edges || [];

        if (!rawNodes.length) {
          setLoading(false);
          setError("No graph data available. Run a scan first.");
          return;
        }

        const { Network } = await import("vis-network");

        const nodeData = rawNodes.map((n: any) => {
          const style = getNodeStyle(n);
          return {
            id: n.id,
            label: n.label,
            group: n.group,
            shape: style.shape,
            color: style.color,
            size: style.size,
            font: { size: n.group === "target" ? 14 : 11, color: "#e2e8f0" },
            borderWidth: 2,
            title: n.title || n.label,
          };
        });

        const edgeData = rawEdges.map((e: any) => ({
          from: e.from,
          to: e.to,
          label: e.label,
          arrows: "to",
          color: { color: "#475569", hover: "#94a3b8" },
          font: { size: 9, color: "#94a3b8" },
          smooth: { type: "continuous" },
        }));

        const options = {
          nodes: { borderWidth: 2, font: { color: "#e2e8f0" } },
          edges: { color: "#475569" },
          physics: {
            solver: "forceAtlas2Based",
            forceAtlas2Based: { gravitationalConstant: -40, centralGravity: 0.005, springLength: 150, springConstant: 0.04 },
            stabilization: { iterations: 200 },
          },
          interaction: { hover: true, tooltipDelay: 200, navigationButtons: true, keyboard: true },
          groups: Object.fromEntries(
            Object.entries(GROUP_STYLES).map(([k, v]) => [k, { shape: v.shape, color: v.color.background }])
          ),
          layout: { improvedLayout: true },
        };

        network = new Network(containerRef.current!, { nodes: nodeData as any, edges: edgeData as any }, options as any);
        networkRef.current = network;

        network.on("click", (params: any) => {
          if (params.nodes.length) {
            const nodeId = params.nodes[0];
            const nodeData = rawNodes.find((n: any) => n.id === nodeId);
            if (nodeData) {
              setSelectedNode({ id: nodeData.id, label: nodeData.label, info: nodeData.title || "" });
            }
          } else {
            setSelectedNode(null);
          }
        });

        setStats({
          targets: rawNodes.filter((n: any) => n.group === "target").length,
          ports: rawNodes.filter((n: any) => n.group === "port").length,
          findings: rawNodes.filter((n: any) => n.group === "finding").length,
          services: rawNodes.filter((n: any) => n.group === "service").length,
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
      if (network) network.destroy();
    };
  }, []);

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
        </div>

        {selectedNode && (
          <div className="w-72 bg-card border rounded-xl p-4 overflow-y-auto">
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
                  <div className="text-xs mt-1 leading-relaxed" dangerouslySetInnerHTML={{ __html: selectedNode.info }} />
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
          <div className="w-4 h-4 rounded-sm flex-shrink-0" style={{ background: style.color.background }} />
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
