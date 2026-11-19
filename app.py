
import streamlit as st
from viewer import show_protein_structure
from structures import find_pdb_structures

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
    if not accession.strip():
        st.warning("Please enter a UniProt accession number.")
    else:
        with st.spinner("Searching for PDB structures..."):
            try:
                pdb_ids = find_pdb_structures(accession)

                if pdb_ids:
                    st.session_state["pdb_results"] = pdb_ids
                    st.success(
                        f"Found {len(pdb_ids)} PDB structures!"
                    )
                else:
                    st.session_state["pdb_results"] = []
                    st.info("No matching PDB structures found.")

            except (ValueError, RuntimeError) as error:
                st.session_state["pdb_results"] = []
                st.error(str(error))

if "pdb_results" in st.session_state:
    pdb_ids = st.session_state["pdb_results"]

    if pdb_ids:
        selected_pdb = st.selectbox(
            "Choose a PDB structure",
            pdb_ids
        )

        st.link_button(
            "View on RCSB PDB",
            f"https://www.rcsb.org/structure/{selected_pdb}"
        )

        if st.button("Display Selected Structure"):
            show_protein_structure(selected_pdb)


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