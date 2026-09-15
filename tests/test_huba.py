import pytest
from pydantic import ValidationError
from src.huba.validator import GeneticVariantRecord


def test_valid_genetic_record():
    record = GeneticVariantRecord(
        sample_id="PAT-001",
        gene="cyp2d6",
        rsid="RS1065852",
        genotype="A/G"
    )
    assert record.gene == "CYP2D6"
    assert record.rsid == "rs1065852"
    assert record.genotype == "AG"


def test_invalid_rsid_format():
    with pytest.raises(ValidationError) as excinfo:
        GeneticVariantRecord(
            sample_id="PAT-002",
            gene="CYP2C19",
            rsid="INVALID_RSID",
            genotype="AA"
        )
    assert "Invalid rsID format" in str(excinfo.value)


def test_missing_or_blank_sample_id():
    with pytest.raises(ValidationError):
        GeneticVariantRecord(
            sample_id="   ",
            gene="CYP2D6",
            rsid="rs1065852",
            genotype="AA"
        )


def test_empty_genotype_rejection():
    with pytest.raises(ValidationError):
        GeneticVariantRecord(
            sample_id="PAT-003",
            gene="SLCO1B1",
            rsid="rs4149056",
            genotype=""
        )