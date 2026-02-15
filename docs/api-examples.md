# API Examples

## Submit analysis job

`POST /analyze`

```json
{
  "entities": ["CCO", "CHEMBL25", "50-78-2", "InChI=1S/C9H8O4..."]
}
```

Response:

```json
{
  "jobId": "4f1828a7-f9ec-4cdf-9655-0b07865fd652",
  "message": "Analysis queued"
}
```

## Poll status

`GET /status/{jobId}`

```json
{
  "job_id": "4f1828a7-f9ec-4cdf-9655-0b07865fd652",
  "state": "running",
  "progress": 0.5,
  "submitted_at": "2026-02-01T11:02:03.111Z",
  "updated_at": "2026-02-01T11:02:07.190Z",
  "error": null
}
```

## Results payload

`GET /results/{jobId}`

```json
{
  "job_id": "4f1828a7-f9ec-4cdf-9655-0b07865fd652",
  "status": { "state": "completed", "progress": 1.0 },
  "rankings": [
    {
      "input_identifier": "CHEMBL25",
      "target_relevance": "ChEMBL curated compound",
      "mechanism_of_action": "Requires linked mechanism endpoint expansion",
      "predicted_activity": {
        "assay_count": 25,
        "best_reported_activity_nM": 300,
        "source": "chembl"
      },
      "adme_tox": {
        "logp": 2.1,
        "solubility_class": "good",
        "metabolic_liability": "low",
        "tox_alerts": [],
        "overall_risk": "low"
      },
      "synthetic_feasibility_score": 0.81,
      "drug_likeness": {
        "molecular_weight": 305.2,
        "lipinski_violations": 0,
        "lipe": 4.4,
        "verdict": "promising"
      },
      "pathway_or_disease_association": [
        "Molecule type: Small molecule",
        "Therapeutic flag: true"
      ],
      "confidence_score": 0.8,
      "recommendation": "promote",
      "rejection_or_promotion_reasons": [
        "Sub-micromolar reported activity supports pharmacological relevance."
      ]
    }
  ]
}
```
