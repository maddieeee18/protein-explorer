
import streamlit as st

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
