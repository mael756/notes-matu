import streamlit as st
from decimal import Decimal, ROUND_HALF_UP
from streamlit_local_storage import LocalStorage

# --- CONFIGURATION ---
st.set_page_config(page_title="Calculateur Maturité", page_icon="🎓")

# Initialisation du stockage
if 'ls' not in st.session_state:
    st.session_state.ls = LocalStorage()

def round_01(val):
    return val.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

def round_05(val):
    return (val * 2).quantize(Decimal("1"), rounding=ROUND_HALF_UP) / 2

st.title("🎓 Calculateur de Maturité")

# --- RÉCUPÉRATION SÉCURISÉE ---
try:
    all_data = st.session_state.ls.getAll(key="get_all_notes")
except Exception:
    all_data = None

def get_stored(key_name):
    if all_data and isinstance(all_data, dict) and key_name in all_data:
        try:
            return float(all_data[key_name])
        except:
            return 4.0
    return 4.0

# --- BRANCHES MATURITÉ ---
def section_maturite(nom):
    with st.expander(f"📚 {nom}", expanded=True):
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{nom} S1", 1.0, 6.0, get_stored(f"s1{nom}"), 0.1, key=f"in_s1{nom}")
        s2 = c2.number_input(f"{nom} S2", 1.0, 6.0, get_stored(f"s2{nom}"), 0.1, key=f"in_s2{nom}")
        ecr = c1.number_input(f"{nom} Écrit", 1.0, 6.0, get_stored(f"e{nom}"), 0.1, key=f"in_e{nom}")
        ora = c2.number_input(f"{nom} Oral", 1.0, 6.0, get_stored(f"o{nom}"), 0.1, key=f"in_o{nom}")
        
        # Sauvegarde
        st.session_state.ls.setItem(f"s1{nom}", s1, key=f"set_s1{nom}")
        st.session_state.ls.setItem(f"s2{nom}", s2, key=f"set_s2{nom}")
        st.session_state.ls.setItem(f"e{nom}", ecr, key=f"set_e{nom}")
        st.session_state.ls.setItem(f"o{nom}", ora, key=f"set_o{nom}")
        
        ann = round_01((Decimal(str(s1)) + Decimal(str(s2))) / 2)
        return round_05((2 * ann + Decimal(str(ecr)) + Decimal(str(ora))) / 4)

n_fr = section_maturite("Français")
n_ma = section_maturite("Mathématiques")
n_al = section_maturite("Allemand")
n_an = section_maturite("Anglais")

# --- ÉCONOMIE ---
with st.expander("💰 Économie", expanded=True):
    s1c = st.number_input("Compta S1", 1.0, 6.0, get_stored("s1c"), 0.1, key="in_s1c")
    s2c = st.number_input("Compta S2", 1.0, 6.0, get_stored("s2c"), 0.1, key="in_s2c")
    ecrc = st.number_input("Compta Écrit", 1.0, 6.0, get_stored("ecrc"), 0.1, key="in_ecrc")
    st.session_state.ls.setItem("s1c", s1c, key="set_s1c")
    st.session_state.ls.setItem("s2c", s2c, key="set_s2c")
    st.session_state.ls.setItem("ecrc", ecrc, key="set_ecrc")

    s1e = st.number_input("Éco Po S1", 1.0, 6.0, get_stored("s1e"), 0.1, key="in_s1e")
    s2e = st.number_input("Éco Po S2", 1.0, 6.0, get_stored("s2e"), 0.1, key="in_s2e")
    orae = st.number_input("Éco Po Oral", 1.0, 6.0, get_stored("orae"), 0.1, key="in_orae")
    st.session_state.ls.setItem("s1e", s1e, key="set_s1e")
    st.session_state.ls.setItem("s2e", s2e, key="set_s2e")
    st.session_state.ls.setItem("orae", orae, key="set_orae")

    ac = round_01((Decimal(str(s1c)) + Decimal(str(s2c))) / 2)
    nc = round_01((ac + Decimal(str(ecrc))) / 2)
    ae = round_01((Decimal(str(s1e)) + Decimal(str(s2e))) / 2)
    ne = round_01((ae + Decimal(str(orae))) / 2)
    n_eco = round_05((3 * nc + 2 * ne) / 5)

# --- RÉSULTATS ---
st.divider()
st.subheader("🏆 Résultats Finaux")
cols = st.columns(5)
cols[0].metric("FR", f"{n_fr}")
cols[1].metric("MA", f"{n_ma}")
cols[2].metric("AL", f"{n_al}")
cols[3].metric("AN", f"{n_an}")
cols[4].metric("ECO", f"{n_eco}")

if st.button("Réinitialiser"):
    st.session_state.ls.deleteAll(key="clear_all")
    st.rerun()
