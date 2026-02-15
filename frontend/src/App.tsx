import { useState } from "react";
import { EntityUploader } from "./components/EntityUploader";
import { ResultsTable } from "./components/ResultsTable";
import { useAnalysisApi } from "./hooks/useAnalysisApi";
import type { FeasibilityAnalysis } from "./types";

export default function App() {
  const [statusText, setStatusText] = useState("Idle");
  const [results, setResults] = useState<FeasibilityAnalysis[]>([]);
  const { loading, submit, pollStatus, getResults } = useAnalysisApi();

  const handleSubmit = async (entities: string[]) => {
    setStatusText("Submitting job...");
    const jobId = await submit(entities);

    let state = "queued";
    while (state === "queued" || state === "running") {
      const status = await pollStatus(jobId);
      state = status.state;
      setStatusText(`Status: ${status.state} (${Math.round(status.progress * 100)}%)`);
      if (state !== "completed") {
        await new Promise((resolve) => setTimeout(resolve, 1000));
      }
    }

    const ranked = await getResults(jobId);
    setResults(ranked);
    setStatusText("Analysis complete");
  };

  return (
    <main style={{ maxWidth: 1100, margin: "0 auto", fontFamily: "Arial" }}>
      <h1>Drug Development Feasibility Analyzer</h1>
      <p>
        Evaluate target relevance, activity confidence, ADME/Tox risk, synthetic tractability, and promotion/rejection rationale.
      </p>
      <EntityUploader onSubmit={handleSubmit} />
      <p>{loading ? "Loading..." : statusText}</p>
      {results.length > 0 && <ResultsTable results={results} />}
    </main>
  );
}
