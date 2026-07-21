"use client";

import { StatsCards } from "./StatsCards";
import { RecentAssessments } from "./RecentAssessments";
import { QuickActions } from "./QuickActions";
import { SystemStatus } from "./SystemStatus";

export function Dashboard() {
  return (
    <div className="min-h-screen bg-background p-6">
      <div className="max-w-7xl mx-auto space-y-6">
        <header className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
            <p className="text-muted-foreground mt-1">
              Overview of your security assessment platform
            </p>
          </div>
          <div className="flex items-center gap-4">
            <span className="px-3 py-1 text-sm bg-green-100 text-green-800 rounded-full">
              System Operational
            </span>
          </div>
        </header>

        <StatsCards />

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-7">
          <div className="col-span-4 lg:col-span-4">
            <RecentAssessments />
          </div>
          <div className="col-span-3 lg:col-span-3 space-y-6">
            <QuickActions />
            <SystemStatus />
          </div>
        </div>
      </div>
    </div>
  );
}