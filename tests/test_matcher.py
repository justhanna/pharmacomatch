import pandas as pd
import pytest
from src.core.matcher import PharmacogenomicMatcher


@pytest.fixture
def matcher():
    return PharmacogenomicMatcher(rules_path="data/reference/rules.json")


def test_supported_drugs_list(matcher):
    drugs = matcher.get_supported_drugs()
    assert "Warfarin" in drugs
    assert "Fluorouracil" in drugs
    assert "Codeine" in drugs
    assert len(drugs) >= 5


def test_high_risk_clopidogrel_detection(matcher):
    patient_df = pd.DataFrame([
        {"sample_id": "PAT-002", "gene": "CYP2C19", "rsid": "rs4244285", "genotype": "AA"}
    ])
    result = matcher.analyze_patient_drug(patient_df, "Clopidogrel")

    assert result["status"] == "MATCH_FOUND"
    assert result["risk_level"] == "High"
    assert result["phenotype"] == "Poor Metabolizer"
    assert result["action"] == "Contraindicated"


def test_missing_variant_handling(matcher):
    # Pacjent ma wariant tylko dla CYP2D6, sprawdzamy lek na SLCO1B1
    patient_df = pd.DataFrame([
        {"sample_id": "PAT-001", "gene": "CYP2D6", "rsid": "rs1065852", "genotype": "AA"}
    ])
    result = matcher.analyze_patient_drug(patient_df, "Simvastatin")

    assert result["status"] == "VARIANT_NOT_TESTED"
    assert "nie został znaleziony" in result["message"]