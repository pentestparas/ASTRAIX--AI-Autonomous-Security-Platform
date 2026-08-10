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
import { useState } from "react";
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
    <aside className="flex flex-col w-64 shrink-0 bg-sidebar text-sidebar-foreground border-r border-border h-screen">
      <div className="p-4 border-b border-border/70">
        <Link href="/dashboard" className="flex items-center gap-2.5">
          <div className="relative flex items-center justify-center w-9 h-9 rounded-xl btn-gradient glow-primary shadow-md">
            <Radar className="w-5 h-5 text-primary-foreground" />
          </div>
          <div className="leading-tight">
            <span className="block text-base font-bold tracking-tight">Astra<span className="text-gradient">IX</span></span>
            <span className="block text-[10px] uppercase tracking-[0.16em] text-muted-foreground">
              Security Analyst
            </span>
          </div>
        </Link>
      </div>

      <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
        <p className="eyebrow px-3 pb-2">Workspace</p>
        {navigation.map((item) => {
          const isActive = pathname === item.href || pathname.startsWith(item.href + "/");
          return (
            <Link
              key={item.name}
              href={item.href}
              className={`group flex items-center gap-3 px-3 py-2.5 rounded-lg text-[13px] font-medium transition-all ${
                isActive
                  ? "bg-gradient-to-r from-primary/20 via-primary/10 to-transparent text-foreground border border-primary/25 shadow-[inset_0_1px_0_hsl(210_40%_98%/0.04),0_0_16px_-6px_hsl(188_94%_47%/0.35)]"
                  : "text-muted-foreground hover:text-foreground hover:bg-accent/70 border border-transparent"
              }`}
            >
              <item.icon className={`w-4 h-4 ${isActive ? "text-primary" : "text-muted-foreground group-hover:text-foreground"}`} />
              {item.name}
              {item.name === "Scans" && runningScans > 0 && (
                <span className="ml-auto inline-flex items-center gap-1.5 rounded-full bg-primary/15 border border-primary/30 px-2 py-0.5 text-[11px] font-semibold text-primary">
                  <span className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse" />
                  {runningScans}
                </span>
              )}
            </Link>
          );
        })}

        <div className="pt-4 mt-4 border-t border-border/70">
          <button
            onClick={() => setSettingsOpen(!settingsOpen)}
            className="flex items-center justify-between w-full px-3 py-2.5 text-[13px] font-medium text-muted-foreground hover:text-foreground hover:bg-accent/70 rounded-lg transition-colors border border-transparent"
          >
            <span className="flex items-center gap-3">
              <Settings className="w-4 h-4" />
              Settings
            </span>
            <ChevronDown className={`w-4 h-4 transition-transform ${settingsOpen ? "rotate-180" : ""}`} />
          </button>

          {settingsOpen && (
            <div className="ml-4 mt-1 space-y-1 border-l border-border/60 pl-2">
              {settingsNav.map((item) => {
                const isActive = pathname === item.href;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className={`flex items-center gap-3 px-3 py-2 rounded-lg text-[13px] transition-colors ${
                      isActive
                        ? "bg-primary/10 text-primary border border-primary/20"
                        : "text-muted-foreground hover:bg-accent/70 hover:text-foreground border border-transparent"
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

      <div className="p-4 border-t border-border/70">
        <button
          onClick={handleSignOut}
          className="flex items-center gap-3 px-3 py-2.5 w-full text-[13px] font-medium text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-lg transition-colors border border-transparent hover:border-destructive/30"
        >
          <LogOut className="w-4 h-4" />
          Sign out
        </button>
      </div>
    </aside>
  );
}