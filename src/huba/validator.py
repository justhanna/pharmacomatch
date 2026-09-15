import re
from typing import Optional
from pydantic import BaseModel, field_validator, ValidationError


class GeneticVariantRecord(BaseModel):
    sample_id: str
    gene: str
    rsid: str
    genotype: str

    @field_validator("sample_id")
    @classmethod
    def validate_sample_id(cls, v: str) -> str:
        clean = str(v).strip()
        if not clean or clean.lower() == "nan":
            raise ValueError("Sample ID cannot be empty.")
        return clean

    @field_validator("gene")
    @classmethod
    def normalize_gene(cls, v: str) -> str:
        clean = str(v).strip().upper()
        if not clean or clean == "NAN":
            raise ValueError("Gene identifier cannot be empty.")
        return clean

    @field_validator("rsid")
    @classmethod
    def validate_rsid(cls, v: str) -> str:
        clean = str(v).strip().lower()
        if not re.match(r"^rs\d+$", clean):
            raise ValueError(f"Invalid rsID format: '{v}'. Expected format like 'rs1065852'.")
        return clean

    @field_validator("genotype")
    @classmethod
    def validate_genotype(cls, v: str) -> str:
        # Usuwa białe znaki, ukośniki (A/G -> AG) i rzutuje na wielkie litery
        clean = re.sub(r"[^ACGTacgt*0-9]", "", str(v)).upper()
        if not clean or len(clean) < 2:
            raise ValueError(f"Invalid or missing genotype value: '{v}'.")
        return clean