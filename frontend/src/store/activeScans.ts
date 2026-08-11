import { create } from "zustand";
import { persist } from "zustand/middleware";

export interface ActiveScan {
  id: string;
  target: string;
  scanType: string;
  startedAt: number;
  status: "running" | "paused" | "stopped" | "completed" | "failed";
}

interface ActiveScansState {
  scans: Record<string, ActiveScan>;
  addScan: (scan: ActiveScan) => void;
  updateScan: (id: string, patch: Partial<ActiveScan>) => void;
  removeScan: (id: string) => void;
  clear: () => void;
  runningCount: () => number;
}

export const useActiveScansStore = create<ActiveScansState>()(
  persist(
    (set, get) => ({
      scans: {},
      addScan: (scan) =>
        set((state) => ({ scans: { ...state.scans, [scan.id]: scan } })),
      updateScan: (id, patch) =>
        set((state) => {
          const scan = state.scans[id];
          if (!scan) return state;
          return { scans: { ...state.scans, [id]: { ...scan, ...patch } } };
        }),
      removeScan: (id) =>
        set((state) => {
          const next = { ...state.scans };
          delete next[id];
          return { scans: next };
        }),
      clear: () => set({ scans: {} }),
      runningCount: () =>
        Object.values(get().scans).filter((s) => s.status === "running").length,
    }),
    { name: "astraix-active-scans" }
  )
);
