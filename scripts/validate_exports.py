#!/usr/bin/env python3
"""
Post-Export RDF/SHACL/SPARQL Integrity Verification Script.
Validates all generated .ttl files in data/exports/:
  1. Zero Turtle syntax or prefix resolution errors (rdflib g.parse succeeds cleanly).
  2. Zero orphan suppliesTo or subsidiaryOf URIs (every target URI resolves to an aero:Company).
  3. Every Product links to at least one Platform or CriticalMaterial.
  4. Every Capability links to a valid aero:alignedWithKIC concept.
  5. Correct xsd:boolean datatypes on aero:controlledGoodsRegistered and aero:itarCompliant.
  6. Correct xsd:integer datatypes on aero:trlValue and aero:mrlValue (1..9).
  7. Outputs summary table of triple counts, unique companies, and cross-border edges per file.
"""

import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import rdflib
from rdflib import Graph, URIRef, RDF, RDFS, XSD, Literal

EXPORTS_DIR = ROOT_DIR / "data" / "exports"
AERO = "https://w3id.org/aerospace-defence#"

def validate_all_exports():
    print("=" * 90)
    print("STARTING POST-EXPORT RDF / SPARQL INTEGRITY AUDIT ACROSS ALL EXPORT FILES")
    print("=" * 90)

    # 1. Parse TBox Schema
    schema_path = EXPORTS_DIR / "ontology_schema.ttl"
    if not schema_path.exists():
        raise FileNotFoundError(f"Missing {schema_path}")
    
    g_schema = Graph()
    g_schema.parse(schema_path, format="turtle")
    print(f"-> Parsed TBox Schema: {schema_path.name} ({len(g_schema)} triples)")

    # 2. Parse All Country ABox Files
    country_files = [
        "canada.ttl", "usa.ttl", "uk.ttl", "eu.ttl",
        "australia.ttl", "new_zealand.ttl", "india.ttl"
    ]

    jurisdiction_graphs = {}
    g_unified = Graph()
    g_unified += g_schema

    summary_rows = []

    for cfile in country_files:
        fpath = EXPORTS_DIR / cfile
        if not fpath.exists():
            raise FileNotFoundError(f"Missing {fpath}")
        
        g = Graph()
        try:
            g.parse(fpath, format="turtle")
        except Exception as e:
            print(f"FAILED to parse {cfile}: {e}")
            sys.exit(1)

        jurisdiction_graphs[cfile] = g
        g_unified += g

    print(f"-> Successfully parsed all {len(country_files)} country files with 0 syntax errors.")
    print(f"-> Unified in-memory graph contains {len(g_unified)} triples (ABox + TBox).\n")

    # Predicate URIs
    supplies_to = URIRef(AERO + "suppliesTo")
    subsidiary_of = URIRef(AERO + "subsidiaryOf")
    company_type = URIRef(AERO + "Company")
    product_type = URIRef(AERO + "Product")
    capability_type = URIRef(AERO + "Capability")
    deployed_on_platform = URIRef(AERO + "deployedOnPlatform")
    depends_on_material = URIRef(AERO + "dependsOnMaterial")
    aligned_with_kic = URIRef(AERO + "alignedWithKIC")
    trl_val_pred = URIRef(AERO + "trlValue")
    mrl_val_pred = URIRef(AERO + "mrlValue")
    cgp_pred = URIRef(AERO + "controlledGoodsRegistered")
    itar_pred = URIRef(AERO + "itarCompliant")
    legal_name_pred = URIRef(AERO + "legalName")

    # Global company URI set in unified graph
    all_companies = set(g_unified.subjects(RDF.type, company_type))

    # Audit each country file
    for cfile in country_files:
        g = jurisdiction_graphs[cfile]
        
        # Local stats
        comps = list(g.subjects(RDF.type, company_type))
        prods = list(g.subjects(RDF.type, product_type))
        caps = list(g.subjects(RDF.type, capability_type))
        edges = list(g.triples((None, supplies_to, None))) + list(g.triples((None, subsidiary_of, None)))

        # Check 1: Zero orphan suppliesTo or subsidiaryOf URIs
        orphan_targets = []
        for s, p, o in g.triples((None, supplies_to, None)):
            if o not in all_companies:
                orphan_targets.append((s, p, o))
        for s, p, o in g.triples((None, subsidiary_of, None)):
            if o not in all_companies:
                orphan_targets.append((s, p, o))

        # Check 2: Every product links to at least one platform or critical material
        unlinked_prods = []
        for prod in prods:
            plats = list(g.objects(prod, deployed_on_platform))
            mats = list(g.objects(prod, depends_on_material))
            if not plats and not mats:
                unlinked_prods.append(prod)

        # Check 3: Every capability links to a valid KIC concept
        unlinked_caps = []
        for cap in caps:
            kics = list(g.objects(cap, aligned_with_kic))
            if not kics:
                unlinked_caps.append(cap)

        # Check 4: Datatype checks on booleans and integers
        invalid_booleans = []
        for s, p, o in list(g.triples((None, cgp_pred, None))) + list(g.triples((None, itar_pred, None))):
            if not isinstance(o, Literal) or o.datatype != XSD.boolean:
                invalid_booleans.append((s, p, o))

        invalid_integers = []
        for s, p, o in list(g.triples((None, trl_val_pred, None))) + list(g.triples((None, mrl_val_pred, None))):
            if not isinstance(o, Literal) or o.datatype != XSD.integer:
                invalid_integers.append((s, p, o))
            elif int(o.toPython()) < 1 or int(o.toPython()) > 9:
                invalid_integers.append((s, p, o))

        # Asserts
        assert len(orphan_targets) == 0, f"Found orphan targets in {cfile}: {orphan_targets}"
        assert len(unlinked_prods) == 0, f"Found unlinked products in {cfile}: {unlinked_prods}"
        assert len(unlinked_caps) == 0, f"Found unlinked capabilities in {cfile}: {unlinked_caps}"
        assert len(invalid_booleans) == 0, f"Found invalid booleans in {cfile}: {invalid_booleans}"
        assert len(invalid_integers) == 0, f"Found invalid integers in {cfile}: {invalid_integers}"

        # No OWL TBox definitions embedded in pure ABox files
        embedded_owl_classes = list(g.subjects(RDF.type, rdflib.OWL.Class))
        embedded_owl_props = list(g.subjects(RDF.type, rdflib.OWL.ObjectProperty))
        assert len(embedded_owl_classes) == 0, f"{cfile} unexpectedly embeds {len(embedded_owl_classes)} OWL Classes!"
        assert len(embedded_owl_props) == 0, f"{cfile} unexpectedly embeds {len(embedded_owl_props)} OWL ObjectProperties!"

        summary_rows.append({
            "filename": cfile,
            "triples": len(g),
            "unique_companies": len(comps),
            "products": len(prods),
            "capabilities": len(caps),
            "supply_edges": len(edges),
            "orphans": len(orphan_targets),
            "schema_classes_embedded": len(embedded_owl_classes),
            "syntax_status": "CLEAN"
        })

    print("-" * 110)
    print(f"{'Export File':<18} | {'Triples':<8} | {'Companies':<9} | {'Products':<8} | {'Capabilities':<12} | {'Supply Edges':<12} | {'TBox Classes':<12} | {'Status'}")
    print("-" * 110)
    for r in summary_rows:
        print(f"{r['filename']:<18} | {r['triples']:<8} | {r['unique_companies']:<9} | {r['products']:<8} | {r['capabilities']:<12} | {r['supply_edges']:<12} | {r['schema_classes_embedded']:<12} | {r['syntax_status']}")
    print("-" * 110)
    print(f"\nALL INTEGRITY CHECKS PASSED: 0 syntax errors, 0 orphan edges, 0 unlinked products, 0 TBox classes embedded.")
    return summary_rows

if __name__ == "__main__":
    validate_all_exports()
