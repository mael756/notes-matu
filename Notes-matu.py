import streamlit as st
from decimal import Decimal, ROUND_HALF_UP

# --- CONFIGURATION ---
st.set_page_config(page_title="Calculateur Maturité", page_icon="🎓")

def round_01(val):
    return val.quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)

def round_05(val):
    return (val * 2).quantize(Decimal("1"), rounding=ROUND_HALF_UP) / 2

st.title("🎓 Calculateur de Maturité")
st.write("Entrez vos moyennes de semestre et vos notes d'examen.")

# --- BRANCHES MATURITÉ ---
def section_maturite(nom):
    with st.expander(f"📚 {nom}", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            s1 = st.number_input(f"{nom} - Sem 1", 1.0, 6.0, 4.0, 0.1, key=f"s1{nom}")
            s2 = st.number_input(f"{nom} - Sem 2", 1.0, 6.0, 4.0, 0.1, key=f"s2{nom}")
        with col2:
            ecr = st.number_input(f"{nom} - Écrit", 1.0, 6.0, 4.0, 0.1, key=f"e{nom}")
            ora = st.number_input(f"{nom} - Oral", 1.0, 6.0, 4.0, 0.1, key=f"o{nom}")
        
        ann = round_01((Decimal(str(s1)) + Decimal(str(s2))) / 2)
        finale = round_05((2 * ann + Decimal(str(ecr)) + Decimal(str(ora))) / 4)
        return finale

note_fr = section_maturite("Français")
note_ma = section_maturite("Mathématiques")
note_al = section_maturite("Allemand")
note_an = section_maturite("Anglais")

# --- BRANCHE ÉCONOMIE ---
with st.expander("💰 Économie (Compta + Éco Po)", expanded=True):
    st.subheader("Comptabilité")
    c1, c2 = st.columns(2)
    s1_c = c1.number_input("Compta Sem 1", 1.0, 6.0, 4.0, 0.1)
    s2_c = c2.number_input("Compta Sem 2", 1.0, 6.0, 4.0, 0.1)
    ecr_c = st.number_input("Compta Note Écrit", 1.0, 6.0, 4.0, 0.1)
    
    st.subheader("Économie Politique")
    e1, e2 = st.columns(2)
    s1_e = e1.number_input("Éco Po Sem 1", 1.0, 6.0, 4.0, 0.1)
    s2_e = e2.number_input("Éco Po Sem 2", 1.0, 6.0, 4.0, 0.1)
    ora_e = st.number_input("Éco Po Note Oral", 1.0, 6.0, 4.0, 0.1)

    ann_c = round_01((Decimal(str(s1_c)) + Decimal(str(s2_c))) / 2)
    note_compta = round_01((ann_c + Decimal(str(ecr_c))) / 2)
    
    ann_e = round_01((Decimal(str(s1_e)) + Decimal(str(s2_e))) / 2)
    note_ecopo = round_01((ann_e + Decimal(str(ora_e))) / 2)
    
    note_eco_finale = round_05((3 * note_compta + 2 * note_ecopo) / 5)

# --- RÉSULTATS FINAUX ---
st.divider()
st.header("🏆 Vos Notes Finales")
res = st.columns(5)
res[0].metric("Français", f"{note_fr}")
res[1].metric("Maths", f"{note_ma}")
res[2].metric("Allemand", f"{note_al}")
res[3].metric("Anglais", f"{note_an}")
res[4].metric("Économie", f"{note_eco_finale}")
