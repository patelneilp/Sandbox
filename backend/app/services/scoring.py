from __future__ import annotations

import math
from typing import Any

from app.models.schemas import ADMETRisk, DrugLikeness, FeasibilityAnalysis


def _estimate_synthetic_feasibility(smiles: str | None) -> float:
    if not smiles:
        return 0.45
    complexity_penalty = min(smiles.count("[") * 0.05 + smiles.count("@") * 0.03, 0.4)
    aromatic_bonus = min(smiles.count("c") * 0.01, 0.2)
    score = 0.75 + aromatic_bonus - complexity_penalty
    return max(0.0, min(score, 1.0))


def _admet_from_props(props: dict[str, Any]) -> ADMETRisk:
    logp = props.get("XLogP")
    mw = props.get("MolecularWeight")

    if mw and mw > 550:
        solubility = "low"
    elif logp and logp > 4:
        solubility = "moderate"
    else:
        solubility = "good"

    metabolic = "high" if logp and logp > 5 else "moderate" if logp and logp > 3 else "low"
    tox_alerts = ["High lipophilicity"] if logp and logp > 5 else []
    overall = "high" if tox_alerts else "moderate" if metabolic == "moderate" else "low"

    return ADMETRisk(
        logp=logp,
        solubility_class=solubility,
        metabolic_liability=metabolic,
        tox_alerts=tox_alerts,
        overall_risk=overall,
    )


def _drug_likeness(props: dict[str, Any], predicted_potency_nm: float | None) -> DrugLikeness:
    mw = props.get("MolecularWeight")
    logp = props.get("XLogP")
    hbd = props.get("HBondDonorCount", 0)
    hba = props.get("HBondAcceptorCount", 0)

    violations = 0
    violations += 1 if mw and mw > 500 else 0
    violations += 1 if logp and logp > 5 else 0
    violations += 1 if hbd > 5 else 0
    violations += 1 if hba > 10 else 0

    pIC50 = -math.log10((predicted_potency_nm or 1000) * 1e-9)
    lipe = pIC50 - (logp or 0)
    verdict = "promising" if violations <= 1 and lipe >= 2 else "needs optimization"

    return DrugLikeness(
        molecular_weight=mw,
        lipinski_violations=violations,
        lipe=round(lipe, 2),
        verdict=verdict,
    )


def build_analysis(
    identifier: str,
    resolved_structure: str | None,
    bioactivity_summary: dict[str, Any],
    pubchem_props: dict[str, Any],
    disease_links: list[str],
) -> FeasibilityAnalysis:
    potency_nm = bioactivity_summary.get("best_reported_activity_nM")
    admet = _admet_from_props(pubchem_props)
    likeness = _drug_likeness(pubchem_props, potency_nm)
    synth = _estimate_synthetic_feasibility(resolved_structure)

    confidence = 0.35
    confidence += 0.25 if potency_nm else 0.0
    confidence += 0.2 if pubchem_props else 0.0
    confidence += 0.2 if disease_links else 0.0
    confidence = min(confidence, 1.0)

    reasons = []
    if potency_nm and potency_nm < 500:
        reasons.append("Sub-micromolar reported activity supports pharmacological relevance.")
    if admet.overall_risk == "high":
        reasons.append("ADME/Tox profile indicates high risk due to lipophilicity/metabolism.")
    if likeness.lipinski_violations > 1:
        reasons.append("Multiple Lipinski rule violations reduce oral drug-likeness.")
    if synth < 0.5:
        reasons.append("Estimated synthetic complexity may slow medicinal chemistry cycles.")

    recommendation = "promote" if confidence > 0.6 and admet.overall_risk != "high" else "reject_or_optimize"

    return FeasibilityAnalysis(
        input_identifier=identifier,
        resolved_structure=resolved_structure,
        target_relevance=bioactivity_summary.get("target_relevance", "Insufficient target data"),
        mechanism_of_action=bioactivity_summary.get("mechanism_of_action", "Unknown or not curated"),
        predicted_activity=bioactivity_summary,
        adme_tox=admet,
        synthetic_feasibility_score=round(synth, 3),
        drug_likeness=likeness,
        pathway_or_disease_association=disease_links,
        confidence_score=round(confidence, 3),
        recommendation=recommendation,
        rejection_or_promotion_reasons=reasons
        or ["Automated assessment produced neutral evidence; collect targeted assays."],
    )
