#!/usr/bin/env python3
"""
Interactive SPARQL Query Runner for Standalone Aerospace & Defence Knowledge Graph Files.
Allows querying any .ttl file (or master file) from the command line or running presets.
"""

import sys
import argparse
from pathlib import Path
import pyoxigraph

# Prefixes automatically included
PREFIXES = """
PREFIX aero: <https://w3id.org/aerospace-defence#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
"""


def load_graph(ttl_path: Path) -> pyoxigraph.Store:
    print(f"Loading '{ttl_path.name}' into Oxigraph engine...", file=sys.stderr)
    store = pyoxigraph.Store()
    with open(ttl_path, "rb") as f:
        store.load(f, "text/turtle")
    print(f"Loaded {len(store):,} triples successfully.", file=sys.stderr)
    return store


def format_table(results: list, headers: list) -> str:
    if not results:
        return "No results found."

    # Compute column widths
    widths = {h: len(h) for h in headers}
    rows = []
    for r in results:
        row = {}
        for h in headers:
            try:
                term = r[h]
                val = term.value if term is not None else ""
            except (KeyError, IndexError):
                val = ""
            # Strip namespace if long URI
            if "https://w3id.org/aerospace-defence#" in val:
                val = val.replace("https://w3id.org/aerospace-defence#", "aero:")
            widths[h] = max(widths[h], min(len(val), 60))
            row[h] = val
        rows.append(row)

    # Build header
    header_line = " | ".join(f"{h:<{widths[h]}}" for h in headers)
    separator = "-+-".join("-" * widths[h] for h in headers)
    
    # Build rows
    output_lines = [header_line, separator]
    for row in rows:
        line = " | ".join(f"{row[h]:<{widths[h]}}" for h in headers)
        output_lines.append(line)

    return "\n".join(output_lines)


def main():
    parser = argparse.ArgumentParser(description="Query Standalone .ttl Aerospace & Defence Knowledge Graph")
    parser.add_argument("--file", "-f", type=str, default=str(Path.home() / "Desktop" / "Aero_Defence_Global_Supply_Chain_Ontology.ttl"),
                        help="Path to Turtle (.ttl) file (defaults to Desktop master)")
    parser.add_argument("--query", "-q", type=str, help="Custom SPARQL query string")
    parser.add_argument("--query-file", type=str, help="Path to .rq SPARQL query file")
    parser.add_argument("--preset", "-p", choices=["competence", "platform", "services", "dossier"],
                        help="Run built-in simulation preset")
    parser.add_argument("--country", "-c", type=str, default="CAN", help="Target country filter for presets (e.g. CAN, GBR, FRA, AUS, NZL, IND)")
    parser.add_argument("--kic", type=str, default="KIC_AdvancedMaterials", help="KIC identifier for competence preset")
    parser.add_argument("--platform", type=str, default="Platform_F35_Lightning_II", help="Platform identifier for platform preset")
    parser.add_argument("--cage", type=str, default="L2391", help="CAGE code for dossier preset")
    parser.add_argument("--limit", "-l", type=int, default=15, help="Result limit")

    args = parser.parse_args()
    ttl_file = Path(args.file).resolve()
    if not ttl_file.exists():
        print(f"Error: Cannot find file {ttl_file}", file=sys.stderr)
        sys.exit(1)

    store = load_graph(ttl_file)

    if args.preset == "competence":
        q = f"""
        {PREFIXES}
        SELECT ?companyName ?cageCode ?tier ?city ?capTitle ?trl
        WHERE {{
            ?company aero:legalName ?companyName ;
                     aero:headquartersCountry "{args.country}" ;
                     aero:hasCapability ?cap .
            OPTIONAL {{ ?company aero:cageCode ?cageCode . }}
            OPTIONAL {{ ?company aero:headquartersCity ?city . }}
            OPTIONAL {{
                ?company a ?tierType .
                FILTER (?tierType IN (aero:PrimeContractor, aero:Tier1Supplier, aero:Tier2Supplier, aero:SMESupplier))
                BIND(STRAFTER(STR(?tierType), "#") AS ?tier)
            }}
            ?cap rdfs:label ?capTitle ;
                 aero:alignedWithKIC aero:{args.kic} ;
                 aero:trlValue ?trl .
            FILTER (?trl >= 8)
        }}
        ORDER BY DESC(?trl) ?companyName
        LIMIT {args.limit}
        """
        headers = ["companyName", "cageCode", "tier", "city", "capTitle", "trl"]

    elif args.preset == "platform":
        q = f"""
        {PREFIXES}
        SELECT DISTINCT ?companyName ?cageCode ?city ?productName ?partNumber ?fscCode
        WHERE {{
            ?company aero:legalName ?companyName ;
                     aero:headquartersCountry "{args.country}" ;
                     aero:manufacturesProduct ?product .
            OPTIONAL {{ ?company aero:cageCode ?cageCode . }}
            OPTIONAL {{ ?company aero:headquartersCity ?city . }}
            ?product rdfs:label ?productName ;
                     aero:deployedOnPlatform aero:{args.platform} .
            OPTIONAL {{ ?product aero:partNumber ?partNumber . }}
            OPTIONAL {{ ?product aero:fscCode ?fscCode . }}
        }}
        ORDER BY ?companyName ?productName
        LIMIT {args.limit}
        """
        headers = ["companyName", "cageCode", "city", "productName", "partNumber", "fscCode"]

    elif args.preset == "services":
        q = f"""
        {PREFIXES}
        SELECT DISTINCT ?companyName ?city ?serviceType ?serviceName ?accreditation
        WHERE {{
            ?company aero:legalName ?companyName ;
                     aero:headquartersCountry "{args.country}" ;
                     aero:providesService ?service .
            OPTIONAL {{ ?company aero:headquartersCity ?city . }}
            ?service a ?sClass ;
                     rdfs:label ?serviceName .
            FILTER (?sClass IN (aero:MROService, aero:TestingQualificationService, aero:EngineeringService, aero:SimulationTrainingService, aero:LogisticsSupportService, aero:CyberSecurityService))
            BIND(STRAFTER(STR(?sClass), "#") AS ?serviceType)
            OPTIONAL {{ ?service aero:serviceAccreditation ?accreditation . }}
        }}
        ORDER BY ?companyName ?serviceName
        LIMIT {args.limit}
        """
        headers = ["companyName", "city", "serviceType", "serviceName", "accreditation"]

    elif args.preset == "dossier":
        q = f"""
        {PREFIXES}
        SELECT ?companyName ?country ?city ?website ?clearance
        WHERE {{
            ?company aero:cageCode "{args.cage}" ;
                     aero:legalName ?companyName ;
                     aero:headquartersCountry ?country .
            OPTIONAL {{ ?company aero:headquartersCity ?city . }}
            OPTIONAL {{ ?company aero:website ?website . }}
            OPTIONAL {{ ?company aero:facilitySecurityClearance ?clearance . }}
        }}
        """
        headers = ["companyName", "country", "city", "website", "clearance"]

    elif args.query_file:
        q = Path(args.query_file).read_text(encoding="utf-8")
        headers = None
    elif args.query:
        q = args.query
        headers = None
    else:
        # Default query: Top 10 companies and their capabilities
        q = f"""
        {PREFIXES}
        SELECT ?companyName ?country ?city ?capTitle ?trl
        WHERE {{
            ?company aero:legalName ?companyName ;
                     aero:headquartersCountry ?country ;
                     aero:hasCapability ?cap .
            OPTIONAL {{ ?company aero:headquartersCity ?city . }}
            ?cap rdfs:label ?capTitle ;
                 aero:trlValue ?trl .
        }}
        LIMIT {args.limit}
        """
        headers = ["companyName", "country", "city", "capTitle", "trl"]

    # Execute query
    results = list(store.query(q))
    if not results:
        print("0 results returned.")
        return

    if headers is None:
        # Infer headers from keys in first solution
        # pyoxigraph solution doesn't have keys directly; let's inspect the solution
        sample = results[0]
        # QuerySolution can be mapped to variables by running a regex on query or accessing binding names
        import re
        var_match = re.search(r"SELECT\s+(DISTINCT\s+)?([^\sWHERE\{]+)", q, re.IGNORECASE)
        if var_match:
            vars_raw = var_match.group(2).strip().split()
            headers = [v.replace("?", "") for v in vars_raw if v.startswith("?")]
        else:
            headers = ["Result"]

    print(f"\nReturned {len(results)} rows:\n")
    print(format_table(results, headers))


if __name__ == "__main__":
    main()
