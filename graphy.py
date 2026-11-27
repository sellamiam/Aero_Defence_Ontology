from rdflib import Graph
import glob

g = Graph()

# Load all country TTL files in exports into one unified graph
for ttl_file in glob.glob("/Users/mohamedsellamia/projects/Aero_Defence_Ontology/data/exports/*.ttl"):
    g.parse(ttl_file, format="turtle")

print(f"Unified graph loaded: {len(g)} triples\n")

# Example 1: Cross-border supply chain links (who supplies whom across countries)
supply_query = """
PREFIX aero: <https://w3id.org/aerospace-defence#>

SELECT DISTINCT ?supplierName ?supplierCountry ?buyerName ?buyerCountry
WHERE {
    ?supplier aero:suppliesTo ?buyer ;
              aero:legalName ?supplierName ;
              aero:headquartersCountry ?supplierCountry .
    ?buyer aero:legalName ?buyerName ;
           aero:headquartersCountry ?buyerCountry .
    FILTER(?supplierCountry != ?buyerCountry)
}
LIMIT 15
"""

print("=== CROSS-BORDER SUPPLIER LINKS ===")
for row in g.query(supply_query):
    print(f"{row.supplierName} ({row.supplierCountry}) --> {row.buyerName} ({row.buyerCountry})")

# Example 2: Products by NSN/FSC code, critical material dependency, and target platform
product_query = """
PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?companyName ?country ?prodLabel ?nsn ?matLabel ?platLabel
WHERE {
    ?company aero:manufacturesProduct ?prod ;
             aero:legalName ?companyName ;
             aero:headquartersCountry ?country .
    ?prod rdfs:label ?prodLabel .
    OPTIONAL { ?prod aero:nsnCode ?nsn . }
    OPTIONAL {
        ?prod aero:dependsOnMaterial ?mat .
        ?mat rdfs:label ?matLabel .
    }
    OPTIONAL {
        ?prod aero:deployedOnPlatform ?plat .
        ?plat rdfs:label ?platLabel .
    }
    FILTER(BOUND(?matLabel) && BOUND(?platLabel))
}
LIMIT 15
"""

print("\n=== PRODUCTS WITH CRITICAL MATERIALS & PLATFORMS ===")
for row in g.query(product_query):
    print(f"{row.companyName} ({row.country}) | {row.prodLabel} [NSN: {row.nsn}] | Material: {row.matLabel} | Platform: {row.platLabel}")