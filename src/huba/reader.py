from pathlib import Path
import pandas as pd


class PatientDataReader:
    """Obsługuje wczytywanie danych pacjentów z plików CSV, TSV oraz VCF."""

    @staticmethod
    def read_tabular(file_path: Path) -> pd.DataFrame:
        sep = "\t" if file_path.suffix.lower() == ".tsv" else ","
        df = pd.read_csv(file_path, sep=sep, dtype=str)
        # Normalizacja nagłówków kolumn
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        return df

    @staticmethod
    def read_vcf(file_path: Path) -> pd.DataFrame:
        records = []
        sample_id = file_path.stem

        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("#"):
                    continue
                parts = line.strip().split("\t")
                if len(parts) < 5:
                    continue

                rsid = parts[2]
                ref = parts[3]
                alt = parts[4]

                gene = "UNKNOWN"
                if len(parts) > 7 and "GENE=" in parts[7]:
                    for token in parts[7].split(";"):
                        if token.startswith("GENE="):
                            gene = token.split("=")[1]

                records.append({
                    "sample_id": sample_id,
                    "gene": gene,
                    "rsid": rsid,
                    "genotype": f"{ref}{alt}"
                })

        return pd.DataFrame(records)

    def load(self, file_path: Path) -> pd.DataFrame:
        ext = file_path.suffix.lower()
        if ext in [".csv", ".tsv"]:
            return self.read_tabular(file_path)
        elif ext == ".vcf":
            return self.read_vcf(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")