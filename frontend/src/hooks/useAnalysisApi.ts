import { useState } from "react";
import type { FeasibilityAnalysis, JobStatus } from "../types";

const API_BASE = "http://localhost:8000";

export const useAnalysisApi = () => {
  const [loading, setLoading] = useState(false);

  const submit = async (entities: string[]) => {
    setLoading(true);
    const response = await fetch(`${API_BASE}/analyze`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ entities }),
    });
    const data = await response.json();
    setLoading(false);
    return data.jobId as string;
  };

  const pollStatus = async (jobId: string): Promise<JobStatus> => {
    const response = await fetch(`${API_BASE}/status/${jobId}`);
    return response.json();
  };

  const getResults = async (jobId: string): Promise<FeasibilityAnalysis[]> => {
    const response = await fetch(`${API_BASE}/results/${jobId}`);
    const payload = await response.json();
    return payload.rankings;
  };

  return { loading, submit, pollStatus, getResults };
};
