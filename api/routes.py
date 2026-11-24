"""
API Routes for Aerospace & Defence Ontology & Matching Engine.
"""

from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, Query, Body
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from matching.models import MatchingCriteria, MatchResponse
from matching.engine import MatchingEngine
from matching.consortium import ConsortiumEngine, ConsortiumProposal
from analytics.dossier import ExecutiveDossierGenerator
from store.graph_store import GraphStore
from api.dashboard import DASHBOARD_HTML

router = APIRouter()

# Global engine and store instances
_engine: Optional[MatchingEngine] = None
_graph_store: Optional[GraphStore] = None
_consortium_engine: Optional[ConsortiumEngine] = None
_dossier_gen: Optional[ExecutiveDossierGenerator] = None


def get_engine() -> MatchingEngine:
    global _engine
    if _engine is None:
        _engine = MatchingEngine()
    return _engine


def get_graph_store() -> GraphStore:
    global _graph_store
    if _graph_store is None:
        _graph_store = GraphStore()
        if len(_graph_store.store) == 0:
            _graph_store.build_and_populate()
    return _graph_store


def get_consortium_engine() -> ConsortiumEngine:
    global _consortium_engine
    if _consortium_engine is None:
        _consortium_engine = ConsortiumEngine(matching_engine=get_engine(), graph_store=get_graph_store())
    return _consortium_engine


def get_dossier_generator() -> ExecutiveDossierGenerator:
    global _dossier_gen
    if _dossier_gen is None:
        _dossier_gen = ExecutiveDossierGenerator(graph_store=get_graph_store())
    return _dossier_gen


class SPARQLRequest(BaseModel):
    query: str


class ConsortiumRequest(BaseModel):
    program_title: str
    required_capabilities: List[str]
    target_country: str = "CAN"
    require_cgp: bool = True


@router.get("/dashboard", response_class=HTMLResponse, summary="Executive Command Dashboard")
def get_dashboard():
    """Serves the interactive C-Suite Visual Graph Explorer & Procurement Command Center."""
    return HTMLResponse(content=DASHBOARD_HTML, status_code=200)


@router.post("/match", response_model=MatchResponse, summary="Execute Hybrid Procurement Match")
def execute_match(criteria: MatchingCriteria):
    """
    Evaluates suppliers against an RFP query and multi-criteria filters:
    combines semantic vector similarity, certification compliance, TRL thresholds,
    and geographic/offset constraints with zero leaks.
    """
    engine = get_engine()
    try:
        return engine.match(criteria)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/consortium", response_model=ConsortiumProposal, summary="Assemble Teaming Consortium")
def assemble_consortium_endpoint(req: ConsortiumRequest):
    """
    Assembles a strategic Prime + Tier-1 + SME teaming consortium for major defence procurements,
    maximizing capability coverage and Canadian ITB Offset multipliers.
    """
    c_engine = get_consortium_engine()
    try:
        return c_engine.assemble_consortium(
            program_title=req.program_title,
            required_capabilities=req.required_capabilities,
            target_country=req.target_country,
            require_cgp=req.require_cgp,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dossier/{cage_code}", summary="Generate Strategic Intelligence Dossier")
def get_dossier_endpoint(cage_code: str):
    """Generates an executive C-Suite strategic intelligence dossier for a defence contractor by CAGE or Company Name."""
    d_gen = get_dossier_generator()
    store = get_graph_store()
    clean_id = cage_code.strip()
    
    # 1. Try direct CAGE code
    try:
        return d_gen.generate_dossier(clean_id.upper())
    except ValueError:
        pass

    # 2. Try lookup by company name
    q_lower = clean_id.lower()
    sparql = f"""
        PREFIX aero: <https://w3id.org/aerospace-defence#>
        SELECT ?cage WHERE {{
            ?c aero:cageCode ?cage ;
               aero:legalName ?name .
            FILTER(CONTAINS(LCASE(?name), "{q_lower}"))
        }} LIMIT 1
    """
    rows = store.query_sparql(sparql)
    if rows:
        try:
            return d_gen.generate_dossier(rows[0]["cage"])
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    raise HTTPException(status_code=404, detail=f"Contractor with CAGE or Name '{clean_id}' not found.")


@router.get("/companies", summary="Search Companies by Name or CAGE")
def search_companies(q: Optional[str] = None, limit: int = 25):
    """Search companies by legal name, trade name, or CAGE code."""
    store = get_graph_store()
    if not q:
        sparql = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            SELECT ?cage ?name ?city ?province ?country WHERE {{
                ?c aero:cageCode ?cage ;
                   aero:legalName ?name ;
                   aero:headquartersCountry ?country .
                OPTIONAL {{ ?c aero:headquartersCity ?city . }}
                OPTIONAL {{ ?c aero:headquartersProvince ?province . }}
            }} LIMIT {limit}
        """
    else:
        q_clean = q.replace('"', '\\"').lower()
        sparql = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            SELECT ?cage ?name ?city ?province ?country WHERE {{
                ?c aero:cageCode ?cage ;
                   aero:legalName ?name ;
                   aero:headquartersCountry ?country .
                OPTIONAL {{ ?c aero:headquartersCity ?city . }}
                OPTIONAL {{ ?c aero:headquartersProvince ?province . }}
                FILTER(CONTAINS(LCASE(?name), "{q_clean}") || CONTAINS(LCASE(?cage), "{q_clean}"))
            }} LIMIT {limit}
        """
    rows = store.query_sparql(sparql)
    return {"companies": rows}


@router.get("/companies/{cage_code}", summary="Get 360-degree Company Profile")
def get_company(cage_code: str):
    """Returns the full knowledge graph profile for a company by CAGE/NCAGE code or Company Name."""
    store = get_graph_store()
    clean_id = cage_code.strip()
    
    # 1. Direct CAGE code lookup
    profile = store.get_company_profile(clean_id.upper())
    if profile:
        return profile
        
    # 2. Company Name search fallback
    q_lower = clean_id.lower()
    sparql = f"""
        PREFIX aero: <https://w3id.org/aerospace-defence#>
        SELECT ?cage WHERE {{
            ?c aero:cageCode ?cage ;
               aero:legalName ?name .
            FILTER(CONTAINS(LCASE(?name), "{q_lower}"))
        }} LIMIT 1
    """
    rows = store.query_sparql(sparql)
    if rows:
        profile = store.get_company_profile(rows[0]["cage"])
        if profile:
            return profile

    raise HTTPException(status_code=404, detail=f"Company with CAGE or Name '{clean_id}' not found.")


@router.get("/graph/subgraph", summary="Fetch Dynamic Knowledge Graph Subgraph")
def get_graph_subgraph(
    cage: Optional[str] = Query(None, description="Focus on a specific company by CAGE"),
    country: Optional[str] = Query(None, description="Filter by country (e.g. CAN, GBR, FRA, DEU, EU, ALL)"),
    mode: str = Query("ecosystem", description="Graph perspective: ecosystem, company, tier, platform"),
    limit: int = Query(60, description="Max entities to load"),
):
    """
    Returns rich, dynamic graph nodes and edges from the Oxigraph triplestore
    for Vis.js network rendering with high-tech styling.
    """
    store = get_graph_store()
    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []
    node_ids = set()

    def add_node(nid: str, label: str, group: str, shape: str, size: int, color_bg: str, color_border: str, title: str, **kwargs):
        if nid not in node_ids:
            node_ids.add(nid)
            node = {
                "id": nid,
                "label": label,
                "group": group,
                "shape": shape,
                "size": size,
                "color": {
                    "background": color_bg,
                    "border": color_border,
                    "highlight": {"background": color_border, "border": "#ffffff"},
                    "hover": {"background": color_border, "border": "#ffffff"}
                },
                "borderWidth": 2,
                "title": title,
                "font": {"color": "#ffffff", "face": "Inter", "size": 11, "strokeWidth": 2, "strokeColor": "#070a10"}
            }
            node.update(kwargs)
            nodes.append(node)

    def add_edge(src: str, dst: str, label: str, color: str = "#64748b", dashes: bool = False, width: float = 1.5):
        if src in node_ids and dst in node_ids:
            edges.append({
                "from": src,
                "to": dst,
                "label": label,
                "color": {"color": color, "highlight": "#38bdf8", "hover": "#38bdf8"},
                "arrows": {"to": {"enabled": True, "scaleFactor": 0.6}},
                "dashes": dashes,
                "width": width,
                "font": {"color": "#94a3b8", "size": 9, "align": "middle", "strokeWidth": 2, "strokeColor": "#070a10"}
            })

    # If CAGE or company mode
    if cage and isinstance(cage, str):
        clean_cage = cage.strip().upper()
        # Find company
        q_comp = f"""
        PREFIX aero: <https://w3id.org/aerospace-defence#>
        SELECT ?c ?name ?tier ?city ?province ?country WHERE {{
            ?c aero:cageCode "{clean_cage}" ;
               aero:legalName ?name ;
               aero:headquartersCountry ?country .
            OPTIONAL {{ ?c aero:headquartersCity ?city . }}
            OPTIONAL {{ ?c aero:headquartersProvince ?province . }}
            OPTIONAL {{
                ?c a ?t .
                FILTER(?t IN (aero:PrimeContractor, aero:Tier1Supplier, aero:Tier2Supplier, aero:SMESupplier))
                BIND(STRAFTER(STR(?t), "#") AS ?tier)
            }}
        }} LIMIT 1
        """
        comp_rows = store.query_sparql(q_comp)
        if comp_rows:
            c = comp_rows[0]
            cid = f"comp_{clean_cage}"
            tier = c.get("tier", "PrimeContractor")
            tier_col = "#00f2fe" if "Prime" in tier else ("#10b981" if "Tier1" in tier else "#f59e0b")
            add_node(
                cid, c["name"], "anchor", "dot", 34, tier_col, "#ffffff",
                f"<b>{c['name']}</b><br>CAGE: {clean_cage}<br>HQ: {c.get('city', '')}, {c.get('country', '')}<br>Tier: {tier}",
                cage=clean_cage, tier=tier, country=c.get("country", "CAN"), borderWidth=3
            )

            # Capabilities
            q_caps = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?cap ?title ?trl WHERE {{
                ?c aero:cageCode "{clean_cage}" ;
                   aero:hasCapability ?cap .
                ?cap rdfs:label ?title .
                OPTIONAL {{ ?cap aero:trlValue ?trl . }}
            }} LIMIT 6
            """
            for idx, cap in enumerate(store.query_sparql(q_caps)):
                cap_id = f"cap_{clean_cage}_{idx}"
                trl = cap.get("trl", "9")
                add_node(
                    cap_id, f"TRL{trl}: {cap['title'][:25]}", "capability", "diamond", 15, "#ec4899", "#f472b6",
                    f"<b>Capability</b>: {cap['title']}<br>Readiness Level: TRL {trl}"
                )
                add_edge(cid, cap_id, "hasCapability", "#ec4899")

            # Products & Deployed Platforms
            q_prods = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            SELECT ?p ?title ?partNo ?plat ?platTitle WHERE {{
                ?c aero:cageCode "{clean_cage}" ;
                   aero:manufacturesProduct ?p .
                ?p rdfs:label ?title .
                OPTIONAL {{ ?p aero:partNumber ?partNo . }}
                OPTIONAL {{
                    ?p aero:deployedOnPlatform ?plat .
                    ?plat rdfs:label ?platTitle .
                }}
            }} LIMIT 6
            """
            for idx, prod in enumerate(store.query_sparql(q_prods)):
                pid = f"prod_{clean_cage}_{idx}"
                add_node(
                    pid, prod["title"][:22], "product", "box", 14, "#3b82f6", "#60a5fa",
                    f"<b>Product</b>: {prod['title']}<br>Part No: {prod.get('partNo', 'N/A')}"
                )
                add_edge(cid, pid, "manufactures", "#3b82f6")

                if prod.get("plat") and prod.get("platTitle"):
                    plat_id = f"plat_{prod['plat'].split('#')[-1]}"
                    add_node(
                        plat_id, f"✈ {prod['platTitle'][:24]}", "platform", "hexagon", 24, "#a855f7", "#c084fc",
                        f"<b>Platform</b>: {prod['platTitle']}"
                    )
                    add_edge(pid, plat_id, "deployedOn", "#a855f7", width=2.0)

            # Subsidiaries / Corporate ties
            q_subs = f"""
            PREFIX aero: <https://w3id.org/aerospace-defence#>
            SELECT ?parentName ?cage ?rel WHERE {{
                {{
                    <{c['c']}> aero:subsidiaryOf ?p .
                    ?p aero:legalName ?parentName .
                    OPTIONAL {{ ?p aero:cageCode ?cage . }}
                    BIND("subsidiaryOf" AS ?rel)
                }} UNION {{
                    <{c['c']}> aero:hasSubsidiary ?p .
                    ?p aero:legalName ?parentName .
                    OPTIONAL {{ ?p aero:cageCode ?cage . }}
                    BIND("hasSubsidiary" AS ?rel)
                }}
            }} LIMIT 4
            """
            for idx, sub in enumerate(store.query_sparql(q_subs)):
                sub_cage = sub.get("cage") or f"sub_{clean_cage}_{idx}"
                sub_id = f"comp_{sub_cage}"
                add_node(
                    sub_id, sub["parentName"], "subsidiary", "dot", 20, "#6366f1", "#818cf8",
                    f"<b>Corporate Affiliation</b>: {sub['parentName']}",
                    cage=sub.get("cage", "")
                )
                if sub["rel"] == "subsidiaryOf":
                    add_edge(cid, sub_id, "subsidiaryOf", "#6366f1")
                else:
                    add_edge(cid, sub_id, "hasSubsidiary", "#6366f1")

            return {
                "nodes": nodes,
                "edges": edges,
                "stats": {
                    "total_nodes": len(nodes),
                    "total_edges": len(edges),
                    "mode": "company",
                    "focused_cage": clean_cage,
                    "focused_name": c["name"]
                }
            }

    # Otherwise: Ecosystem, Tier, or Platform mode
    country_filter = ""
    if country and isinstance(country, str) and country.upper() != "ALL":
        if country.upper() == "EU":
            country_filter = 'FILTER(?country IN ("FRA", "DEU", "ITA", "ESP", "NLD", "SWE", "BEL"))'
        else:
            country_filter = f'FILTER(?country = "{country.upper()}")'

    if isinstance(mode, str) and mode == "platform":
        q_plat = f"""
        PREFIX aero: <https://w3id.org/aerospace-defence#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?plat ?platName ?comp ?compName ?cage ?country ?tier WHERE {{
            ?comp aero:legalName ?compName ;
                  aero:cageCode ?cage ;
                  aero:headquartersCountry ?country ;
                  aero:manufacturesProduct ?p .
            {country_filter}
            ?p aero:deployedOnPlatform ?plat .
            ?plat rdfs:label ?platName .
            OPTIONAL {{
                ?comp a ?t .
                FILTER(?t IN (aero:PrimeContractor, aero:Tier1Supplier, aero:Tier2Supplier, aero:SMESupplier))
                BIND(STRAFTER(STR(?t), "#") AS ?tier)
            }}
        }} ORDER BY ?platName LIMIT {limit}
        """
        rows = store.query_sparql(q_plat)
        for r in rows:
            plat_id = f"plat_{r['plat'].split('#')[-1]}"
            add_node(
                plat_id, f"✈ {r['platName'][:24]}", "platform", "hexagon", 26, "#a855f7", "#c084fc",
                f"<b>Platform</b>: {r['platName']}"
            )
            cid = f"comp_{r['cage']}"
            tier = r.get("tier", "Tier1Supplier")
            tier_col = "#00f2fe" if "Prime" in tier else ("#10b981" if "Tier1" in tier else "#f59e0b")
            add_node(
                cid, r["compName"], "supplier", "dot", 18, tier_col, "#ffffff",
                f"<b>{r['compName']}</b><br>CAGE: {r['cage']}<br>Country: {r['country']}<br>Tier: {tier}",
                cage=r["cage"], tier=tier, country=r["country"]
            )
            add_edge(cid, plat_id, "deployedOn", "#a855f7", width=1.5)

    else:
        # Ecosystem or Tier mode: load balanced network of Primes, Tier 1s, and Platforms
        q_eco = f"""
        PREFIX aero: <https://w3id.org/aerospace-defence#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

        SELECT DISTINCT ?comp ?name ?cage ?country ?tier ?city ?plat ?platName WHERE {{
            ?comp aero:legalName ?name ;
                  aero:cageCode ?cage ;
                  aero:headquartersCountry ?country .
            {country_filter}
            OPTIONAL {{ ?comp aero:headquartersCity ?city . }}
            OPTIONAL {{
                ?comp a ?t .
                FILTER(?t IN (aero:PrimeContractor, aero:Tier1Supplier, aero:Tier2Supplier, aero:SMESupplier))
                BIND(STRAFTER(STR(?t), "#") AS ?tier)
            }}
            OPTIONAL {{
                ?comp aero:manufacturesProduct ?p .
                ?p aero:deployedOnPlatform ?plat .
                ?plat rdfs:label ?platName .
            }}
        }} LIMIT {limit}
        """
        rows = store.query_sparql(q_eco)

        # First collect companies
        comp_platform_map = {}
        for r in rows:
            cid = f"comp_{r['cage']}"
            tier = r.get("tier", "Tier1Supplier")
            is_prime = "Prime" in tier
            is_tier1 = "Tier1" in tier
            size = 28 if is_prime else (21 if is_tier1 else 16)
            tier_col = "#00f2fe" if is_prime else ("#10b981" if is_tier1 else "#f59e0b")
            add_node(
                cid, r["name"], "company", "dot", size, tier_col, "#ffffff",
                f"<b>{r['name']}</b><br>CAGE: {r['cage']}<br>HQ: {r.get('city', '')}, {r['country']}<br>Tier: {tier}",
                cage=r["cage"], tier=tier, country=r["country"], borderWidth=2
            )
            if r.get("plat") and r.get("platName"):
                plat_id = f"plat_{r['plat'].split('#')[-1]}"
                add_node(
                    plat_id, f"✈ {r['platName'][:22]}", "platform", "hexagon", 24, "#a855f7", "#c084fc",
                    f"<b>Platform</b>: {r['platName']}"
                )
                add_edge(cid, plat_id, "deployedOn", "#a855f7", width=1.5)
                comp_platform_map[cid] = plat_id

        # Add multi-tier supply chain linkages: connect Tier-1s to Primes sharing the same platform or cluster
        primes = [n for n in nodes if n.get("tier") == "PrimeContractor"]
        tier1s = [n for n in nodes if n.get("tier") == "Tier1Supplier"]
        for t1 in tier1s:
            t1_plat = comp_platform_map.get(t1["id"])
            for p in primes:
                p_plat = comp_platform_map.get(p["id"])
                if t1_plat and p_plat and t1_plat == p_plat and t1["id"] != p["id"]:
                    add_edge(t1["id"], p["id"], "suppliesTo", "#00f2fe", dashes=True, width=2.0)
                    break

        # Also pull corporate subsidiaries
        q_corp = """
        PREFIX aero: <https://w3id.org/aerospace-defence#>
        SELECT ?subName ?subCage ?parentName ?parentCage WHERE {
            ?sub aero:subsidiaryOf ?parent .
            ?sub aero:legalName ?subName ; aero:cageCode ?subCage .
            ?parent aero:legalName ?parentName ; aero:cageCode ?parentCage .
        } LIMIT 10
        """
        for c_rel in store.query_sparql(q_corp):
            sub_id = f"comp_{c_rel['subCage']}"
            parent_id = f"comp_{c_rel['parentCage']}"
            if sub_id in node_ids and parent_id in node_ids:
                add_edge(sub_id, parent_id, "subsidiaryOf", "#6366f1", width=2.0)

    return {
        "nodes": nodes,
        "edges": edges,
        "stats": {
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "mode": mode if isinstance(mode, str) else "ecosystem",
            "country": country if isinstance(country, str) else "ALL"
        }
    }


@router.post("/sparql", summary="Execute Raw SPARQL 1.1 Query")
def execute_sparql(req: SPARQLRequest):
    """Executes an arbitrary SPARQL 1.1 query directly against the Oxigraph triplestore."""
    store = get_graph_store()
    try:
        results = store.query_sparql(req.query)
        return {"query": req.query, "row_count": len(results), "results": results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"SPARQL error: {str(e)}")


@router.get("/taxonomies/kics", summary="List Canadian Key Industrial Capabilities")
def list_kics():
    """Returns official Canadian Key Industrial Capabilities with registered supplier counts."""
    store = get_graph_store()
    sparql = """
        PREFIX aero: <https://w3id.org/aerospace-defence#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

        SELECT ?kic ?label ?definition (COUNT(DISTINCT ?c) AS ?supplierCount) WHERE {
            ?kic a aero:KeyIndustrialCapability ;
                 skos:prefLabel ?label .
            OPTIONAL { ?kic skos:definition ?definition . }
            OPTIONAL {
                ?c aero:hasCapability ?cap .
                ?cap aero:alignedWithKIC ?kic .
            }
        } GROUP BY ?kic ?label ?definition ORDER BY DESC(?supplierCount)
    """
    return {"kics": store.query_sparql(sparql)}


@router.get("/stats", summary="Get Ontology Graph Statistics")
def get_graph_statistics():
    """Returns high-level graph metrics and entity distributions across Canada, UK, and EU."""
    store = get_graph_store()
    sparql = """
        PREFIX aero: <https://w3id.org/aerospace-defence#>
        SELECT ?country (COUNT(DISTINCT ?c) AS ?count) WHERE {
            ?c a aero:Company ;
               aero:headquartersCountry ?country .
        } GROUP BY ?country ORDER BY DESC(?count)
    """
    country_dist = store.query_sparql(sparql)
    return {
        "total_triples": len(store.store),
        "companies_by_country": country_dist,
        "supported_standards": [
            "AS9100D",
            "ISO 9001:2015",
            "Controlled Goods Program (Canada)",
            "NATO AQAP 2110",
            "Cyber Essentials Plus (UK)",
            "NADCAP (Composites, NDT, Chemical)",
        ],
    }


@router.get("/health", summary="Service Health Check")
def health_check():
    store = get_graph_store()
    return {
        "status": "healthy",
        "triplestore_triples": len(store.store),
        "version": "2.0.0",
    }
