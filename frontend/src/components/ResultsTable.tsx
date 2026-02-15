import { useMemo, useState } from "react";
import type { FeasibilityAnalysis } from "../types";

interface Props {
  results: FeasibilityAnalysis[];
}

export const ResultsTable = ({ results }: Props) => {
  const [riskFilter, setRiskFilter] = useState("all");
  const [sortKey, setSortKey] = useState<"confidence_score" | "synthetic_feasibility_score">("confidence_score");

  const visible = useMemo(() => {
    return [...results]
      .filter((item) => (riskFilter === "all" ? true : item.adme_tox.overall_risk === riskFilter))
      .sort((a, b) => b[sortKey] - a[sortKey]);
  }, [results, riskFilter, sortKey]);

  return (
    <section>
      <h2>Ranked feasibility analysis</h2>
      <label>
        ADME risk
        <select value={riskFilter} onChange={(event) => setRiskFilter(event.target.value)}>
          <option value="all">All</option>
          <option value="low">Low</option>
          <option value="moderate">Moderate</option>
          <option value="high">High</option>
        </select>
      </label>
      <label>
        Sort by
        <select value={sortKey} onChange={(event) => setSortKey(event.target.value as typeof sortKey)}>
          <option value="confidence_score">Activity confidence</option>
          <option value="synthetic_feasibility_score">Synthetic score</option>
        </select>
      </label>
      <table>
        <thead>
          <tr>
            <th>Identifier</th>
            <th>Confidence</th>
            <th>Synthetic score</th>
            <th>ADME risk</th>
            <th>Recommendation</th>
          </tr>
        </thead>
        <tbody>
          {visible.map((row) => (
            <tr key={row.input_identifier}>
              <td>{row.input_identifier}</td>
              <td>{row.confidence_score.toFixed(2)}</td>
              <td>{row.synthetic_feasibility_score.toFixed(2)}</td>
              <td>{row.adme_tox.overall_risk}</td>
              <td>{row.recommendation}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
};
