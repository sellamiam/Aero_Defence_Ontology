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
