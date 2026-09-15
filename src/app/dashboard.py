from pathlib import Path
import pandas as pd
import streamlit as st
import sys

# Dodajemy katalog główny projektu do sys.path, aby importy działały bezproblemowo
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from src.core.matcher import PharmacogenomicMatcher

st.set_page_config(
    page_title="PharmacoMatch | System Personalizacji Terapii",
    page_icon="💊",
    layout="wide"
)

st.title("💊 PharmacoMatch")
st.caption("System analizy interakcji lek-gen w medycynie personalizowanej (HUBA Engine)")


# Ładowanie silnika reguł
@st.cache_resource
def load_matcher():
    return PharmacogenomicMatcher()


matcher = load_matcher()
processed_dir = Path("data/processed")
processed_files = sorted(list(processed_dir.glob("*.parquet")))

if not processed_files:
    st.warning("Brak przetworzonych danych pacjentów w `data/processed/`. Uruchom najpierw `python run_huba.py`.")
    st.stop()

# Sidebar: Wybór danych
st.sidebar.header("Karta Pacjenta i Terapii")

patient_options = {}
for f in processed_files:
    df_preview = pd.read_parquet(f, columns=["sample_id"])
    if not df_preview.empty:
        sid = df_preview["sample_id"].iloc[0]
        patient_options[sid] = f

selected_patient_id = st.sidebar.selectbox(
    "Wybierz identyfikator pacjenta:",
    sorted(list(patient_options.keys()))
)

selected_file = patient_options[selected_patient_id]
patient_df = pd.read_parquet(selected_file)

supported_drugs = matcher.get_supported_drugs()
selected_drug = st.sidebar.selectbox("Wybierz planowany lek:", supported_drugs)

# Sekcja główna
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🧬 Profil Genetyczny Pacjenta")
    st.dataframe(
        patient_df[["sample_id", "gene", "rsid", "genotype"]],
        use_container_width=True,
        hide_index=True
    )

with col2:
    st.subheader("🎯 Wynik Analizy Farmakogenomicznej")
    result = matcher.analyze_patient_drug(patient_df, selected_drug)

    if result["status"] == "MATCH_FOUND":
        risk_level = result["risk_level"]

        if risk_level == "High":
            st.error(f"⚠️ Poziom ryzyka: WYSOKI ({result['phenotype']})")
        elif risk_level == "Moderate":
            st.warning(f"⚡ Poziom ryzyka: UMIARKOWANY ({result['phenotype']})")
        else:
            st.success(f"✅ Poziom ryzyka: NISKI ({result['phenotype']})")

        st.markdown(f"**Gen / Wariant:** `{result['gene']}` (`{result['rsid']}`)")
        st.markdown(f"**Genotyp pacjenta:** `{result['genotype']}`")
        st.markdown(f"**Zalecane działanie kliniczne:** `{result['action']}`")

        st.info(f"**Rekomendacja CPIC:**\n\n{result['recommendation']}")

    elif result["status"] == "VARIANT_NOT_TESTED":
        st.info(result["message"])
    else:
        st.warning(result["message"])

st.divider()
st.caption("PharmacoMatch • Moduł integracyjny HUBA • Przetwarzanie wsadowe i walidacja Pydantic")