"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  TrendingUp,
  TrendingDown,
  Shield,
  AlertTriangle,
  Activity,
  Server,
  CheckCircle,
  XCircle,
} from "lucide-react";
import { useEffect, useState } from "react";
import { dashboardApi } from "@/services/api";

interface StatCardProps {
  title: string;
  value: string | number;
  change?: string;
  changeType?: "increase" | "decrease" | "neutral";
  icon: React.ReactNode;
  iconColor: string;
  loading?: boolean;
}

function StatCard({
  title,
  value,
  change,
  changeType,
  icon,
  iconColor,
  loading,
}: StatCardProps) {
  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
        <CardTitle className="text-sm font-medium">{title}</CardTitle>
        <div className={`text-2xl ${iconColor}`}>{icon}</div>
      </CardHeader>
      <CardContent>
        {loading ? (
          <div className="h-8 w-20 animate-pulse bg-muted rounded" />
        ) : (
          <div className="text-2xl font-bold">{value}</div>
        )}
        {change && (
          <p
            className={`text-xs mt-1 ${
              changeType === "increase"
                ? "text-green-600"
                : changeType === "decrease"
                  ? "text-red-600"
                  : "text-muted-foreground"
            }`}
          >
            {changeType === "increase" && (
              <TrendingUp className="inline w-3 h-3 mr-1" />
            )}
            {changeType === "decrease" && (
              <TrendingDown className="inline w-3 h-3 mr-1" />
            )}
            {changeType === "neutral" && (
              <Activity className="inline w-3 h-3 mr-1" />
            )}
            {change}
          </p>
        )}
      </CardContent>
    </Card>
  );
}

export function StatsCards() {
  const [stats, setStats] = useState<{
    total_projects: number;
    active_scans: number;
    critical_findings: number;
    open_findings: number;
    resolved_findings: number;
    assets_discovered: number;
    total_findings: number;
  } | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      try {
        const orgId = localStorage.getItem("organization_id");
        if (orgId) {
          const res = await dashboardApi.getStats(orgId);
          if (res.success && res.data) {
            setStats(res.data);
          }
        }
      } catch (e) {
        console.error("Failed to load stats:", e);
      } finally {
        setLoading(false);
      }
    }
    loadStats();
  }, []);

  const remediationRate =
    stats && stats.total_findings > 0
      ? Math.round((stats.resolved_findings / stats.total_findings) * 100)
      : 0;

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
      <StatCard
        title="Total Projects"
        value={stats?.total_projects ?? 0}
        change="Active projects"
        changeType="neutral"
        icon={<Server className="w-5 h-5" />}
        iconColor="text-purple-500"
        loading={loading}
      />
      <StatCard
        title="Active Scans"
        value={stats?.active_scans ?? 0}
        change={loading ? undefined : `${stats?.active_scans ?? 0} running`}
        changeType="neutral"
        icon={<Activity className="w-5 h-5" />}
        iconColor="text-blue-500"
        loading={loading}
      />
      <StatCard
        title="Critical Findings"
        value={stats?.critical_findings ?? 0}
        change="Requires immediate attention"
        changeType={
          (stats?.critical_findings ?? 0) > 0 ? "increase" : "decrease"
        }
        icon={<AlertTriangle className="w-5 h-5" />}
        iconColor="text-red-500"
        loading={loading}
      />
      <StatCard
        title="Remediation Rate"
        value={`${remediationRate}%`}
        change="Findings resolved"
        changeType={remediationRate >= 70 ? "increase" : "decrease"}
        icon={<CheckCircle className="w-5 h-5" />}
        iconColor="text-green-500"
        loading={loading}
      />
    </div>
  );
}