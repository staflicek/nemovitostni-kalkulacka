import streamlit as st
import math

st.set_page_config(layout="wide")

# 🔠 Vlastní CSS styly
st.markdown(
    """
    <style>
    h1 {font-size: 36px !important;}
    h2, h3 {font-size: 28px !important;}

    /* Popisky metrik */
    div[data-testid="stMetricLabel"] {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #333 !important;
    }

    /* Hodnoty metrik */
    div[data-testid="stMetricValue"] {
        font-size: 32px !important;
        font-weight: bold !important;
        color: black !important;
    }

    /* Zvýšení velikosti popisků nad vstupy */
    div[data-testid="stWidgetLabel"] > label > div > p {
        font-size: 24px !important;
        font-weight: bold !important;
        color: #000000 !important;
    }

    /* Hodnoty uvnitř vstupů */
    input {
        font-size: 20px !important;
        font-weight: bold !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🏠 Kalkulačka výnosnosti nemovitosti")

# ----------------------------
# 1) Požadovaný výnos a pořizovací cena
# ----------------------------
st.markdown("## 📊 Za kolik koupím, za kolik rekonstruuju a jaký z toho chci mít roční výnos?")
pozadovany_vynos = st.slider("Požadovaný čistý výnos (%)", 1.0, 15.0, 6.0) / 100
kupni_cena_bez = st.number_input("Kupní cena bez rekonstrukce (Kč)", min_value=0, value=3_000_000, step=100_000)
naklady_rekonstrukce = st.number_input("Náklady na rekonstrukci (Kč)", min_value=0, value=0, step=50_000)

realna_porizovaci_cena = kupni_cena_bez + naklady_rekonstrukce

# ----------------------------
# 2) Dashboard 1 – cílové hodnoty
# ----------------------------
pozadovane_rocni_ciste = realna_porizovaci_cena * pozadovany_vynos
pozadovane_mesicni_ciste = pozadovane_rocni_ciste / 12
ROI_cilove = pozadovane_rocni_ciste / realna_porizovaci_cena if realna_porizovaci_cena > 0 else 0

st.markdown("## 📊 Cílové hodnoty")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Reálná pořizovací cena", f"{realna_porizovaci_cena:,.0f} Kč")
with c2:
    st.metric("Na tento výnos potřebuji, aby po odečtení provozních nákladů zůstalo", f"{pozadovane_mesicni_ciste:,.0f} Kč/měs.")
with c3:
    st.metric("ROI (cílové)", f"{ROI_cilove:.2%}")

# ----------------------------
# 3) Další vstupy pro reálné hodnoty
# ----------------------------
st.markdown("---")
st.subheader("📥 Za kolik jsem schopný nemovitost reálně pronajmout a jaké budou provozní náklady?")

mesicni_najemne_real = st.number_input("Reálné měsíční hrubé nájemné (Kč)", min_value=0, value=14_000, step=500)
mesicni_naklady_real = st.number_input("Provozní měsíční náklady (Kč)", min_value=0, value=3_000, step=500)

# ----------------------------
# 4) Dashboard 2 – reálné hodnoty
# ----------------------------
rocni_ciste_real = (mesicni_najemne_real - mesicni_naklady_real) * 12
rocni_hrube_real = mesicni_najemne_real * 12

ROI_real = rocni_ciste_real / realna_porizovaci_cena if realna_porizovaci_cena > 0 else 0

# Výpočet rozdílu potřebného nájmu
rozdil_mesicni = pozadovane_mesicni_ciste - (mesicni_najemne_real - mesicni_naklady_real)

st.markdown("## 🏡 Jaké jsou reálně dosažitelné hodnoty?")
c4, c5, c6, c7 = st.columns(4)
with c4:
    st.metric("Čistý roční nájem (reálný)", f"{rocni_ciste_real:,.0f} Kč")
with c5:
    st.metric("Hrubé roční nájemné (reálné)", f"{rocni_hrube_real:,.0f} Kč")
with c6:
    st.metric("ROI (reálné)", f"{ROI_real:.2%}")
with c7:
    if rozdil_mesicni > 0:
        st.metric("Kolik chybí do cíle", f"+{rozdil_mesicni:,.0f} Kč/měs.")
    else:
        st.metric("Přesah oproti cíli", f"{abs(rozdil_mesicni):,.0f} Kč/měs.")

# ----------------------------
# 5) Dashboard 3 – Cizí kapitál (hypotéka)
# ----------------------------
st.markdown("---")
st.subheader("💰 Co musím splácet a kolik mě bude splácení stát? Jak bude v této situaci vypadat měsíční cashflow?")

hypoteka = st.number_input("Výše hypotéky (Kč)", min_value=0, value=2_000_000, step=100_000)
urok = st.number_input("Úroková sazba (%)", min_value=0.1, value=5.0, step=0.1) / 100
doba = st.number_input("Doba splatnosti (roky)", min_value=1, value=20, step=1)

# anuitní splátka
n = doba * 12
r = urok / 12

if hypoteka > 0 and urok > 0:
    splatka = hypoteka * r * (1 + r) ** n / ((1 + r) ** n - 1)
else:
    splatka = 0

# měsíční čistý výnos (nájem - náklady)
mesicni_cisty_real = mesicni_najemne_real - mesicni_naklady_real

# měsíční cashflow
cashflow = mesicni_cisty_real - splatka

c8, c9, c10 = st.columns(3)
with c8:
    st.metric("Měsíční splátka hypotéky", f"{splatka:,.0f} Kč")
with c9:
    st.metric("Reálný čistý měsíční výnos", f"{mesicni_cisty_real:,.0f} Kč")
with c10:
    if cashflow >= 0:
        st.metric("Měsíční cashflow", f"+{cashflow:,.0f} Kč")
    else:
        st.metric("Měsíční cashflow", f"{cashflow:,.0f} Kč")

