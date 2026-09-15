from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# 1. Valid patient file (CSV)
patient_001 = """sample_id,gene,rsid,genotype
PAT-001,CYP2D6,rs1065852,AA
PAT-001,CYP2C19,rs4244285,GG
PAT-001,SLCO1B1,rs4149056,CT
"""

# 2. Patient with dirty values (spaces, malformed rsID, slashes)
patient_002 = """sample_id,gene,rsid,genotype
PAT-002, cyp2d6 ,rs1065852,A/G
PAT-002,CYP2C19,INVALID_RSID,AA
PAT-002,SLCO1B1,rs4149056,CC
"""

# 3. TSV format with a missing genotype row
patient_003 = """sample_id\tgene\trsid\tgenotype
PAT-003\tCYP2D6\trs1065852\tGG
PAT-003\tCYP2C19\trs4244285\t
PAT-003\tSLCO1B1\trs4149056\tTT
"""

# 4. Minimal synthetic VCF file
patient_004_vcf = """##fileformat=VCFv4.2
##source=PharmacoMatchSyntheticGenerator
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
chr22\t42523900\trs1065852\tA\tA\t99\tPASS\tGENE=CYP2D6
chr10\t96541234\trs4244285\tA\tA\t99\tPASS\tGENE=CYP2C19
chr12\t21345678\trs4149056\tC\tC\t99\tPASS\tGENE=SLCO1B1
"""

(RAW_DIR / "patient_001.csv").write_text(patient_001, encoding="utf-8")
(RAW_DIR / "patient_002.csv").write_text(patient_002, encoding="utf-8")
(RAW_DIR / "patient_003.tsv").write_text(patient_003, encoding="utf-8")
(RAW_DIR / "PAT-004.vcf").write_text(patient_004_vcf, encoding="utf-8")

print("Generated 4 test files in data/raw/ with varied formats and edge cases.")