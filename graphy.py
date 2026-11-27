from rdflib import Graph

g = Graph()
g.parse("/Users/mohamedsellamia/projects/Aero_Defence_Ontology/data/exports/canada.ttl", format="turtle")
print(f"Loaded {len(g)} triples")

query = """
PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT COUNT(DISTINCT ?companyName) ?cage ?city ?capLabel ?typeLabel
WHERE {
    ?company aero:legalName ?companyName ;
             aero:hasCapability ?cap .
    OPTIONAL { ?company aero:cageCode ?cage . }

    OPTIONAL { ?cap rdfs:label ?capLabel . }
    OPTIONAL {
        ?cap a ?capType .
        ?capType rdfs:label ?typeLabel .
    }
    FILTER(
        CONTAINS(LCASE(STR(COALESCE(?capLabel, ""))), "avionics") ||
        CONTAINS(LCASE(STR(COALESCE(?typeLabel, ""))), "avionics")
    )
}
LIMIT 20
"""

results = list(g.query(query))
print(f"Found {len(results)} matches\n")

for row in results:
    print(f"{row.companyName} ({row.cage}) - {row.city} | {row.capLabel or row.typeLabel}")
