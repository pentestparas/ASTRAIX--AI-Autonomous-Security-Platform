import axios, { AxiosInstance, AxiosRequestConfig, InternalAxiosRequestConfig } from "axios";
import type {
  ApiResponse,
  PaginatedResponse,
  Assessment,
  Finding,
  Asset,
  Plugin,
  Organization,
  Project,
  Membership,
  ApiKey,
  User,
  TokenResponse,
  ScanRequest,
  ScanResponse,
  ScanProgress,
  DashboardStats,
  RecentActivity,
  SystemStatus,
  VaptAssessmentDetail,
} from "@/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        "Content-Type": "application/json",
      },
      timeout: 60000,
    });

    this.client.interceptors.request.use(
      (config: InternalAxiosRequestConfig) => {
        const token =
          typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
        if (token && config.headers) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => Promise.reject(error)
    );

    this.client.interceptors.response.use(
      (response) => response,
      async (error) => {
        if (error.response?.status === 401) {
          if (typeof window !== "undefined") {
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            window.location.href = "/login";
          }
        }
        return Promise.reject(error);
      }
    );
  }

  async get<T>(url: string, params?: Record<string, unknown>) {
    const response = await this.client.get<ApiResponse<T>>(url, { params });
    return response.data;
  }

  async post<T>(url: string, data?: unknown, config?: AxiosRequestConfig) {
    const response = await this.client.post<ApiResponse<T>>(url, data, config);
    return response.data;
  }

  async put<T>(url: string, data?: unknown) {
    const response = await this.client.put<ApiResponse<T>>(url, data);
    return response.data;
  }

  async patch<T>(url: string, data?: unknown) {
    const response = await this.client.patch<ApiResponse<T>>(url, data);
    return response.data;
  }

  async delete<T>(url: string) {
    const response = await this.client.delete<ApiResponse<T>>(url);
    return response.data;
  }

  async getPaginated<T>(url: string, params?: Record<string, unknown>) {
    const response = await this.client.get<ApiResponse<PaginatedResponse<T>>>(url, { params });
    return response.data;
  }
}

export const apiClient = new ApiClient();

// --- Auth ---
export const authApi = {
  login: (email: string, password: string) =>
    apiClient.post<TokenResponse>("/auth/login/json", { email, password }),
  register: (data: {
    email: string;
    password: string;
    full_name?: string;
    organization_name?: string;
    organization_slug?: string;
  }) => apiClient.post<User>("/auth/register", data),
  me: () => apiClient.get<User>("/auth/me"),
  refresh: () => apiClient.post<TokenResponse>("/auth/refresh"),
};

// --- Organizations ---
export const organizationsApi = {
  list: () => apiClient.get<Organization[]>("/organizations"),
  get: (id: string) => apiClient.get<Organization>(`/organizations/${id}`),
  create: (data: { name: string; slug: string; description?: string }) =>
    apiClient.post<Organization>("/organizations", data),
  update: (id: string, data: Partial<Organization>) =>
    apiClient.patch<Organization>(`/organizations/${id}`, data),
  delete: (id: string) => apiClient.delete(`/organizations/${id}`),
};

// --- Projects ---
export const projectsApi = {
  list: (organizationId: string, params?: { page?: number; limit?: number }) =>
    apiClient.getPaginated<Project>(`/projects?organization_id=${organizationId}`, params),
  get: (id: string) => apiClient.get<Project>(`/projects/${id}`),
  create: (organizationId: string, data: { name: string; slug: string; description?: string }) =>
    apiClient.post<Project>(`/projects?organization_id=${organizationId}`, data),
  update: (id: string, data: Partial<Project>) =>
    apiClient.patch<Project>(`/projects/${id}`, data),
  delete: (organizationId: string, id: string) =>
    apiClient.delete(`/projects/${id}?organization_id=${organizationId}`),
};

// --- Memberships ---
export const membershipsApi = {
  list: (organizationId: string, projectId?: string) =>
    apiClient.get<Membership[]>(`/memberships?organization_id=${organizationId}${projectId ? `&project_id=${projectId}` : ""}`),
  invite: (organizationId: string, data: { email: string; role: string; project_id?: string }) =>
    apiClient.post<Membership>(`/memberships?organization_id=${organizationId}`, data),
  update: (id: string, data: { role?: string; is_default?: boolean }) =>
    apiClient.patch<Membership>(`/memberships/${id}`, data),
  remove: (id: string) => apiClient.delete(`/memberships/${id}`),
};

// --- API Keys ---
export const apiKeysApi = {
  list: (organizationId: string) =>
    apiClient.get<ApiKey[]>(`/api-keys?organization_id=${organizationId}`),
  create: (organizationId: string, data: { name: string; scopes: string[]; expires_in_days?: number }) =>
    apiClient.post<{ api_key: ApiKey; key: string }>(`/api-keys?organization_id=${organizationId}`, data),
  revoke: (id: string) => apiClient.delete(`/api-keys/${id}`),
  toggle: (id: string, isActive: boolean) =>
    apiClient.patch<ApiKey>(`/api-keys/${id}`, { is_active: isActive }),
};

// --- Assessments ---
export const assessmentsApi = {
  list: (
    params?: {
      page?: number;
      limit?: number;
      status?: string;
      organization_id?: string;
      project_id?: string;
    }
  ) => apiClient.getPaginated<Assessment>("/assessments", params),
  get: (id: string) => apiClient.get<Assessment>(`/assessments/${id}`),
  create: (data: Partial<Assessment>) => apiClient.post<Assessment>("/assessments", data),
  start: (id: string) => apiClient.post<Assessment>(`/assessments/${id}/start`),
  cancel: (id: string) => apiClient.delete(`/assessments/${id}`),
  stop: (id: string) => apiClient.delete(`/assessments/${id}`),
};

// --- Scan Engine ---
export const scanApi = {
  run: (data: ScanRequest) =>
    apiClient.post<ScanResponse>("/assess", data, { timeout: 300000 }),
  getCapabilities: () => apiClient.get<{ capability: string; status: string }[]>("/capabilities"),
};

// --- VAPT Scan (AI-planned pipeline with live progress) ---
export const vaptScanApi = {
  run: (data: ScanRequest | any) =>
    apiClient.post<ScanResponse>("/vapt/scan", data, { timeout: 600000 }),
  progress: (scanId: string, since = 0) =>
    apiClient.get<ScanProgress>(
      `/vapt/scan/${scanId}/progress`,
      { since }
    ),
  detail: (assessmentId: string) =>
    apiClient.get<VaptAssessmentDetail>(`/vapt/assessments/${assessmentId}`),
  pause: (scanId: string) => apiClient.post(`/vapt/scan/${scanId}/pause`),
  resume: (scanId: string) => apiClient.post(`/vapt/scan/${scanId}/resume`),
  stop: (scanId: string) => apiClient.post(`/vapt/scan/${scanId}/stop`),
  restart: (scanId: string) =>
    apiClient.post<ScanResponse>(`/vapt/scan/${scanId}/restart`, undefined, {
      timeout: 600000,
    }),
};

// --- Findings ---
export const findingsApi = {
  list: (
    params?: {
      page?: number;
      limit?: number;
      page_size?: number;
      severity?: string;
      status?: string;
      organization_id?: string;
      project_id?: string;
      assessment_id?: string;
    }
  ) => apiClient.getPaginated<Finding>("/findings", params),
  get: (id: string) => apiClient.get<Finding>(`/findings/${id}`),
  update: (id: string, data: { status?: string; severity?: string }) =>
    apiClient.patch<Finding>(`/findings/${id}`, data),
  bulkUpdate: (
    ids: string[],
    data: { status?: string; severity?: string }
  ) => apiClient.post("/findings/bulk-update", { ids, ...data }),
  delete: (id: string) => apiClient.delete(`/findings/${id}`),
};

// --- Assets ---
export const assetsApi = {
  list: (
    params?: {
      page?: number;
      limit?: number;
      type?: string;
      organization_id?: string;
      project_id?: string;
    }
  ) => apiClient.getPaginated<Asset>("/assets", params),
  get: (id: string) => apiClient.get<Asset>(`/assets/${id}`),
  create: (data: Partial<Asset>) => apiClient.post<Asset>("/assets", data),
  update: (id: string, data: Partial<Asset>) => apiClient.patch<Asset>(`/assets/${id}`, data),
  delete: (id: string) => apiClient.delete(`/assets/${id}`),
};

// --- Plugins ---
export const pluginsApi = {
  list: () => apiClient.get<Plugin[]>("/plugins"),
  get: (id: string) => apiClient.get<Plugin>(`/plugins/${id}`),
  enable: (id: string) => apiClient.post<Plugin>(`/plugins/${id}/enable`),
  disable: (id: string) => apiClient.post<Plugin>(`/plugins/${id}/disable`),
};

// --- Dashboard Stats ---
export const dashboardApi = {
  getStats: (organizationId: string) =>
    apiClient.get<DashboardStats>(`/dashboard/stats?organization_id=${organizationId}`),
  getRecentActivity: (organizationId: string, limit = 10) =>
    apiClient.get<RecentActivity[]>(`/dashboard/activity?organization_id=${organizationId}&limit=${limit}`),
};

// --- Health ---
export const healthApi = {
  check: () => apiClient.get<{ status: string; service: string; version: string }>("/health"),
  ready: () => apiClient.get<{ status: string }>("/ready"),
};

// --- System Status (real component checks) ---
export const systemApi = {
  status: () => apiClient.get<SystemStatus>("/system/status"),
};

// --- Attack Surface Graph ---
export const graphApi = {
  get: (scanId?: string) =>
    apiClient.get<{ nodes: any[]; edges: any[] }>(`/graph${scanId ? `?scan_id=${scanId}` : ""}`),
};

// --- Reports ---
export interface ReportTemplateInfo {
  id: string;
  name: string;
  description: string;
  version: string;
  frameworks: string[];
}

export interface ReportGenerateResponse {
  download_url: string | null;
  report: string;
  filename: string;
  format: string;
  mime?: string;
  title: string;
  findings_count: number;
}

export const reportsApi = {
  generate: (assessmentId: string, template: string, format: string) =>
    apiClient.post<ReportGenerateResponse>("/reports/generate", {
      assessment_id: assessmentId,
      template,
      format,
    }),
  getTemplates: () =>
    apiClient.get<ReportTemplateInfo[]>("/reports/templates"),
  list: (params?: { page?: number; limit?: number }) =>
    apiClient.getPaginated<{ id: string; created_at: string; template: string }>("/reports", params),
};