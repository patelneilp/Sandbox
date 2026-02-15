# Backend Service

FastAPI backend for drug feasibility analysis.

## Features

- REST endpoints:
  - `POST /analyze`
  - `GET /status/{jobId}`
  - `GET /results/{jobId}`
- Async background job manager plus optional Redis/RQ queue adapter (`app/workers/rq_queue.py`).
- Cached external API calls (TTL cache) for ChEMBL and PubChem.
- Rate-limit handling with exponential backoff for HTTP 429 responses.
- Heuristic scoring for ADME/Tox, synthetic feasibility, and drug-likeness.

## External API integration snippets

- ChEMBL molecule endpoint:
  - `https://www.ebi.ac.uk/chembl/api/data/molecule/CHEMBL25.json`
- PubChem property endpoint:
  - `https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/aspirin/property/MolecularWeight,XLogP,HBondDonorCount,HBondAcceptorCount,CanonicalSMILES/JSON`

## Running tests

```bash
pytest
```
