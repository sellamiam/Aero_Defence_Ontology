import csv
import glob
from rdflib import Graph

g = Graph()

# Load all country/market TTL files (and schema if present in exports) into one unified graph
ttl_files = sorted(glob.glob("/Users/mohamedsellamia/projects/Aero_Defence_Ontology/data/exports/*.ttl"))
for ttl_file in ttl_files:
    g.parse(ttl_file, format="turtle")

print(f"Loaded {len(ttl_files)} files | Unified graph: {len(g)} triples\n")

# Full details for every company across all markets, including products and services
company_details_query = """
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
    (GROUP_CONCAT(DISTINCT STR(?domainName); separator=" | ") AS ?Domains)
    (GROUP_CONCAT(DISTINCT STR(?certName); separator=" | ") AS ?Certifications)
    (GROUP_CONCAT(DISTINCT STR(?capLabel); separator=" | ") AS ?Capabilities)
    (GROUP_CONCAT(DISTINCT STR(?prodLabel); separator=" | ") AS ?Products)
    (GROUP_CONCAT(DISTINCT STR(?servLabel); separator=" | ") AS ?Services)
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
    
    OPTIONAL { 
        ?company aero:operatesInDomain ?domain .
        BIND(REPLACE(STR(?domain), "https://w3id.org/aerospace-defence#", "") AS ?domainName)
    }
    
    OPTIONAL { 
        ?company aero:holdsCertification ?cert .
        OPTIONAL { ?cert rdfs:label ?certLabelRaw . }
        BIND(COALESCE(?certLabelRaw, REPLACE(STR(?cert), "https://w3id.org/aerospace-defence#", "")) AS ?certName)
    }
    
    OPTIONAL { 
        ?company aero:hasCapability ?cap .
        ?cap rdfs:label ?capLabel .
    }
    
    OPTIONAL { 
        ?company aero:manufacturesProduct ?prod .
        ?prod rdfs:label ?prodLabel .
    }
    
    OPTIONAL { 
        ?company aero:providesService ?serv .
        ?serv rdfs:label ?servLabel .
    }

    # Filter out unharvested placeholder/stub nodes (buyers, parent stubs, generic sectors)
    # A genuine verified enterprise must have at least one verified property (CAGE code, City, Website, Product, or Service)
    FILTER(
        BOUND(?cageCode) ||
        BOUND(?city) ||
        BOUND(?website) ||
        BOUND(?prodLabel) ||
        BOUND(?servLabel)
    )
}
GROUP BY ?company
ORDER BY ?Country ?Legal_Name
"""

results = list(g.query(company_details_query))
print(f"=== ALL COMPANIES ACROSS ALL MARKETS ({len(results)} enterprises) ===\n")

# Print first 10 rows as a console sanity check
for row in results[:10]:
    print(f"{row.Legal_Name} ({row.Country}) | Tier: {row.Supplier_Tiers or 'N/A'} | CAGE: {row.CAGE_Code or 'N/A'}")
    print(f"  Products: {row.Products or 'None'}")
    print(f"  Services: {row.Services or 'None'}\n")

# Export all rows to CSV for full inspection
output_csv = "/Users/mohamedsellamia/projects/Aero_Defence_Ontology/all_companies_full_details.csv"
headers = [
    "URI", "Legal_Name", "Trade_Name", "Supplier_Tiers", "CAGE_Code", "DUNS",
    "Business_Number", "City", "Province_State", "Country", "Website",
    "Security_Clearance", "CGP_Registered", "ITAR_Compliant", "Domains",
    "Certifications", "Capabilities", "Products", "Services"
]

with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(headers)
    for row in results:
        writer.writerow([str(val) if val is not None else "" for val in row])

print(f"Saved complete multi-market company dataset to: {output_csv}")
