"use client";

import { Fragment, useEffect, useMemo, useState } from "react";
import { useParams } from "next/navigation";
import { projectsApi, assessmentsApi, assetsApi, findingsApi } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
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
  ArrowLeft,
  Activity,
  ShieldAlert,
  Server,
  Play,
  ChevronDown,
  ChevronRight,
} from "lucide-react";
import Link from "next/link";
import type { Project, Assessment, Asset, Finding } from "@/types";

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

  const severityColors: Record<string, string> = {
    critical: "bg-red-500 text-white",
    high: "bg-orange-500 text-white",
    medium: "bg-yellow-500 text-white",
    low: "bg-blue-500 text-white",
    info: "bg-gray-500 text-white",
  };

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
                </TableRow>
              </TableHeader>
              <TableBody>
                {findings.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                      No findings yet for this project
                    </TableCell>
                  </TableRow>
                ) : (
                  findings.map((f) => (
                    <TableRow key={f.id}>
                      <TableCell>
                        <Badge className={severityColors[f.severity] ?? severityColors.info}>
                          {f.severity}
                        </Badge>
                      </TableCell>
                      <TableCell className="font-medium">{f.title}</TableCell>
                      <TableCell className="text-muted-foreground">
                        {f.asset?.name ?? "—"}
                      </TableCell>
                      <TableCell>
                        <Badge variant="secondary" className="capitalize">
                          {f.status}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {f.cvss_score ?? "—"}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      )}
    </div>
  );
}