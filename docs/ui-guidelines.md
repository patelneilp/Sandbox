# UI/UX Guidelines

- Keep entity input forgiving: support comma/newline delimiters and mixed identifier types.
- Show explicit async feedback (`queued`, `running`, `% complete`) for long cheminformatics queries.
- Rank candidates by confidence by default; expose sorting by synthetic feasibility and ADME risk.
- Keep a persistent explanatory panel for medicinal chemistry interpretation (LiPE, Lipinski, ADMET rationale).
- For rejected compounds, surface the exact rejection reasons before any aggregate score.
- Include a provenance badge indicating data source (`chembl`, `pubchem`, `heuristic`) to avoid over-trust in inferred fields.
