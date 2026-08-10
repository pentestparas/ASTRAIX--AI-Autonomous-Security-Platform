"use client";

import { useEffect, useState } from "react";
import { assessmentsApi, reportsApi, type ReportTemplateInfo } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  FileText,
  Download,
  Eye,
  FileBarChart,
  ShieldCheck,
  Loader2,
  CheckCircle2,
  AlertCircle,
} from "lucide-react";
import type { Assessment } from "@/types";

const templateIcons: Record<string, typeof ShieldCheck> = {
  executive: ShieldCheck,
  technical: FileBarChart,
  compliance: FileText,
};

const formats = [
  { id: "pdf", label: "PDF", icon: FileText },
  { id: "html", label: "HTML", icon: Eye },
  { id: "json", label: "JSON", icon: FileBarChart },
];

const MIME_TYPES: Record<string, string> = {
  pdf: "application/pdf",
  html: "text/html",
  json: "application/json",
};

export default function ReportsPage() {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [templates, setTemplates] = useState<ReportTemplateInfo[]>([]);
  const [selectedAssessment, setSelectedAssessment] = useState("");
  const [selectedTemplate, setSelectedTemplate] = useState("executive");
  const [selectedFormat, setSelectedFormat] = useState("pdf");
  const [generating, setGenerating] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [successMessage, setSuccessMessage] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const orgId = localStorage.getItem("organization_id");
        const [assessmentsRes, templatesRes] = await Promise.all([
          assessmentsApi.list({
            page: 1,
            limit: 50,
            organization_id: orgId ?? undefined,
          }),
          reportsApi.getTemplates(),
        ]);
        if (assessmentsRes.success && assessmentsRes.data) {
          setAssessments((assessmentsRes.data.items ?? []).filter((a) => a.status === "completed"));
        }
        if (templatesRes.success && templatesRes.data) {
          const items = Array.isArray(templatesRes.data) ? templatesRes.data : [];
          setTemplates(items);
          if (items.length > 0 && !items.some((t) => t.id === selectedTemplate)) {
            setSelectedTemplate(items[0].id);
          }
        }
      } catch (e) {
        console.error("Failed to load report data:", e);
        setError("Failed to load assessments or report templates.");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  function downloadReport(reportContent: string, filename: string, format: string) {
    const mime = MIME_TYPES[format] ?? "application/octet-stream";
    const blob =
      format === "pdf"
        ? new Blob([new Uint8Array(Array.from(reportContent, (c) => c.charCodeAt(0) & 0xff))], { type: mime })
        : new Blob([reportContent], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  async function handleGenerate() {
    if (!selectedAssessment) return;
    setGenerating(true);
    setSuccessMessage("");
    setError("");
    try {
      const res = await reportsApi.generate(
        selectedAssessment,
        selectedTemplate,
        selectedFormat
      );
      if (res.success && res.data?.report) {
        const format = res.data.format || selectedFormat;
        const ext = ({ json: "json", html: "html", pdf: "pdf" } as Record<string, string>)[format] || "json";
        const filename = res.data.filename || `report_${selectedAssessment.slice(0, 8)}_${selectedTemplate}.${ext}`;
        downloadReport(res.data.report, filename, format);
        setSuccessMessage(`Report downloaded as ${filename}`);
        setTimeout(() => setSuccessMessage(""), 3000);
      } else {
        setError("Report generation returned no content.");
      }
    } catch (e) {
      console.error("Failed to generate report:", e);
      setError("Report generation failed. Please try again.");
    } finally {
      setGenerating(false);
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Reports</h1>
        <p className="text-muted-foreground mt-1">
          Generate security assessment reports
        </p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Generate Report</CardTitle>
          </CardHeader>
          <CardContent className="space-y-6">
            <div>
              <label className="text-sm font-medium mb-2 block">
                Select Assessment
              </label>
              <select
                className="w-full px-3 py-2 border rounded-lg bg-background text-sm"
                value={selectedAssessment}
                onChange={(e) => setSelectedAssessment(e.target.value)}
              >
                <option value="">Choose an assessment...</option>
                {assessments.map((a) => (
                  <option key={a.id} value={a.id}>
                    {a.asset_name ?? a.id} — {a.type}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">
                Report Template
              </label>
              {templates.length === 0 ? (
                <p className="text-xs text-muted-foreground">No templates available.</p>
              ) : (
                <div className="grid gap-3">
                  {templates.map((t) => {
                    const Icon = templateIcons[t.id] ?? FileBarChart;
                    return (
                      <button
                        key={t.id}
                        onClick={() => setSelectedTemplate(t.id)}
                        className={`flex items-start gap-3 p-3 border rounded-lg text-left transition-colors ${
                          selectedTemplate === t.id
                            ? "border-primary bg-primary/5"
                            : "hover:border-primary/50"
                        }`}
                      >
                        <Icon className="w-5 h-5 text-primary mt-0.5" />
                        <div>
                          <div className="font-medium text-sm">{t.name}</div>
                          <div className="text-xs text-muted-foreground">
                            {t.description}
                          </div>
                          {(t.frameworks ?? []).length > 0 && (
                            <div className="flex gap-1 mt-1">
                              {t.frameworks.map((f) => (
                                <Badge key={f} variant="secondary" className="text-xs">
                                  {f}
                                </Badge>
                              ))}
                            </div>
                          )}
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>

            <div>
              <label className="text-sm font-medium mb-2 block">Format</label>
              <div className="flex gap-2">
                {formats.map((f) => (
                  <button
                    key={f.id}
                    onClick={() => setSelectedFormat(f.id)}
                    className={`flex items-center gap-2 px-4 py-2 border rounded-lg text-sm transition-colors ${
                      selectedFormat === f.id
                        ? "border-primary bg-primary/5 text-primary"
                        : "hover:border-primary/50"
                    }`}
                  >
                    <f.icon className="w-4 h-4" />
                    {f.label}
                  </button>
                ))}
              </div>
            </div>

            {successMessage && (
              <div className="flex items-center gap-2 text-sm text-green-400 bg-green-500/10 border border-green-500/30 px-3 py-2 rounded-lg">
                <CheckCircle2 className="w-4 h-4" />
                {successMessage}
              </div>
            )}
            {error && (
              <div className="flex items-center gap-2 text-sm text-red-400 bg-red-500/10 border border-red-500/30 px-3 py-2 rounded-lg">
                <AlertCircle className="w-4 h-4" />
                {error}
              </div>
            )}
            <Button
              className="w-full"
              disabled={!selectedAssessment || generating}
              onClick={handleGenerate}
            >
              {generating ? (
                <>
                  <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                  Generating...
                </>
              ) : (
                <>
                  <Download className="w-4 h-4 mr-2" />
                  Generate Report
                </>
              )}
            </Button>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Compliance Frameworks</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {[
                {
                  name: "OWASP ASVS",
                  desc: "Application Security Verification Standard",
                  progress: 72,
                },
                {
                  name: "CIS Controls",
                  desc: "Center for Internet Security",
                  progress: 85,
                },
                {
                  name: "NIST CSF",
                  desc: "Cybersecurity Framework",
                  progress: 65,
                },
                {
                  name: "SOC2",
                  desc: "Service Organization Control 2",
                  progress: 40,
                },
                {
                  name: "PCI DSS",
                  desc: "Payment Card Industry Data Security Standard",
                  progress: 55,
                },
              ].map((fw) => (
                <div key={fw.name} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="font-medium">{fw.name}</span>
                    <span className="text-muted-foreground">{fw.progress}%</span>
                  </div>
                  <div className="h-2 bg-muted rounded-full overflow-hidden">
                    <div
                      className="h-full bg-primary rounded-full transition-all"
                      style={{ width: `${fw.progress}%` }}
                    />
                  </div>
                  <p className="text-xs text-muted-foreground">{fw.desc}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}