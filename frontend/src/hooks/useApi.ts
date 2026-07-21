import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { assessmentsApi, findingsApi, assetsApi, pluginsApi, healthApi } from "@/services/api";
import type { Assessment, Finding, Asset, Plugin } from "@/types";

export function useHealth() {
  return useQuery({
    queryKey: ["health"],
    queryFn: healthApi.check,
    refetchInterval: 30000,
  });
}

export function useAssessments(params?: { page?: number; pageSize?: number; status?: string }) {
  return useQuery({
    queryKey: ["assessments", params],
    queryFn: () => assessmentsApi.list(params),
  });
}

export function useAssessment(id: string) {
  return useQuery({
    queryKey: ["assessments", id],
    queryFn: () => assessmentsApi.get(id),
    enabled: !!id,
  });
}

export function useCreateAssessment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: assessmentsApi.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assessments"] });
    },
  });
}

export function useStartAssessment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: assessmentsApi.start,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assessments"] });
    },
  });
}

export function useStopAssessment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: assessmentsApi.stop,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["assessments"] });
    },
  });
}

export function useFindings(params?: { assessmentId?: string; severity?: string; page?: number; pageSize?: number }) {
  return useQuery({
    queryKey: ["findings", params],
    queryFn: () => findingsApi.list(params),
  });
}

export function useAssets(params?: { page?: number; pageSize?: number; type?: string }) {
  return useQuery({
    queryKey: ["assets", params],
    queryFn: () => assetsApi.list(params),
  });
}

export function usePlugins() {
  return useQuery({
    queryKey: ["plugins"],
    queryFn: pluginsApi.list,
  });
}

export function useTogglePlugin() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: ({ id, enabled }: { id: string; enabled: boolean }) =>
      enabled ? pluginsApi.enable(id) : pluginsApi.disable(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["plugins"] });
    },
  });
}