from pathlib import Path

RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)

# Pacjent 1: Czysty plik CSV (profil kardiologiczny i przeciwbólowy)
patient_001 = """sample_id,gene,rsid,genotype
PAT-001,CYP2D6,rs1065852,AA
PAT-001,CYP2C19,rs4244285,GG
PAT-001,SLCO1B1,rs4149056,CT
PAT-001,VKORC1,rs9923231,AG
PAT-001,DPYD,rs3918290,GG
"""

# Pacjent 2: Brudny plik CSV (białe znaki, ukośniki w genotypie, jeden błędny rsID)
patient_002 = """sample_id,gene,rsid,genotype
PAT-002, cyp2d6 ,rs1065852,A/G
PAT-002,CYP2C19,INVALID_RSID_123,AA
PAT-002,SLCO1B1,rs4149056,CC
PAT-002,VKORC1,rs9923231,AA
PAT-002,DPYD,rs3918290,GG
"""

# Pacjent 3: Plik TSV (tab-separated) z pustym genotypem do odrzucenia
patient_003 = """sample_id\tgene\trsid\tgenotype
PAT-003\tCYP2D6\trs1065852\tGG
PAT-003\tCYP2C19\trs4244285\t
PAT-003\tSLCO1B1\trs4149056\tTT
PAT-003\tVKORC1\trs9923231\tGG
PAT-003\tDPYD\trs3918290\tAG
"""

# Pacjent 4: Czysty format VCF
patient_004_vcf = """##fileformat=VCFv4.2
##source=PharmacoMatchSyntheticLab
#CHROM\tPOS\tID\tREF\tALT\tQUAL\tFILTER\tINFO
chr22\t42523900\trs1065852\tA\tA\t99\tPASS\tGENE=CYP2D6
chr10\t96541234\trs4244285\tA\tA\t99\tPASS\tGENE=CYP2C19
chr12\t21345678\trs4149056\tC\tC\t99\tPASS\tGENE=SLCO1B1
chr16\t31107932\trs9923231\tA\tA\t99\tPASS\tGENE=VKORC1
chr1\t97915614\trs3918290\tA\tG\t99\tPASS\tGENE=DPYD
"""

# Pacjent 5: Pacjent onkologiczny (DPYD deficiency - wysokie ryzyko dla Fluorouracylu)
patient_005 = """sample_id,gene,rsid,genotype
PAT-005,CYP2D6,rs1065852,GG
PAT-005,CYP2C19,rs4244285,AG
PAT-005,SLCO1B1,rs4149056,TT
PAT-005,VKORC1,rs9923231,GG
PAT-005,DPYD,rs3918290,AA
"""

# Pacjent 6: Plik z brakiem nagłówka sample_id (HUBA musi uzupełnić ID z nazwy pliku)
patient_006 = """gene,rsid,genotype
CYP2D6,rs1065852,AG
CYP2C19,rs4244285,AA
SLCO1B1,rs4149056,CC
VKORC1,rs9923231,AG
DPYD,rs3918290,GG
"""

# Pacjent 7: Pacjent o optymalnym profilu (wszystkie leki bezpieczne / standardowe)
patient_007 = """sample_id,gene,rsid,genotype
PAT-007,CYP2D6,rs1065852,GG
PAT-007,CYP2C19,rs4244285,GG
PAT-007,SLCO1B1,rs4149056,TT
PAT-007,VKORC1,rs9923231,GG
PAT-007,DPYD,rs3918290,GG
"""

(RAW_DIR / "patient_001.csv").write_text(patient_001, encoding="utf-8")
(RAW_DIR / "patient_002.csv").write_text(patient_002, encoding="utf-8")
(RAW_DIR / "patient_003.tsv").write_text(patient_003, encoding="utf-8")
(RAW_DIR / "PAT-004.vcf").write_text(patient_004_vcf, encoding="utf-8")
(RAW_DIR / "PAT-005.csv").write_text(patient_005, encoding="utf-8")
(RAW_DIR / "PAT-006.csv").write_text(patient_006, encoding="utf-8")
(RAW_DIR / "PAT-007.csv").write_text(patient_007, encoding="utf-8")

print("Generated 7 diverse test files in data/raw/.")