"use client";

import { useEffect, useState } from "react";
import { scanApi, projectsApi } from "@/services/api";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
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
  Play,
  CheckCircle,
  Clock,
  Plus,
  Scan,
  Loader2,
  Check,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import type { Project } from "@/types";

const scanTypesInfo = [
  {
    id: "network",
    label: "Network VAPT",
    description: "Scan network ranges for open ports and services",
    tools: ["Nmap", "Masscan", "Netbiosenum", "SMB Enum", "DNS Recon"],
    color: "blue",
  },
  {
    id: "web",
    label: "Web App VAPT",
    description: "Assess web applications for OWASP Top 10",
    tools: ["Nikto", "SQLMap", "XSStrike", "Dirbuster", "Burp Suite"],
    color: "green",
  },
  {
    id: "cloud",
    label: "Cloud Security",
    description: "Review cloud infrastructure for misconfigurations",
    tools: ["Prowler", "Scout Suite", "CloudSploit", "Principal Mapper"],
    color: "purple",
  },
  {
    id: "code",
    label: "Code Audit",
    description: "Static analysis of source code",
    tools: ["Semgrep", "Bandit", "SonarQube", "CodeQL", "Brakeman"],
    color: "orange",
  },
];

interface ScanResult {
  id: string;
  name: string;
  type: string;
  status: string;
  target: string;
  findings_count: number;
  started_at: string | null;
  asset?: { name: string };
}

export default function ScansPage() {
  const [scanResults, setScanResults] = useState<ScanResult[]>([]);
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewScan, setShowNewScan] = useState(false);
  const [target, setTarget] = useState("");
  const [selectedScanTypes, setSelectedScanTypes] = useState<string[]>(["web"]);
  const [selectedProject, setSelectedProject] = useState("");
  const [creating, setCreating] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");

  async function loadData() {
    try {
      const orgId = localStorage.getItem("organization_id");
      if (!orgId) {
        setLoading(false);
        return;
      }
      const projectsRes = await projectsApi.list(orgId);
      const projects = projectsRes as unknown as any[];
      if (Array.isArray(projects)) {
        setProjects(projects);
      }
    } catch (e) {
      console.error("Failed to load data:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadData();
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
    if (!target.trim()) return;
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

      const results: ScanResult[] = [];

      for (const scanType of selectedScanTypes) {
        const capabilityMap: Record<string, string> = {
          network: "network_vapt",
          web: "web_vapt",
          cloud: "cloud_posture",
          code: "code_audit",
        };

        const res = await scanApi.run({
          target: target.trim(),
          capability_id: capabilityMap[scanType] || "web_vapt",
          config: {
            organization_id: orgId,
            project_id: selectedProject || undefined,
            scan_type: scanType,
          },
        });

        const resData = res as unknown as { success?: boolean; data?: any };
        const scanData = resData && resData.success && resData.data ? resData.data : res;
        if (scanData && scanData.id) {
          results.push(scanData);
        }
      }

      if (results.length > 0) {
        setScanResults((prev) => [...results, ...prev]);
        setSuccessMessage(`${results.length} scan(s) started successfully!`);
        setTimeout(() => {
          setShowNewScan(false);
          setTarget("");
          setSelectedScanTypes(["web"]);
          setSelectedProject("");
          setSuccessMessage("");
        }, 2000);
      }
    } catch (e: unknown) {
      alert(e instanceof Error ? e.message : "Failed to start scan");
    } finally {
      setCreating(false);
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Scans</h1>
          <p className="text-muted-foreground mt-1">
            Manage and monitor your security assessments
          </p>
        </div>
        <Button onClick={() => setShowNewScan(true)}>
          <Plus className="w-4 h-4 mr-2" />
          New Scan
        </Button>
      </div>

      {successMessage && (
        <div className="bg-green-50 border border-green-200 text-green-800 px-4 py-3 rounded-lg flex items-center gap-2">
          <CheckCircle className="w-5 h-5" />
          {successMessage}
        </div>
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
                <TableHead>Scan Type</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Findings</TableHead>
                <TableHead>Started</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <TableRow key={i}>
                    <TableCell colSpan={5}>
                      <div className="h-8 animate-pulse bg-muted rounded" />
                    </TableCell>
                  </TableRow>
                ))
              ) : scanResults.length === 0 ? (
                <TableRow>
                  <TableCell
                    colSpan={5}
                    className="text-center py-12 text-muted-foreground"
                  >
                    <Scan className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p className="mb-4">No scans yet. Start your first security assessment.</p>
                    <Button onClick={() => setShowNewScan(true)}>
                      <Plus className="w-4 h-4 mr-2" />
                      New Scan
                    </Button>
                  </TableCell>
                </TableRow>
              ) : (
                scanResults.map((scan) => (
                  <TableRow key={scan.id}>
                    <TableCell className="font-medium">
                      {scan.target}
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline" className="capitalize">
                        {scan.type.replace("_", " ")}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge className="bg-yellow-100 text-yellow-800">
                        <Clock className="w-3 h-3 mr-1" />
                        Pending
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">0</Badge>
                    </TableCell>
                    <TableCell>
                      {scan.started_at
                        ? formatDistanceToNow(new Date(scan.started_at), {
                            addSuffix: true,
                          })
                        : "Just now"}
                    </TableCell>
                  </TableRow>
                ))
              )}
            </TableBody>
          </Table>
        </CardContent>
      </Card>

      <Dialog open={showNewScan} onOpenChange={setShowNewScan}>
        <DialogContent className="max-w-2xl max-h-[90vh] overflow-y-auto">
          <DialogHeader>
            <DialogTitle>Start New Scan</DialogTitle>
            <DialogDescription>
              Configure and launch a new security assessment scan. Select one or more scan types.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-6 py-4">
            <div className="space-y-2">
              <Label htmlFor="target">Target</Label>
              <Input
                id="target"
                placeholder="e.g., https://example.com or 192.168.1.0/24"
                value={target}
                onChange={(e) => setTarget(e.target.value)}
              />
              <p className="text-xs text-muted-foreground">
                Enter a URL, IP address, or network range to scan
              </p>
            </div>

            <div className="space-y-3">
              <Label>Scan Types (select multiple)</Label>
              <div className="grid gap-3">
                {scanTypesInfo.map((type) => (
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
                        <span className="font-medium">{type.label}</span>
                        <Badge
                          variant="secondary"
                          className={`text-xs ${
                            type.color === "blue" ? "bg-blue-100 text-blue-800" :
                            type.color === "green" ? "bg-green-100 text-green-800" :
                            type.color === "purple" ? "bg-purple-100 text-purple-800" :
                            "bg-orange-100 text-orange-800"
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
                ))}
              </div>
            </div>

            {projects.length > 0 && (
              <div className="space-y-2">
                <Label htmlFor="project">Project (optional)</Label>
                <select
                  id="project"
                  className="w-full px-3 py-2 border rounded-lg bg-background text-sm"
                  value={selectedProject}
                  onChange={(e) => setSelectedProject(e.target.value)}
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
              disabled={!target.trim() || selectedScanTypes.length === 0 || creating}
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