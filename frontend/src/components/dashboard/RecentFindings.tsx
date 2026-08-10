"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { ShieldAlert, Bug, ExternalLink } from "lucide-react";
import { useEffect, useState } from "react";
import { findingsApi } from "@/services/api";
import type { Finding } from "@/types";

const severityStyles: Record<string, string> = {
  critical: "bg-red-500/15 text-red-400 border-red-500/30",
  high: "bg-orange-500/15 text-orange-400 border-orange-500/30",
  medium: "bg-yellow-500/15 text-yellow-400 border-yellow-500/30",
  low: "bg-blue-500/15 text-blue-400 border-blue-500/30",
  info: "bg-secondary text-secondary-foreground border-border/60",
};

function DetailRow({ label, value }: { label: string; value?: unknown }) {
  if (value === undefined || value === null || value === "") return null;
  return (
    <div className="grid grid-cols-3 gap-2 text-sm">
      <div className="text-muted-foreground font-medium">{label}</div>
      <div className="col-span-2 break-words">{String(value)}</div>
    </div>
  );
}

function formatDetails(finding: Finding) {
  const d = (finding.details ?? {}) as Record<string, unknown>;
  return {
    host: d.host ?? d.hostname,
    port: d.port,
    path: d.path ?? d.url ?? d.matched_at,
    protocol: d.protocol,
    service: d.service,
    vulnerability_type: d.vulnerability_type ?? d.issue_type,
    payload: d.payload,
    cve: finding.cve ?? d.cve,
    cwe: finding.cwe ?? d.cwe,
    tool: d.tool ?? finding.plugin_id,
    confidence: d.confidence,
    evidence: d.evidence ?? d.output ?? d.description,
    related_cves: d.related_cves,
  };
}

export function RecentFindings() {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<Finding | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const orgId = localStorage.getItem("organization_id");
        const res = await findingsApi.list({
          page: 1,
          limit: 10,
          organization_id: orgId ?? undefined,
        });
        if (res.success && res.data) {
          setFindings(res.data.items.slice(0, 7));
        }
      } catch (e) {
        console.error("Failed to load findings:", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  return (
    <>
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Recent Findings</CardTitle>
          <Bug className="w-4 h-4 text-muted-foreground" />
        </CardHeader>
        <CardContent className="p-0">
          <div className="divide-y">
            {loading
              ? Array.from({ length: 4 }).map((_, i) => (
                  <div
                    key={i}
                    className="h-10 animate-pulse bg-muted rounded mx-4 my-2"
                  />
                ))
              : findings.length === 0 && (
                  <p className="px-4 py-8 text-center text-sm text-muted-foreground">
                    No findings yet — run a scan to detect vulnerabilities
                  </p>
                )}
            {findings.map((f) => (
              <button
                key={f.id}
                onClick={() => setSelected(f)}
                className="w-full text-left px-4 py-3 hover:bg-muted/60 transition-colors"
              >
                <div className="flex items-center justify-between gap-3">
                  <div className="min-w-0">
                    <div className="text-sm font-medium truncate">
                      {f.title}
                    </div>
                    <div className="text-xs text-muted-foreground truncate">
                      {f.asset?.name ??
                        (f.details?.target as string) ??
                        f.plugin_id}
                    </div>
                  </div>
                  <Badge
                    className={
                      severityStyles[f.severity] ?? severityStyles.info
                    }
                  >
                    {f.severity}
                  </Badge>
                </div>
              </button>
            ))}
          </div>
        </CardContent>
      </Card>

      <Dialog open={!!selected} onOpenChange={(open) => !open && setSelected(null)}>
        <DialogContent className="max-w-2xl max-h-[85vh] overflow-y-auto">
          {selected && <FindingDetail finding={selected} />}
        </DialogContent>
      </Dialog>
    </>
  );
}

function FindingDetail({ finding }: { finding: Finding }) {
  const det = formatDetails(finding);
  const extra = Object.entries(finding.details ?? {}).filter(
    ([k]) =>
      ![
        "tool",
        "target",
        "host",
        "hostname",
        "port",
        "path",
        "url",
        "matched_at",
        "protocol",
        "service",
        "vulnerability_type",
        "issue_type",
        "payload",
        "cve",
        "cwe",
        "confidence",
        "evidence",
        "output",
        "description",
        "related_cves",
      ].includes(k)
  );

  return (
    <div className="space-y-5">
      <DialogHeader>
        <div className="flex items-center gap-2">
          <Badge className={severityStyles[finding.severity] ?? severityStyles.info}>
            {finding.severity}
          </Badge>
          {finding.cvss_score !== undefined && (
            <Badge variant="secondary">CVSS {finding.cvss_score}</Badge>
          )}
          <Badge variant="outline" className="capitalize">
            {finding.status}
          </Badge>
        </div>
        <DialogTitle className="text-lg leading-snug mt-2">
          {finding.title}
        </DialogTitle>
      </DialogHeader>

      {finding.description && (
        <div>
          <h4 className="text-sm font-semibold mb-1">Description</h4>
          <p className="text-sm text-muted-foreground whitespace-pre-wrap">
            {finding.description}
          </p>
        </div>
      )}

      <div className="rounded-lg border p-4 space-y-2">
        <h4 className="text-sm font-semibold flex items-center gap-1.5">
          <ShieldAlert className="w-4 h-4" /> How it was captured
        </h4>
        <DetailRow label="Tool" value={det.tool} />
        <DetailRow label="Target" value={finding.details?.target} />
        <DetailRow label="Host" value={det.host} />
        <DetailRow label="Port" value={det.port} />
        <DetailRow label="Path / URL" value={det.path} />
        <DetailRow label="Protocol" value={det.protocol} />
        <DetailRow label="Service" value={det.service} />
        <DetailRow label="Vuln type" value={det.vulnerability_type} />
        <DetailRow label="Confidence" value={det.confidence} />
        <DetailRow label="CVE" value={det.cve} />
        <DetailRow label="CWE" value={det.cwe} />
        {det.related_cves != null && (
          <DetailRow
            label="Related CVEs"
            value={Array.isArray(det.related_cves) ? det.related_cves.join(", ") : det.related_cves}
          />
        )}
      </div>

      {det.payload != null && String(det.payload).trim() !== "" && (
        <div>
          <h4 className="text-sm font-semibold mb-1">Payload executed</h4>
          <pre className="text-xs bg-muted rounded-lg p-3 overflow-x-auto whitespace-pre-wrap break-all">
            {String(det.payload)}
          </pre>
        </div>
      )}

      {det.evidence != null && String(det.evidence).trim() !== "" && (
        <div>
          <h4 className="text-sm font-semibold mb-1">Evidence</h4>
          <pre className="text-xs bg-muted rounded-lg p-3 overflow-x-auto whitespace-pre-wrap break-all">
            {String(det.evidence)}
          </pre>
        </div>
      )}

      {extra.length > 0 && (
        <div>
          <h4 className="text-sm font-semibold mb-1">Tool output</h4>
          <div className="rounded-lg border p-3 space-y-1.5">
            {extra.map(([k, v]) => (
              <DetailRow key={k} label={k} value={v} />
            ))}
          </div>
        </div>
      )}

      {finding.remediation && (
        <div className="rounded-lg border border-green-500/30 bg-green-500/10 p-4">
          <h4 className="text-sm font-semibold text-green-400 mb-1">
            Resolution
          </h4>
          <p className="text-sm text-muted-foreground whitespace-pre-wrap">
            {finding.remediation}
          </p>
        </div>
      )}

      {finding.reference && (
        <div className="flex items-center gap-2 text-sm">
          <ExternalLink className="w-3.5 h-3.5 text-muted-foreground" />
          <span className="text-muted-foreground break-all">
            {finding.reference}
          </span>
        </div>
      )}
    </div>
  );
}
