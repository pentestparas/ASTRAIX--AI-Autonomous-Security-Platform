"use client";

import { useEffect, useState } from "react";
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
  Plus,
  Activity,
  ShieldAlert,
  Server,
  Play,
} from "lucide-react";
import Link from "next/link";
import type { Project, Assessment, Asset, Finding } from "@/types";

export default function ProjectDetailPage() {
  const params = useParams();
  const projectId = params?.id as string;

  const [project, setProject] = useState<Project | null>(null);
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [assets, setAssets] = useState<Asset[]>([]);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"assessments" | "assets" | "findings">("assessments");

  useEffect(() => {
    async function load() {
      try {
        const [projRes, assessRes, assetRes, findingRes] = await Promise.all([
          projectsApi.get(projectId),
          assessmentsApi.list({ project_id: projectId, limit: 20 }),
          assetsApi.list({ project_id: projectId, limit: 50 }),
          findingsApi.list({ project_id: projectId, limit: 50 }),
        ]);

        if (projRes.success && projRes.data) setProject(projRes.data as Project);
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
        <Button>
          <Plus className="w-4 h-4 mr-2" />
          Add Asset
        </Button>
      </div>

      <div className="grid gap-4 md:grid-cols-4">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-3">
              <Server className="w-8 h-8 text-blue-500" />
              <div>
                <div className="text-2xl font-bold">{assets.length}</div>
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
                <div className="text-2xl font-bold">{assessments.length}</div>
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
                <div className="text-2xl font-bold">{findings.length}</div>
                <div className="text-sm text-muted-foreground">Findings</div>
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
                  {findings.filter((f) => f.severity === "critical" || f.severity === "high").length}
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
                  <TableHead>Asset</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Findings</TableHead>
                  <TableHead>Started</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {assessments.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                      No scans yet for this project
                    </TableCell>
                  </TableRow>
                ) : (
                  assessments.map((a) => (
                    <TableRow key={a.id}>
                      <TableCell className="font-medium">
                        {a.asset?.name ?? "—"}
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
                  <TableHead>Name</TableHead>
                  <TableHead>Type</TableHead>
                  <TableHead>Identifier</TableHead>
                  <TableHead>Criticality</TableHead>
                  <TableHead>Last Scanned</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {assets.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={5} className="text-center py-8 text-muted-foreground">
                      No assets yet. Add an asset to start scanning.
                    </TableCell>
                  </TableRow>
                ) : (
                  assets.map((asset) => (
                    <TableRow key={asset.id}>
                      <TableCell className="font-medium">{asset.name}</TableCell>
                      <TableCell className="capitalize">{asset.type}</TableCell>
                      <TableCell className="font-mono text-sm text-muted-foreground">
                        {asset.identifier}
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            asset.criticality === "critical"
                              ? "destructive"
                              : asset.criticality === "high"
                                ? "default"
                                : "secondary"
                          }
                          className="capitalize"
                        >
                          {asset.criticality}
                        </Badge>
                      </TableCell>
                      <TableCell className="text-muted-foreground text-sm">
                        {asset.last_scanned
                          ? new Date(asset.last_scanned).toLocaleString()
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