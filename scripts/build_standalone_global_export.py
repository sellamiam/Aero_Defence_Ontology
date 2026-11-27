#!/usr/bin/env python3
"""
Standalone Global Aerospace & Defence Supply Chain Knowledge Graph Exporter.
Coordinates harvesters across all 6 jurisdictions (Canada, UK, EU, Australia, New Zealand, India),
injects cross-tier supply chain linkages, embeds formal OWL 2 schemas, and exports:
  1. Standalone jurisdiction files: canada.ttl, uk.ttl, eu.ttl, australia.ttl, new_zealand.ttl, india.ttl
  2. Standalone global unified file: Aero_Defence_Global_Supply_Chain_Ontology.ttl
  3. Copies to /Users/mohamedsellamia/Desktop/ for instant access by William Langley.
"""

import sys
import os
import json
import shutil
import time
from pathlib import Path
from typing import List, Dict, Any
import logging

# Ensure project root is in python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

import rdflib
import pyoxigraph
from pipeline.extractor import RDFTripleExtractor
from harvesters.canada_harvester import CanadaHarvester
from harvesters.uk_harvester import UKHarvester
from harvesters.eu_harvester import EUHarvester
from harvesters.australia_harvester import AustraliaHarvester
from harvesters.nz_harvester import NewZealandHarvester
from harvesters.india_harvester import IndiaHarvester
from harvesters.usa_harvester import USAHarvester

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("GlobalExportBuilder")

DESKTOP_DIR = Path("/Users/mohamedsellamia/Desktop")
EXPORTS_DIR = ROOT_DIR / "data" / "exports"


def inject_cross_border_supply_chain_links(all_companies: List[Dict[str, Any]]) -> None:
    """
    Connects Tier 1/2 suppliers to major primes and platforms across international borders,
    enabling multi-hop graph traversal and supplier substitution in simulation frameworks.
    """
    name_to_comp = {c["legal_name"]: c for c in all_companies}

    # Cross-border supply chain mappings (Supplier -> List of Primes/Customers)
    linkages = [
        # F-35 Joint Strike Fighter Global Industrial Participation
        ("Magellan Aerospace Corporation", ["Bombardier Inc."]),
        ("Quickstep Holdings Limited", ["BAE Systems Australia Limited", "BAE Systems plc"]),
        ("Ferra Engineering Pty Ltd", ["BAE Systems Australia Limited"]),
        ("GKN Aerospace Services Limited", ["BAE Systems plc", "Airbus SE"]),
        ("Dynamatic Technologies Limited", ["Hindustan Aeronautics Limited"]),
        ("Tata Advanced Systems Limited", ["Hindustan Aeronautics Limited"]),
        ("Héroux-Devtek Inc.", ["Dassault Aviation SA", "Bombardier Inc."]),
        
        # Naval Type 26 / Canadian Surface Combatant / Hunter Frigate
        ("CEA Technologies Pty Ltd", ["BAE Systems Australia Limited"]),
        ("Ultra Electronics Maritime Systems Canada", ["BAE Systems plc"]),
        ("Marops Limited", ["Austal Limited"]),
        ("Zenith Tecnica Limited", ["Rocket Lab Limited"]),
        
        # Aeroengine Global Supply Chain
        ("Bharat Electronics Limited", ["Hindustan Aeronautics Limited"]),
        ("Tonbo Imaging India Private Limited", ["Bharat Dynamics Limited"]),
        ("Dawn Aerospace Limited", ["Rocket Lab Limited"]),
        ("Flightcell International Limited", ["Bell Textron Canada Ltd."]),

        # United States <-> Allied Cross-Border Supply Chain (F-35, P-8, Type 26, Space)
        ("Magellan Aerospace Corporation", ["Lockheed Martin Corporation", "RTX Corporation"]),
        ("Héroux-Devtek Inc.", ["The Boeing Company", "Lockheed Martin Corporation"]),
        ("Quickstep Holdings Limited", ["Lockheed Martin Corporation", "Northrop Grumman Corporation"]),
        ("Ferra Engineering Pty Ltd", ["The Boeing Company", "Lockheed Martin Corporation"]),
        ("GKN Aerospace Services Limited", ["Lockheed Martin Corporation", "The Boeing Company"]),
        ("Pratt & Whitney Canada Corp.", ["RTX Corporation", "The Boeing Company"]),
        ("General Dynamics Land Systems-Canada", ["General Dynamics Corporation"]),
        ("L3Harris MAS Inc.", ["L3Harris Technologies, Inc."]),
        ("CAE Inc.", ["CAE USA Inc.", "Lockheed Martin Corporation"]),
        ("Ultra Electronics Maritime Systems Canada", ["BAE Systems, Inc."]),
        ("Rocket Lab Limited", ["Rocket Lab USA, Inc."]),
    ]

    for supplier_name, prime_names in linkages:
        if supplier_name in name_to_comp:
            comp = name_to_comp[supplier_name]
            if "supplies_to" not in comp:
                comp["supplies_to"] = []
            for p in prime_names:
                if p in name_to_comp and p not in comp["supplies_to"]:
                    comp["supplies_to"].append(p)

    logger.info("Successfully established cross-border supply chain linkages.")


def main():
    start_time = time.time()
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)
    extractor = RDFTripleExtractor(data_dir=ROOT_DIR / "data")

    logger.info("=" * 80)
    logger.info("STARTING STANDALONE GLOBAL SUPPLY CHAIN ONTOLOGY EXPORT PIPELINE")
    logger.info("=" * 80)

    # 1. Harvest each jurisdiction
    harvesters_config = [
        ("Canada", CanadaHarvester(), 1000, "canada.ttl"),
        ("USA", USAHarvester(), None, "usa.ttl"),
        ("UK", UKHarvester(), 160, "uk.ttl"),
        ("EU", EUHarvester(), 220, "eu.ttl"),
        ("Australia", AustraliaHarvester(), 120, "australia.ttl"),
        ("NewZealand", NewZealandHarvester(), 60, "new_zealand.ttl"),
        ("India", IndiaHarvester(), 180, "india.ttl"),
    ]

    all_harvested_companies: List[Dict[str, Any]] = []
    jurisdiction_data: Dict[str, List[Dict[str, Any]]] = {}

    for name, harvester, target_count, ttl_filename in harvesters_config:
        logger.info(f"Harvesting {name} (target: {target_count} companies)...")
        records = harvester.harvest(limit=target_count)
        jurisdiction_data[name] = records
        all_harvested_companies.extend(records)
        logger.info(f"-> Harvested {len(records)} companies for {name}.")

    logger.info(f"Total companies harvested across all 6 jurisdictions: {len(all_harvested_companies)}")

    # 2. Inject cross-border supply chain links
    inject_cross_border_supply_chain_links(all_harvested_companies)

    # 3. Export separate jurisdiction files
    export_summary = []
    logger.info("-" * 80)
    logger.info("SERIALIZING STANDALONE JURISDICTION TURTLE (.TTL) FILES")
    logger.info("-" * 80)

    for name, _, _, ttl_filename in harvesters_config:
        records = jurisdiction_data[name]
        logger.info(f"Building RDF graph for {name} ({len(records)} companies)...")
        g = extractor.build_rdf_graph(companies=records, include_schema=True)
        
        target_path = EXPORTS_DIR / ttl_filename
        extractor.export_standalone_ttl(g, target_path)

        # Write .txt copy alongside .ttl in data/exports/ and Desktop
        txt_filename = Path(ttl_filename).with_suffix(".txt").name
        target_txt_path = EXPORTS_DIR / txt_filename
        shutil.copy2(target_path, target_txt_path)

        desktop_path = DESKTOP_DIR / ttl_filename
        desktop_txt_path = DESKTOP_DIR / txt_filename
        shutil.copy2(target_path, desktop_path)
        shutil.copy2(target_path, desktop_txt_path)

        file_size_mb = os.path.getsize(target_path) / (1024 * 1024)
        logger.info(f"-> Generated {ttl_filename}: {len(g)} triples, {file_size_mb:.2f} MB")
        logger.info(f"   Copied to Desktop: {desktop_path}")

        export_summary.append({
            "jurisdiction": name,
            "filename": ttl_filename,
            "companies": len(records),
            "triples": len(g),
            "size_mb": round(file_size_mb, 2),
            "path": str(target_path),
            "desktop_path": str(desktop_path),
        })

    # 4. Export the unified master global ontology file
    logger.info("-" * 80)
    logger.info("BUILDING MASTER UNIFIED GLOBAL SUPPLY CHAIN ONTOLOGY (.TTL)")
    logger.info("-" * 80)

    master_filename = "Aero_Defence_Global_Supply_Chain_Ontology.ttl"
    master_txt_filename = "Aero_Defence_Global_Supply_Chain_Ontology.txt"
    master_path = EXPORTS_DIR / master_filename
    master_txt_path = EXPORTS_DIR / master_txt_filename
    desktop_master_path = DESKTOP_DIR / master_filename
    desktop_master_txt_path = DESKTOP_DIR / master_txt_filename

    logger.info(f"Building complete master RDF graph for all {len(all_harvested_companies)} companies...")
    master_graph = extractor.build_rdf_graph(companies=all_harvested_companies, include_schema=True)

    extractor.export_standalone_ttl(master_graph, master_path)
    shutil.copy2(master_path, master_txt_path)
    shutil.copy2(master_path, desktop_master_path)
    shutil.copy2(master_path, desktop_master_txt_path)

    master_size_mb = os.path.getsize(master_path) / (1024 * 1024)
    logger.info(f"-> MASTER GLOBAL ONTOLOGY GENERATED:")
    logger.info(f"   Total Triples: {len(master_graph)}")
    logger.info(f"   Total Companies: {len(all_harvested_companies)}")
    logger.info(f"   File Size: {master_size_mb:.2f} MB")
    logger.info(f"   Saved at: {master_path}")
    logger.info(f"   Desktop copy: {desktop_master_path}")

    # 5. Fast verification with pyoxigraph
    logger.info("-" * 80)
    logger.info("VERIFYING RDF SYNTAX AND EXECUTING SAMPLE SIMULATION SPARQL QUERIES")
    logger.info("-" * 80)

    store = pyoxigraph.Store()
    logger.info("Loading master Turtle file into Oxigraph in-memory store...")
    with open(master_path, "rb") as f:
        store.load(f, "text/turtle")
    logger.info(f"Oxigraph loaded {len(store)} triples successfully. 0 syntax errors.")

    # SPARQL Query 1: Competence Matching (Substitute Supplier in another country)
    q1 = """
    PREFIX aero: <https://w3id.org/aerospace-defence#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT ?companyName ?country ?tier ?capTitle ?trl
    WHERE {
        ?company aero:legalName ?companyName ;
                 aero:headquartersCountry ?country ;
                 aero:hasCapability ?cap .
        ?cap rdfs:label ?capTitle ;
             aero:alignedWithKIC aero:KIC_AdvancedMaterials ;
             aero:trlValue ?trl .
        FILTER (?country IN ("AUS", "CAN", "GBR", "IND", "FRA", "USA"))
        FILTER (?trl >= 8)
    }
    ORDER BY ?country ?companyName
    LIMIT 10
    """
    logger.info("Running SPARQL Query 1: Cross-Jurisdiction Competence Matching on KIC_AdvancedMaterials...")
    results_q1 = list(store.query(q1))
    logger.info(f"Query 1 returned {len(results_q1)} matches.")
    for r in results_q1[:5]:
        print(f"  [Q1 Match] {r['country'].value}: {r['companyName'].value} -> {r['capTitle'].value} (TRL {r['trl'].value})")

    # SPARQL Query 2: Platform Alternative Suppliers (e.g. F-35 suppliers across jurisdictions)
    q2 = """
    PREFIX aero: <https://w3id.org/aerospace-defence#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

    SELECT DISTINCT ?companyName ?country ?prodName ?partNo
    WHERE {
        ?company aero:legalName ?companyName ;
                 aero:headquartersCountry ?country ;
                 aero:manufacturesProduct ?prod .
        ?prod rdfs:label ?prodName ;
              aero:deployedOnPlatform aero:Platform_F35_Lightning_II .
        OPTIONAL { ?prod aero:partNumber ?partNo . }
    }
    ORDER BY ?country ?companyName
    LIMIT 10
    """
    logger.info("Running SPARQL Query 2: F-35 Alternative Suppliers across Jurisdictions...")
    results_q2 = list(store.query(q2))
    logger.info(f"Query 2 returned {len(results_q2)} matches.")
    for r in results_q2[:5]:
        try:
            part_no_str = r['partNo'].value if r['partNo'] is not None else ""
        except (KeyError, IndexError):
            part_no_str = ""
        print(f"  [Q2 Match] {r['country'].value}: {r['companyName'].value} -> {r['prodName'].value} ({part_no_str})")

    # Save summary report
    summary_data = {
        "build_timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "total_companies": len(all_harvested_companies),
        "total_triples": len(master_graph),
        "master_file": {
            "name": master_filename,
            "path": str(master_path),
            "desktop_path": str(desktop_master_path),
            "size_mb": round(master_size_mb, 2),
            "triples": len(master_graph),
        },
        "jurisdiction_files": export_summary,
        "elapsed_seconds": round(time.time() - start_time, 2),
    }

    summary_file = EXPORTS_DIR / "export_summary.json"
    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary_data, f, indent=2)

    logger.info("=" * 80)
    logger.info(f"GLOBAL EXPORT COMPLETED IN {time.time() - start_time:.2f} SECONDS.")
    logger.info(f"Summary written to {summary_file}")
    logger.info("=" * 80)


if __name__ == "__main__":
    main()
