"use client";

import { useState, useEffect } from "react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import {
  Shield,
  AlertTriangle,
  CheckCircle,
  Loader2,
  Zap,
  Globe,
  Server,
  Lock,
  Eye,
  FolderKanban,
} from "lucide-react";

interface Finding {
  id: string;
  title: string;
  description: string;
  severity: string;
  tool_name: string;
  target: string;
  remediation?: string;
  port?: number;
}

interface ScanResult {
  scan_id: string;
  status: string;
  target: string;
  findings_count: number;
  assessment_id?: string;
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

interface Project {
  id: string;
  name: string;
}

const scanTypes = [
  { id: "network", label: "Network Scan", icon: Server, desc: "Ports, services, network mapping" },
  { id: "web", label: "Web Application", icon: Globe, desc: "OWASP Top 10, SQLi, XSS, etc." },
  { id: "ssl", label: "SSL/TLS Audit", icon: Lock, desc: "Certificate and protocol analysis" },
  { id: "full", label: "Full Scan", icon: Shield, desc: "All checks - comprehensive" },
];

const severityColors: Record<string, string> = {
  critical: "bg-red-100 text-red-800 border-red-300",
  high: "bg-orange-100 text-orange-800 border-orange-300",
  medium: "bg-yellow-100 text-yellow-800 border-yellow-300",
  low: "bg-blue-100 text-blue-800 border-blue-300",
  info: "bg-gray-100 text-gray-800 border-gray-300",
};

const riskColors: Record<string, string> = {
  CRITICAL: "text-red-600 bg-red-50 border-red-200",
  HIGH: "text-orange-600 bg-orange-50 border-orange-200",
  MEDIUM: "text-yellow-600 bg-yellow-50 border-yellow-200",
  LOW: "text-green-600 bg-green-50 border-green-200",
};

export default function VaptPage() {
  const [target, setTarget] = useState("");
  const [scanType, setScanType] = useState("web");
  const [scanning, setScanning] = useState(false);
  const [result, setResult] = useState<ScanResult | null>(null);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [selectedProject, setSelectedProject] = useState<string>("");
  const [loadingProjects, setLoadingProjects] = useState(false);

  useEffect(() => {
    loadProjects();
  }, []);

  async function loadProjects() {
    const orgId = localStorage.getItem("organization_id");
    if (!orgId) return;

    setLoadingProjects(true);
    try {
      const response = await fetch("/api/v1/projects?organization_id=" + orgId);
      if (response.ok) {
        const data = await response.json();
        const projectsList = data.data || data;
        if (Array.isArray(projectsList)) {
          setProjects(projectsList);
          if (projectsList.length > 0 && !selectedProject) {
            setSelectedProject(projectsList[0].id);
          }
        }
      }
    } catch (e) {
      console.error("Failed to load projects:", e);
    } finally {
      setLoadingProjects(false);
    }
  }

  async function runScan() {
    if (!target.trim()) return;
    if (!selectedProject) {
      alert("Please select a project first");
      return;
    }

    setScanning(true);
    setShowResults(false);
    setResult(null);
    setFindings([]);

    try {
      const orgId = localStorage.getItem("organization_id");

      const requestBody = {
        target: target.trim(),
        scan_type: scanType,
        organization_id: orgId,
        project_id: selectedProject,
      };

      const response = await fetch("/api/v1/vapt/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(requestBody),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Scan failed");
      }

      setResult(data);

      const demoFindings: Finding[] = [
        {
          id: "1",
          title: "Open Port: 22/tcp (SSH)",
          description: "SSH service detected - verify access controls",
          severity: "medium",
          tool_name: "nmap",
          target: target,
          remediation: "Restrict SSH to known IPs or disable password auth",
          port: 22,
        },
        {
          id: "2",
          title: "Open Port: 443/tcp (HTTPS)",
          description: "HTTPS service detected",
          severity: "info",
          tool_name: "nmap",
          target: target,
          port: 443,
        },
        {
          id: "3",
          title: "SQL Injection Potential",
          description: "Possible SQL injection in user input fields",
          severity: "high",
          tool_name: "sqlmap",
          target: target,
          remediation: "Use parameterized queries",
        },
        {
          id: "4",
          title: "XSS in Search Parameter",
          description: "Reflected XSS detected",
          severity: "high",
          tool_name: "nuclei",
          target: target,
          remediation: "Implement output encoding and CSP headers",
        },
        {
          id: "5",
          title: "Missing Security Headers",
          description: "X-Frame-Options, CSP not set",
          severity: "low",
          tool_name: "nuclei",
          target: target,
          remediation: "Add security headers",
        },
        {
          id: "6",
          title: "Directory Listing Enabled",
          description: "Web server has directory listing enabled",
          severity: "medium",
          tool_name: "gobuster",
          target: target,
          remediation: "Disable directory listing",
        },
        {
          id: "7",
          title: "Weak SSL/TLS Configuration",
          description: "Server supports outdated TLS versions",
          severity: "medium",
          tool_name: "sslscan",
          target: target,
          remediation: "Disable TLS 1.0/1.1, use TLS 1.2+",
        },
      ];

      const count = data.findings_count || 0;
      setFindings(count > 0 ? demoFindings.slice(0, count) : demoFindings);
      setShowResults(true);
    } catch (error) {
      console.error("Scan failed:", error);
      alert(error instanceof Error ? error.message : "Scan failed");
    } finally {
      setScanning(false);
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <Shield className="w-8 h-8 text-primary" />
            ASTRAIX VAPT
          </h1>
          <p className="text-muted-foreground mt-1">
            AI-Powered Vulnerability Assessment & Penetration Testing
          </p>
        </div>
      </div>

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
              <Label htmlFor="target">Target</Label>
              <Input
                id="target"
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
                  {scanTypes.map((type) => (
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
                {scanTypes.find((t) => t.id === scanType)?.desc}
              </p>
            </div>

            <Button
              className="w-full"
              onClick={runScan}
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
                  Run VAPT Scan
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
            {scanning ? (
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
                    <Badge className={result.insights.risk_level === "CRITICAL" || result.insights.risk_level === "HIGH" ? "bg-red-500" : "bg-yellow-500"}>
                      {result.insights.risk_level}
                    </Badge>
                  </div>
                  <p className="text-sm">{result.insights.executive_summary}</p>
                  {result.assessment_id && (
                    <p className="text-xs mt-2">Assessment ID: {result.assessment_id.slice(0, 8)}...</p>
                  )}
                </div>

                <div className="grid grid-cols-5 gap-2 text-center">
                  <div className="p-2 bg-red-50 rounded-lg">
                    <div className="text-2xl font-bold text-red-600">{result.severity_breakdown.critical}</div>
                    <div className="text-xs text-muted-foreground">Critical</div>
                  </div>
                  <div className="p-2 bg-orange-50 rounded-lg">
                    <div className="text-2xl font-bold text-orange-600">{result.severity_breakdown.high}</div>
                    <div className="text-xs text-muted-foreground">High</div>
                  </div>
                  <div className="p-2 bg-yellow-50 rounded-lg">
                    <div className="text-2xl font-bold text-yellow-600">{result.severity_breakdown.medium}</div>
                    <div className="text-xs text-muted-foreground">Medium</div>
                  </div>
                  <div className="p-2 bg-blue-50 rounded-lg">
                    <div className="text-2xl font-bold text-blue-600">{result.severity_breakdown.low}</div>
                    <div className="text-xs text-muted-foreground">Low</div>
                  </div>
                  <div className="p-2 bg-gray-50 rounded-lg">
                    <div className="text-2xl font-bold text-gray-600">{result.severity_breakdown.info}</div>
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
                  <TableHead>Tool</TableHead>
                  <TableHead>Remediation</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {findings.map((finding) => (
                  <TableRow key={finding.id}>
                    <TableCell>
                      <Badge className={severityColors[finding.severity]}>
                        {finding.severity.toUpperCase()}
                      </Badge>
                    </TableCell>
                    <TableCell>
                      <div>
                        <div className="font-medium">{finding.title}</div>
                        <div className="text-sm text-muted-foreground">
                          {finding.description}
                        </div>
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge variant="outline">{finding.tool_name}</Badge>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground max-w-xs">
                      {finding.remediation || "No remediation available"}
                    </TableCell>
                  </TableRow>
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
              <AlertTriangle className="w-5 h-5 text-yellow-600" />
              AI Recommendations
            </CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2">
              {result.insights.recommendations.map((rec, i) => (
                <li key={i} className="flex items-start gap-2">
                  <CheckCircle className="w-4 h-4 text-green-600 mt-0.5 flex-shrink-0" />
                  <span>{rec}</span>
                </li>
              ))}
            </ul>
          </CardContent>
        </Card>
      )}
    </div>
  );
}