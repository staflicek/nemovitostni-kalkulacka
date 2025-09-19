import streamlit as st
import numpy_financial as npf

st.set_page_config(page_title="Kalkulačka výnosnosti", layout="wide")
st.title("📊 Kalkulačka výnosnosti nemovitosti")

# --- Vstupy ---
varianta = st.radio(
    "Zvolte variantu výpočtu:",
    ["A: Výpočet pro celý byt", "B: Výpočet pro počet pokojů"],
    index=0
)

col1, col2 = st.columns(2)

with col1:
    pozadovany_vynos = st.slider("Požadovaný čistý výnos (%)", 1.0, 10.0, 6.0, 0.1) / 100
    rekonstrukce = st.number_input("Náklady na rekonstrukci (Kč)", min_value=0, value=0, step=50000)
    kupni_cena = st.number_input("Kupní cena bez rekonstrukce (Kč)", min_value=0, value=3_000_000, step=100_000)

with col2:
    realne_najemne = st.number_input("Reálné měsíční čisté nájemné (Kč)", min_value=0, value=14_000, step=500)
    provozni_naklady = st.number_input("Provozní měsíční náklady (Kč)", min_value=0, value=3_000, step=500)
    ltv = st.slider("LTV (%)", 0, 100, 80, 1) / 100
    splatnost_let = st.slider("Splatnost hypotéky (roky)", 1, 40, 30, 1)
    urok = st.number_input("Úroková sazba hypotéky (%)", min_value=0.0, value=5.0, step=0.1) / 100

# --- Výpočty ---
hypo_vyse = kupni_cena * ltv
nper = splatnost_let * 12
mesicni_sazba = urok / 12
splatka = npf.pmt(mesicni_sazba, nper, -hypo_vyse) if nper > 0 else 0

rocni_ciste_najemne = realne_najemne * 12
rocni_hrube_najemne = (realne_najemne + provozni_naklady) * 12
max_cena = rocni_ciste_najemne / pozadovany_vynos if pozadovany_vynos > 0 else 0
cilovy_najem_mesicne = (kupni_cena + rekonstrukce) * pozadovany_vynos / 12
mesicni_cashflow = realne_najemne - splatka
ROI = rocni_ciste_najemne / (kupni_cena + rekonstrukce) if kupni_cena > 0 else 0

realna_porizovaci_cena = kupni_cena + rekonstrukce
realne_hrube_najemne = realne_najemne + provozni_naklady
ROI_real = rocni_ciste_najemne / realna_porizovaci_cena if realna_porizovaci_cena > 0 else 0

# --- Funkce pro KPI card ---
def kpi_card(title, value, color="#f0f2f6", icon="📊"):
    st.markdown(
        f"""
        <div style="
            background-color:{color};
            padding:20px;
            border-radius:15px;
            box-shadow:0 2px 4px rgba(0,0,0,0.1);
            text-align:center;
            margin:5px;">
            <h4 style="margin:0; font-size:16px; color:#333;">{icon} {title}</h4>
            <p style="margin:0; font-size:22px; font-weight:bold; color:#000;">{value}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# --- Dashboard 1: Cílové hodnoty ---
st.markdown("## 📈 Dashboard 1 – Cílové hodnoty")

row1 = st.columns(4)
with row1[0]: kpi_card("Max. pořizovací cena", f"{max_cena:,.0f} Kč", "#e8f5e9", "🏠")
with row1[1]: kpi_card("Potřebné nájemné", f"{cilovy_najem_mesicne:,.0f} Kč/měs.", "#fff3e0", "💰")
with row1[2]: kpi_card("Výše hypotéky", f"{hypo_vyse:,.0f} Kč", "#e3f2fd", "🏦")
with row1[3]: kpi_card("Měsíční splátka", f"{splatka:,.0f} Kč", "#fce4ec", "📉")

row2 = st.columns(3)
with row2[0]: kpi_card("Měsíční cashflow", f"{mesicni_cashflow:,.0f} Kč", "#ede7f6", "💸")
with row2[1]: kpi_card("Čistý roční nájem", f"{rocni_ciste_najemne:,.0f} Kč", "#f9fbe7", "📈")
with row2[2]: kpi_card("ROI (cílové)", f"{ROI*100:.2f} %", "#fffde7", "🔑")

st.divider()

# --- Dashboard 2: Reálné hodnoty ---
st.markdown("## 🏡 Dashboard 2 – Reálné hodnoty")

row3 = st.columns(3)
with row3[0]: kpi_card("Reálné čisté nájemné", f"{realne_najemne:,.0f} Kč/měs.", "#f1f8e9", "💵")
with row3[1]: kpi_card("Reálná pořizovací cena", f"{realna_porizovaci_cena:,.0f} Kč", "#ede7f6", "🏗️")
with row3[2]: kpi_card("Reálné hrubé nájemné", f"{realne_hrube_najemne:,.0f} Kč/měs.", "#fffde7", "📊")

row4 = st.columns(1)
with row4[0]: kpi_card("ROI (reálné)", f"{ROI_real*100:.2f} %", "#e0f7fa", "🔑")
