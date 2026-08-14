"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  CheckCircle,
  AlertCircle,
  XCircle,
  Loader2,
  Database,
  Server,
  Network,
  Container,
  BookOpen,
  RefreshCw,
} from "lucide-react";
import { systemApi } from "@/services/api";
import type { SystemStatus } from "@/types";

interface ComponentRowProps {
  name: string;
  icon: React.ReactNode;
  status: string;
  details: React.ReactNode;
}

function ComponentRow({ name, icon, status, details }: ComponentRowProps) {
  const ok = status === "operational";
  const statusIcon = ok ? (
    <CheckCircle className="w-4 h-4 text-green-500" />
  ) : status === "degraded" ? (
    <AlertCircle className="w-4 h-4 text-yellow-500" />
  ) : (
    <XCircle className="w-4 h-4 text-red-500" />
  );

  return (
    <div className="flex items-center justify-between py-2 border-b last:border-0">
      <div className="flex items-center gap-3 min-w-0">
        <div className="p-1.5 bg-muted rounded shrink-0">{icon}</div>
        <div className="min-w-0">
          <p className="font-medium text-sm">{name}</p>
          <div className="text-xs text-muted-foreground truncate">{details}</div>
        </div>
      </div>
      <div className="flex items-center gap-2 shrink-0 ml-3">
        {statusIcon}
        <span className="text-xs capitalize">{status}</span>
      </div>
    </div>
  );
}

function DockerDetails({ details }: { details: any }) {
  const tools = details?.tools || {};
  const toolList = Object.entries(tools)
    .filter(([, ok]) => ok)
    .map(([name]) => name);

  return (
    <div className="space-y-1">
      <p>
        {details?.kali_image_available
          ? "Kali image available"
          : "Kali image missing"}
        {toolList.length > 0 && ` • ${toolList.length}/${Object.keys(tools).length} tools`}
      </p>
      {toolList.length > 0 && (
        <div className="flex flex-wrap gap-1">
          {toolList.map((t) => (
            <span
              key={t}
              className="text-[11px] px-1.5 py-0.5 bg-muted rounded font-mono"
            >
              {t}
            </span>
          ))}
        </div>
      )}
    </div>
  );
}

function KbDetails({ details }: { details: any }) {
  const rows: [string, string | number][] = [
    ["chunks", details?.chunks ?? "-"],
    ["sources", details?.sources ?? "-"],
    ["vocab size", details?.vocab_size ?? "-"],
    ["semantic search", details?.semantic_search ? "enabled" : "disabled"],
  ];
  return (
    <div className="flex flex-wrap gap-x-4 gap-y-0.5">
      {rows.map(([k, v]) => (
        <span key={k}>
          <span className="text-muted-foreground">{k}:</span>{" "}
          <span className="font-mono">{String(v)}</span>
        </span>
      ))}
    </div>
  );
}

export function SystemStatus() {
  const [status, setStatus] = useState<SystemStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load() {
    setLoading(true);
    setError("");
    try {
      const res = (await systemApi.status()) as any;
      setStatus(res?.data ?? res);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Failed to load system status");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void load();
    const id = window.setInterval(() => void load(), 30000);
    return () => window.clearInterval(id);
  }, []);

  const components = status?.components;

  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Server className="w-5 h-5" />
            System Health
          </CardTitle>
        </CardHeader>
        <CardContent>
          {loading && !components ? (
            <div className="flex items-center justify-center py-6 gap-2 text-muted-foreground">
              <Loader2 className="w-4 h-4 animate-spin" />
              Checking components...
            </div>
          ) : error ? (
            <div className="py-6 text-center">
              <p className="text-sm text-red-400 mb-3">{error}</p>
              <button
                onClick={() => void load()}
                className="inline-flex items-center gap-1.5 text-xs text-primary hover:underline"
              >
                <RefreshCw className="w-3 h-3" /> Retry
              </button>
            </div>
          ) : (
            <div className="space-y-1">
              <ComponentRow
                name="PostgreSQL"
                icon={<Database className="w-4 h-4" />}
                status={components?.postgres?.status || "down"}
                details={String(components?.postgres?.details ?? "unreachable")}
              />
              <ComponentRow
                name="Redis"
                icon={<Network className="w-4 h-4" />}
                status={components?.redis?.status || "down"}
                details={String(components?.redis?.details ?? "unreachable")}
              />
              <ComponentRow
                name="Neo4j Knowledge Graph"
                icon={<Network className="w-4 h-4" />}
                status={components?.neo4j?.status || "down"}
                details={String(components?.neo4j?.details ?? "unreachable")}
              />
              <ComponentRow
                name="Docker Exec (Kali)"
                icon={<Container className="w-4 h-4" />}
                status={components?.docker?.status || "down"}
                details={<DockerDetails details={components?.docker?.details} />}
              />
              <ComponentRow
                name="Knowledge Base"
                icon={<BookOpen className="w-4 h-4" />}
                status={components?.knowledge_base?.status || "down"}
                details={<KbDetails details={components?.knowledge_base?.details} />}
              />
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
