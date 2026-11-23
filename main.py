#!/usr/bin/env python3
"""
Aerospace & Defence Ontology & Matching Engine - Unified Command Line Interface.
"""

import sys
import argparse
import json
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("AeroDefenceCLI")


def cmd_run_swarm(args):
    """Executes the multi-agent swarm pipeline."""
    from swarm.orchestrator import SwarmOrchestrator
    orchestrator = SwarmOrchestrator()
    limit = args.limit if hasattr(args, "limit") else None
    results = orchestrator.run_full_pipeline(limit_per_region=limit)
    print("\n" + "=" * 60)
    print("SWARM PIPELINE EXECUTION SUMMARY")
    print("=" * 60)
    print(f"Status: {results['status'].upper()}")
    print(f"Total Duration: {results['total_duration_sec']}s")
    print(f"Canada Records: {results['summary_metrics']['canada_records']}")
    print(f"EU & UK Records: {results['summary_metrics']['eu_uk_records']}")
    print(f"Companies Resolved: {results['summary_metrics']['companies_resolved']}")
    print(f"Total Triples in Graph: {results['summary_metrics']['total_triples']}")
    print(f"Vectors Indexed: {results['summary_metrics']['vectors_indexed']}")
    print(f"Evaluation Benchmarks Passed: {results['summary_metrics']['benchmarks_passed']}")
    print("=" * 60)


def cmd_match(args):
    """Executes a capability matching query."""
    from matching.engine import MatchingEngine
    from matching.models import MatchingCriteria

    engine = MatchingEngine()
    criteria = MatchingCriteria(
        query_text=args.query,
        required_country=args.country,
        required_certifications=args.certs.split(",") if args.certs else [],
        require_controlled_goods=args.cgp,
        require_itar_compliant=args.itar,
        min_trl=args.min_trl,
        top_k=args.top_k,
    )

    response = engine.match(criteria)
    print("\n" + "=" * 70)
    print(f"MATCH RESULTS FOR: '{args.query}'")
    if response.parsed_intent:
        pi = response.parsed_intent
        geo_str = f"{pi.get('target_country') or 'ANY'}"
        if pi.get("target_region"):
            geo_str += f" ({pi.get('target_region')})"
        print(f"Intent Parsed: Target Geo={geo_str} | Cleaned='{pi.get('cleaned_query')}'")
    print(f"Confidence: {response.confidence_summary}")
    print(f"Total candidates evaluated: {response.total_matches_found} | Latency: {response.execution_time_ms}ms")
    print("=" * 70)

    if not response.top_matches:
        print("\n[NO MATCHES FOUND] No suppliers met the strict criteria and geographic filters.\n")
    else:
        for m in response.top_matches:
            prov_str = f", {m.province}" if m.province else ""
            print(f"\n[Rank #{m.rank} | {m.confidence_level}] {m.legal_name} ({m.city}{prov_str}, {m.country})")
            print(f"  CAGE: {m.cage_code} | Tier: {m.tier} | CGP: {m.controlled_goods}")
            print(f"  Overall Score: {m.overall_score:.4f} (Semantic: {m.breakdown.semantic_score}, Cert: {m.breakdown.certification_score}, TRL: {m.breakdown.trl_score}, Geo: {m.breakdown.geographic_score})")
            print(f"  Active Weights: {m.breakdown.active_weights}")
            if m.matched_capability_title:
                print(f"  Matched Capability: {m.matched_capability_title}")
            print(f"  Justification: {m.justification}")
    print("\n" + "=" * 70)


def cmd_consortium(args):
    """Assembles a strategic prime + SME teaming consortium."""
    from matching.consortium import ConsortiumEngine
    c_engine = ConsortiumEngine()
    wps = [w.strip() for w in args.caps.split(",") if w.strip()]
    proposal = c_engine.assemble_consortium(
        program_title=args.title,
        required_capabilities=wps,
        target_country=args.country,
        require_cgp=not args.no_cgp,
    )

    print("\n" + "=" * 70)
    print(f"STRATEGIC CONSORTIUM PROPOSAL: {proposal.program_title.upper()}")
    print("=" * 70)
    print(f"Work-Package Coverage: {proposal.capability_coverage_pct}% | Canadian Content: {proposal.estimated_canadian_content_value}%")
    print(f"ITB Policy Multiplier Rating: {proposal.total_itb_multiplier_score}x")
    print(f"Compliance Posture: {proposal.compliance_summary}")
    print("\n[LEAD PRIME CONTRACTOR]")
    lp = proposal.lead_prime
    prov_str = f", {lp.province}" if lp.province else ""
    print(f"  {lp.legal_name} ({lp.city}{prov_str}, {lp.country}) - CAGE: {lp.cage_code}")
    print(f"  Role: {lp.role} | Clearance: {lp.security_clearance}")
    print(f"  Primary Workshare: {', '.join(lp.assigned_capabilities)}")

    print("\n[STRATEGIC TEAMING PARTNERS & SMES]")
    for p in proposal.teaming_partners:
        prov_s = f", {p.province}" if p.province else ""
        print(f"  * {p.legal_name} ({p.city}{prov_s}, {p.country}) - CAGE: {p.cage_code}")
        print(f"    Role: {p.role} | Offset Multiplier: {p.itb_offset_multiplier}x")
        print(f"    Assigned Work-Packages: {', '.join(p.assigned_capabilities)}")

    print("\n[STRATEGIC RATIONALE]")
    print(f"  {proposal.strategic_rationale}")
    print("=" * 70 + "\n")


def cmd_dossier(args):
    """Generates an executive C-Suite strategic intelligence dossier."""
    from analytics.dossier import ExecutiveDossierGenerator
    d_gen = ExecutiveDossierGenerator()
    res = d_gen.generate_dossier(args.cage.upper())

    print("\n" + res["dossier_markdown"] + "\n")

    # Save to disk
    out_file = Path(f"data/dossier_{args.cage.upper()}.md")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(res["dossier_markdown"])
    print(f"[SUCCESS] Dossier saved to: {out_file}\n")


def cmd_profile(args):
    """Fetches full 360 profile of a company by CAGE code."""
    from store.graph_store import GraphStore
    store = GraphStore()
    if len(store.store) == 0:
        store.build_and_populate()
    profile = store.get_company_profile(args.cage.upper())
    if not profile:
        print(f"Error: Company with CAGE {args.cage} not found.")
        sys.exit(1)
    print(json.dumps(profile, indent=2))


def cmd_sparql(args):
    """Executes SPARQL query against Oxigraph triplestore."""
    from store.graph_store import GraphStore
    store = GraphStore()
    if len(store.store) == 0:
        store.build_and_populate()
    results = store.query_sparql(args.query)
    print(json.dumps(results, indent=2))


def cmd_benchmark(args):
    """Runs automated procurement evaluation benchmarks."""
    from matching.engine import MatchingEngine
    engine = MatchingEngine()
    bench = engine.run_benchmark_scenarios()
    print("\n" + "=" * 70)
    print("PROCUREMENT MATCHING ENGINE BENCHMARKS")
    print("=" * 70)
    for sc in bench["scenarios"]:
        status = "PASSED" if sc["passed"] else "FAILED"
        print(f"[{status}] {sc['name']}")
        print(f"  Top Match: {sc['top_matched_company']} (Expected any of: {sc['expected_any_of']})")
        print(f"  Latency: {sc['latency_ms']}ms\n")
    print("=" * 70)
    print(f"ALL SCENARIOS PASSED: {bench['all_passed']}")
    print("=" * 70)


def cmd_serve(args):
    """Starts the FastAPI web server."""
    import uvicorn
    print(f"Starting Aerospace & Defence Ontology API on http://{args.host}:{args.port}")
    uvicorn.run("api.main:app", host=args.host, port=args.port, reload=args.reload)


def main():
    parser = argparse.ArgumentParser(
        description="Aerospace & Defence Ontology & Matching Engine Orchestrator CLI"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # swarm
    swarm_p = subparsers.add_parser("run-swarm", help="Run multi-agent swarm pipeline")
    swarm_p.add_argument("--limit", type=int, default=None, help="Optional record limit per region")

    # match
    match_p = subparsers.add_parser("match", help="Execute procurement match query")
    match_p.add_argument("query", type=str, help="Capability / RFP query text")
    match_p.add_argument("--country", type=str, default=None, help="Target Country (CAN, GBR, FRA, DEU, etc.)")
    match_p.add_argument("--certs", type=str, default=None, help="Comma-separated certifications (e.g. AS9100D,CGP_Canada)")
    match_p.add_argument("--cgp", action="store_true", default=None, help="Require Canadian Controlled Goods")
    match_p.add_argument("--itar", action="store_true", default=None, help="Require ITAR compliance")
    match_p.add_argument("--min-trl", type=int, default=None, help="Minimum TRL (1-9)")
    match_p.add_argument("--top-k", type=int, default=5, help="Number of results")

    # consortium
    consortium_p = subparsers.add_parser("consortium", help="Assemble strategic prime + SME teaming consortium")
    consortium_p.add_argument("title", type=str, help="Defence program / RFP title")
    consortium_p.add_argument("--caps", type=str, required=True, help="Comma-separated required capabilities")
    consortium_p.add_argument("--country", type=str, default="CAN", help="Target country (default: CAN)")
    consortium_p.add_argument("--no-cgp", action="store_true", help="Disable mandatory Controlled Goods Program requirement")

    # dossier
    dossier_p = subparsers.add_parser("dossier", help="Generate executive strategic intelligence dossier")
    dossier_p.add_argument("cage", type=str, help="Contractor CAGE / NCAGE code")

    # profile
    prof_p = subparsers.add_parser("profile", help="Show 360-degree company profile")
    prof_p.add_argument("cage", type=str, help="CAGE / NCAGE code")

    # sparql
    sparql_p = subparsers.add_parser("sparql", help="Run SPARQL 1.1 query")
    sparql_p.add_argument("query", type=str, help="SPARQL query string")

    # benchmark
    subparsers.add_parser("benchmark", help="Run matching engine evaluation benchmarks")

    # serve
    serve_p = subparsers.add_parser("serve", help="Launch FastAPI web server")
    serve_p.add_argument("--host", type=str, default="127.0.0.1", help="Bind host")
    serve_p.add_argument("--port", type=int, default=8000, help="Bind port")
    serve_p.add_argument("--reload", action="store_true", help="Auto-reload on code change")

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmd_map = {
        "run-swarm": cmd_run_swarm,
        "match": cmd_match,
        "consortium": cmd_consortium,
        "dossier": cmd_dossier,
        "profile": cmd_profile,
        "sparql": cmd_sparql,
        "benchmark": cmd_benchmark,
        "serve": cmd_serve,
    }

    cmd_map[args.command](args)


if __name__ == "__main__":
    main()
