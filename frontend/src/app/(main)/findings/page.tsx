"use client";

import { useEffect, useState } from "react";
import { findingsApi } from "@/services/api";
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
  ShieldAlert,
  Globe,
  ExternalLink,
  CalendarClock,
  Fingerprint,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import type { Finding } from "@/types";

const severityConfig = {
  critical: { label: "Critical", className: "bg-red-500/15 text-red-400 border-red-500/30" },
  high: { label: "High", className: "bg-orange-500/15 text-orange-400 border-orange-500/30" },
  medium: { label: "Medium", className: "bg-yellow-500/15 text-yellow-400 border-yellow-500/30" },
  low: { label: "Low", className: "bg-blue-500/15 text-blue-400 border-blue-500/30" },
  info: { label: "Info", className: "bg-secondary text-secondary-foreground border-border/60" },
};

const cvssColor = (s: number) =>
  s >= 9 ? "text-red-400 font-bold" : s >= 7 ? "text-orange-400 font-bold" : s >= 4 ? "text-yellow-400" : "text-green-400";

const statusOptions = ["open", "triaged", "resolved", "false_positive", "accepted"];

export default function FindingsPage() {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);
  const [severity, setSeverity] = useState<string>("");
  const [status, setStatus] = useState<string>("");
  const [selected, setSelected] = useState<Finding | null>(null);

  async function loadFindings() {
    try {
      const orgId = localStorage.getItem("organization_id");
      const res = await findingsApi.list({
        page: 1,
        limit: 100,
        organization_id: orgId ?? undefined,
        severity: severity || undefined,
        status: status || undefined,
      });
      if (res.success && res.data) {
        setFindings(res.data.items);
      }
    } catch (e) {
      console.error("Failed to load findings:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    setLoading(true);
    loadFindings();
  }, [severity, status]);

  async function handleStatusChange(id: string, newStatus: Finding["status"]) {
    try {
      await findingsApi.update(id, { status: newStatus });
      setSelected((prev) => (prev && prev.id === id ? { ...prev, status: newStatus } : prev));
      loadFindings();
    } catch (e) {
      console.error("Failed to update finding:", e);
    }
  }

  const fmtLabel = (s: string) =>
    s.replace("_", " ").replace(/\b\w/g, (c: string) => c.toUpperCase());

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Vulnerabilities</h1>
          <p className="text-muted-foreground mt-1">
            True-positive security findings confirmed by verification
          </p>
        </div>
        <div className="flex items-center gap-2">
          <select
            className="px-3 py-2 text-sm border rounded-lg bg-background"
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
          >
            <option value="">All Severities</option>
            {Object.entries(severityConfig).map(([key, cfg]) => (
              <option key={key} value={key}>
                {cfg.label}
              </option>
            ))}
          </select>
          <select
            className="px-3 py-2 text-sm border rounded-lg bg-background"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="">True Positives</option>
            {statusOptions.map((s) => (
              <option key={s} value={s}>
                {fmtLabel(s)}
              </option>
            ))}
          </select>
        </div>
      </div>

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
              {loading ? (
                Array.from({ length: 5 }).map((_, i) => (
                  <TableRow key={i}>
                    <TableCell colSpan={6}>
                      <div className="h-8 animate-pulse bg-muted rounded" />
                    </TableCell>
                  </TableRow>
                ))
              ) : findings.length === 0 ? (
                <TableRow>
                  <TableCell
                    colSpan={6}
                    className="text-center py-12 text-muted-foreground"
                  >
                    <ShieldAlert className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p>No vulnerabilities found.</p>
                  </TableCell>
                </TableRow>
              ) : (
                findings.map((finding) => {
                  const sev = severityConfig[finding.severity] || severityConfig.info;
                  return (
                    <TableRow
                      key={finding.id}
                      className="cursor-pointer hover:bg-muted/50"
                      onClick={() => setSelected(finding)}
                    >
                      <TableCell>
                        <Badge className={sev.className} variant="default">
                          {sev.label}
                        </Badge>
                      </TableCell>
                      <TableCell className="font-medium max-w-md truncate">
                        {finding.title || "—"}
                      </TableCell>
                      <TableCell className="text-muted-foreground max-w-xs truncate">
                        {finding.asset?.name ?? finding.asset_id ?? "—"}
                      </TableCell>
                      <TableCell onClick={(e) => e.stopPropagation()}>
                        <select
                          className="text-xs px-2 py-1 border rounded bg-background"
                          value={finding.status}
                          onChange={(e) =>
                            handleStatusChange(finding.id, e.target.value as Finding["status"])
                          }
                        >
                          {statusOptions.map((s) => (
                            <option key={s} value={s}>
                              {fmtLabel(s)}
                            </option>
                          ))}
                        </select>
                      </TableCell>
                      <TableCell>
                        {finding.cvss_score != null ? (
                          <span className={cvssColor(finding.cvss_score)}>
                            {finding.cvss_score.toFixed(1)}
                          </span>
                        ) : (
                          "—"
                        )}
                      </TableCell>
                      <TableCell className="text-muted-foreground text-sm">
                        {formatDistanceToNow(new Date(finding.created_at), {
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
                    onChange={(e) => handleStatusChange(selected.id, e.target.value as Finding["status"])}
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