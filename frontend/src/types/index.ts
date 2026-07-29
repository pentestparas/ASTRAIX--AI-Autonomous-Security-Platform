// --- Core Types for VAPT Platform ---

export interface Plugin {
  id: string;
  name: string;
  description: string;
  version: string;
  author: string;
  type: "scanner" | "analyzer" | "reporter" | "integrator";
  enabled: boolean;
  config?: Record<string, unknown>;
}

export interface User {
  id: string;
  email: string;
  full_name?: string;
  organization_id?: string;
  is_active: boolean;
  is_superuser: boolean;
  last_login?: string;
  created_at: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  description?: string;
  logo_url?: string;
  settings: Record<string, unknown>;
  subscription_tier: string;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Project {
  id: string;
  organization_id: string;
  name: string;
  slug: string;
  description?: string;
  settings: Record<string, unknown>;
  is_active: boolean;
  created_at: string;
  updated_at: string;
  // Computed fields
  assets_count?: number;
  assessments_count?: number;
  open_findings_count?: number;
  critical_findings_count?: number;
}

export interface Membership {
  id: string;
  user_id: string;
  organization_id: string;
  project_id?: string;
  role: "owner" | "admin" | "analyst" | "viewer";
  is_default: boolean;
  created_at: string;
  user?: User;
}

export interface ApiKey {
  id: string;
  name: string;
  key_prefix: string;
  scopes: string[];
  expires_at?: string;
  last_used_at?: string;
  is_active: boolean;
  created_at: string;
}

export interface ApiKeyCreateResponse {
  api_key: ApiKey;
  key: string; // Only returned once!
}

export interface Asset {
  id: string;
  organization_id: string;
  project_id: string;
  name: string;
  type: "ip" | "hostname" | "domain" | "url" | "container_image" | "source_code" | "cloud_account" | "iac_directory";
  identifier: string;
  criticality: "critical" | "high" | "medium" | "low";
  tags: string[];
  metadata_json: Record<string, unknown>;
  last_scanned?: string;
  created_at: string;
  updated_at: string;
}

export interface Assessment {
  id: string;
  organization_id: string;
  project_id: string;
  asset_id: string;
  type: string;
  status: "pending" | "running" | "completed" | "failed" | "cancelled";
  config: Record<string, unknown>;
  started_at?: string;
  completed_at?: string;
  findings_count: number;
  error?: string;
  created_at: string;
  updated_at: string;
  // Relations
  asset?: Asset;
  project?: Project;
  asset_name?: string;
}

export interface Finding {
  id: string;
  organization_id: string;
  project_id: string;
  asset_id: string;
  assessment_id: string;
  plugin_id: string;
  title: string;
  description?: string;
  severity: "critical" | "high" | "medium" | "low" | "info";
  status: "open" | "triaged" | "resolved" | "false_positive" | "accepted";
  cvss_score?: number;
  cwe?: string[];
  cve?: string[];
  references?: string[];
  remediation?: string;
  fingerprint: string;
  tags: string[];
  metadata: Record<string, unknown>;
  created_at: string;
  updated_at: string;
  // Computed
  asset?: Asset;
}

export interface Capability {
  id: string;
  version: string;
  display_name: string;
  description: string;
  workflows: string[];
  supported_assets: string[];
  required_plugins: { plugin_id: string; min_version: string }[];
  compliance: { framework: string; control: string }[];
}

export interface ScanRequest {
  target: string;
  capability_id: string;
  ports?: number[];
  follow_redirects?: boolean;
  config?: Record<string, unknown>;
}

export interface ScanResponse {
  assessment_id: string;
  correlation_id: string;
  capability: string;
  status: string;
  finding_count: number;
  findings: FindingSummary[];
  risk_score_min: number;
  risk_score_max: number;
  risk_score_avg: number;
  error?: string;
}

export interface FindingSummary {
  id: string;
  title: string;
  description: string;
  severity: string;
  confidence: number;
  risk_score?: number;
  category: string;
  asset: string;
  tags: string[];
  plugin: string;
  cwe: string[];
  cve: string[];
  metadata: Record<string, unknown>;
}

// --- API Response Types ---

export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  errors?: Record<string, string[]>;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

// --- Auth Types ---

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name?: string;
  organization_name?: string;
  organization_slug?: string;
}

// --- Dashboard Stats ---

export interface DashboardStats {
  total_projects: number;
  active_scans: number;
  total_findings: number;
  critical_findings: number;
  high_findings: number;
  medium_findings: number;
  low_findings: number;
  resolved_findings: number;
  open_findings: number;
  assets_discovered: number;
  scans_this_week: number;
  scans_this_month: number;
}

export interface RecentActivity {
  id: string;
  type: "scan_started" | "scan_completed" | "finding_created" | "finding_resolved";
  description: string;
  timestamp: string;
  metadata?: Record<string, unknown>;
}

// --- Report Types ---

export interface ReportTemplate {
  id: string;
  name: string;
  description: string;
  type: "executive" | "technical" | "compliance";
  compliance_frameworks: string[];
}

export interface ReportRequest {
  assessment_id: string;
  template: string;
  format: "pdf" | "html" | "json" | "csv";
  include_raw_findings?: boolean;
}