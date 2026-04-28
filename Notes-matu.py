import streamlit as st
from decimal import Decimal, ROUND_HALF_UP
from streamlit_local_storage import LocalStorage

# --- CONFIGURATION ---
st.set_page_config(page_title="Calculateur Maturité", page_icon="🎓")
local_storage = LocalStorage()

def round_01(val):
    return val.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

def round_05(val):
    return (val * 2).quantize(Decimal("1"), rounding=ROUND_HALF_UP) / 2

st.title("🎓 Calculateur de Maturité")
st.info("Tes notes sont sauvegardées localement sur ce téléphone/ordi.")

def get_val(key):
    stored = local_storage.getItem(key)
    return float(stored) if stored is not None else 4.0

# --- BRANCHES MATURITÉ ---
def section_maturite(nom):
    with st.expander(f"📚 {nom}", expanded=True):
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{nom} S1", 1.0, 6.0, get_val(f"s1{nom}"), 0.1, key=f"in_s1{nom}")
        local_storage.setItem(f"s1{nom}", s1)
        s2 = c2.number_input(f"{nom} S2", 1.0, 6.0, get_val(f"s2{nom}"), 0.1, key=f"in_s2{nom}")
        local_storage.setItem(f"s2{nom}", s2)
        ecr = c1.number_input(f"{nom} Écrit", 1.0, 6.0, get_val(f"e{nom}"), 0.1, key=f"in_e{nom}")
        local_storage.setItem(f"e{nom}", ecr)
        ora = c2.number_input(f"{nom} Oral", 1.0, 6.0, get_val(f"o{nom}"), 0.1, key=f"in_o{nom}")
        local_storage.setItem(f"o{nom}", ora)
        
        ann = round_01((Decimal(str(s1)) + Decimal(str(s2))) / 2)
        # Formule : (2*année + écrit + oral) / 4 (Source: dawwd.jpeg)
        return round_05((2 * ann + Decimal(str(ecr)) + Decimal(str(ora))) / 4)

n_fr = section_maturite("Français")
n_ma = section_maturite("Mathématiques")
n_al = section_maturite("Allemand")
n_an = section_maturite("Anglais")

# --- BRANCHE ÉCONOMIE ---
with st.expander("💰 Économie", expanded=True):
    # Compta (Source: WhatsApp Image)
    s1c = st.number_input("Compta S1", 1.0, 6.0, get_val("s1c"), 0.1)
    local_storage.setItem("s1c", s1c)
    s2c = st.number_input("Compta S2", 1.0, 6.0, get_val("s2c"), 0.1)
    local_storage.setItem("s2c", s2c)
    ecrc = st.number_input("Compta Écrit", 1.0, 6.0, get_val("ecrc"), 0.1)
    local_storage.setItem("ecrc", ecrc)
    
    # Eco Po (Source: WhatsApp Image)
    s1e = st.number_input("Éco Po S1", 1.0, 6.0, get_val("s1e"), 0.1)
    local_storage.setItem("s1e", s1e)
    s2e = st.number_input("Éco Po S2", 1.0, 6.0, get_val("s2e"), 0.1)
    local_storage.setItem("s2e", s2e)
    orae = st.number_input("Éco Po Oral", 1.0, 6.0, get_val("orae"), 0.1)
    local_storage.setItem("orae", orae)

    ac = round_01((Decimal(str(s1c)) + Decimal(str(s2c))) / 2)
    nc = round_01((ac + Decimal(str(ecrc))) / 2)
    ae = round_01((Decimal(str(s1e)) + Decimal(str(s2e))) / 2)
    ne = round_01((ae + Decimal(str(orae))) / 2)
    # Formule : (3*compta + 2*ecopo) / 5 (Source: WhatsApp Image)
    n_eco = round_05((3 * nc + 2 * ne) / 5)

# --- AFFICHAGE ---
st.divider()
st.subheader("🏆 Résultats Finaux")
c = st.columns(5)
c[0].metric("FR", f"{n_fr}")
c[1].metric("MA", f"{n_ma}")
c[2].metric("AL", f"{n_al}")
c[3].metric("AN", f"{n_an}")
c[4].metric("ECO", f"{n_eco}")

if st.button("Effacer tout"):
    local_storage.deleteAll()
    st.rerun()
