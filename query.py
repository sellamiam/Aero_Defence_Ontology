from rdflib import Graph

g = Graph()
g.parse("/Users/mohamedsellamia/projects/Aero_Defence_Ontology/data/exports/canada.ttl", format="turtle")
print(f"Loaded {len(g)} triples")

query = """
PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?companyName ?cage ?city ?capability ?trl
WHERE {
    ?company aero:legalName ?companyName ;
             aero:hasCapability ?cap .
    ?cap rdfs:label ?capability .
    OPTIONAL { ?company aero:cageCode ?cage . }
    OPTIONAL { ?company aero:headquartersCity ?city . }
    OPTIONAL { ?cap aero:trlValue ?trl . }
    FILTER(CONTAINS(LCASE(STR(?capability)), "avionics"))
}
LIMIT 20
"""

results = list(g.query(query))
print(f"Found {len(results)} matches\n")

for row in results:
    city = row.city or "N/A"
    cage = row.cage or "N/A"
    trl = row.trl or "N/A"
    print(f"{row.companyName} ({cage}) - {city} | {row.capability} (TRL {trl})")