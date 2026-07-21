"use client";

import { useEffect, useState } from "react";
import { organizationsApi } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Loader2, Save } from "lucide-react";
import type { Organization } from "@/types";

export default function OrganizationSettingsPage() {
  const [org, setOrg] = useState<Partial<Organization>>({});
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    async function load() {
      try {
        const orgId = localStorage.getItem("organization_id");
        if (!orgId) return;
        const res = await organizationsApi.get(orgId);
        if (res.success && res.data) {
          setOrg(res.data);
        }
      } catch (e) {
        console.error("Failed to load organization:", e);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  async function handleSave() {
    const orgId = localStorage.getItem("organization_id");
    if (!orgId) {
      alert("Please login first to save settings");
      return;
    }
    setSaving(true);
    try {
      await organizationsApi.update(orgId, {
        name: org.name,
        description: org.description,
      });
      setMessage("Settings saved successfully");
      setTimeout(() => setMessage(""), 3000);
    } catch (e) {
      console.error("Failed to save:", e);
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="w-6 h-6 animate-spin text-muted-foreground" />
      </div>
    );
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Organization Settings</h1>
        <p className="text-muted-foreground mt-1">
          Manage your organization details and preferences
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>General</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="text-sm font-medium mb-2 block">Organization Name</label>
            <Input
              value={org.name ?? ""}
              onChange={(e) => setOrg({ ...org, name: e.target.value })}
              placeholder="Your organization"
            />
          </div>
          <div>
            <label className="text-sm font-medium mb-2 block">Description</label>
            <textarea
              className="w-full px-3 py-2 border rounded-lg bg-background text-sm min-h-[100px]"
              value={org.description ?? ""}
              onChange={(e) => setOrg({ ...org, description: e.target.value })}
              placeholder="Describe your organization"
            />
          </div>
          <div>
            <label className="text-sm font-medium mb-2 block">Slug</label>
            <Input value={org.slug ?? ""} disabled />
            <p className="text-xs text-muted-foreground mt-1">
              The slug cannot be changed after creation
            </p>
          </div>
          <div>
            <label className="text-sm font-medium mb-2 block">Subscription Tier</label>
            <div className="px-3 py-2 border rounded-lg text-sm bg-muted">
              {org.subscription_tier ?? "—"}
            </div>
          </div>

          {message && (
            <p className="text-sm text-green-600 bg-green-50 px-3 py-2 rounded-lg">
              {message}
            </p>
          )}

          <Button onClick={handleSave} disabled={saving}>
            {saving ? <Loader2 className="w-4 h-4 mr-2 animate-spin" /> : <Save className="w-4 h-4 mr-2" />}
            Save Changes
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}