#!/usr/bin/env python3
"""
High-performance export and validation script for multi-market company dataset.
Parses the unified master ontology and generates all_companies_full_details.csv
without cartesian product slowdowns or unharvested placeholder stubs.
"""

import csv
import glob
import time
from collections import defaultdict
from pathlib import Path

try:
    import pyoxigraph
    USE_OXIGRAPH = True
except ImportError:
    import rdflib
    USE_OXIGRAPH = False

def run_graphy():
    t0 = time.time()
    export_dir = Path("/Users/mohamedsellamia/projects/Aero_Defence_Ontology/data/exports")
    master_file = export_dir / "Aero_Defence_Global_Supply_Chain_Ontology.ttl"
    
    if not master_file.exists():
        # Fall back to local path
        master_file = Path("data/exports/Aero_Defence_Global_Supply_Chain_Ontology.ttl")

    print(f"Loading master ontology from: {master_file}")
    
    store = pyoxigraph.Store()
    with open(master_file, "rb") as f:
        store.load(f, "text/turtle")
    
    print(f"Loaded {len(store)} triples in {time.time()-t0:.2f}s\n")

    # 1. Product mapping
    prod_map = defaultdict(list)
    for sol in store.query("""
    PREFIX aero: <https://w3id.org/aerospace-defence#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?company ?label WHERE {
        ?company aero:manufacturesProduct ?p .
        ?p rdfs:label ?label .
    }
    """):
        prod_map[sol["company"].value].append(sol["label"].value)

    # 2. Capability mapping
    cap_map = defaultdict(list)
    for sol in store.query("""
    PREFIX aero: <https://w3id.org/aerospace-defence#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?company ?label WHERE {
        ?company aero:hasCapability ?c .
        ?c rdfs:label ?label .
    }
    """):
        cap_map[sol["company"].value].append(sol["label"].value)

    # 3. Service mapping
    serv_map = defaultdict(list)
    for sol in store.query("""
    PREFIX aero: <https://w3id.org/aerospace-defence#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?company ?label WHERE {
        ?company aero:providesService ?s .
        ?s rdfs:label ?label .
    }
    """):
        serv_map[sol["company"].value].append(sol["label"].value)

    # 4. Domain mapping
    domain_map = defaultdict(set)
    for sol in store.query("""
    PREFIX aero: <https://w3id.org/aerospace-defence#>
    SELECT ?company ?d WHERE {
        ?company aero:operatesInDomain ?d .
    }
    """):
        domain_map[sol["company"].value].add(sol["d"].value.split("#")[-1])

    # 5. Certification mapping
    cert_map = defaultdict(set)
    for sol in store.query("""
    PREFIX aero: <https://w3id.org/aerospace-defence#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    SELECT ?company ?cert (SAMPLE(?lbl) AS ?label) WHERE {
        ?company aero:holdsCertification ?cert .
        OPTIONAL { ?cert rdfs:label ?lbl . }
    } GROUP BY ?company ?cert
    """):
        label = sol["label"].value if sol["label"] else sol["cert"].value.split("#")[-1]
        cert_map[sol["company"].value].add(label)

    # 6. Core company properties
    core_query = """
    PREFIX aero: <https://w3id.org/aerospace-defence#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT 
        ?company
        (SAMPLE(?legalName) AS ?Legal_Name)
        (SAMPLE(?tradeName) AS ?Trade_Name)
        (GROUP_CONCAT(DISTINCT REPLACE(STR(?tierType), "https://w3id.org/aerospace-defence#", ""); separator=" | ") AS ?Supplier_Tiers)
        (SAMPLE(?cageCode) AS ?CAGE_Code)
        (SAMPLE(?dunsNumber) AS ?DUNS)
        (SAMPLE(?businessNumber) AS ?Business_Number)
        (SAMPLE(?city) AS ?City)
        (SAMPLE(?province) AS ?Province_State)
        (SAMPLE(?country) AS ?Country)
        (SAMPLE(?website) AS ?Website)
        (SAMPLE(?clearance) AS ?Security_Clearance)
        (SAMPLE(?cgp) AS ?CGP_Registered)
        (SAMPLE(?itar) AS ?ITAR_Compliant)
    WHERE {
        ?company a aero:Company .
        OPTIONAL { ?company aero:legalName ?legalName . }
        OPTIONAL { ?company aero:tradeName ?tradeName . }
        OPTIONAL { 
            ?company a ?tierType . 
            FILTER(?tierType != aero:Company && ?tierType != <http://www.w3.org/ns/org#Organization>)
        }
        OPTIONAL { ?company aero:cageCode ?cageCode . }
        OPTIONAL { ?company aero:dunsNumber ?dunsNumber . }
        OPTIONAL { ?company aero:businessNumber ?businessNumber . }
        OPTIONAL { ?company aero:headquartersCity ?city . }
        OPTIONAL { ?company aero:headquartersProvince ?province . }
        OPTIONAL { ?company aero:headquartersCountry ?country . }
        OPTIONAL { ?company aero:website ?website . }
        OPTIONAL { ?company aero:facilitySecurityClearance ?clearance . }
        OPTIONAL { ?company aero:controlledGoodsRegistered ?cgp . }
        OPTIONAL { ?company aero:itarCompliant ?itar . }

        # Filter out unharvested placeholder/stub nodes (buyers, parent stubs, generic sectors)
        FILTER(
            BOUND(?cageCode) ||
            BOUND(?city) ||
            BOUND(?website)
        )
    }
    GROUP BY ?company
    ORDER BY ?Country ?Legal_Name
    """

    print("Querying core company entities...")
    companies = list(store.query(core_query))
    print(f"=== ALL VERIFIED COMPANIES ACROSS ALL MARKETS ({len(companies)} enterprises) ===\n")

    # Sample output
    for row in companies[:10]:
        c_uri = row["company"].value
        p_list = " | ".join(sorted(set(prod_map.get(c_uri, [])))) or "None"
        s_list = " | ".join(sorted(set(serv_map.get(c_uri, [])))) or "None"
        c_tier = row["Supplier_Tiers"].value if row["Supplier_Tiers"] else "N/A"
        c_cage = row["CAGE_Code"].value if row["CAGE_Code"] else "N/A"
        c_name = row["Legal_Name"].value if row["Legal_Name"] else "Unknown"
        c_country = row["Country"].value if row["Country"] else "N/A"
        print(f"{c_name} ({c_country}) | Tier: {c_tier} | CAGE: {c_cage}")
        print(f"  Products: {p_list[:120]}...")
        print(f"  Services: {s_list[:120]}...\n")

    output_csv = Path("/Users/mohamedsellamia/projects/Aero_Defence_Ontology/all_companies_full_details.csv")
    if not output_csv.parent.exists():
        output_csv = Path("all_companies_full_details.csv")

    headers = [
        "URI", "Legal_Name", "Trade_Name", "Supplier_Tiers", "CAGE_Code", "DUNS",
        "Business_Number", "City", "Province_State", "Country", "Website",
        "Security_Clearance", "CGP_Registered", "ITAR_Compliant", "Domains",
        "Certifications", "Capabilities", "Products", "Services"
    ]

    with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for row in companies:
            c_uri = row["company"].value
            val = lambda k: row[k].value if row[k] is not None else ""
            
            domains_str = " | ".join(sorted(domain_map.get(c_uri, [])))
            certs_str = " | ".join(sorted(cert_map.get(c_uri, [])))
            caps_str = " | ".join(sorted(set(cap_map.get(c_uri, []))))
            prods_str = " | ".join(sorted(set(prod_map.get(c_uri, []))))
            servs_str = " | ".join(sorted(set(serv_map.get(c_uri, []))))

            writer.writerow([
                c_uri,
                val("Legal_Name"),
                val("Trade_Name"),
                val("Supplier_Tiers"),
                val("CAGE_Code"),
                val("DUNS"),
                val("Business_Number"),
                val("City"),
                val("Province_State"),
                val("Country"),
                val("Website"),
                val("Security_Clearance"),
                val("CGP_Registered"),
                val("ITAR_Compliant"),
                domains_str,
                certs_str,
                caps_str,
                prods_str,
                servs_str,
            ])

    print(f"Saved complete multi-market company dataset to: {output_csv} in {time.time()-t0:.2f}s")

if __name__ == "__main__":
    run_graphy()
