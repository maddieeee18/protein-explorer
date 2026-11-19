
import streamlit as st
from viewer import show_protein_structure

st.set_page_config(
    page_title="Protein Explorer",
    page_icon="🧬",
    layout="wide"
)

st.title("🧬 Protein Explorer")

st.write(
    "Protein Structure Fetcher, "
    "Interactive Viewer and Domain Identifier"
)

st.divider()

accession = st.text_input(
    "Enter UniProt Accession Number",
    placeholder="Example: P36888"
)

if st.button("Explore Protein"):
    if accession.strip():
        st.success(
            f"Searching for protein: {accession.strip()}"
        )
    else:
        st.warning("Please enter a UniProt accession number.")

st.divider()

st.caption("Developed by Medha and Ananya")
st.subheader("Interactive 3D Protein Viewer")

pdb_id = st.text_input(
    "Enter a PDB ID",
    placeholder="Example: 1UBQ"
)

if st.button("View 3D Structure"):
    if pdb_id.strip():
        show_protein_structure(pdb_id)
    else:
        st.warning("Please enter a PDB ID.")