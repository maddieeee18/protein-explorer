
import streamlit as st
import streamlit.components.v1 as components
import py3Dmol
import requests


def show_protein_structure(pdb_id):
    """Fetch and display an interactive PDB structure."""

    pdb_id = pdb_id.strip().upper()

    if not pdb_id.isalnum() or len(pdb_id) != 4:
        st.error("Please enter a valid 4-character PDB ID.")
        return

    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"

    try:
        response = requests.get(url, timeout=20)
        response.raise_for_status()

        viewer = py3Dmol.view(width=800, height=500)
        viewer.addModel(response.text, "pdb")
        viewer.setStyle({"cartoon": {"color": "spectrum"}})
        viewer.setBackgroundColor("#101827")
        viewer.zoomTo()

        components.html(
            viewer._make_html(),
            height=520,
            scrolling=False
        )

        st.download_button(
            "Download PDB Structure",
            data=response.content,
            file_name=f"{pdb_id}.pdb",
            mime="chemical/x-pdb"
        )

    except requests.RequestException:
        st.error(
            "Could not retrieve this structure from RCSB PDB."
        )
        
