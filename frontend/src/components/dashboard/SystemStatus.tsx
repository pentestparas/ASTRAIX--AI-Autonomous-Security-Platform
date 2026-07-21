"use client";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import { CheckCircle, AlertCircle, XCircle, Loader2, Server, Database, Cpu, HardDrive, Wifi, Zap } from "lucide-react";

interface ServiceStatus {
  name: string;
  icon: React.ReactNode;
  status: "healthy" | "degraded" | "down";
  details: string;
}

interface ResourceUsage {
  label: string;
  value: number;
  icon: React.ReactNode;
  color: string;
}

const services: ServiceStatus[] = [
  { name: "API Server", icon: <Server className="w-4 h-4" />, status: "healthy", details: "v0.1.0 • 99.9% uptime" },
  { name: "Database", icon: <Database className="w-4 h-4" />, status: "healthy", details: "PostgreSQL 16 • 45% used" },
  { name: "Cache", icon: <Cpu className="w-4 h-4" />, status: "healthy", details: "Redis 7 • 12% used" },
  { name: "Task Queue", icon: <Zap className="w-4 h-4" />, status: "healthy", details: "Celery • 3 workers active" },
  { name: "File Storage", icon: <HardDrive className="w-4 h-4" />, status: "healthy", details: "MinIO • 2.1 TB free" },
  { name: "Message Bus", icon: <Wifi className="w-4 h-4" />, status: "degraded", details: "RabbitMQ • High latency" },
];

const resources: ResourceUsage[] = [
  { label: "CPU", value: 34, icon: <Cpu className="w-4 h-4" />, color: "bg-blue-500" },
  { label: "Memory", value: 67, icon: <HardDrive className="w-4 h-4" />, color: "bg-green-500" },
  { label: "Disk", value: 45, icon: <Database className="w-4 h-4" />, color: "bg-yellow-500" },
  { label: "Network", value: 12, icon: <Wifi className="w-4 h-4" />, color: "bg-purple-500" },
];

function ServiceRow({ name, icon, status, details }: ServiceStatus) {
  const statusIcons = {
    healthy: <CheckCircle className="w-4 h-4 text-green-500" />,
    degraded: <AlertCircle className="w-4 h-4 text-yellow-500" />,
    down: <XCircle className="w-4 h-4 text-red-500" />,
  };

  return (
    <div className="flex items-center justify-between py-2 border-b last:border-0">
      <div className="flex items-center gap-3">
        <div className="p-1.5 bg-muted rounded">{icon}</div>
        <div>
          <p className="font-medium text-sm">{name}</p>
          <p className="text-xs text-muted-foreground">{details}</p>
        </div>
      </div>
      <div className="flex items-center gap-2">
        {statusIcons[status]}
        <span className="text-xs capitalize">{status}</span>
      </div>
    </div>
  );
}

function ResourceBar({ label, value, icon, color }: ResourceUsage) {
  return (
    <div className="space-y-1">
      <div className="flex items-center justify-between text-sm">
        <div className="flex items-center gap-2">
          <span className={`p-1 rounded ${color.replace("bg-", "bg-").replace("500", "100")} text-[${color.replace("bg-", "").replace("500", "600")}]`}>
            {icon}
          </span>
          <span>{label}</span>
        </div>
        <span className="font-medium">{value}%</span>
      </div>
      <Progress value={value} className="h-1.5" />
    </div>
  );
}

export function SystemStatus() {
  return (
    <div className="space-y-6">
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Zap className="w-5 h-5" />
            System Health
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2">
          {services.map((service) => (
            <ServiceRow key={service.name} {...service} />
          ))}
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Cpu className="w-5 h-5" />
            Resource Usage
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {resources.map((resource) => (
            <ResourceBar key={resource.label} {...resource} />
          ))}
        </CardContent>
      </Card>
    </div>
  );
}