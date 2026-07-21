"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Plus, Scan, Shield, Cloud, Code, Settings, ArrowRight } from "lucide-react";
import { useRouter } from "next/navigation";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { projectsApi } from "@/services/api";

interface QuickAction {
  label: string;
  description: string;
  icon: React.ReactNode;
  variant: "default" | "outline";
  action: () => void;
}

export function QuickActions() {
  const router = useRouter();
  const [showCreateProject, setShowCreateProject] = useState(false);
  const [projectName, setProjectName] = useState("");
  const [projectDesc, setProjectDesc] = useState("");
  const [creating, setCreating] = useState(false);

  async function handleCreateProject() {
    if (!projectName.trim()) return;
    setCreating(true);
    try {
      const orgId = localStorage.getItem("organization_id");
      if (!orgId) {
        alert("Please login first to create a project");
        setCreating(false);
        return;
      }
      const res = await projectsApi.create(orgId, {
        name: projectName,
        slug: projectName.toLowerCase().replace(/\s+/g, "-").replace(/[^a-z0-9-]/g, ""),
        description: projectDesc,
      });
      if (res.success && res.data) {
        setShowCreateProject(false);
        setProjectName("");
        setProjectDesc("");
        router.push(`/projects/${res.data.id}`);
      }
    } catch (e) {
      console.error("Failed to create project:", e);
    } finally {
      setCreating(false);
    }
  }

  const quickActions: QuickAction[] = [
    {
      label: "New Network Scan",
      description: "Scan network ranges for vulnerabilities",
      icon: <Scan className="w-5 h-5" />,
      variant: "default",
      action: () => router.push("/scans"),
    },
    {
      label: "Web Application Scan",
      description: "Assess web applications for OWASP Top 10",
      icon: <Code className="w-5 h-5" />,
      variant: "outline",
      action: () => router.push("/scans"),
    },
    {
      label: "Cloud Configuration Audit",
      description: "Review cloud infrastructure for misconfigurations",
      icon: <Cloud className="w-5 h-5" />,
      variant: "outline",
      action: () => router.push("/scans"),
    },
    {
      label: "Create Assessment",
      description: "Build a custom security assessment",
      icon: <Plus className="w-5 h-5" />,
      variant: "outline",
      action: () => setShowCreateProject(true),
    },
  ];

  return (
    <>
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center justify-between">
            Quick Actions
            <Button variant="ghost" size="sm">
              <Settings className="w-4 h-4" />
            </Button>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {quickActions.map((action, index) => (
            <Button
              key={index}
              variant={action.variant}
              className="w-full justify-start gap-3 text-left p-4 hover:bg-accent transition-colors"
              onClick={action.action}
            >
              <div className="p-2 bg-primary/10 text-primary rounded-lg">{action.icon}</div>
              <div className="flex-1">
                <p className="font-medium">{action.label}</p>
                <p className="text-sm text-muted-foreground">{action.description}</p>
              </div>
              <ArrowRight className="w-4 h-4 text-muted-foreground" />
            </Button>
          ))}
        </CardContent>
      </Card>

      <Dialog open={showCreateProject} onOpenChange={setShowCreateProject}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create New Project</DialogTitle>
            <DialogDescription>
              Projects help you organize security assessments by target. Create one to get started.
            </DialogDescription>
          </DialogHeader>
          <div className="space-y-4 py-4">
            <div className="space-y-2">
              <Label htmlFor="project-name">Project Name</Label>
              <Input
                id="project-name"
                placeholder="e.g., Production Infrastructure"
                value={projectName}
                onChange={(e) => setProjectName(e.target.value)}
              />
            </div>
            <div className="space-y-2">
              <Label htmlFor="project-desc">Description (optional)</Label>
              <Input
                id="project-desc"
                placeholder="Brief description of what's being assessed"
                value={projectDesc}
                onChange={(e) => setProjectDesc(e.target.value)}
              />
            </div>
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setShowCreateProject(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreateProject} disabled={!projectName.trim() || creating}>
              {creating ? "Creating..." : "Create Project"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </>
  );
}