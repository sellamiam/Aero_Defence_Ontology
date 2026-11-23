"""
Graph Store Engine.
Powered by pyoxigraph (high-performance Rust SPARQL 1.1 triplestore) with RDFLib interoperability.
Supports disk persistence, SPARQL querying, graph traversals, and Neo4j Cypher export.
"""

from typing import List, Dict, Any, Optional
from pathlib import Path
import pyoxigraph
from pyoxigraph import Store, RdfFormat
import logging

logger = logging.getLogger("GraphStore")


class GraphStore:
    """Manages the Oxigraph RDF triplestore and provides SPARQL 1.1 execution."""

    _shared_stores: Dict[str, Store] = {}

    def __init__(self, db_path: Optional[Path] = None, data_dir: Optional[Path] = None):
        self.workspace_root = Path(__file__).resolve().parent.parent
        self.data_dir = data_dir or (self.workspace_root / "data")
        self.db_path = db_path or (self.data_dir / "graph" / "oxigraph_db")
        self.db_path.parent.mkdir(parents=True, exist_ok=True)

        key = str(self.db_path)
        if key not in GraphStore._shared_stores:
            try:
                GraphStore._shared_stores[key] = Store(key)
            except OSError:
                logger.info(f"Read-write lock busy; opening read-only Store connection to {key}...")
                GraphStore._shared_stores[key] = Store.read_only(key)
        self.store = GraphStore._shared_stores[key]

    def build_and_populate(self) -> Dict[str, Any]:
        """Loads all schemas, taxonomies, and extracted instance graphs into Oxigraph."""
        logger.info("Populating Oxigraph store from RDF files...")
        self.store.clear()
        ontology_dir = self.workspace_root / "ontology"
        processed_dir = self.data_dir / "processed"

        # Load Schema and Taxonomies (N-Triples or Turtle)
        schema_files = [
            ontology_dir / "schema.ttl",
            ontology_dir / "taxonomy" / "canadian_kics.ttl",
            ontology_dir / "taxonomy" / "platforms.ttl",
            ontology_dir / "standards.ttl",
        ]
        for sf in schema_files:
            if sf.exists():
                try:
                    with open(sf, "rb") as f:
                        self.store.load(f, RdfFormat.TURTLE)
                except Exception as e:
                    logger.warning(f"Could not load {sf.name} into Oxigraph: {e}")

        # Load Processed Instance Graph
        nt_file = processed_dir / "knowledge_graph.nt"
        if not nt_file.exists():
            from pipeline.extractor import RDFTripleExtractor
            extractor = RDFTripleExtractor(data_dir=self.data_dir)
            g = extractor.build_rdf_graph()
            extractor.export_graph(g)

        if nt_file.exists():
            with open(nt_file, "rb") as f:
                self.store.load(f, RdfFormat.N_TRIPLES)

        total_triples = len(self.store)

        # Count total companies and capabilities in graph
        company_count_query = """
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            SELECT (COUNT(DISTINCT ?c) AS ?count) WHERE {
                ?c a aero:Company .
            }
        """
        res = list(self.store.query(company_count_query))
        company_count = int(res[0]["count"].value) if res else 0

        logger.info(f"Oxigraph store loaded. Total Triples: {total_triples}, Unique Companies: {company_count}")
        return {
            "total_triples": total_triples,
            "total_entities": company_count,
            "db_path": str(self.db_path),
        }

    def query_sparql(self, sparql: str) -> List[Dict[str, Any]]:
        """Executes a SPARQL 1.1 query and returns rows as dictionaries with clean string values."""
        results = []
        try:
            query_res = self.store.query(sparql)
            if hasattr(query_res, "variables"):
                variables = query_res.variables
                for row in query_res:
                    row_dict = {}
                    for var in variables:
                        val = row[var]
                        if val is not None:
                            row_dict[var.value] = val.value if hasattr(val, "value") else str(val)
                    results.append(row_dict)
            else:
                return [{"result": bool(query_res)}]
        except Exception as e:
            logger.error(f"SPARQL execution error: {e}")
            raise
        return results

    def get_company_profile(self, cage_code: str) -> Optional[Dict[str, Any]]:
        """Retrieves comprehensive 360-degree company profile from graph using CAGE code."""
        query = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?c ?legalName ?tradeName ?country ?province ?city ?website ?cgp ?itar ?tier ?parentName
            WHERE {{
                ?c aero:cageCode "{cage_code}" ;
                   aero:legalName ?legalName ;
                   aero:headquartersCountry ?country ;
                   aero:headquartersCity ?city .
                OPTIONAL {{ ?c aero:headquartersProvince ?province . }}
                OPTIONAL {{ ?c aero:tradeName ?tradeName . }}
                OPTIONAL {{ ?c aero:website ?website . }}
                OPTIONAL {{ ?c aero:controlledGoodsRegistered ?cgp . }}
                OPTIONAL {{ ?c aero:itarCompliant ?itar . }}
                OPTIONAL {{ ?c a ?tier . FILTER(?tier != aero:Company && ?tier != aero:Organization) }}
                OPTIONAL {{ ?c aero:subsidiaryOf ?parent . ?parent aero:legalName ?parentName . }}
            }} LIMIT 1
        """
        rows = self.query_sparql(query)
        if not rows:
            return None

        base = rows[0]
        comp_uri = base["c"]

        # Fetch certifications
        certs_q = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?certName WHERE {{
                <{comp_uri}> aero:holdsCertification ?cert .
                OPTIONAL {{ ?cert rdfs:label ?certName . }}
            }}
        """
        certs = [r.get("certName") or r.get("cert") for r in self.query_sparql(certs_q)]

        # Fetch capabilities
        caps_q = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?title ?desc ?trl ?kic WHERE {{
                <{comp_uri}> aero:hasCapability ?cap .
                ?cap rdfs:label ?title ;
                     aero:capabilityDescription ?desc .
                OPTIONAL {{ ?cap aero:trlValue ?trl . }}
                OPTIONAL {{ ?cap aero:alignedWithKIC ?kic . }}
            }}
        """
        caps = self.query_sparql(caps_q)

        # Fetch products
        prods_q = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?pName WHERE {{
                <{comp_uri}> aero:manufacturesProduct ?p .
                ?p rdfs:label ?pName .
            }}
        """
        prods = [r["pName"] for r in self.query_sparql(prods_q)]

        # Fetch services
        servs_q = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?sName WHERE {{
                <{comp_uri}> aero:providesService ?s .
                ?s rdfs:label ?sName .
            }}
        """
        services = [r["sName"] for r in self.query_sparql(servs_q)]

        # Fetch subsidiaries
        subs_q = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            SELECT ?subName ?subCage WHERE {{
                <{comp_uri}> aero:hasSubsidiary ?sub .
                ?sub aero:legalName ?subName ;
                     aero:cageCode ?subCage .
            }}
        """
        subs = self.query_sparql(subs_q)

        tier_val = base.get("tier", "").split("#")[-1] if base.get("tier") else "Company"

        return {
            "cage_code": cage_code,
            "legal_name": base["legalName"],
            "trade_name": base.get("tradeName"),
            "country": base["country"],
            "province": base.get("province"),
            "city": base["city"],
            "website": base.get("website"),
            "tier": tier_val,
            "controlled_goods": str(base.get("cgp", "")).lower() == "true",
            "itar_compliant": str(base.get("itar", "")).lower() == "true",
            "parent_company": base.get("parentName"),
            "subsidiaries": subs,
            "certifications": [c for c in certs if c],
            "capabilities": caps,
            "products": prods,
            "services": services,
        }

    def export_neo4j_cypher(self, output_path: Optional[Path] = None) -> Path:
        """Generates a Cypher (.cyp) script to import the graph into Neo4j."""
        target = output_path or (self.data_dir / "graph" / "neo4j_import.cyp")
        target.parent.mkdir(parents=True, exist_ok=True)

        logger.info(f"Generating Neo4j Cypher import script at {target}...")
        cypher_lines = [
            "// Neo4j Cypher Script for Aerospace & Defence Knowledge Graph",
            "CREATE CONSTRAINT company_cage IF NOT EXISTS FOR (c:Company) REQUIRE c.cage_code IS UNIQUE;",
            "CREATE CONSTRAINT capability_id IF NOT EXISTS FOR (cap:Capability) REQUIRE cap.id IS UNIQUE;",
        ]

        # Extract companies
        comps = self.query_sparql("""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            SELECT ?cage ?name ?country ?city ?tier WHERE {
                ?c aero:cageCode ?cage ;
                   aero:legalName ?name ;
                   aero:headquartersCountry ?country ;
                   aero:headquartersCity ?city .
                OPTIONAL { ?c a ?tier . FILTER(?tier != aero:Company && ?tier != aero:Organization) }
            }
        """)
        for c in comps:
            name_esc = c['name'].replace("'", "\\'")
            cypher_lines.append(
                f"MERGE (c:Company {{cage_code: '{c['cage']}'}}) "
                f"SET c.name = '{name_esc}', c.country = '{c['country']}', c.city = '{c['city']}';"
            )

        with open(target, "w", encoding="utf-8") as f:
            f.write("\n".join(cypher_lines))
        return target
