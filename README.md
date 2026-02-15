# Drug Feasibility Monorepo

This repository contains a full-stack skeleton for ranking chemical entities as drug-development candidates.

## Structure

- `backend/` — FastAPI service, async job processing, external API integrations, cache layer, and tests.
- `frontend/` — React UI for uploading entities and inspecting ranked feasibility analyses.
- `shared/` — Shared schemas and utility definitions used across backend/frontend.
- `docs/` — API response examples and UI guidance.

## Quick start

### Backend

```bash
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

### Run tests

```bash
cd backend
pytest
```

## Note

This is a production-oriented scaffold with mock scoring formulas plus real public API integration points (ChEMBL/PubChem). You can replace heuristic scoring with validated QSAR/ML pipelines, and wire Redis workers for horizontal scaling.
