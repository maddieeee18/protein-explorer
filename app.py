
import streamlit as st
from viewer import show_protein_structure
from structures import find_pdb_structures
from domains import get_protein_data, get_protein_summary, get_domains

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


st.divider()

st.header("Protein Domain Identification")

domain_accession = st.text_input(
    "Enter UniProt accession for domain analysis",
    placeholder="Example: P36888",
    key="domain_search"
)

if st.button("Identify Domains"):

    if not domain_accession.strip():
        st.warning("Please enter a UniProt accession.")

    else:

        with st.spinner("Identifying protein domains..."):

            try:

                protein = get_protein_data(domain_accession)

                summary = get_protein_summary(protein)

                domains = get_domains(protein)

                st.success("Protein information retrieved!")

                st.subheader("Protein Information")

                st.write("**Accession:**", summary["accession"])
                st.write("**Protein Name:**", summary["name"])
                st.write("**Gene:**", summary["gene"])
                st.write("**Organism:**", summary["organism"])
                st.write(
                    "**Sequence Length:**",
                    summary["length"]
                )

                st.subheader("Identified Protein Domains")

                if domains:
                    st.dataframe(
                        domains,
                        use_container_width=True,
                        hide_index=True
                    )
                else:
                    st.info("No annotated domains found.")

            except (ValueError, RuntimeError) as error:
                st.error(str(error))
    