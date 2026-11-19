import requests


# ==========================================
# MEMBER 2 - PROTEIN DOMAIN IDENTIFICATION
# ==========================================

# Function 1: Fetch protein data from UniProt

def get_protein_data(accession):

    accession = accession.strip().upper()

    if not accession:
        raise ValueError("Please enter a UniProt accession number.")

    url = f"https://rest.uniprot.org/uniprotkb/{accession}.json"

    try:
        response = requests.get(url, timeout=30)

        if response.status_code == 404:
            raise ValueError("Protein accession not found.")

        response.raise_for_status()

        protein_data = response.json()

        return protein_data

    except requests.RequestException as error:
        raise RuntimeError(
            "Unable to retrieve protein data from UniProt."
        ) from error


# Function 2: Get basic protein information

def get_protein_summary(protein):

    accession = protein.get(
        "primaryAccession", "Not available"
    )

    description = protein.get("proteinDescription") or {}

    recommended = description.get("recommendedName") or {}

    protein_name = (
        recommended.get("fullName") or {}
    ).get("value")

    if not protein_name:
        submitted = description.get("submissionNames") or []

        if submitted:
            protein_name = (
                submitted[0].get("fullName") or {}
            ).get("value")

    if not protein_name:
        protein_name = "Not available"

    genes = protein.get("genes") or []

    gene_name = "Not available"

    if genes:
        gene_name = (
            genes[0].get("geneName") or {}
        ).get("value", "Not available")

    organism = (
        protein.get("organism") or {}
    ).get("scientificName", "Not available")

    sequence_length = (
        protein.get("sequence") or {}
    ).get("length", "Not available")

    return {
        "accession": accession,
        "name": protein_name,
        "gene": gene_name,
        "organism": organism,
        "length": sequence_length
    }


# Function 3: Identify protein domains

def get_domains(protein):

    domains = []

    features = protein.get("features") or []

    for feature in features:

        feature_type = feature.get("type", "")

        if feature_type.lower() == "domain":

            domain_name = feature.get(
                "description", "Unnamed domain"
            )

            location = feature.get("location") or {}

            start = (
                location.get("start") or {}
            ).get("value", "Unknown")

            end = (
                location.get("end") or {}
            ).get("value", "Unknown")

            domain = {
                "Domain Name": domain_name,
                "Start Position": start,
                "End Position": end
            }

            domains.append(domain)

    return domains


# Function 4: Display protein information

def show_protein_information(summary):

    print("\n========== PROTEIN INFORMATION ==========")

    print("Accession:", summary["accession"])
    print("Protein Name:", summary["name"])
    print("Gene:", summary["gene"])
    print("Organism:", summary["organism"])
    print("Sequence Length:", summary["length"])


# Function 5: Display identified domains

def show_domains(domains):

    print("\n========== PROTEIN DOMAINS ==========")

    if not domains:
        print("No annotated protein domains found.")
        return

    for number, domain in enumerate(domains, start=1):

        print("\nDomain", number)

        print("Name:", domain["Domain Name"])

        print(
            "Start Position:",
            domain["Start Position"]
        )

        print(
            "End Position:",
            domain["End Position"]
        )


# Main program for independent testing

def main():

    print("======================================")
    print("     PROTEIN DOMAIN IDENTIFIER")
    print("======================================")

    accession = input(
        "Enter UniProt accession (example P36888): "
    )

    try:

        protein = get_protein_data(accession)

        summary = get_protein_summary(protein)

        domains = get_domains(protein)

        show_protein_information(summary)

        show_domains(domains)

        print("\nDomain identification completed.")

    except (ValueError, RuntimeError) as error:

        print("Error:", error)


if __name__ == "__main__":
    main()
    