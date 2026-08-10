"use client";

import { useEffect, useState } from "react";
import { apiKeysApi } from "@/services/api";
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
  Key,
  Plus,
  Loader2,
  Copy,
  Trash2,
  Eye,
  EyeOff,
  CheckCircle,
} from "lucide-react";
import type { ApiKey } from "@/types";

export default function ApiKeysSettingsPage() {
  const [apiKeys, setApiKeys] = useState<ApiKey[]>([]);
  const [loading, setLoading] = useState(true);
  const [showNewKey, setShowNewKey] = useState<string | null>(null);
  const [creating, setCreating] = useState(false);
  const [newKeyName, setNewKeyName] = useState("");
  const [newKeyPrefix, setNewKeyPrefix] = useState("");

  async function load() {
    try {
      const orgId = localStorage.getItem("organization_id");
      if (!orgId) return;
      const res = await apiKeysApi.list(orgId);
      if (res.success && res.data) {
        setApiKeys(Array.isArray(res.data) ? res.data : []);
      }
    } catch (e) {
      console.error("Failed to load API keys:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    load();
  }, []);

  async function handleCreate() {
    const orgId = localStorage.getItem("organization_id");
    if (!orgId) {
      alert("Please login first to create an API key");
      return;
    }
    if (!newKeyName) {
      setCreating(false);
      return;
    }
    setCreating(true);
    try {
      const res = await apiKeysApi.create(orgId, {
        name: newKeyName,
        scopes: ["read", "write"],
      });
      if (res.success && res.data) {
        setShowNewKey(res.data.key);
        setNewKeyPrefix(res.data.api_key.key_prefix);
        setNewKeyName("");
        load();
      }
    } catch (e) {
      console.error("Failed to create API key:", e);
    } finally {
      setCreating(false);
    }
  }

  async function handleRevoke(id: string) {
    try {
      await apiKeysApi.revoke(id);
      load();
    } catch (e) {
      console.error("Failed to revoke:", e);
    }
  }

  async function handleToggle(id: string, isActive: boolean) {
    try {
      await apiKeysApi.toggle(id, !isActive);
      load();
    } catch (e) {
      console.error("Failed to toggle:", e);
    }
  }

  function copyKey(key: string) {
    navigator.clipboard.writeText(key);
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">API Keys</h1>
        <p className="text-muted-foreground mt-1">
          Manage API keys for programmatic access
        </p>
      </div>

      {showNewKey && (
        <Card className="border-green-500/40 bg-green-500/5">
          <CardContent className="pt-6">
            <div className="flex items-start justify-between">
              <div className="space-y-2">
                <div className="flex items-center gap-2 text-green-400">
                  <CheckCircle className="w-5 h-5" />
                  <span className="font-medium">API Key Created</span>
                </div>
                <p className="text-sm text-green-400">
                  Copy this key now. You will not be able to see it again.
                </p>
                <div className="flex items-center gap-2">
                  <code className="px-3 py-2 bg-secondary border border-border rounded text-sm font-mono">
                    {showNewKey}
                  </code>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => copyKey(showNewKey)}
                  >
                    <Copy className="w-4 h-4 mr-1" />
                    Copy
                  </Button>
                </div>
              </div>
              <Button
                variant="ghost"
                size="sm"
                onClick={() => setShowNewKey(null)}
              >
                Dismiss
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardHeader>
          <CardTitle>Create New Key</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-3">
            <Input
              placeholder="Key name (e.g., CI/CD Pipeline)"
              value={newKeyName}
              onChange={(e) => setNewKeyName(e.target.value)}
              className="max-w-sm"
            />
            <Button
              onClick={handleCreate}
              disabled={creating || !newKeyName}
            >
              {creating ? (
                <Loader2 className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Plus className="w-4 h-4 mr-2" />
              )}
              Create Key
            </Button>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Your API Keys ({apiKeys.length})</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          {loading ? (
            <div className="flex justify-center py-12">
              <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
            </div>
          ) : apiKeys.length === 0 ? (
            <div className="text-center py-12 text-muted-foreground">
              <Key className="w-12 h-12 mx-auto mb-4 opacity-50" />
              <p>No API keys yet. Create one to get started.</p>
            </div>
          ) : (
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Key Prefix</TableHead>
                  <TableHead>Scopes</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead>Created</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {apiKeys.map((key) => (
                  <TableRow key={key.id}>
                    <TableCell className="font-medium">{key.name}</TableCell>
                    <TableCell>
                      <code className="text-sm">{key.key_prefix}...</code>
                    </TableCell>
                    <TableCell>
                      <div className="flex gap-1">
                        {key.scopes.map((s) => (
                          <Badge key={s} variant="secondary" className="text-xs">
                            {s}
                          </Badge>
                        ))}
                      </div>
                    </TableCell>
                    <TableCell>
                      <Badge
                        variant={key.is_active ? "default" : "secondary"}
                        className={
                          key.is_active
                            ? "bg-green-500/15 text-green-400"
                            : "bg-secondary text-secondary-foreground border-border/60"
                        }
                      >
                        {key.is_active ? "Active" : "Revoked"}
                      </Badge>
                    </TableCell>
                    <TableCell className="text-sm text-muted-foreground">
                      {new Date(key.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      <div className="flex items-center gap-1">
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleToggle(key.id, key.is_active)}
                          title={key.is_active ? "Revoke" : "Re-enable"}
                        >
                          {key.is_active ? (
                            <EyeOff className="w-4 h-4" />
                          ) : (
                            <Eye className="w-4 h-4" />
                          )}
                        </Button>
                        <Button
                          variant="ghost"
                          size="icon"
                          onClick={() => handleRevoke(key.id)}
                        >
                          <Trash2 className="w-4 h-4 text-destructive" />
                        </Button>
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          )}
        </CardContent>
      </Card>
    </div>
  );
}