"use client";

import { useEffect, useState } from "react";
import { findingsApi } from "@/services/api";
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
  ShieldAlert,
  Filter,
  Search,
  ChevronDown,
  AlertTriangle,
  Info,
  AlertCircle,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import type { Finding } from "@/types";

const severityConfig = {
  critical: { label: "Critical", className: "bg-red-500 text-white", icon: AlertTriangle },
  high: { label: "High", className: "bg-orange-500 text-white", icon: AlertCircle },
  medium: { label: "Medium", className: "bg-yellow-500 text-white", icon: AlertCircle },
  low: { label: "Low", className: "bg-blue-500 text-white", icon: Info },
  info: { label: "Info", className: "bg-gray-500 text-white", icon: Info },
};

const statusOptions = ["open", "triaged", "resolved", "false_positive", "accepted"];

export default function FindingsPage() {
  const [findings, setFindings] = useState<Finding[]>([]);
  const [loading, setLoading] = useState(true);
  const [severity, setSeverity] = useState<string>("");
  const [status, setStatus] = useState<string>("");

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
    loadFindings();
  }, [severity, status]);

  async function handleStatusChange(id: string, newStatus: string) {
    try {
      await findingsApi.update(id, { status: newStatus });
      loadFindings();
    } catch (e) {
      console.error("Failed to update finding:", e);
    }
  }

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Findings</h1>
          <p className="text-muted-foreground mt-1">
            Manage and triage security findings
          </p>
        </div>
        <div className="flex items-center gap-2">
          <select
            className="px-3 py-2 text-sm border rounded-lg bg-background"
            value={severity}
            onChange={(e) => setSeverity(e.target.value)}
          >
            <option value="">All Severities</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
            <option value="info">Info</option>
          </select>
          <select
            className="px-3 py-2 text-sm border rounded-lg bg-background"
            value={status}
            onChange={(e) => setStatus(e.target.value)}
          >
            <option value="">All Status</option>
            {statusOptions.map((s) => (
              <option key={s} value={s}>
                {s.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase())}
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
                    <p>No findings found.</p>
                  </TableCell>
                </TableRow>
              ) : (
                findings.map((finding) => {
                  const sev = severityConfig[finding.severity] || severityConfig.info;
                  const SevIcon = sev.icon;
                  return (
                    <TableRow key={finding.id}>
                      <TableCell>
                        <Badge className={sev.className} variant="default">
                          <SevIcon className="w-3 h-3 mr-1" />
                          {sev.label}
                        </Badge>
                      </TableCell>
                      <TableCell className="font-medium max-w-md truncate">
                        {finding.title}
                      </TableCell>
                      <TableCell className="text-muted-foreground">
                        {finding.asset?.name ?? "—"}
                      </TableCell>
                      <TableCell>
                        <select
                          className="text-xs px-2 py-1 border rounded bg-background"
                          value={finding.status}
                          onChange={(e) =>
                            handleStatusChange(finding.id, e.target.value)
                          }
                        >
                          {statusOptions.map((s) => (
                            <option key={s} value={s}>
                              {s.replace("_", " ").replace(/\b\w/g, (c) => c.toUpperCase())}
                            </option>
                          ))}
                        </select>
                      </TableCell>
                      <TableCell>
                        {finding.cvss_score ? (
                          <span
                            className={
                              finding.cvss_score >= 9
                                ? "text-red-600 font-bold"
                                : finding.cvss_score >= 7
                                  ? "text-orange-600 font-bold"
                                  : finding.cvss_score >= 4
                                    ? "text-yellow-600"
                                    : "text-green-600"
                            }
                          >
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
    </div>
  );
}