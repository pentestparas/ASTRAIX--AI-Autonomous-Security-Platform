"use client";

import { useEffect, useState, useRef, Fragment } from "react";
import { useRouter } from "next/navigation";
import { projectsApi, apiClient, assessmentsApi, vaptScanApi } from "@/services/api";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Play,
  CheckCircle,
  Clock,
  Pause,
  XCircle,
  Plus,
  Scan,
  Loader2,
  Check,
  Shield,
  ShieldAlert,
  AlertTriangle,
  Zap,
  Globe,
  Server,
  Lock,
  Eye,
  FolderKanban,
  Network,
  Code2,
  Cloud,
  Brain,
  ListChecks,
  Terminal,
  BookOpen,
  ShieldCheck,
  FileText,
  Sparkles,
  CheckCircle2,
  Bug,
  Search,
  X,
  Activity,
  StopCircle,
  RotateCcw,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import type { Project, ScanProgressEvent } from "@/types";
import { useActiveScansStore } from "@/store/activeScans";

interface PlanTool {
  id: string;
  name: string;
  description: string;
  reason: string;
}

interface PlanPhase {
  id: string;
  name: string;
  description: string;
  tools: PlanTool[];
  kb_context?: string[];
}

interface ScanHistoryItem {
  id: string;
  name: string;
  type: string;
  status: string;
  target: string;
  findings_count: number;
  started_at: string | null;
  asset?: { name: string };
}

interface Finding {
  id: string;
  title: string;
  description: string;
  severity: string;
  tool_name: string;
  target: string;
  host?: string;
  port?: number;
  protocol?: string;
  service?: string;
  path?: string;
  vulnerability_type?: string;
  remediation?: string;
  reference?: string;
  cve?: string;
  cwe?: string;
  payload?: string;
  confidence?: string;
  kb_context?: string;
  kb_sources?: string[];
  discovered_at?: string;
}

interface VaptScanResult {
  scan_id: string;
  status: string;
  target: string;
  findings_count: number;
  assessment_id?: string;
  findings?: Record<string, unknown>[];
  severity_breakdown: {
    critical: number;
    high: number;
    medium: number;
    low: number;
    info: number;
  };
  insights: {
    risk_level: string;
    recommendations: string[];
    executive_summary: string;
  };
}

const scanTypesInfo = [
  {
    id: "network",
    label: "Network VAPT",
    description: "Scan network ranges for open ports and services",
    tools: ["Nmap", "Masscan", "Netbiosenum", "SMB Enum", "DNS Recon"],
    color: "blue",
    icon: Network,
  },
  {
    id: "web",
    label: "Web App VAPT",
    description: "Assess web applications for OWASP Top 10",
    tools: ["Nikto", "SQLMap", "XSStrike", "Dirbuster", "Burp Suite"],
    color: "green",
    icon: Globe,
  },
  {
    id: "cloud",
    label: "Cloud Security",
    description: "Review cloud infrastructure for misconfigurations",
    tools: ["Prowler", "Scout Suite", "CloudSploit", "Principal Mapper"],
    color: "purple",
    icon: Cloud,
  },
  {
    id: "code",
    label: "Code Audit",
    description: "Static analysis of source code",
    tools: ["Semgrep", "Bandit", "SonarQube", "CodeQL", "Brakeman"],
    color: "orange",
    icon: Code2,
  },
];

const vaptScanTypes = [
  { id: "network", label: "Network Scan", icon: Server, desc: "Ports, services, network mapping" },
  { id: "web", label: "Web Application", icon: Globe, desc: "OWASP Top 10, SQLi, XSS, etc." },
  { id: "ssl", label: "SSL/TLS Audit", icon: Lock, desc: "Certificate and protocol analysis" },
  { id: "full", label: "Full Scan", icon: Shield, desc: "All checks - comprehensive" },
];

const severityColors: Record<string, string> = {
  critical: "bg-red-500/15 text-red-400 border-red-500/30",
  high: "bg-orange-500/15 text-orange-400 border-orange-500/30",
  medium: "bg-yellow-500/15 text-yellow-400 border-yellow-500/30",
  low: "bg-blue-500/15 text-blue-400 border-blue-500/30",
  info: "bg-secondary text-secondary-foreground border-border/60",
};

const riskColors: Record<string, string> = {
  CRITICAL: "text-red-400 bg-red-500/10 border-red-500/30",
  HIGH: "text-orange-400 bg-orange-500/10 border-orange-500/30",
  MEDIUM: "text-yellow-400 bg-yellow-500/10 border-yellow-500/30",
  LOW: "text-green-400 bg-green-500/10 border-green-500/30",
};

const statusConfig: Record<string, { label: string; icon: typeof Clock; className: string }> = {
  pending:    { label: "Pending",    icon: Clock,        className: "bg-yellow-500/15 text-yellow-400" },
  running:    { label: "Running",    icon: Pause,        className: "bg-blue-500/15 text-blue-400" },
  paused:     { label: "Paused",     icon: Pause,        className: "bg-amber-500/15 text-amber-400" },
  completed:  { label: "Completed",  icon: CheckCircle,  className: "bg-green-500/15 text-green-400" },
  failed:     { label: "Failed",     icon: XCircle,      className: "bg-red-500/15 text-red-400" },
  stopped:    { label: "Stopped",    icon: StopCircle,   className: "bg-red-500/15 text-red-400" },
  cancelled:  { label: "Cancelled",  icon: XCircle,      className: "bg-secondary text-secondary-foreground border-border/60" },
};

const typeLabels: Record<string, string> = {
  network_vapt: "Network VAPT", web_vapt: "Web App VAPT", cloud_posture: "Cloud Security",
  code_audit: "Code Audit", network: "Network Scan", web: "Web Application",
  ssl: "SSL/TLS Audit", full: "Full Scan",
};

const typeIcons: Record<string, typeof Shield> = {
  network_vapt: Network, web_vapt: Globe, cloud_posture: Cloud,
  code_audit: Code2, network: Server, web: Globe, ssl: Lock, full: Shield,
};

function getTypeLabel(type: string): string {
  return typeLabels[type] || type.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

function getTypeIcon(type: string) {
  return typeIcons[type] || Shield;
}

function getSeverityBadge(severity: string) {
  const colorMap: Record<string, string> = {
    critical: "bg-red-500/15 text-red-400 border-red-500/30",
    high: "bg-orange-500/15 text-orange-400 border-orange-500/30",
    medium: "bg-yellow-500/15 text-yellow-400 border-yellow-500/30",
    low: "bg-blue-500/15 text-blue-400 border-blue-500/30",
    info: "bg-secondary text-secondary-foreground border-border/60",
  };
  return colorMap[severity] || colorMap.info;
}

const phaseIcons: Record<string, typeof Shield> = {
  recon: Search,
  enumeration: Globe,
  vuln_scan: Bug,
  crypto: Lock,
  web: Globe,
  deep: Bug,
};

type ToolState = "queued" | "running" | "done" | "failed";

function LiveScanConsole({
  events,
  target,
  scanType,
  running,
  paused,
  onPause,
  onResume,
  onStop,
  scanId,
  onResolveApproval,
}: {
  events: ScanProgressEvent[];
  target: string;
  scanType: string;
  running: boolean;
  paused?: boolean;
  onPause?: () => void;
  onResume?: () => void;
  onStop?: () => void;
  scanId?: string;
  onResolveApproval?: (approvalId: string, approved: boolean) => void;
}) {
  const planEvent = events.find((e) => e.type === "plan_ready");
  const phases: PlanPhase[] = (planEvent?.data as { phases?: PlanPhase[] })?.phases || [];
  const decisionEvent = events.find((e) => e.type === "ai_decision");
  const strategy =
    (decisionEvent?.data as { insights?: string })?.insights ||
    (planEvent?.data as { strategy?: string })?.strategy ||
    "";

  const toolStarted = new Set<string>();
  const toolFinished = new Set<string>();
  const toolFailed = new Set<string>();
  const toolCommands = new Map<string, string>();
  events.forEach((e) => {
    if (e.type === "tool_started") {
      toolStarted.add(e.data?.tool);
      if (e.data?.command) toolCommands.set(e.data.tool, e.data.command);
    }
    if (e.type === "tool_finished") toolFinished.add(e.data?.tool);
    if (e.type === "tool_failed") toolFailed.add(e.data?.tool);
  });

  const toolState = (id: string): ToolState => {
    if (toolFailed.has(id)) return "failed";
    if (toolFinished.has(id)) return "done";
    if (toolStarted.has(id)) return "running";
    return "queued";
  };

  const findings = events
    .filter((e) => e.type === "finding_found")
    .map((e) => e.data as Record<string, unknown>);

  const pipelineSteps = [
    { id: "ai_analyzing", label: "AI Analyzing target", icon: Brain },
    { id: "plan_ready", label: "AI plan ready — tools selected", icon: ListChecks },
    { id: "tool_started", label: "Executing security tools", icon: Terminal },
    { id: "ai_research", label: "Researcher Agent — knowledge base enrichment", icon: BookOpen },
    { id: "ai_verification", label: "Verifier Agent — eliminating false positives", icon: ShieldCheck },
    { id: "report_generating", label: "Generating executive report", icon: FileText },
  ];

  const typeCount = new Map<string, number>();
  events.forEach((e) => typeCount.set(e.type, (typeCount.get(e.type) || 0) + 1));
  let lastActiveStep = -1;
  pipelineSteps.forEach((s, i) => {
    if ((typeCount.get(s.id) || 0) > 0) lastActiveStep = i;
  });

  const totalTools = phases.reduce((n, p) => n + p.tools.length, 0);
  const doneTools = toolFinished.size + toolFailed.size;
  const progressPct = totalTools ? Math.round((doneTools / totalTools) * 100) : 0;

  const [now, setNow] = useState(Date.now());
  useEffect(() => {
    if (!running) return;
    const id = window.setInterval(() => setNow(Date.now()), 1000);
    return () => window.clearInterval(id);
  }, [running]);

  const toolStartedAt = new Map<string, number>();
  const toolFinishedAt = new Map<string, number>();
  events.forEach((e) => {
    if (e.type === "tool_started" && !toolStartedAt.has(e.data?.tool)) {
      toolStartedAt.set(e.data?.tool, e.ts * 1000);
    }
    if (e.type === "tool_finished" && !toolFinishedAt.has(e.data?.tool)) {
      toolFinishedAt.set(e.data?.tool, e.ts * 1000);
    }
  });

  const phaseStartedAt = (phase: PlanPhase): number => {
    const first = phase.tools
      .map((t) => toolStartedAt.get(t.id))
      .filter((v): v is number => v !== undefined);
    if (first.length === 0) return Infinity;
    // phase via its own start timestamp
    const phaseStart = events
      .filter((e) => e.type === "phase_started" && String(e.data?.phase) === phase.id)
      .sort((a, b) => a.ts - b.ts)[0];
    return phaseStart ? phaseStart.ts * 1000 : Math.min(...first);
  };

  const fmtClock = (tsMs: number) =>
    new Date(tsMs).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });

  const fmtDur = (ms: number) => {
    const s = Math.floor(ms / 1000);
    if (s < 60) return `${s}s`;
    return `${Math.floor(s / 60)}m ${s % 60}s`;
  };

  const lastActivityAt = events.length
    ? Math.max(...events.map((e) => e.ts)) * 1000
    : now;
  const idleSec = running ? (now - lastActivityAt) / 1000 : 0;
  const scanStalled = events.find((e) => e.type === "scan_stalled");
  const stalled = running && !paused && (idleSec > 300 || !!scanStalled);

  const approvalRequests = events
    .filter((e) => e.type === "tool_approval_requested")
    .map((e) => e.data as Record<string, any>);
  const resolvedApprovalIds = new Set(
    events
      .filter((e) => e.type === "tool_approval_resolved")
      .map((e) => String(e.data?.approval_id || ""))
      .filter(Boolean)
  );
  const approvalList = approvalRequests.filter(
    (r) => r?.approval_id && !resolvedApprovalIds.has(String(r.approval_id))
  );

  const agentSteps = events
    .filter((e) => e.type === "agent_step")
    .map((e, i) => ({
      key: i,
      index: e.data?.index ?? i,
      tool: String(e.data?.tool_id || e.data?.tool || "?"),
      decision: String(e.data?.decision || ""),
      reason: String(e.data?.reason || ""),
      findingCount: Number(e.data?.findings_count || 0),
      error: !!e.data?.error,
    }));

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-sm font-semibold flex items-center gap-2">
            {paused ? (
              <Pause className="w-4 h-4 text-amber-400" />
            ) : running ? (
              <Loader2 className="w-4 h-4 animate-spin text-primary" />
            ) : (
              <CheckCircle2 className="w-4 h-4 text-green-500" />
            )}
            AI Security Scan
          </p>
          <p className="text-xs text-muted-foreground mt-0.5">
            {target} · {getTypeLabel(scanType)}
          </p>
        </div>
        <div className="flex items-center gap-2">
          {running || paused ? (
            <>
              <span
                className={`w-2 h-2 rounded-full ${
                  paused
                    ? "bg-amber-400"
                    : stalled
                      ? "bg-amber-500 animate-ping"
                      : "bg-green-500 animate-pulse"
                }`}
                title={
                  paused
                    ? "Paused"
                    : idleSec > 0
                      ? `Last activity ${Math.round(idleSec)}s ago`
                      : "Active"
                }
              />
              <span className="text-[11px] text-muted-foreground">
                {paused
                  ? "paused at checkpoint"
                  : stalled
                    ? "No activity for a while"
                    : `active ${idleSec < 1 ? "now" : `${Math.round(idleSec)}s ago`}`}
              </span>
            </>
          ) : null}
          {running || paused ? (
            <>
              <Badge variant={stalled ? "destructive" : paused ? "secondary" : "default"}>
                {stalled ? "Possibly stalled" : paused ? "Paused" : "Running"}
              </Badge>
              <span className="text-xs text-muted-foreground">{progressPct}%</span>
              <span className="flex items-center gap-1.5">
                {paused ? (
                  <Button size="sm" onClick={onResume}>
                    <Play className="w-3.5 h-3.5 mr-1" />
                    Continue
                  </Button>
                ) : (
                  <Button size="sm" variant="outline" onClick={onPause}>
                    <Pause className="w-3.5 h-3.5 mr-1" />
                    Pause
                  </Button>
                )}
                <Button size="sm" variant="destructive" onClick={onStop}>
                  <StopCircle className="w-3.5 h-3.5 mr-1" />
                  Stop
                </Button>
              </span>
            </>
          ) : null}
        </div>
      </div>

      {scanStalled && (
        <div className="p-3 rounded-lg border border-amber-500/40 bg-amber-500/10 text-sm">
          <p className="text-xs font-semibold text-amber-600 mb-0.5 flex items-center gap-1">
            <AlertTriangle className="w-3.5 h-3.5" /> Possible stall detected
          </p>
          <p className="text-xs text-amber-700">
            {String(scanStalled.data?.message || "No activity detected - the target may be unresponsive.")}{" "}
            The watchdog will keep the scan alive until it recovers.
          </p>
        </div>
      )}

      {approvalList.length > 0 && (
        <div className="space-y-2">
          <p className="text-xs font-semibold flex items-center gap-1.5 text-amber-500">
            <ShieldAlert className="w-3.5 h-3.5" />
            Dangerous tool approval required
          </p>
          {approvalList.map((req) => (
            <div
              key={req.approval_id}
              className="p-3 rounded-lg border border-amber-500/40 bg-amber-500/10"
            >
              <div className="flex items-center justify-between gap-2 flex-wrap">
                <div className="min-w-0">
                  <p className="text-sm font-mono font-semibold truncate">
                    {req.tool_name}
                    {req.args?.target ? <span className="text-muted-foreground"> · {req.args.target}</span> : null}
                  </p>
                  <p className="text-xs text-amber-700 mt-0.5 break-words font-mono">
                    {JSON.stringify(req.args || {})}
                  </p>
                  {req.reason && <p className="text-xs text-muted-foreground mt-0.5">{req.reason}</p>}
                </div>
                <div className="flex gap-1.5 shrink-0">
                  <Button
                    size="sm"
                    onClick={() => onResolveApproval?.(req.approval_id, true)}
                  >
                    <Check className="w-3.5 h-3.5 mr-1" />
                    Approve
                  </Button>
                  <Button
                    size="sm"
                    variant="outline"
                    onClick={() => onResolveApproval?.(req.approval_id, false)}
                  >
                    <X className="w-3.5 h-3.5 mr-1" />
                    Reject
                  </Button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {agentSteps.length > 0 && (
        <div className="p-3 rounded-lg border border-primary/20 bg-primary/5">
          <p className="text-xs font-semibold text-primary mb-1.5 flex items-center gap-1">
            <Brain className="w-3.5 h-3.5" /> Autonomous agent loop
          </p>
          <div className="space-y-1">
            {agentSteps.slice(-8).map((s) => (
              <div key={s.key} className="flex items-center gap-2 text-xs">
                {s.error ? (
                  <XCircle className="w-3 h-3 text-destructive shrink-0" />
                ) : s.decision === "ran" ? (
                  <Check className="w-3 h-3 text-green-500 shrink-0" />
                ) : (
                  <Clock className="w-3 h-3 text-muted-foreground shrink-0" />
                )}
                <span className="font-mono text-muted-foreground shrink-0">
                  step {s.index}
                </span>
                <span className="font-mono font-medium">{s.tool}</span>
                <span className="text-muted-foreground truncate">{s.reason}</span>
                <span className="ml-auto text-[10px] text-muted-foreground shrink-0">
                  {s.findingCount > 0 ? `+${s.findingCount} findings` : "no findings"}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="h-1.5 rounded-full bg-muted overflow-hidden">
        <div
          className="h-full bg-primary transition-all duration-500"
          style={{ width: `${progressPct}%` }}
        />
      </div>

      {strategy && (
        <div className="p-3 rounded-lg bg-primary/10 border border-primary/30 text-sm">
          <p className="text-xs font-semibold text-primary mb-1 flex items-center gap-1">
            <Sparkles className="w-3 h-3" /> AI Strategy
          </p>
          {strategy}
        </div>
      )}

      <div className="space-y-1.5">
        {pipelineSteps.map((step, i) => {
          const hasEvents = (typeCount.get(step.id) || 0) > 0;
          const isActive = running && !paused && hasEvents && i === lastActiveStep;
          const isDone = running && !paused ? hasEvents && i < lastActiveStep : hasEvents;
          const StepIcon = step.icon;
          return (
            <div
              key={step.id}
              className={`flex items-center gap-2.5 px-2.5 py-1.5 rounded-md ${
                isActive ? "bg-primary/10 border border-primary/20" : ""
              }`}
            >
              {isActive ? (
                <Loader2 className="w-3.5 h-3.5 text-primary animate-spin shrink-0" />
              ) : isDone ? (
                <Check className="w-3.5 h-3.5 text-green-500 shrink-0" />
              ) : (
                <Clock className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
              )}
              <StepIcon className="w-3.5 h-3.5 text-muted-foreground shrink-0" />
              <span className={`text-xs ${isDone || isActive ? "font-medium" : "text-muted-foreground"}`}>
                {step.label}
              </span>
              {hasEvents && (
                <span className="ml-auto text-[11px] text-muted-foreground font-mono">
                  {fmtClock(
                    typeCount.get(step.id) ? (events.find((e) => e.type === step.id)?.ts || 0) * 1000 : 0,
                  )}
                </span>
              )}
            </div>
          );
        })}
      </div>

      <div className="space-y-2">
        {phases.map((phase) => {
          const PhaseIcon = phaseIcons[phase.id] || Activity;
          const tools = phase.tools || [];
          const stateCounts = { done: 0, running: 0, failed: 0, queued: 0 };
          tools.forEach((t) => {
            stateCounts[toolState(t.id)]++;
          });
          const phaseState: ToolState =
            stateCounts.failed > 0
              ? "failed"
              : stateCounts.running > 0
                ? "running"
                : stateCounts.done === tools.length && tools.length > 0
                  ? "done"
                  : "queued";

          const runningTool = tools.find((t) => toolState(t.id) === "running");
          return (
            <div key={phase.id} className="p-3 rounded-lg border bg-card">
              <div className="flex items-center justify-between mb-1.5">
                <p className="text-sm font-medium flex items-center gap-1.5">
                  <PhaseIcon className="w-4 h-4 text-primary" />
                  {phase.name}
                </p>
                <span className="text-xs text-muted-foreground flex items-center gap-1.5">
                  {Number.isFinite(phaseStartedAt(phase)) && (
                    <span className="font-mono">{fmtClock(phaseStartedAt(phase))}</span>
                  )}
                  {phaseState === "done"
                    ? "Completed"
                    : phaseState === "running"
                      ? "Running..."
                      : phaseState === "failed"
                        ? "Partial"
                        : "Queued"}
                </span>
              </div>
              <p className="text-xs text-muted-foreground mb-2">{phase.description}</p>
              <div className="flex flex-wrap gap-1.5">
                {tools.map((t) => {
                  const state = toolState(t.id);
                  const startMs = toolStartedAt.get(t.id);
                  const durMs =
                    state === "running" && startMs
                      ? now - startMs
                      : state === "done" && toolFinishedAt.has(t.id)
                        ? (toolFinishedAt.get(t.id) || 0) - (startMs || 0)
                        : 0;
                  return (
                    <span
                      key={t.id}
                      title={startMs ? `${t.name} started ${fmtClock(startMs)}` : t.description}
                      className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-md text-xs border ${
                        state === "running"
                          ? "bg-primary/10 border-primary/40 text-primary"
                          : state === "done"
? "bg-green-500/10 border-green-500/40 text-green-400"
                          : state === "failed"
                            ? "bg-red-500/10 border-red-500/40 text-red-400"
                              : "bg-muted/50 border-border text-muted-foreground"
                      }`}
                    >
                      {state === "running" ? (
                        <Loader2 className="w-3 h-3 animate-spin" />
                      ) : state === "done" ? (
                        <Check className="w-3 h-3" />
                      ) : state === "failed" ? (
                        <X className="w-3 h-3" />
                      ) : (
                        <Clock className="w-3 h-3" />
                      )}
                      <span className="font-mono">{t.name}</span>
                      {durMs > 0 && (
                        <span className="ml-1 text-[10px] opacity-80">{fmtDur(durMs)}</span>
                      )}
                    </span>
                  );
                })}
              </div>
              {runningTool && toolCommands.get(runningTool.id) && (
                <p className="mt-2 text-[11px] font-mono text-muted-foreground truncate">
                  $ {toolCommands.get(runningTool.id)}
                </p>
              )}
            </div>
          );
        })}
      </div>

      {findings.length > 0 && (
        <div>
          <p className="text-xs font-semibold mb-1.5 flex items-center gap-1.5">
            <Bug className="w-3.5 h-3.5 text-red-500" />
            Live findings ({findings.length})
          </p>
          <div className="max-h-44 overflow-y-auto space-y-1.5 pr-1">
            {findings.map((f, i) => (
              <div
                key={i}
                className="flex items-start gap-2 p-2 rounded-lg border bg-card"
              >
                <Badge className={getSeverityBadge(String(f.severity || "info").toLowerCase())}>
                  {String(f.severity || "info").toUpperCase()}
                </Badge>
                <div className="min-w-0 flex-1">
                  <p className="text-sm truncate">{String(f.title || "Finding")}</p>
                  <p className="text-xs text-muted-foreground">
                    {String(f.tool_name || "unknown")}
                    {f.target ? ` · ${String(f.target)}` : ""}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function ScansPage() {
  const [scanResults, setScanResults] = useState<ScanHistoryItem[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewScan, setShowNewScan] = useState(false);
  const [dialogTarget, setDialogTarget] = useState("");
  const [selectedScanTypes, setSelectedScanTypes] = useState<string[]>(["web"]);
  const [selectedProjectDialog, setSelectedProjectDialog] = useState("");
  const [creating, setCreating] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  const [target, setTarget] = useState("");
  const [scanType, setScanType] = useState("web");
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState<VaptScanResult | null>(null);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [selectedProject, setSelectedProject] = useState<string>("");
  const [loadingProjects, setLoadingProjects] = useState(false);

  const [liveEvents, setLiveEvents] = useState<ScanProgressEvent[]>([]);
  const [liveScanId, setLiveScanId] = useState<string | null>(null);
  const [liveRunning, setLiveRunning] = useState(false);
  const [livePaused, setLivePaused] = useState(false);
  const [confirmStop, setConfirmStop] = useState(false);
  const [expandedFinding, setExpandedFinding] = useState<string | null>(null);
  const router = useRouter();
  const liveActiveRef = useRef(false);
  const addScan = useActiveScansStore((s) => s.addScan);
  const updateScan = useActiveScansStore((s) => s.updateScan);
  const removeScan = useActiveScansStore((s) => s.removeScan);

  async function pollProgress(scanId: string) {
    let since = 0;
    while (liveActiveRef.current) {
      try {
        const res = (await vaptScanApi.progress(scanId, since)) as any;
        const events: ScanProgressEvent[] = res?.events || [];
        if (events.length) {
          setLiveEvents((prev) => [...prev, ...events]);
          since = res?.total ?? since + events.length;
          if (events.some((e) => e.type === "scan_completed")) {
            updateScan(scanId, { status: "completed" });
            removeScan(scanId);
            liveActiveRef.current = false;
            setLiveRunning(false);
            setLivePaused(false);
            void refreshHistory();
            return;
          }
        }
        const status = res?.status?.status;
        if (status === "paused") {
          setLivePaused(true);
          updateScan(scanId, { status: "paused" });
        } else if (status && ["running", "pending", "queued", "planning"].includes(status)) {
          setLivePaused(false);
          updateScan(scanId, { status: "running" });
        }
        if (status && !["running", "pending", "queued", "planning", "paused"].includes(status)) {
          if (status === "failed") updateScan(scanId, { status: "failed" });
          if (status === "stopped") updateScan(scanId, { status: "stopped" });
          removeScan(scanId);
          liveActiveRef.current = false;
          setLiveRunning(false);
          setLivePaused(false);
          void refreshHistory();
          return;
        }
      } catch {
        // transient poll errors are ignored; scan request itself reports failure
      }
      await new Promise((r) => setTimeout(r, 2000));
    }
  }

  async function handlePauseScan() {
    if (!liveScanId) return;
    try {
      await vaptScanApi.pause(liveScanId);
      setLivePaused(true);
      updateScan(liveScanId, { status: "paused" });
    } catch {
      // ignore - console will reflect the live status on next poll
    }
  }

  async function handleResumeScan() {
    if (!liveScanId) return;
    try {
      await vaptScanApi.resume(liveScanId);
      setLivePaused(false);
      updateScan(liveScanId, { status: "running" });
    } catch {
      // ignore - console will reflect the live status on next poll
    }
  }

  async function handleResolveApproval(approvalId: string, approved: boolean) {
    if (!liveScanId) return;
    try {
      await vaptScanApi.approve(liveScanId, approvalId, approved);
    } catch {
      // ignore - console will reflect the live status on next poll
    }
  }

  async function handleStopScan() {
    if (!liveScanId) return;
    setConfirmStop(false);
    try {
      await vaptScanApi.stop(liveScanId);
    } catch {
      // server may already have finished the scan; fall through to cleanup
    }
    liveActiveRef.current = false;
    setLiveRunning(false);
    setLivePaused(false);
    updateScan(liveScanId, { status: "stopped" });
    removeScan(liveScanId);
    void refreshHistory();
  }

  async function handleRestartScan(scan: ScanHistoryItem) {
    if (!scan.target) return;
    try {
      setLiveEvents([]);
      setLiveScanId(scan.id);
      setLiveRunning(true);
      setLivePaused(false);
      liveActiveRef.current = true;
      addScan({
        id: scan.id,
        target: scan.target,
        scanType: scan.type,
        startedAt: Date.now(),
        status: "running",
      });
      void pollProgress(scan.id);
      await vaptScanApi.restart(scan.id);
    } catch (e) {
      alert(e instanceof Error ? e.message : "Failed to restart scan");
    } finally {
      liveActiveRef.current = false;
    }
  }

  const initialProjectSet = useRef(false);

  async function refreshHistory() {
    const orgId = localStorage.getItem("organization_id");
    if (!orgId) return;
    try {
      const assessmentsRes = await assessmentsApi.list({ organization_id: orgId });
      const assessmentsList = (assessmentsRes as any)?.data?.items || [];
      if (Array.isArray(assessmentsList)) {
        setScanResults(assessmentsList.map((a: any) => ({
          id: a.id,
          name: a.name || "",
          type: a.type || "unknown",
          status: a.status || "pending",
          target: a.asset?.identifier || a.config?.target || "unknown",
          findings_count: a.findings_count || 0,
          started_at: a.started_at || a.created_at || null,
          asset: a.asset || undefined,
        })));
      }
    } catch (e) {
      console.error("Failed to refresh history:", e);
    }
  }

  useEffect(() => {
    const orgId = localStorage.getItem("organization_id");
    if (!orgId) {
      setLoading(false);
      return;
    }

    setLoadingProjects(true);

    Promise.all([
      projectsApi.list(orgId),
      assessmentsApi.list({ organization_id: orgId }),
    ]).then(([projectsRes, assessmentsRes]) => {
      const projectsList = Array.isArray(projectsRes) ? projectsRes : (projectsRes as any)?.data?.items || (projectsRes as any)?.data || [];
      if (Array.isArray(projectsList)) {
        setProjects(projectsList);
        if (projectsList.length > 0 && !initialProjectSet.current) {
          initialProjectSet.current = true;
          setSelectedProject(projectsList[0].id);
        }
      }

      const assessmentsList = (assessmentsRes as any)?.data?.items || [];
      if (Array.isArray(assessmentsList)) {
        const mapped: ScanHistoryItem[] = assessmentsList.map((a: any) => ({
          id: a.id,
          name: a.name || "",
          type: a.type || "unknown",
          status: a.status || "pending",
          target: a.asset?.identifier || a.config?.target || "unknown",
          findings_count: a.findings_count || 0,
          started_at: a.started_at || a.created_at || null,
          asset: a.asset || undefined,
        }));
        setScanResults(mapped);

        const storeHasLive = Object.values(
          useActiveScansStore.getState().scans
        ).some((s) => s.status === "running");
        const runningFromHistory = mapped.find((s) => s.status === "running");
        if (runningFromHistory && !storeHasLive) {
          addScan({
            id: runningFromHistory.id,
            target: runningFromHistory.target,
            scanType: runningFromHistory.type,
            startedAt:
              Date.parse(runningFromHistory.started_at ?? "") || Date.now(),
            status: "running",
          });
          setLiveScanId(runningFromHistory.id);
          setLiveRunning(true);
          setTarget(runningFromHistory.target);
          setScanType(runningFromHistory.type);
          liveActiveRef.current = true;
          void pollProgress(runningFromHistory.id);
        }
      }
    }).catch((e) => {
      console.error("Failed to load data:", e);
    }).finally(() => {
      setLoading(false);
      setLoadingProjects(false);
    });

    return () => {
      liveActiveRef.current = false;
    };
  }, []);

  useEffect(() => {
    const restored = useActiveScansStore.getState().scans;
    const running = Object.values(restored).filter(
      (s) => s.status === "running" || s.status === "paused"
    );
    if (running.length === 0) return;
    const first = running[0];
    setLiveScanId(first.id);
    setLiveRunning(true);
    setLivePaused(first.status === "paused");
    setTarget(first.target);
    setScanType(first.scanType);
    liveActiveRef.current = true;
    void pollProgress(first.id);
  }, []);

  function toggleScanType(typeId: string) {
    setSelectedScanTypes((prev) => {
      if (prev.includes(typeId)) {
        if (prev.length === 1) return prev;
        return prev.filter((t) => t !== typeId);
      }
      return [...prev, typeId];
    });
  }

  async function handleCreateScan() {
    if (!dialogTarget.trim()) return;
    if (selectedScanTypes.length === 0) {
      alert("Please select at least one scan type");
      return;
    }
    setCreating(true);
    setSuccessMessage("");
    try {
      const orgId = localStorage.getItem("organization_id");
      if (!orgId) {
        alert("Please login first to create a scan");
        setCreating(false);
        return;
      }

      for (const scanTypeId of selectedScanTypes) {
        const capabilityMap: Record<string, string> = {
          network: "network_vapt", web: "web_vapt",
          cloud: "cloud_posture", code: "code_audit",
        };

        const scanId = crypto.randomUUID();
        setLiveEvents([]);
        setLiveScanId(scanId);
        setLiveRunning(true);
        liveActiveRef.current = true;
        addScan({
          id: scanId,
          target: dialogTarget.trim(),
          scanType: capabilityMap[scanTypeId] || "web_vapt",
          startedAt: Date.now(),
          status: "running",
        });
        void pollProgress(scanId);

        try {
          await vaptScanApi.run({
            target: dialogTarget.trim(),
            scan_type: capabilityMap[scanTypeId] || "web_vapt",
            organization_id: orgId,
            project_id: selectedProjectDialog || undefined,
            client_scan_id: scanId,
          });
        } finally {
          liveActiveRef.current = false;
        }
      }
      setLiveRunning(false);

      setSuccessMessage(`${selectedScanTypes.length} scan(s) started successfully!`);
      await refreshHistory();
      setTimeout(() => {
        setShowNewScan(false);
        setDialogTarget("");
        setSelectedScanTypes(["web"]);
        setSelectedProjectDialog("");
        setSuccessMessage("");
      }, 2000);
    } catch (e: unknown) {
      alert(e instanceof Error ? e.message : "Failed to start scan");
    } finally {
      setCreating(false);
    }
  }

  async function runQuickScan() {
    if (!target.trim()) return;
    if (!selectedProject) {
      alert("Please select a project first");
      return;
    }

    setScanning(true);
    setShowResults(false);
    setResult(null);
    setFindings([]);
    setLiveEvents([]);

    const scanId = crypto.randomUUID();
    setLiveScanId(scanId);
    setLiveRunning(true);
    liveActiveRef.current = true;
    addScan({
      id: scanId,
      target: target.trim(),
      scanType,
      startedAt: Date.now(),
      status: "running",
    });
    void pollProgress(scanId);

    try {
      const orgId = localStorage.getItem("organization_id");

      const data = (await vaptScanApi.run({
        target: target.trim(),
        scan_type: scanType,
        organization_id: orgId,
        project_id: selectedProject,
        client_scan_id: scanId,
      })) as any as VaptScanResult;

      if (data.status === "stopped") {
        setLiveRunning(false);
        setLivePaused(false);
        void refreshHistory();
        return;
      }

      setResult(data);

      const rawFindings: Record<string, unknown>[] = data.findings || [];
      const mappedFindings: Finding[] = rawFindings.map((f) => ({
        id: String(f.id || crypto.randomUUID()),
        title: String(f.title || ""),
        description: String(f.description || ""),
        severity: String(f.severity || "info"),
        tool_name: String(f.tool_name || "unknown"),
        target: String(f.target || target),
        remediation: f.remediation ? String(f.remediation) : undefined,
        port: f.port ? Number(f.port) : undefined,
        host: f.host ? String(f.host) : undefined,
        protocol: f.protocol ? String(f.protocol) : undefined,
        service: f.service ? String(f.service) : undefined,
        path: f.path ? String(f.path) : undefined,
        vulnerability_type: f.vulnerability_type ? String(f.vulnerability_type) : undefined,
        reference: f.reference ? String(f.reference) : undefined,
        cve: f.cve ? String(f.cve) : undefined,
        cwe: f.cwe ? String(f.cwe) : undefined,
        payload: f.payload ? String(f.payload) : undefined,
        confidence: f.confidence ? String(f.confidence) : undefined,
        kb_context: f.kb_context ? String(f.kb_context) : undefined,
        kb_sources: Array.isArray(f.kb_sources) ? (f.kb_sources as string[]) : undefined,
        discovered_at: f.discovered_at ? String(f.discovered_at) : undefined,
      }));

      setFindings(mappedFindings);
      setShowResults(true);

      await refreshHistory();
    } catch (error) {
      console.error("Scan failed:", error);
      alert(error instanceof Error ? error.message : "Scan failed");
    } finally {
      setScanning(false);
      liveActiveRef.current = false;
      setTimeout(() => setLiveRunning(false), 2500);
    }
  }

  function StatusBadge({ status }: { status: string }) {
    const cfg = statusConfig[status] || statusConfig.pending;
    const Icon = cfg.icon;
    return (
      <Badge className={cfg.className}>
        <Icon className="w-3 h-3 mr-1" />
        {cfg.label}
      </Badge>
    );
  }

  const totalScans = scanResults.length;
  const totalFindings = scanResults.reduce((s, r) => s + r.findings_count, 0);
  const completedScans = scanResults.filter((r) => r.status === "completed").length;
  const failedScans = scanResults.filter((r) => r.status === "failed").length;

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Scans</h1>
          <p className="text-muted-foreground mt-1">
            Run instant security scans or launch comprehensive assessments
          </p>
        </div>
        <Button onClick={() => setShowNewScan(true)} variant="outline">
          <Plus className="w-4 h-4 mr-2" />
          New Scan
        </Button>
      </div>

      {successMessage && (
        <div className="bg-green-500/10 border border-green-500/30 text-green-400 px-4 py-3 rounded-lg flex items-center gap-2">
          <CheckCircle className="w-5 h-5" />
          {successMessage}
        </div>
      )}

      {!loading && scanResults.length > 0 && (
        <div className="grid gap-4 grid-cols-2 sm:grid-cols-4">
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">{totalScans}</div>
              <p className="text-sm text-muted-foreground">Total Scans</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-green-400">{completedScans}</div>
              <p className="text-sm text-muted-foreground">Completed</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold text-red-400">{failedScans}</div>
              <p className="text-sm text-muted-foreground">Failed</p>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="pt-6">
              <div className="text-2xl font-bold">{totalFindings}</div>
              <p className="text-sm text-muted-foreground">Total Findings</p>
            </CardContent>
          </Card>
        </div>
      )}

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Zap className="w-5 h-5" />
              Quick Scan
            </CardTitle>
            <CardDescription>
              Run an automated security scan on any target
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="space-y-2">
              <Label>Project</Label>
              <Select value={selectedProject} onValueChange={setSelectedProject}>
                <SelectTrigger>
                  <SelectValue placeholder="Select a project" />
                </SelectTrigger>
                <SelectContent>
                  {loadingProjects ? (
                    <SelectItem value="loading" disabled>
                      Loading projects...
                    </SelectItem>
                  ) : projects.length === 0 ? (
                    <SelectItem value="none" disabled>
                      No projects found
                    </SelectItem>
                  ) : (
                    projects.map((project) => (
                      <SelectItem key={project.id} value={project.id}>
                        <div className="flex items-center gap-2">
                          <FolderKanban className="w-4 h-4" />
                          {project.name}
                        </div>
                      </SelectItem>
                    ))
                  )}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                Scan results will be saved to selected project
              </p>
            </div>

            <div className="space-y-2">
              <Label htmlFor="quickTarget">Target</Label>
              <Input
                id="quickTarget"
                placeholder="example.com or 192.168.1.1"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
              />
            </div>

            <div className="space-y-2">
              <Label>Scan Type</Label>
              <Select value={scanType} onValueChange={setScanType}>
                <SelectTrigger>
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  {vaptScanTypes.map((type) => (
                    <SelectItem key={type.id} value={type.id}>
                      <div className="flex items-center gap-2">
                        <type.icon className="w-4 h-4" />
                        <span>{type.label}</span>
                      </div>
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
              <p className="text-xs text-muted-foreground">
                {vaptScanTypes.find((t) => t.id === scanType)?.desc}
              </p>
            </div>

            <Button
              className="w-full"
              onClick={runQuickScan}
              disabled={!target.trim() || !selectedProject || scanning}
            >
              {scanning ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Scanning...
                </>
              ) : (
                <>
                  <Zap className="w-4 h-4 mr-2" />
                  Run Scan
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Eye className="w-5 h-5" />
              Scan Status
            </CardTitle>
          </CardHeader>
          <CardContent>
            {liveRunning && liveScanId ? (
              <LiveScanConsole
                events={liveEvents}
                target={target}
                scanType={scanType}
                running={liveRunning}
                paused={livePaused}
                scanId={liveScanId}
                onResolveApproval={handleResolveApproval}
                onPause={handlePauseScan}
                onResume={handleResumeScan}
                onStop={() => setConfirmStop(true)}
              />
            ) : scanning ? (
              <div className="flex flex-col items-center justify-center py-8">
                <Loader2 className="w-12 h-12 animate-spin text-primary mb-4" />
                <p className="text-muted-foreground">Running security scan...</p>
                <p className="text-sm text-muted-foreground mt-1">
                  Analyzing {target} for vulnerabilities
                </p>
              </div>
            ) : result ? (
              <div className="space-y-4">
                <div className={`p-4 rounded-lg border ${riskColors[result.insights.risk_level] || riskColors.LOW}`}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-semibold">Risk Level</span>
                    <Badge className={getSeverityBadge(result.insights.risk_level.toLowerCase())}>
                      {result.insights.risk_level}
                    </Badge>
                  </div>
                  <p className="text-sm">{result.insights.executive_summary}</p>
                  {result.assessment_id && (
                    <p className="text-xs mt-2 text-muted-foreground">
                      Assessment ID: {result.assessment_id.slice(0, 8)}...
                    </p>
                  )}
                  <div className="flex flex-wrap gap-2 mt-3">
                    <Button size="sm" variant="outline" onClick={() => router.push("/reports")}>
                      <FileText className="w-4 h-4 mr-2" />
                      Download Report
                    </Button>
                    <Button size="sm" variant="outline" onClick={() => router.push("/graph")}>
                      <Network className="w-4 h-4 mr-2" />
                      View Attack Graph
                    </Button>
                  </div>
                </div>

                <div className="grid grid-cols-5 gap-2 text-center">
                  <div className="p-2 bg-red-500/10 border border-red-500/25 rounded-lg">
                    <div className="text-2xl font-bold text-red-400">{result.severity_breakdown.critical}</div>
                    <div className="text-xs text-muted-foreground">Critical</div>
                  </div>
                  <div className="p-2 bg-orange-500/10 border border-orange-500/25 rounded-lg">
                    <div className="text-2xl font-bold text-orange-400">{result.severity_breakdown.high}</div>
                    <div className="text-xs text-muted-foreground">High</div>
                  </div>
                  <div className="p-2 bg-yellow-500/10 border border-yellow-500/25 rounded-lg">
                    <div className="text-2xl font-bold text-yellow-400">{result.severity_breakdown.medium}</div>
                    <div className="text-xs text-muted-foreground">Medium</div>
                  </div>
                  <div className="p-2 bg-blue-500/10 border border-blue-500/25 rounded-lg">
                    <div className="text-2xl font-bold text-blue-400">{result.severity_breakdown.low}</div>
                    <div className="text-xs text-muted-foreground">Low</div>
                  </div>
                  <div className="p-2 bg-secondary/40 border border-border/60 rounded-lg">
                    <div className="text-2xl font-bold text-foreground">{result.severity_breakdown.info}</div>
                    <div className="text-xs text-muted-foreground">Info</div>
                  </div>
                </div>
              </div>
            ) : (
              <div className="flex flex-col items-center justify-center py-8 text-center">
                <Shield className="w-12 h-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">Enter a target and run a scan</p>
                <p className="text-sm text-muted-foreground mt-1">
                  Results will appear here
                </p>
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {showResults && findings.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle>Findings ({findings.length})</CardTitle>
            <CardDescription>
              Vulnerability findings from the scan
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Severity</TableHead>
                  <TableHead>Finding</TableHead>
                  <TableHead>Where</TableHead>
                  <TableHead>How</TableHead>
                  <TableHead>Insights</TableHead>
                  <TableHead>Discovered</TableHead>
                  <TableHead className="w-10"></TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {findings.map((finding) => (
                  <Fragment key={finding.id}>
                    <TableRow>
                      <TableCell>
                        <Badge className={severityColors[finding.severity] || severityColors.info}>
                          {finding.severity.toUpperCase()}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <div className="max-w-xs">
                          <div className="font-medium">{finding.title}</div>
                          <div className="text-sm text-muted-foreground line-clamp-2">
                            {finding.description}
                          </div>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="text-sm font-mono">
                          {finding.host || finding.target}
                          {finding.port ? `:${finding.port}` : ""}
                          {finding.path ? finding.path : ""}
                        </div>
                        {finding.service && (
                          <div className="text-xs text-muted-foreground">{finding.service}</div>
                        )}
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">{finding.tool_name}</Badge>
                        {finding.vulnerability_type && (
                          <div className="text-xs text-muted-foreground mt-1">
                            {finding.vulnerability_type}
                          </div>
                        )}
                      </TableCell>
                      <TableCell>
                        {finding.cve || finding.cwe ? (
                          <div className="space-y-1">
                            {finding.cve && (
                              <div className="text-xs">
                                <Badge variant="outline" className="mr-1">CVE</Badge>
                                <span className="font-mono">{finding.cve}</span>
                              </div>
                            )}
                            {finding.cwe && (
                              <div className="text-xs">
                                <Badge variant="outline" className="mr-1">CWE</Badge>
                                <span className="font-mono">{finding.cwe}</span>
                              </div>
                            )}
                          </div>
                        ) : (
                          <span className="text-xs text-muted-foreground">-</span>
                        )}
                        {finding.confidence && (
                          <div className="text-xs mt-1">
                            Confidence: <span className="font-medium">{finding.confidence}</span>
                          </div>
                        )}
                      </TableCell>
                      <TableCell className="text-xs text-muted-foreground whitespace-nowrap">
                        {finding.discovered_at
                          ? new Date(finding.discovered_at).toLocaleString()
                          : "-"}
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="sm"
                          onClick={() =>
                            setExpandedFinding(expandedFinding === finding.id ? null : finding.id)
                          }
                        >
                          <Eye className="w-4 h-4" />
                        </Button>
                      </TableCell>
                    </TableRow>
                    {expandedFinding === finding.id && (
                      <TableRow key={`${finding.id}-detail`}>
                        <TableCell colSpan={7}>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm p-2">
                            <div>
                              <div className="font-semibold mb-1">Description</div>
                              <p className="text-muted-foreground">{finding.description}</p>
                              {finding.payload && (
                                <>
                                  <div className="font-semibold mb-1 mt-3">Payload / Evidence</div>
                                  <pre className="text-xs bg-muted p-2 rounded-md overflow-x-auto font-mono">
                                    {finding.payload}
                                  </pre>
                                </>
                              )}
                            </div>
                            <div>
                              {finding.kb_context && (
                                <>
                                  <div className="font-semibold mb-1">Knowledge Base Context</div>
                                  <p className="text-muted-foreground">{finding.kb_context}</p>
                                </>
                              )}
                              {finding.kb_sources && finding.kb_sources.length > 0 && (
                                <>
                                  <div className="font-semibold mb-1 mt-3">Sources</div>
                                  <ul className="list-disc list-inside text-xs text-muted-foreground space-y-1">
                                    {finding.kb_sources.map((s) => (
                                      <li key={s} className="break-all">{s}</li>
                                    ))}
                                  </ul>
                                </>
                              )}
                              {finding.remediation && (
                                <>
                                  <div className="font-semibold mb-1 mt-3">Remediation</div>
                                  <p className="text-muted-foreground">{finding.remediation}</p>
                                </>
                              )}
                              {finding.reference && (
                                <>
                                  <div className="font-semibold mb-1 mt-3">Reference</div>
                                  <a
                                    href={finding.reference}
                                    target="_blank"
                                    rel="noreferrer"
                                    className="text-primary text-xs break-all underline"
                                  >
                                    {finding.reference}
                                  </a>
                                </>
                              )}
                            </div>
                          </div>
                        </TableCell>
                      </TableRow>
                    )}
                  </Fragment>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      {result && result.insights.recommendations.length > 0 && (
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-yellow-400" />
              AI Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {result.insights.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-400 mt-0.5 flex-shrink-0" />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Scan History</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Target</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Findings</TableHead>
                <TableHead>Started</TableHead>
                <TableHead className="w-24 text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <TableRow key={i}>
                    <TableCell colSpan={6}>
                      <div className="h-8 animate-pulse bg-muted rounded" />
                    </TableCell>
                  </TableRow>
                ))
              ) : scanResults.length === 0 ? (
                <TableRow>
                  <TableCell
                    colSpan={6}
                    className="text-center py-12 text-muted-foreground"
                  >
                    <Scan className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p className="mb-2">No scans yet.</p>
                    <p className="text-sm mb-4">
                      Use the quick scan form above or click &quot;New Scan&quot; to start.
                    </p>
                    <Button onClick={() => setShowNewScan(true)}>
                      <Plus className="w-4 h-4 mr-2" />
                      New Scan
                    </Button>
                  </TableCell>
                </TableRow>
              ) : (
                scanResults.map((scan) => {
                  const TypeIcon = getTypeIcon(scan.type);
                  return (
                    <TableRow key={scan.id}>
                      <TableCell className="font-medium">
                        {scan.target}
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline" className="capitalize gap-1">
                          <TypeIcon className="w-3 h-3" />
                          {getTypeLabel(scan.type)}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <StatusBadge status={scan.status} />
                      </TableCell>
                      <TableCell>
                        <Badge variant="outline">{scan.findings_count}</Badge>
                      </TableCell>
                      <TableCell className="text-sm text-muted-foreground">
                        {scan.started_at
                          ? formatDistanceToNow(new Date(scan.started_at), { addSuffix: true })
                          : "Just now"}
                      </TableCell>
                      <TableCell className="text-right">
                        {["completed", "failed", "stopped", "cancelled"].includes(scan.status) && (
                          <Button
                            size="sm"
                            variant="outline"
                            onClick={() => handleRestartScan(scan)}
                          >
                            <RotateCcw className="w-3.5 h-3.5 mr-1" />
                            Restart
                          </Button>
                        )}
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Dialog open={confirmStop} onOpenChange={setConfirmStop}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <StopCircle className="w-5 h-5 text-red-400" />
              Stop this scan?
            </DialogTitle>
            <DialogDescription>
              The scan will be stopped immediately and marked as stopped in history.
              Findings already discovered are kept, but the remaining phases are aborted.
            </DialogDescription>
          </DialogHeader>
          <DialogFooter>
            <Button variant="outline" onClick={() => setConfirmStop(false)}>
              Keep Scanning
            </Button>
            <Button variant="destructive" onClick={handleStopScan}>
              <StopCircle className="w-4 h-4 mr-2" />
              Stop Scan
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      <Dialog open={showNewScan} onOpenChange={setShowNewScan}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Start New Scan</DialogTitle>
            <DialogDescription>
              Configure and launch a new security assessment. Select one or more scan types.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-6 py-4">
            <div className="space-y-2">
              <Label htmlFor="dialogTarget">Target</Label>
              <Input
                id="dialogTarget"
                placeholder="e.g., https://example.com or 192.168.1.0/24"
                value={dialogTarget}
                onChange={(e) => setDialogTarget(e.target.value)}
              />
              <p className="text-xs text-muted-foreground">
                Enter a URL, IP address, or network range to scan
              </p>
            </div>

            <div className="space-y-3">
              <Label>Scan Types (select multiple)</Label>
              <div className="grid gap-3">
                {scanTypesInfo.map((type) => {
                  const TypeIcon = type.icon;
                  return (
                    <button
                      key={type.id}
                      onClick={() => toggleScanType(type.id)}
                      className={`flex items-start gap-4 p-4 border rounded-lg text-left transition-all ${
                        selectedScanTypes.includes(type.id)
                          ? "border-primary bg-primary/5 ring-2 ring-primary/20"
                          : "hover:border-primary/50"
                      }`}
                    >
                      <div className={`mt-0.5 w-5 h-5 rounded border-2 flex items-center justify-center ${
                        selectedScanTypes.includes(type.id)
                          ? "border-primary bg-primary"
                          : "border-muted-foreground"
                      }`}>
                        {selectedScanTypes.includes(type.id) && (
                          <Check className="w-3 h-3 text-white" />
                        )}
                      </div>
                      <div className="flex-1">
                        <div className="flex items-center gap-2">
                          <TypeIcon className="w-4 h-4" />
                          <span className="font-medium">{type.label}</span>
                          <Badge
                            variant="secondary"
                            className={`text-xs ${
                              type.color === "blue" ? "bg-blue-500/15 text-blue-400" :
                              type.color === "green" ? "bg-green-500/15 text-green-400" :
                              type.color === "purple" ? "bg-purple-500/20 text-purple-300" :
                              "bg-orange-500/15 text-orange-400"
                            }`}
                          >
                            {type.tools.length} tools
                          </Badge>
                        </div>
                        <div className="text-sm text-muted-foreground mt-1">
                          {type.description}
                        </div>
                        <div className="flex flex-wrap gap-1.5 mt-2">
                          {type.tools.map((tool) => (
                            <span
                              key={tool}
                              className="text-xs px-2 py-0.5 bg-muted rounded-md"
                            >
                              {tool}
                            </span>
                          ))}
                        </div>
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>

            {projects.length > 0 && (
              <div className="space-y-2">
                <Label htmlFor="dialogProject">Project (optional)</Label>
                <select
                  id="dialogProject"
                  className="w-full px-3 py-2 border rounded-lg bg-background text-sm"
                  value={selectedProjectDialog}
                  onChange={(e) => setSelectedProjectDialog(e.target.value)}
                >
                  <option value="">No project</option>
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name}
                    </option>
                  ))}
                </select>
              </div>
            )}
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowNewScan(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleCreateScan}
              disabled={!dialogTarget.trim() || selectedScanTypes.length === 0 || creating}
            >
              {creating ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Starting {selectedScanTypes.length} scan(s)...
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 mr-2" />
                  Start {selectedScanTypes.length > 1 ? `${selectedScanTypes.length} Scans` : "Scan"}
                </>
              )}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
