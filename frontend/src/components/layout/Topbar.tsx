"use client";

import { usePathname } from "next/navigation";
import { Activity, ChevronRight } from "lucide-react";
import { useActiveScansStore } from "@/store/activeScans";

const LABELS: Record<string, string> = {
  dashboard: "Dashboard",
  projects: "Projects",
  scans: "Scans",
  findings: "Findings",
  reports: "Reports",
  graph: "Attack Graph",
  settings: "Settings",
};

export function Topbar() {
  const pathname = usePathname() ?? "";
  const runningScans = useActiveScansStore((s) => s.runningCount());
  const segments = pathname.split("/").filter(Boolean).slice(0, 2);
  const current = segments[segments.length - 1] ?? "";

  return (
    <header className="sticky top-0 z-30 flex items-center justify-between h-12 px-6 lg:px-8 border-b border-border/60 bg-background/85 backdrop-blur-md">
      <nav className="flex items-center gap-1.5 text-sm text-muted-foreground">
        <span className="font-medium text-foreground">
          {LABELS[segments[0] ?? ""] ?? "AstraIX"}
        </span>
        {segments.length > 1 && LABELS[current] && (
          <>
            <ChevronRight className="w-3.5 h-3.5 text-muted-foreground/50" />
            <span className="font-medium text-foreground">{LABELS[current]}</span>
          </>
        )}
      </nav>

      <div className="flex items-center gap-3">
        {runningScans > 0 && (
          <span className="inline-flex items-center gap-1.5 rounded-full bg-primary/10 border border-primary/25 px-2.5 py-1 text-[11.5px] font-medium text-primary">
            <Activity className="w-3.5 h-3.5" />
            <span className="font-mono tabular-nums">{runningScans}</span>
            running
          </span>
        )}
        <span className="inline-flex items-center gap-1.5 rounded-full bg-success/10 border border-success/25 px-2.5 py-1 text-[11.5px] font-medium text-success">
          <span className="w-1.5 h-1.5 rounded-full bg-success" />
          Operational
        </span>
      </div>
    </header>
  );
}