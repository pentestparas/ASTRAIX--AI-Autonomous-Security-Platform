"use client";

import { useEffect, useState } from "react";
import { membershipsApi } from "@/services/api";
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
import { Input } from "@/components/ui/input";
import {
  Users,
  Plus,
  Loader2,
  UserMinus,
  Shield,
  Trash2,
} from "lucide-react";
import type { Membership } from "@/types";

const roleConfig = {
  owner: { label: "Owner", className: "bg-purple-500/20 text-purple-300" },
  admin: { label: "Admin", className: "bg-red-500/15 text-red-400" },
  analyst: { label: "Analyst", className: "bg-blue-500/15 text-blue-400" },
  viewer: { label: "Viewer", className: "bg-secondary text-secondary-foreground border-border/60" },
};

export default function MembersSettingsPage() {
  const [memberships, setMemberships] = useState<Membership[]>([]);
  const [loading, setLoading] = useState(true);
  const [inviteEmail, setInviteEmail] = useState("");
  const [inviteRole, setInviteRole] = useState("analyst");
  const [inviting, setInviting] = useState(false);

  async function load() {
    try {
      const orgId = localStorage.getItem("organization_id");
      if (!orgId) return;
      const res = await membershipsApi.list(orgId);
      if (res.success && res.data) {
        const data = res.data as Membership[];
        setMemberships(Array.isArray(data) ? data : []);
      }
    } catch (e) {
      console.error("Failed to load members:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleInvite() {
    if (!inviteEmail) return;
    const orgId = localStorage.getItem("organization_id");
    if (!orgId) return;
    setInviting(true);
    try {
      await membershipsApi.invite(orgId, {
        email: inviteEmail,
        role: inviteRole,
      });
      setInviteEmail("");
      load();
    } catch (e) {
      console.error("Failed to invite:", e);
    } finally {
      setInviting(false);
    }
  }

  async function handleRemove(id: string) {
    try {
      await membershipsApi.remove(id);
      load();
    } catch (e) {
      console.error("Failed to remove member:", e);
    }
  }

  async function handleRoleChange(id: string, role: string) {
    try {
      await membershipsApi.update(id, { role });
      load();
    } catch (e) {
      console.error("Failed to update role:", e);
    }
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Team Members</h1>
        <p className="text-muted-foreground mt-1">
          Manage your organization team and roles
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Invite Member</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-3">
            <Input
              type="email"
              placeholder="email@example.com"
              value={inviteEmail}
              onChange={(e) => setInviteEmail(e.target.value)}
              className="max-w-sm"
            />
            <select
              className="px-3 py-2 border rounded-lg bg-background text-sm"
              value={inviteRole}
              onChange={(e) => setInviteRole(e.target.value)}
            >
              <option value="viewer">Viewer</option>
              <option value="analyst">Analyst</option>
              <option value="admin">Admin</option>
            </select>
            <Button onClick={handleInvite} disabled={inviting || !inviteEmail}>
              {inviting ? (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Plus className="w-4 h-4 mr-2" />
              )}
              Invite
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Members ({memberships.length})</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {loading ? (
            <div className="flex justify-center py-12">
              <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
            </div>
          ) : memberships.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              <Users className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>No members yet. Invite someone to get started.</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>User</TableHead>
                  <TableHead>Role</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {memberships.map((m) => {
                  const role = roleConfig[m.role] || roleConfig.viewer;
                  return (
                    <TableRow key={m.id}>
                      <TableCell>
                        <div>
                          <div className="font-medium">
                            {m.user?.full_name ?? m.user?.email ?? "—"}
                          </div>
                          {m.user?.email && (
                            <div className="text-sm text-muted-foreground">
                              {m.user.email}
                            </div>
                          )}
                        </div>
                      </TableCell>
                      <TableCell>
                        <select
                          className="text-xs px-2 py-1 border rounded bg-background"
                          value={m.role}
                          onChange={(e) =>
                            handleRoleChange(m.id, e.target.value)
                          }
                        >
                          {Object.entries(roleConfig).map(([key, val]) => (
                            <option key={key} value={key}>
                              {val.label}
                            </option>
                          ))}
                        </select>
                      </TableCell>
                      <TableCell>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleRemove(m.id)}
                        >
                          <Trash2 className="w-4 h-4 text-destructive" />
                        </Button>
                      </TableCell>
                    </TableRow>
                  );
                })}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}