from app.services.scoring import build_analysis


def test_build_analysis_produces_confidence_and_recommendation():
    result = build_analysis(
        identifier="CHEMBL25",
        resolved_structure="CC(=O)OC1=CC=CC=C1C(=O)O",
        bioactivity_summary={
            "target_relevance": "COX inhibitor",
            "mechanism_of_action": "Enzyme inhibition",
            "best_reported_activity_nM": 120,
        },
        pubchem_props={
            "MolecularWeight": 180.16,
            "XLogP": 1.2,
            "HBondDonorCount": 1,
            "HBondAcceptorCount": 4,
        },
        disease_links=["Inflammation pathway"],
    )

    assert result.confidence_score > 0.7
    assert result.recommendation == "promote"
    assert result.drug_likeness.lipinski_violations == 0
