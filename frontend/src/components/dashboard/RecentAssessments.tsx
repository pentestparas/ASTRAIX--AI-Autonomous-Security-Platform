"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  MoreHorizontal,
  Play,
  Pause,
  CheckCircle,
  XCircle,
  Clock,
  Filter,
  Search,
  Eye,
  RotateCcw,
  Ban,
} from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import { useEffect, useState } from "react";
import { assessmentsApi } from "@/services/api";
import type { Assessment } from "@/types";
import { useActiveScansStore } from "@/store/activeScans";
import Link from "next/link";

const statusConfig = {
  running: {
    label: "Running",
    className: "bg-blue-100 text-blue-800",
    icon: Play,
  },
  completed: {
    label: "Completed",
    className: "bg-green-100 text-green-800",
    icon: CheckCircle,
  },
  failed: {
    label: "Failed",
    className: "bg-red-100 text-red-800",
    icon: XCircle,
  },
  cancelled: {
    label: "Cancelled",
    className: "bg-gray-100 text-gray-800",
    icon: XCircle,
  },
  pending: {
    label: "Pending",
    className: "bg-yellow-100 text-yellow-800",
    icon: Clock,
  },
};

export function RecentAssessments() {
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [menuOpenId, setMenuOpenId] = useState<string | null>(null);
  const [actingId, setActingId] = useState<string | null>(null);
  const runningScans = useActiveScansStore((s) => s.runningCount());

  async function refresh() {
    try {
      const orgId = localStorage.getItem("organization_id");
      const res = await assessmentsApi.list({
        page: 1,
        limit: 10,
        organization_id: orgId ?? undefined,
      });
      if (res.success && res.data) {
        setAssessments(res.data.items.slice(0, 5));
      }
    } catch (e) {
      console.error("Failed to load assessments:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, [runningScans]);

  useEffect(() => {
    if (runningScans === 0) return;
    const id = window.setInterval(refresh, 8000);
    return () => window.clearInterval(id);
  }, [runningScans]);

  async function handleRerun(id: string) {
    setMenuOpenId(null);
    setActingId(id);
    try {
      await assessmentsApi.start(id);
      await refresh();
    } catch (e) {
      console.error("Failed to re-run scan:", e);
    } finally {
      setActingId(null);
    }
  }

  async function handleCancel(id: string) {
    setMenuOpenId(null);
    setActingId(id);
    try {
      await assessmentsApi.cancel(id);
      await refresh();
    } catch (e) {
      console.error("Failed to cancel scan:", e);
    } finally {
      setActingId(null);
    }
  }

  return (
    <Card>
      <CardHeader className="flex flex-row items-center justify-between">
        <CardTitle>Recent Assessments</CardTitle>
        <div className="flex items-center gap-2">
          <button className="p-2 hover:bg-muted rounded-lg transition-colors">
            <Filter className="w-4 h-4" />
          </button>
          <button className="p-2 hover:bg-muted rounded-lg transition-colors">
            <Search className="w-4 h-4" />
          </button>
        </div>
      </CardHeader>
      <CardContent>
        <div className="overflow-x-auto">
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Findings</TableHead>
                <TableHead>Started</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {loading ? (
                Array.from({ length: 3 }).map((_, i) => (
                  <TableRow key={i}>
                    <TableCell colSpan={6}>
                      <div className="h-8 animate-pulse bg-muted rounded" />
                    </TableCell>
                  </TableRow>
                ))
              ) : assessments.length === 0 ? (
                <TableRow>
                  <TableCell colSpan={6} className="text-center py-8 text-muted-foreground">
                    No assessments yet. Start your first scan!
                  </TableCell>
                </TableRow>
              ) : (
                assessments.map((assessment) => {
                  const config = statusConfig[assessment.status] || statusConfig.pending;
                  const StatusIcon = config.icon;
                  return (
                    <TableRow key={assessment.id}>
                      <TableCell className="font-medium">
                        {assessment.asset?.name ?? assessment.id}
                      </TableCell>
                      <TableCell className="capitalize">
                        {assessment.type}
                      </TableCell>
                      <TableCell>
                        <Badge className={config.className} variant="default">
                          <StatusIcon className="w-3 h-3 mr-1" />
                          {config.label}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        <Badge
                          variant={
                            assessment.findings_count > 10
                              ? "destructive"
                              : assessment.findings_count > 0
                                ? "secondary"
                                : "outline"
                          }
                        >
                          {assessment.findings_count}
                        </Badge>
                      </TableCell>
                      <TableCell>
                        {assessment.started_at
                          ? formatDistanceToNow(new Date(assessment.started_at), {
                              addSuffix: true,
                            })
                          : "—"}
                      </TableCell>
                      <TableCell className="text-right">
                        <DropdownMenu
                          open={menuOpenId === assessment.id}
                          onOpenChange={(open) =>
                            !open && setMenuOpenId(null)
                          }
                        >
                          <DropdownMenuTrigger asChild>
                            <Button
                              variant="ghost"
                              size="icon"
                              className="h-8 w-8"
                              disabled={actingId === assessment.id}
                              onClick={() => setMenuOpenId(assessment.id)}
                            >
                              {actingId === assessment.id ? (
                                <Pause className="w-4 h-4 animate-spin" />
                              ) : (
                                <MoreHorizontal className="w-4 h-4" />
                              )}
                            </Button>
                          </DropdownMenuTrigger>
                          <DropdownMenuContent align="end">
                            <DropdownMenuItem asChild>
                              <Link href="/scans" className="flex items-center">
                                <Eye className="w-4 h-4 mr-2" />
                                View Details
                              </Link>
                            </DropdownMenuItem>
                            <DropdownMenuSeparator />
                            {assessment.status === "running" ||
                            assessment.status === "pending" ? (
                              <DropdownMenuItem
                                className="text-red-600 focus:text-red-600"
                                onClick={() => handleCancel(assessment.id)}
                              >
                                <Ban className="w-4 h-4 mr-2" />
                                Cancel Scan
                              </DropdownMenuItem>
                            ) : (
                              <DropdownMenuItem
                                onClick={() => handleRerun(assessment.id)}
                              >
                                <RotateCcw className="w-4 h-4 mr-2" />
                                Re-run Scan
                              </DropdownMenuItem>
                            )}
                          </DropdownMenuContent>
                        </DropdownMenu>
                      </TableCell>
                    </TableRow>
                  );
                })
              )}
            </TableBody>
          </Table>
        </div>
      </CardContent>
    </Card>
  );
}