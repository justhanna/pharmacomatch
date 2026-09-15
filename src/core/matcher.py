import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import pandas as pd


class PharmacogenomicMatcher:
    """Mapuje warianty genetyczne pacjenta z regułami CPIC/PharmGKB."""

    def __init__(self, rules_path: str = "data/reference/rules.json"):
        self.rules_path = Path(rules_path)
        self.guidelines = self._load_rules()

    def _load_rules(self) -> List[Dict[str, Any]]:
        if not self.rules_path.exists():
            raise FileNotFoundError(f"Reference rules not found at: {self.rules_path}")
        with open(self.rules_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("guidelines", [])

    def get_supported_drugs(self) -> List[str]:
        return sorted(list({rule["drug"] for rule in self.guidelines}))

    def analyze_patient_drug(self, patient_df: pd.DataFrame, drug_name: str) -> Dict[str, Any]:
        """Zestawia genotypy pacjenta z wybranym lekiem i zwraca ocenę ryzyka."""
        applicable_rules = [r for r in self.guidelines if r["drug"].lower() == drug_name.lower()]

        if not applicable_rules:
            return {
                "drug": drug_name,
                "status": "NO_GUIDELINE",
                "message": f"Brak wytycznych CPIC dla leku {drug_name} w bazie wiedzy."
            }

        rule = applicable_rules[0]
        target_gene = rule["gene"].upper()
        target_rsid = rule["rsid"].lower()

        # Szukamy wariantu u pacjenta
        matched_row = patient_df[
            (patient_df["gene"].str.upper() == target_gene) &
            (patient_df["rsid"].str.lower() == target_rsid)
        ]

        if matched_row.empty:
            return {
                "drug": drug_name,
                "gene": target_gene,
                "rsid": target_rsid,
                "status": "VARIANT_NOT_TESTED",
                "message": f"Wariant {target_rsid} ({target_gene}) nie został znaleziony w profilu pacjenta."
            }

        patient_genotype = matched_row.iloc[0]["genotype"]
        # Sprawdzamy genotyp w macierzy ryzyka (uwzględniając obie orientacje, np. AG i GA)
        risk_matrix = rule.get("risk_matrix", {})
        genotype_key = patient_genotype
        if genotype_key not in risk_matrix and len(genotype_key) == 2:
            reversed_key = genotype_key[1] + genotype_key[0]
            if reversed_key in risk_matrix:
                genotype_key = reversed_key

        assessment = risk_matrix.get(genotype_key)

        if not assessment:
            return {
                "drug": drug_name,
                "gene": target_gene,
                "rsid": target_rsid,
                "genotype": patient_genotype,
                "status": "UNKNOWN_GENOTYPE",
                "message": f"Genotyp {patient_genotype} nie posiada sklasyfikowanego ryzyka w regułach."
            }

        return {
            "drug": drug_name,
            "gene": target_gene,
            "rsid": target_rsid,
            "genotype": patient_genotype,
            "phenotype": assessment["phenotype"],
            "risk_level": assessment["risk_level"],
            "action": assessment["action"],
            "recommendation": assessment["recommendation"],
            "status": "MATCH_FOUND"
        }