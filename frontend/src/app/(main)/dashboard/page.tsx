"use client";

import { StatsCards } from "@/components/dashboard/StatsCards";
import { RecentAssessments } from "@/components/dashboard/RecentAssessments";
import { RecentFindings } from "@/components/dashboard/RecentFindings";
import { SystemStatus } from "@/components/dashboard/SystemStatus";

export default function DashboardPage() {
  return (
    <div className="max-w-7xl mx-auto space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Overview of your security assessment platform
          </p>
        </div>
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center gap-1.5 px-2.5 py-1 text-[13px] bg-success/10 text-success border border-success/25 rounded-full">
            <span className="w-1.5 h-1.5 rounded-full bg-success" />
            System Operational
          </span>
        </div>
      </header>

      <StatsCards />

      <div className="grid gap-6 md:grid-cols-2">
        <div className="space-y-6">
          <RecentAssessments />
          <RecentFindings />
        </div>
        <SystemStatus />
      </div>
    </div>
  );
}