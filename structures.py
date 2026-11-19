
import requests


def find_pdb_structures(accession):
    """Find experimental PDB entries for a UniProt accession."""

    accession = accession.strip().upper()

    if not accession:
        raise ValueError("Enter a UniProt accession number.")

    url = "https://search.rcsb.org/rcsbsearch/v2/query"

    query = {
        "query": {
            "type": "terminal",
            "service": "text",
            "parameters": {
                "attribute": (
                    "rcsb_polymer_entity_container_identifiers."
                    "reference_sequence_identifiers.database_accession"
                ),
                "operator": "exact_match",
                "value": accession
            }
        },
        "return_type": "entry",
        "request_options": {
            "paginate": {
                "start": 0,
                "rows": 20
            }
        }
    }

    try:
        response = requests.post(
            url,
            json=query,
            timeout=30
        )

        if response.status_code == 204:
            return []

        response.raise_for_status()

        results = response.json().get("result_set", [])

        pdb_ids = []

        for result in results:
            pdb_id = result.get("identifier")

            if pdb_id and pdb_id not in pdb_ids:
                pdb_ids.append(pdb_id)

        return pdb_ids

    except requests.RequestException as error:
        raise RuntimeError(
            "Could not connect to the RCSB PDB database."
        ) from error
