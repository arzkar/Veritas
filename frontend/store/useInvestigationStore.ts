import { create } from 'zustand';

export type EpistemicStatus = 
  | 'unverified' 
  | 'supported' 
  | 'contradicted' 
  | 'absent' 
  | 'ambiguous';

export interface ConfidenceMetrics {
  extraction: number;
  retrieval: number;
  analysis: number;
}

export interface Claim {
  id: string;
  statement: string;
  category: string;
  importance: number;
  belief: EpistemicStatus;
  confidence: ConfidenceMetrics;
  primary_slide: number;
  credibility_score: number;
  analyst_summary?: string;
  skeptic_summary?: string;
  red_flag_severity: number;
}

export interface Evidence {
  id: string;
  source_type: string;
  url?: string;
  title?: string;
  content_snippet: string;
  source_authority: number;
  recency_score: number;
  supports_claim: boolean;
  sentiment_score: number;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  agent_name: string;
  event_type: string;
  message: string;
  metadata?: any;
}

interface Job {
  job_id: string;
  company: string;
  status: string;
  created_at: string;
  document_id: string;
}

interface InvestigationState {
  currentJobId: string | null;
  companyName: string | null;
  globalCredibilityScore: number;
  redFlagCount: number;
  claims: Record<string, Claim>;
  evidence: Record<string, Evidence[]>;
  auditLogs: AuditLog[];
  activeSlide: number;
  status: 'idle' | 'ingesting' | 'investigating' | 'completed' | 'failed';
  progress: { current: number; total: number; phase: string } | null;
  jobs: Job[];
  
  // Actions
  setJob: (jobId: string, companyName?: string) => void;
  setStatus: (status: InvestigationState['status']) => void;
  setProgress: (progress: InvestigationState['progress']) => void;
  setGlobalScore: (score: number, redFlagCount: number) => void;
  setAuditLogs: (logs: AuditLog[]) => void;
  upsertClaim: (claim: Claim) => void;
  setClaims: (claims: Record<string, Claim>) => void;
  addEvidence: (claimId: string, evidence: Evidence) => void;
  setActiveSlide: (slide: number) => void;
  setJobs: (jobs: Job[]) => void;
  loadJobData: (jobId: string) => Promise<void>;
  reset: () => void;
}

export const useInvestigationStore = create<InvestigationState>((set, get) => ({
  currentJobId: null,
  companyName: null,
  globalCredibilityScore: 1.0,
  redFlagCount: 0,
  claims: {},
  evidence: {},
  auditLogs: [],
  activeSlide: 1,
  status: 'idle',
  progress: null,
  jobs: [],

  setJob: (jobId, companyName) => set({ currentJobId: jobId, companyName: companyName || null }),
  setStatus: (status) => set({ status }),
  setProgress: (progress) => set({ progress }),
  setGlobalScore: (score, redFlagCount) => set({ globalCredibilityScore: score, redFlagCount }),
  setAuditLogs: (logs) => set({ auditLogs: logs }),
  upsertClaim: (claim) => set((state) => ({
    claims: { ...state.claims, [claim.id]: claim }
  })),
  setClaims: (claims) => set({ claims }),
  addEvidence: (claimId, evidence) => set((state) => ({
    evidence: {
      ...state.evidence,
      [claimId]: [...(state.evidence[claimId] || []), evidence]
    }
  })),
  setActiveSlide: (slide) => set({ activeSlide: slide }),
  setJobs: (jobs) => set({ jobs }),

  loadJobData: async (jobId) => {
    try {
      const response = await fetch(`http://localhost:8000/report/${jobId}`);
      const data = await response.json();
      if (data.status === 'completed') {
        const report = data.report;
        set({
          currentJobId: jobId,
          companyName: data.company,
          globalCredibilityScore: report.global_credibility_score,
          redFlagCount: report.red_flag_count,
          claims: report.claims,
          auditLogs: report.audit_logs || [],
          status: 'completed'
        });
      } else {
        set({ currentJobId: jobId, status: data.status as any });
      }
    } catch (error) {
      console.error('Failed to load job data:', error);
    }
  },

  reset: () => set({
    currentJobId: null,
    companyName: null,
    globalCredibilityScore: 1.0,
    redFlagCount: 0,
    claims: {},
    evidence: {},
    auditLogs: [],
    activeSlide: 1,
    status: 'idle',
    progress: null
  }),
}));
