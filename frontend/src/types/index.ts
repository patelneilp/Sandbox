export interface FeasibilityAnalysis {
  input_identifier: string;
  target_relevance: string;
  mechanism_of_action: string;
  synthetic_feasibility_score: number;
  confidence_score: number;
  recommendation: string;
  adme_tox: {
    overall_risk: string;
  };
  rejection_or_promotion_reasons: string[];
}

export interface JobStatus {
  job_id: string;
  state: "queued" | "running" | "completed" | "failed";
  progress: number;
}
