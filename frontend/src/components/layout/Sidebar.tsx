"use client";

import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import {
  LayoutDashboard,
  FolderKanban,
  Scan,
  ShieldAlert,
  FileText,
  Settings,
  LogOut,
  ChevronDown,
  Key,
  Users,
  GitBranch,
  Radar,
} from "lucide-react";
import { useEffect, useState } from "react";
import { useActiveScansStore } from "@/store/activeScans";

const navigation = [
  { name: "Dashboard", href: "/dashboard", icon: LayoutDashboard },
  { name: "Projects", href: "/projects", icon: FolderKanban },
  { name: "Scans", href: "/scans", icon: Scan },
  { name: "Findings", href: "/findings", icon: ShieldAlert },
  { name: "Reports", href: "/reports", icon: FileText },
  { name: "Attack Graph", href: "/graph", icon: GitBranch },
];

const settingsNav = [
  { name: "Organization", href: "/settings", icon: Settings },
  { name: "Members", href: "/settings/members", icon: Users },
  { name: "API Keys", href: "/settings/api-keys", icon: Key },
];

export function Sidebar() {
  const pathname = usePathname() ?? "";
  const router = useRouter();
  const [mounted, setMounted] = useState(false);
  useEffect(() => setMounted(true), []);
  const runningScans = useActiveScansStore((s) => s.runningCount());
  const [settingsOpen, setSettingsOpen] = useState(pathname.startsWith("/settings"));

  function handleSignOut() {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_id");
    localStorage.removeItem("user_email");
    localStorage.removeItem("organization_id");
    router.push("/login");
  }

  return (
    <aside className="flex flex-col w-60 shrink-0 bg-sidebar text-sidebar-foreground border-r border-border h-screen">
      <div className="px-4 py-4 border-b border-border/60">
        <Link href="/dashboard" className="flex items-center gap-2.5">
          <div className="relative flex items-center justify-center w-8 h-8 rounded-lg btn-gradient glow-primary shadow-md">
            <Radar className="w-4 h-4 text-primary-foreground" />
          </div>
          <div className="leading-tight">
            <span className="block text-base font-bold tracking-tight">Astra<span className="text-gradient">IX</span></span>
            <span className="block text-[9.5px] uppercase tracking-[0.18em] text-muted-foreground">
              Security Analyst
            </span>
          </div>
        </Link>
      </div>

      <nav className="flex-1 px-3 py-3 space-y-0.5 overflow-y-auto">
        <p className="eyebrow px-2.5 pb-1.5">Workspace</p>
        {navigation.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`group flex items-center gap-3 px-2.5 py-2 rounded-md text-sm font-medium transition-colors ${
                isActive
                  ? "bg-primary/10 text-primary border border-primary/20"
                  : "text-muted-foreground hover:text-foreground hover:bg-accent/60 border border-transparent"
              }`}
            >
              <item.icon className={`w-4 h-4 ${isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground"}`} />
              {item.name}
              {mounted && item.name === "Scans" && runningScans > 0 && (
                <span className="ml-auto inline-flex items-center gap-1.5 rounded-full bg-primary/15 border border-primary/30 px-2 py-0.5 text-[11px] font-semibold font-mono text-primary">
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                  {runningScans}
                </span>
              )}
            </Link>
          );
        })}

        <div className="pt-3 mt-3 border-t border-border/60">
          <button
            onClick={() => setSettingsOpen(!settingsOpen)}
            className="flex items-center justify-between w-full px-2.5 py-2 text-sm font-medium text-muted-foreground hover:text-foreground hover:bg-accent/60 rounded-md transition-colors border border-transparent"
          >
            <span className="flex items-center gap-3">
              <Settings className="w-4 h-4" />
              Settings
            </span>
            <ChevronDown className={`w-4 h-4 transition-transform ${settingsOpen ? "rotate-180" : ""}`} />
          </button>

          {settingsOpen && (
            <div className="ml-3 mt-0.5 space-y-0.5 border-l border-border/50 pl-2">
              {settingsNav.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`flex items-center gap-3 px-2.5 py-1.5 rounded-md text-sm transition-colors ${
                      isActive
                        ? "bg-primary/10 text-primary border border-primary/20"
                        : "text-muted-foreground hover:bg-accent/60 hover:text-foreground border border-transparent"
                    }`}
                  >
                    <item.icon className="w-4 h-4" />
                    {item.name}
                  </Link>
                );
              })}
            </div>
          )}
        </div>
      </nav>

      <div className="px-3 py-3 border-t border-border/60">
        <button
          onClick={handleSignOut}
          className="flex items-center gap-3 px-2.5 py-2 w-full text-sm font-medium text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-md transition-colors border border-transparent hover:border-destructive/25"
        >
          <LogOut className="w-4 h-4" />
          Sign out
        </button>
      </div>
    </aside>
  );
}