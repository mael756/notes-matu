import streamlit as st
from decimal import Decimal, ROUND_HALF_UP

# --- CONFIGURATION ---
st.set_page_config(page_title="Calculateur Maturité", page_icon="🎓")

def round_01(val):
    return val.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

def round_05(val):
    return (val * 2).quantize(Decimal("1"), rounding=ROUND_HALF_UP) / 2

st.title("🎓 Calculateur de Maturité")
st.info("💡 Tes notes sont dans l'adresse (URL). Copie le lien pour les garder !")

# --- GESTION DE L'URL (SAUVEGARDE) ---
query_params = st.query_params

def get_p(key):
    return float(query_params.get(key, 4.0))

# --- BRANCHES MATURITÉ (Ordre respecté) ---
def section_maturite(nom, k):
    with st.expander(f"📚 {nom}", expanded=True):
        c1, c2 = st.columns(2)
        s1 = c1.number_input(f"{nom} S1", 1.0, 6.0, get_p(f"{k}s1"), 0.1, key=f"in_{k}s1")
        s2 = c1.number_input(f"{nom} S2", 1.0, 6.0, get_p(f"{k}s2"), 0.1, key=f"in_{k}s2")
        ecr = c2.number_input(f"{nom} Écrit", 1.0, 6.0, get_p(f"{k}e"), 0.1, key=f"in_{k}e")
        ora = c2.number_input(f"{nom} Oral", 1.0, 6.0, get_p(f"{k}o"), 0.1, key=f"in_{k}o")
        
        # Mise à jour URL
        st.query_params[f"{k}s1"] = s1
        st.query_params[f"{k}s2"] = s2
        st.query_params[f"{k}e"] = ecr
        st.query_params[f"{k}o"] = ora
        
        ann = round_01((Decimal(str(s1)) + Decimal(str(s2))) / 2)
        return round_05((2 * ann + Decimal(str(ecr)) + Decimal(str(ora))) / 4)

n_fr = section_maturite("Français", "fr")
n_ma = section_maturite("Mathématiques", "ma")
n_al = section_maturite("Allemand", "al")
n_an = section_maturite("Anglais", "an")

# --- ÉCONOMIE ---
with st.expander("💰 Économie", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Compta**")
        s1c = st.number_input("S1 ", 1.0, 6.0, get_p("cs1"), 0.1, key="ics1")
        s2c = st.number_input("S2 ", 1.0, 6.0, get_p("cs2"), 0.1, key="ics2")
        ecrc = st.number_input("Écrit ", 1.0, 6.0, get_p("ce"), 0.1, key="ice")
    with col2:
        st.write("**Éco Po**")
        s1e = st.number_input("S1", 1.0, 6.0, get_p("es1"), 0.1, key="ies1")
        s2e = st.number_input("S2", 1.0, 6.0, get_p("es2"), 0.1, key="ies2")
        orae = st.number_input("Oral", 1.0, 6.0, get_p("eo"), 0.1, key="ieo")
    
    st.query_params.update({"cs1":s1c,"cs2":s2c,"ce":ecrc,"es1":s1e,"es2":s2e,"eo":orae})

    ac = round_01((Decimal(str(s1c)) + Decimal(str(s2c))) / 2)
    nc = round_01((ac + Decimal(str(ecrc))) / 2)
    ae = round_01((Decimal(str(s1e)) + Decimal(str(s2e))) / 2)
    ne = round_01((ae + Decimal(str(orae))) / 2)
    n_eco = round_05((3 * nc + 2 * ne) / 5)

# --- RÉSULTATS ---
st.divider()
st.subheader("🏆 Résultats Finaux")
c = st.columns(5)
c[0].metric("FR", f"{n_fr}")
c[1].metric("MA", f"{n_ma}")
c[2].metric("AL", f"{n_al}")
c[3].metric("AN", f"{n_an}")
c[4].metric("ECO", f"{n_eco}")

if st.button("Réinitialiser"):
    st.query_params.clear()
    st.rerun()
