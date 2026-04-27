import streamlit as st
from decimal import Decimal, ROUND_HALF_UP

# --- CONFIGURATION PAGE ---
st.set_page_config(page_title="Calculateur Maturité", page_icon="🎓")
st.title("🎓 Calculateur de Moyennes de Maturité")

# --- FONCTIONS D'ARRONDI ---
def round_01(val):
    return val.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

def round_05(val):
    return (val * 2).quantize(Decimal("1"), rounding=ROUND_HALF_UP) / 2

# --- INTERFACE ---
st.info("Utilisez les champs ci-dessous pour entrer vos notes. Les arrondis au 0.5 sont calculés automatiquement.")

# Création de colonnes pour les matières de Maturité
col1, col2 = st.columns(2)

with col1:
    st.header("🇫🇷 Français")
    s1_fr = st.number_input("Français - Semestre 1", 1.0, 6.0, 4.0, 0.1, key="s1fr")
    s2_fr = st.number_input("Français - Semestre 2", 1.0, 6.0, 4.0, 0.1, key="s2fr")
    ecr_fr = st.number_input("Français - Écrit", 1.0, 6.0, 4.0, 0.1, key="efr")
    ora_fr = st.number_input("Français - Oral", 1.0, 6.0, 4.0, 0.1, key="ofr")

    st.header("🇩🇪 Allemand")
    s1_all = st.number_input("Allemand - Semestre 1", 1.0, 6.0, 4.0, 0.1, key="s1al")
    s2_all = st.number_input("Allemand - Semestre 2", 1.0, 6.0, 4.0, 0.1, key="s2al")
    ecr_all = st.number_input("Allemand - Écrit", 1.0, 6.0, 4.0, 0.1, key="eal")
    ora_all = st.number_input("Allemand - Oral", 1.0, 6.0, 4.0, 0.1, key="oal")

with col2:
    st.header("📐 Mathématiques")
    s1_ma = st.number_input("Maths - Semestre 1", 1.0, 6.0, 4.0, 0.1, key="s1ma")
    s2_ma = st.number_input("Maths - Semestre 2", 1.0, 6.0, 4.0, 0.1, key="s2ma")
    ecr_ma = st.number_input("Maths - Écrit", 1.0, 6.0, 4.0, 0.1, key="ema")
    ora_ma = st.number_input("Maths - Oral", 1.0, 6.0, 4.0, 0.1, key="oma")

    st.header("🇬🇧 Anglais")
    s1_an = st.number_input("Anglais - Semestre 1", 1.0, 6.0, 4.0, 0.1, key="s1an")
    s2_an = st.number_input("Anglais - Semestre 2", 1.0, 6.0, 4.0, 0.1, key="s2an")
    ecr_an = st.number_input("Anglais - Écrit", 1.0, 6.0, 4.0, 0.1, key="ean")
    ora_an = st.number_input("Anglais - Oral", 1.0, 6.0, 4.0, 0.1, key="oan")

st.divider()
st.header("💰 Branche Économie")
c1, c2 = st.columns(2)
with c1:
    st.subheader("Comptabilité")
    s1_c = st.number_input("Compta - Sem 1", 1.0, 6.0, 4.0, 0.1)
    s2_c = st.number_input("Compta - Sem 2", 1.0, 6.0, 4.0, 0.1)
    ecr_c = st.number_input("Compta - Écrit", 1.0, 6.0, 4.0, 0.1)
with c2:
    st.subheader("Éco Politique")
    s1_e = st.number_input("Éco Po - Sem 1", 1.0, 6.0, 4.0, 0.1)
    s2_e = st.number_input("Éco Po - Sem 2", 1.0, 6.0, 4.0, 0.1)
    ora_e = st.number_input("Éco Po - Oral", 1.0, 6.0, 4.0, 0.1)

# --- CALCULS ---
def calc_maturite(s1, s2, e, o):
    ann = round_01((Decimal(str(s1)) + Decimal(str(s2))) / 2)
    return round_05((2 * ann + Decimal(str(e)) + Decimal(str(o))) / 4)

res_fr = calc_maturite(s1_fr, s2_fr, ecr_fr, ora_fr)
res_ma = calc_maturite(s1_ma, s2_ma, ecr_ma, ora_ma)
res_al = calc_maturite(s1_all, s2_all, ecr_all, ora_all)
res_an = calc_maturite(s1_an, s2_an, ecr_an, ora_an)

# Calcul Éco
ann_c = round_01((Decimal(str(s1_c)) + Decimal(str(s2_c))) / 2)
note_c = round_01((ann_c + Decimal(str(ecr_c))) / 2)
ann_e = round_01((Decimal(str(s1_e)) + Decimal(str(s2_e))) / 2)
note_e = round_01((ann_e + Decimal(str(ora_e))) / 2)
res_eco = round_05((3 * note_c + 2 * note_e) / 5)

# --- RÉSULTATS ---
st.divider()
st.subheader("📊 Tes Notes Finales")
res1, res2, res3, res4, res5 = st.columns(5)
res1.metric("Français", f"{res_fr}")
res2.metric("Maths", f"{res_ma}")
res3.metric("Allemand", f"{res_al}")
res4.metric("Anglais", f"{res_an}")
res5.metric("Économie", f"{res_eco}")