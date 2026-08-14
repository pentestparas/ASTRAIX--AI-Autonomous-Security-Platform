"use client";

import { Fragment, useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { projectsApi, assessmentsApi, assetsApi, findingsApi } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import {
  ArrowLeft,
  Activity,
  ShieldAlert,
  Server,
  ChevronDown,
  ChevronRight,
  Globe,
  ExternalLink,
  CalendarClock,
  Fingerprint,
} from "lucide-react";
import Link from "next/link";
import { formatDistanceToNow } from "date-fns";
import type { Project, Assessment, Asset, Finding } from "@/types";

const severityConfig = {
  critical: { label: "Critical", className: "bg-red-500/15 text-red-400 border-red-500/30" },
  high: { label: "High", className: "bg-orange-500/15 text-orange-400 border-orange-500/30" },
  medium: { label: "Medium", className: "bg-yellow-500/15 text-yellow-400 border-yellow-500/30" },
  low: { label: "Low", className: "bg-blue-500/15 text-blue-400 border-blue-500/30" },
  info: { label: "Info", className: "bg-secondary text-secondary-foreground border-border/60" },
};

const cvssColor = (s: number) =>
  s >= 9 ? "text-red-400 font-bold" : s >= 7 ? "text-orange-400 font-bold" : s >= 4 ? "text-yellow-400" : "text-green-400";

const statusOptions: Finding["status"][] = ["open", "triaged", "resolved", "false_positive", "accepted"];

const fmtLabel = (s: string) =>
  s.replace("_", " ").replace(/\b\w/g, (c: string) => c.toUpperCase());

function registrableDomain(host: string): string {
  const clean = host.trim().replace(/^https?:\/\//, "").replace(/\/.*$/, "");
  if (/^\d{1,3}(\.\d{1,3}){3}$/.test(clean) || clean === "localhost") return clean;
  const labels = clean.split(".");
  if (labels.length <= 2) return clean;
  return labels.slice(-2).join(".");
}

export default function ProjectDetailPage() {
  const params = useParams();
  const projectId = params?.id as string;

  const [project, setProject] = useState<Project | null>(null);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"assessments" | "assets" | "findings">("assessments");
  const [expandedDomains, setExpandedDomains] = useState<Set<string>>(new Set());
  const [selected, setSelected] = useState<Finding | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [projRes, assessRes, assetRes, findingRes] = await Promise.all([
          projectsApi.get(projectId),
          assessmentsApi.list({ project_id: projectId, limit: 20 }),
          assetsApi.list({ project_id: projectId, limit: 50 }),
          findingsApi.list({ project_id: projectId, limit: 50 }),
        ]);

        if (projRes) {
          const projectData = (projRes as any).data ?? projRes;
          setProject(projectData as Project);
        }
        if (assessRes.success && assessRes.data)
          setAssessments(
            Array.isArray(assessRes.data)
              ? assessRes.data
              : assessRes.data.items ?? []
          );
        if (assetRes.success && assetRes.data)
          setAssets(
            Array.isArray(assetRes.data)
              ? assetRes.data
              : assetRes.data.items ?? []
          );
        if (findingRes.success && findingRes.data)
          setFindings(
            Array.isArray(findingRes.data)
              ? findingRes.data
              : findingRes.data.items ?? []
          );
      } catch (e) {
        console.error("Failed to load project:", e);
      } finally {
        setLoading(false);
      }
    }
    if (projectId) load();
  }, [projectId]);

  async function handleStatusChange(id: string, newStatus: Finding["status"]) {
    try {
      await findingsApi.update(id, { status: newStatus });
      setSelected((prev) => (prev && prev.id === id ? { ...prev, status: newStatus } : prev));
      const [findingRes] = await Promise.all([
        findingsApi.list({ project_id: projectId, limit: 50 }),
      ]);
      if (findingRes.success && findingRes.data)
        setFindings(
          Array.isArray(findingRes.data)
            ? findingRes.data
            : findingRes.data.items ?? []
        );
    } catch (e) {
      console.error("Failed to update finding:", e);
    }
  }

  const groupedAssessments = useMemo(() => {
    const map = new Map<string, Assessment[]>();
    assessments.forEach((a) => {
      const domain =
        registrableDomain(a.asset_name ?? a.asset?.name ?? "") || "Unknown";
      if (!map.has(domain)) map.set(domain, []);
      map.get(domain)!.push(a);
    });
    return [...map.entries()]
      .map(([domain, list]) => {
        const sorted = [...list].sort((a, b) =>
          (b.started_at ?? "").localeCompare(a.started_at ?? "")
        );
        const latest = sorted[0];
        return {
          domain,
          scans: sorted,
          count: list.length,
          totalFindings: list.reduce(
            (sum, a) => sum + (a.findings_count ?? 0),
            0
          ),
          latest,
        };
      })
      .sort((a, b) =>
        (b.latest?.started_at ?? "").localeCompare(a.latest?.started_at ?? "")
      );
  }, [assessments]);

  const groupedAssets = useMemo(() => {
    const map = new Map<string, Asset[]>();
    assets.forEach((a) => {
      const domain = registrableDomain(a.identifier || a.name || "");
      if (!map.has(domain)) map.set(domain, []);
      map.get(domain)!.push(a);
    });
    const severityRank = ["critical", "high", "medium", "low", "info"];
    return [...map.entries()]
      .map(([domain, list]) => ({
        domain,
        count: list.length,
        types: [...new Set(list.map((a) => a.type))],
        criticality:
          severityRank.find((s) => list.some((a) => a.criticality === s)) ||
          "low",
        lastScanned:
          Math.max(
            ...list.map((a) =>
              a.last_scanned ? Date.parse(a.last_scanned) : 0
            )
          ) || null,
      }))
      .sort((a, b) => (b.lastScanned ?? 0) - (a.lastScanned ?? 0));
  }, [assets]);

  function toggleDomain(domain: string) {
    setExpandedDomains((prev) => {
      const next = new Set(prev);
      if (next.has(domain)) next.delete(domain);
      else next.add(domain);
      return next;
    });
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Activity className="w-6 h-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  if (!project) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">Project not found</p>
        <Link href="/projects">
          <Button variant="link" className="mt-2">
            <ArrowLeft className="w-4 h-4 mr-2" />
            Back to Projects
          </Button>
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center gap-4">
        <Link href="/projects">
          <Button variant="ghost" size="icon">
            <ArrowLeft className="w-4 h-4" />
          </Button>
        </Link>
        <div className="flex-1">
          <h1 className="text-3xl font-bold tracking-tight">{project.name}</h1>
          <p className="text-muted-foreground mt-1">
            {project.description || "No description"}
          </p>
        </div>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Server className="w-8 h-8 text-blue-500" />
              <div>
                <div className="text-2xl font-bold">{project.assets_count ?? assets.length}</div>
                <div className="text-sm text-muted-foreground">Assets</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Activity className="w-8 h-8 text-purple-500" />
              <div>
                <div className="text-2xl font-bold">{project.assessments_count ?? assessments.length}</div>
                <div className="text-sm text-muted-foreground">Scans</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <ShieldAlert className="w-8 h-8 text-red-500" />
              <div>
                <div className="text-2xl font-bold">{project.open_findings_count ?? findings.length}</div>
                <div className="text-sm text-muted-foreground">Open Findings</div>
              </div>
            </div>
          </CardContent>
        </Card>
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <ShieldAlert className="w-8 h-8 text-orange-500" />
              <div>
                <div className="text-2xl font-bold">
                  {project.critical_findings_count ?? findings.filter((f) => f.severity === "critical" || f.severity === "high").length}
                </div>
                <div className="text-sm text-muted-foreground">Critical/High</div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      <div className="flex gap-2 border-b">
        {(["assessments", "assets", "findings"] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition-colors capitalize ${
              activeTab === tab
                ? "border-primary text-primary"
                : "border-transparent text-muted-foreground hover:text-foreground"
            }`}
          >
            {tab}
          </button>
        ))}
      </div>

      {activeTab === "assessments" && (
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Domain</TableHead>
                  <TableHead>Scans</TableHead>
                  <TableHead>Findings</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Last Scan</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {groupedAssessments.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                      No scans yet for this project
                    </TableCell>
                  </TableRow>
                ) : (
                  groupedAssessments.map((group) => (
                    <Fragment key={group.domain}>
                      <TableRow
                        className="cursor-pointer hover:bg-muted/50"
                        onClick={() => toggleDomain(group.domain)}
                      >
                        <TableCell className="font-medium">
                          <span className="inline-flex items-center gap-2">
                            {expandedDomains.has(group.domain) ? (
                              <ChevronDown className="w-4 h-4 text-muted-foreground" />
                            ) : (
                              <ChevronRight className="w-4 h-4 text-muted-foreground" />
                            )}
                            {group.domain}
                          </span>
                        </TableCell>
                        <TableCell>
                          <Badge variant="secondary">{group.count}</Badge>
                        </TableCell>
                        <TableCell>
                          <Badge variant="secondary">{group.totalFindings}</Badge>
                        </TableCell>
                        <TableCell>
                          <Badge
                            variant={
                              group.latest?.status === "completed"
                                ? "secondary"
                                : group.latest?.status === "running"
                                  ? "default"
                                  : "outline"
                            }
                            className="capitalize"
                          >
                            {group.latest?.status ?? "—"}
                          </Badge>
                        </TableCell>
                        <TableCell className="text-muted-foreground text-sm">
                          {group.latest?.started_at
                            ? new Date(group.latest.started_at).toLocaleString()
                            : "—"}
                        </TableCell>
                      </TableRow>
                      {expandedDomains.has(group.domain) && (
                        <TableRow className="bg-muted/40">
                          <TableCell colSpan={5} className="p-0">
                            <div className="px-6 py-3">
                              <Table>
                                <TableHeader>
                                  <TableRow>
                                    <TableHead>Asset</TableHead>
                                    <TableHead>Type</TableHead>
                                    <TableHead>Status</TableHead>
                                    <TableHead>Findings</TableHead>
                                    <TableHead>Started</TableHead>
                                  </TableRow>
                                </TableHeader>
                                <TableBody>
                                  {group.scans.map((a) => (
                                    <TableRow key={a.id}>
                                      <TableCell className="font-medium">
                                        {a.asset_name ?? a.asset?.name ?? "—"}
                                      </TableCell>
                                      <TableCell className="capitalize">{a.type}</TableCell>
                                      <TableCell>
                                        <Badge
                                          variant={
                                            a.status === "completed"
                                              ? "secondary"
                                              : a.status === "running"
                                                ? "default"
                                                : "outline"
                                          }
                                          className="capitalize"
                                        >
                                          {a.status}
                                        </Badge>
                                      </TableCell>
                                      <TableCell>
                                        <Badge variant="secondary">{a.findings_count}</Badge>
                                      </TableCell>
                                      <TableCell className="text-muted-foreground text-sm">
                                        {a.started_at
                                          ? new Date(a.started_at).toLocaleString()
                                          : "—"}
                                      </TableCell>
                                    </TableRow>
                                  ))}
                                </TableBody>
                              </Table>
                            </div>
                          </TableCell>
                        </TableRow>
                      )}
                    </Fragment>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      {activeTab === "assets" && (
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Domain</TableHead>
                  <TableHead>Subdomains</TableHead>
                  <TableHead>Types</TableHead>
                  <TableHead>Criticality</TableHead>
                  <TableHead>Last Scanned</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {groupedAssets.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                      No assets yet. Add an asset to start scanning.
                    </TableCell>
                  </TableRow>
                ) : (
                  groupedAssets.map((group) => (
                    <TableRow key={group.domain}>
                      <TableCell className="font-medium">{group.domain}</TableCell>
                      <TableCell>
                        <Badge variant="secondary">{group.count}</Badge>
                      </TableCell>
                      <TableCell className="capitalize text-muted-foreground">
                        {group.types.join(", ")}
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            group.criticality === "critical"
                              ? "destructive"
                              : group.criticality === "high"
                                ? "default"
                                : "secondary"
                          }
                          className="capitalize"
                        >
                          {group.criticality}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-muted-foreground text-sm">
                        {group.lastScanned
                          ? new Date(group.lastScanned).toLocaleString()
                          : "Never"}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      {activeTab === "findings" && (
        <Card>
          <CardContent className="p-0">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Severity</TableHead>
                  <TableHead>Title</TableHead>
                  <TableHead>Asset</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>CVSS</TableHead>
                  <TableHead>Age</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {findings.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                      No vulnerabilities yet for this project
                    </TableCell>
                  </TableRow>
                ) : (
                  findings.map((f) => {
                    const sev = severityConfig[f.severity] || severityConfig.info;
                    return (
                      <TableRow
                        key={f.id}
                        className="cursor-pointer hover:bg-muted/50"
                        onClick={() => setSelected(f)}
                      >
                        <TableCell>
                          <Badge className={sev.className} variant="default">
                            {sev.label}
                          </Badge>
                        </TableCell>
                        <TableCell className="font-medium max-w-md truncate">
                          {f.title || "—"}
                        </TableCell>
                        <TableCell className="text-muted-foreground max-w-xs truncate">
                          {f.asset?.name ?? f.asset_id ?? "—"}
                        </TableCell>
                        <TableCell>
                          <Badge variant="secondary" className="capitalize">
                            {fmtLabel(f.status)}
                          </Badge>
                        </TableCell>
                        <TableCell>
                          {f.cvss_score != null ? (
                            <span className={cvssColor(f.cvss_score)}>
                              {f.cvss_score.toFixed(1)}
                            </span>
                          ) : (
                            "—"
                          )}
                        </TableCell>
                        <TableCell className="text-muted-foreground text-sm">
                          {formatDistanceToNow(new Date(f.created_at), {
                            addSuffix: true,
                          })}
                        </TableCell>
                      </TableRow>
                    );
                  })
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}

      <Dialog open={!!selected} onOpenChange={(open) => !open && setSelected(null)}>
        <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
          {selected && (
            <>
              <DialogHeader>
                <DialogTitle className="text-left pr-8">
                  <div className="text-base font-semibold text-foreground break-words">
                    {selected.title || "Untitled finding"}
                  </div>
                  <div className="mt-2 flex items-center gap-2 flex-wrap">
                    <Badge
                      className={
                        (severityConfig[selected.severity] || severityConfig.info).className
                      }
                      variant="default"
                    >
                      {(severityConfig[selected.severity] || severityConfig.info).label}
                    </Badge>
                    <Badge variant="outline" className="font-mono">
                      {fmtLabel(selected.status)}
                    </Badge>
                    {selected.cvss_score != null && (
                      <span className={`text-sm ${cvssColor(selected.cvss_score)}`}>
                        CVSS {selected.cvss_score.toFixed(1)}
                      </span>
                    )}
                  </div>
                </DialogTitle>
              </DialogHeader>

              <div className="space-y-4 text-sm">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Globe className="w-4 h-4 shrink-0" />
                    <span className="font-medium text-foreground">
                      {selected.asset?.name ?? selected.asset_id ?? "Unknown asset"}
                    </span>
                  </div>
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <CalendarClock className="w-4 h-4 shrink-0" />
                    Found {formatDistanceToNow(new Date(selected.created_at), { addSuffix: true })}
                  </div>
                </div>

                {selected.description ? (
                  <div>
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                      Description
                    </p>
                    <p className="whitespace-pre-wrap text-foreground/90 leading-relaxed">
                      {selected.description}
                    </p>
                  </div>
                ) : null}

                {selected.asset_id && (
                  <div>
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                      Asset ID
                    </p>
                    <p className="font-mono text-xs break-all">{selected.asset_id}</p>
                  </div>
                )}

                {selected.assessment_id && (
                  <div>
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                      Assessment ID
                    </p>
                    <p className="font-mono text-xs break-all">{selected.assessment_id}</p>
                  </div>
                )}

                {selected.plugin_id && (
                  <div className="flex items-center gap-2 text-muted-foreground">
                    <Fingerprint className="w-4 h-4 shrink-0" />
                    <span className="font-mono text-xs">{selected.plugin_id}</span>
                  </div>
                )}

                {selected.remediation ? (
                  <div>
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                      Remediation
                    </p>
                    <p className="whitespace-pre-wrap text-foreground/90 leading-relaxed">
                      {selected.remediation}
                    </p>
                  </div>
                ) : null}

                {selected.reference ? (
                  <div>
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                      References
                    </p>
                    {String(selected.reference)
                      .split(/[\n,]/)
                      .filter(Boolean)
                      .map((ref, i) => (
                        <p key={i} className="text-blue-400 flex items-center gap-1 break-all">
                          <ExternalLink className="w-3.5 h-3.5 shrink-0" />
                          {ref.trim()}
                        </p>
                      ))}
                  </div>
                ) : null}

                {selected.details && Object.keys(selected.details).length > 0 ? (
                  <div>
                    <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wide mb-1">
                      Evidence & Metadata
                    </p>
                    <pre className="p-3 rounded-lg bg-muted/60 border border-border text-xs overflow-x-auto max-h-64">
                      {JSON.stringify(selected.details, null, 2)}
                    </pre>
                  </div>
                ) : null}

                <div className="flex justify-end pt-2 border-t border-border">
                  <select
                    className="text-xs px-2 py-1.5 border rounded bg-background"
                    value={selected.status}
                    onChange={(e) =>
                      handleStatusChange(selected.id, e.target.value as Finding["status"])
                    }
                  >
                    {statusOptions.map((s) => (
                      <option key={s} value={s}>
                        {fmtLabel(s)}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}