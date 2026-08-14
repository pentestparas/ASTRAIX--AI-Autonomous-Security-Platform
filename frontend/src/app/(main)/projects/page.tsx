"use client";

import { useEffect, useState } from "react";
import { projectsApi } from "@/services/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Plus, FolderKanban, ShieldAlert, Activity, MoreHorizontal, Eye, Trash2 } from "lucide-react";
import Link from "next/link";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import type { Project } from "@/types";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateProject, setShowCreateProject] = useState(false);
  const [projectName, setProjectName] = useState("");
  const [projectDesc, setProjectDesc] = useState("");
  const [creating, setCreating] = useState(false);
  const [menuOpenId, setMenuOpenId] = useState<string | null>(null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  async function loadProjects() {
    try {
      const orgId = localStorage.getItem("organization_id");
      if (!orgId) {
        setLoading(false);
        return;
      }
      const res = await projectsApi.list(orgId);
      const projects = res as unknown as any[];
      if (Array.isArray(projects)) {
        setProjects(projects);
      }
    } catch (e) {
      console.error("Failed to load projects:", e);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadProjects();
  }, []);

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
      const projectData = res as unknown as { id?: string };
      if (projectData && projectData.id) {
        setShowCreateProject(false);
        setProjectName("");
        setProjectDesc("");
        loadProjects();
      }
    } catch (e: unknown) {
      const error = e as { response?: { data?: { detail?: string } } };
      const message = error?.response?.data?.detail || "Failed to create project";
      alert(message);
    } finally {
      setCreating(false);
    }
  }

  async function handleDeleteProject(projectId: string) {
    if (!confirm("Are you sure you want to delete this project? This action cannot be undone.")) {
      return;
    }
    setDeletingId(projectId);
    setMenuOpenId(null);
    try {
      const orgId = localStorage.getItem("organization_id");
      if (!orgId) return;
      await projectsApi.delete(orgId, projectId);
      loadProjects();
    } catch (e) {
      console.error("Failed to delete project:", e);
      alert("Failed to delete project");
    } finally {
      setDeletingId(null);
    }
  }

  function handleMenuClick(e: React.MouseEvent, projectId: string) {
    e.preventDefault();
    e.stopPropagation();
    setMenuOpenId(menuOpenId === projectId ? null : projectId);
  }

  return (
    <>
      <div className="max-w-7xl mx-auto space-y-6">
        <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Projects</h1>
          <p className="text-sm text-muted-foreground mt-0.5">
            Manage your security assessment projects
          </p>
        </div>
        <Button onClick={() => setShowCreateProject(true)}>
          <Plus className="w-4 h-4 mr-2" />
          New Project
        </Button>
      </div>

      {loading ? (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {Array.from({ length: 3 }).map((_, i) => (
            <Card key={i}>
              <CardHeader>
                <div className="h-6 w-32 animate-pulse bg-muted rounded" />
              </CardHeader>
              <CardContent>
                <div className="h-4 w-48 animate-pulse bg-muted rounded mb-2" />
                <div className="h-4 w-32 animate-pulse bg-muted rounded" />
              </CardContent>
            </Card>
          ))}
        </div>
      ) : projects.length === 0 ? (
        <Card className="p-12 text-center">
          <FolderKanban className="w-12 h-12 mx-auto text-muted-foreground mb-4" />
          <h3 className="text-base font-semibold mb-1.5">No projects yet</h3>
          <p className="text-sm text-muted-foreground mb-5">
            Create your first project to start organizing security assessments
          </p>
          <Button onClick={() => setShowCreateProject(true)}>
            <Plus className="w-4 h-4 mr-2" />
            Create Project
          </Button>
        </Card>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {projects.map((project) => (
            <div key={project.id} className="relative">
              <Link href={`/projects/${project.id}`}>
                <Card className="hover:border-primary/50 transition-colors cursor-pointer h-full">
                  <CardHeader className="flex flex-row items-center justify-between space-y-0">
                    <CardTitle className="text-base font-semibold">{project.name}</CardTitle>
                  </CardHeader>
                  <CardContent>
                    <p className="text-sm text-muted-foreground mb-4 line-clamp-2">
                      {project.description || "No description"}
                    </p>
                    <div className="flex items-center gap-4 text-sm">
                      <div className="flex items-center gap-1.5 text-muted-foreground">
                        <Activity className="w-3.5 h-3.5" />
                        <span className="tech">{project.assessments_count ?? 0}</span> scans
                      </div>
                      <div className="flex items-center gap-1.5 text-muted-foreground">
                        <ShieldAlert className="w-3.5 h-3.5" />
                        <span className="tech">{project.open_findings_count ?? 0}</span> open
                      </div>
                    </div>
                    <div className="mt-3">
                      <Badge
                        variant={
                          project.critical_findings_count && project.critical_findings_count > 0
                            ? "destructive"
                            : "secondary"
                        }
                        className="tech"
                      >
                        {project.critical_findings_count ?? 0} critical
                      </Badge>
                    </div>
                  </CardContent>
                </Card>
              </Link>
              <div className="absolute top-4 right-4">
                <DropdownMenu open={menuOpenId === project.id} onOpenChange={(open) => !open && setMenuOpenId(null)}>
                  <DropdownMenuTrigger asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="h-8 w-8"
                      onClick={(e) => handleMenuClick(e as unknown as React.MouseEvent, project.id)}
                    >
                      <MoreHorizontal className="w-4 h-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent align="end">
                    <DropdownMenuItem asChild>
                      <Link href={`/projects/${project.id}`} className="flex items-center">
                        <Eye className="w-4 h-4 mr-2" />
                        View Project
                      </Link>
                    </DropdownMenuItem>
                    <DropdownMenuSeparator />
                    <DropdownMenuItem
                      className="text-red-400 focus:text-red-400"
                      onClick={() => handleDeleteProject(project.id)}
                      disabled={deletingId === project.id}
                    >
                      <Trash2 className="w-4 h-4 mr-2" />
                      {deletingId === project.id ? "Deleting..." : "Delete Project"}
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>

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