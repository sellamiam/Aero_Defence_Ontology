"""
Specialized Agent definitions for the Aerospace & Defence Ontology & Matching Swarm.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("SwarmAgents")


class SwarmAgent(ABC):
    """Abstract base class for all specialized swarm agents."""

    def __init__(self, name: str, role: str, description: str):
        self.name = name
        self.role = role
        self.description = description
        self.logger = logging.getLogger(f"Swarm.{name}")
        self.metrics: Dict[str, Any] = {"tasks_completed": 0, "errors": 0, "total_duration_sec": 0.0}

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the agent's designated task given a shared pipeline context."""
        pass

    def record_run(self, duration: float, success: bool = True):
        self.metrics["total_duration_sec"] += duration
        if success:
            self.metrics["tasks_completed"] += 1
        else:
            self.metrics["errors"] += 1


class OntologyArchitectAgent(SwarmAgent):
    """
    Agent 1: Responsible for the W3C OWL 2 schema, Canadian KIC taxonomies,
    NATO STANAG capabilities, platform classifications, and SHACL constraint shapes.
    """

    def __init__(self):
        super().__init__(
            name="OntologyArchitect",
            role="Ontology & Schema Architect",
            description="Designs, maintains and validates W3C OWL/RDF schemas and SHACL constraint shapes.",
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        self.logger.info("Verifying and compiling OWL 2 ontology definitions and SHACL shapes...")
        from pipeline.validator import OntologyValidator

        validator = OntologyValidator()
        validation_results = validator.verify_schema_integrity()
        duration = time.time() - start
        self.record_run(duration, success=validation_results.get("is_valid", False))
        return {
            "status": "success" if validation_results.get("is_valid") else "failed",
            "schema_stats": validation_results,
            "duration_sec": round(duration, 3),
        }


class CanadianHarvesterAgent(SwarmAgent):
    """
    Agent 2: Harvests Canadian aerospace & defence ecosystem data (~1,000 firms),
    mapping to Key Industrial Capabilities (KICs), Controlled Goods, and CAGE codes.
    """

    def __init__(self):
        super().__init__(
            name="CanadianHarvester",
            role="Regional Harvester (Canada)",
            description="Ingests Canadian A&D firms from ISED, AIAC, CADSI, and regional clusters.",
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        self.logger.info("Harvesting Canadian Aerospace & Defence directory records...")
        from harvesters.canada_harvester import CanadaHarvester

        limit = context.get("limit_per_region", None)
        harvester = CanadaHarvester()
        records = harvester.harvest(limit=limit)
        duration = time.time() - start
        self.record_run(duration, success=len(records) > 0)
        return {
            "status": "success",
            "records_harvested": len(records),
            "region": "Canada",
            "sample_names": [r["legal_name"] for r in records[:5]],
            "duration_sec": round(duration, 3),
        }


class EuUkHarvesterAgent(SwarmAgent):
    """
    Agent 3: Harvests EU & UK aerospace & defence companies, covering major primes,
    Tier 1/2 sub-contractors, and innovative SMEs across the UK, France, Germany, Italy, etc.
    """

    def __init__(self):
        super().__init__(
            name="EuUkHarvester",
            role="Regional Harvester (EU & UK)",
            description="Ingests UK and European defence contractors from ADS, ASD, EDA, and national registries.",
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        self.logger.info("Harvesting EU & UK Aerospace & Defence enterprise profiles...")
        from harvesters.uk_harvester import UKHarvester
        from harvesters.eu_harvester import EUHarvester

        limit = context.get("limit_per_region", None)
        uk_records = UKHarvester().harvest(limit=limit)
        eu_records = EUHarvester().harvest(limit=limit)
        total_records = uk_records + eu_records
        duration = time.time() - start
        self.record_run(duration, success=len(total_records) > 0)
        return {
            "status": "success",
            "uk_records": len(uk_records),
            "eu_records": len(eu_records),
            "total_harvested": len(total_records),
            "duration_sec": round(duration, 3),
        }


class EntityResolutionAgent(SwarmAgent):
    """
    Agent 4: Entity resolution, deduplication, corporate hierarchy linking,
    and capability NLP extraction into standardized triples.
    """

    def __init__(self):
        super().__init__(
            name="EntityResolutionSpecialist",
            role="Entity Resolution & Extraction Specialist",
            description="Deduplicates corporate entities, links subsidiaries to parent primes, and extracts capabilities.",
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        self.logger.info("Executing entity resolution, normalization, and capability extraction...")
        from pipeline.entity_resolution import EntityResolutionPipeline
        from pipeline.extractor import RDFTripleExtractor

        pipeline = EntityResolutionPipeline()
        stats = pipeline.process_and_resolve()

        self.logger.info("Generating and exporting updated RDF triples...")
        extractor = RDFTripleExtractor()
        rdf_g = extractor.build_rdf_graph()
        export_paths = extractor.export_graph(rdf_g)
        self.logger.info(f"Exported {len(rdf_g)} triples to {export_paths['ntriples']}")

        duration = time.time() - start
        self.record_run(duration, success=stats.get("companies_resolved", 0) > 0)
        return {
            "status": "success",
            "companies_resolved": stats.get("companies_resolved", 0),
            "subsidiaries_linked": stats.get("subsidiaries_linked", 0),
            "capabilities_extracted": stats.get("capabilities_extracted", 0),
            "total_triples": len(rdf_g),
            "duration_sec": round(duration, 3),
        }


class KnowledgeGraphAgent(SwarmAgent):
    """
    Agent 5: Loads normalized triples into the Oxigraph triplestore, applies SHACL
    validation rules, and populates the semantic vector index.
    """

    def __init__(self):
        super().__init__(
            name="KnowledgeGraphStoreEngineer",
            role="Knowledge Graph Store Engineer",
            description="Builds and manages Oxigraph triplestore, SHACL validation, and vector indices.",
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        self.logger.info("Loading graph triples into Oxigraph and indexing semantic vectors...")
        from store.graph_store import GraphStore
        from store.vector_store import VectorStore

        graph_store = GraphStore()
        graph_stats = graph_store.build_and_populate()

        vector_store = VectorStore()
        vector_stats = vector_store.build_index_from_graph(graph_store)

        duration = time.time() - start
        self.record_run(duration, success=graph_stats.get("total_triples", 0) > 0)
        return {
            "status": "success",
            "total_triples": graph_stats.get("total_triples", 0),
            "total_entities": graph_stats.get("total_entities", 0),
            "vectors_indexed": vector_stats.get("indexed_count", 0),
            "duration_sec": round(duration, 3),
        }


class MatchingEngineAgent(SwarmAgent):
    """
    Agent 6: Executes matching engine validation benchmarks across realistic procurement scenarios.
    """

    def __init__(self):
        super().__init__(
            name="MatchingEngineDeveloper",
            role="Matching Engine Developer",
            description="Runs procurement matching queries, evaluates scoring weights, and verifies results.",
        )

    def execute(self, context: Dict[str, Any]) -> Dict[str, Any]:
        start = time.time()
        self.logger.info("Running procurement and capability matching evaluation benchmarks...")
        from matching.engine import MatchingEngine

        engine = MatchingEngine()
        benchmark_results = engine.run_benchmark_scenarios()
        duration = time.time() - start
        self.record_run(duration, success=len(benchmark_results.get("scenarios", [])) > 0)
        return {
            "status": "success",
            "scenarios_evaluated": len(benchmark_results.get("scenarios", [])),
            "all_passed": benchmark_results.get("all_passed", False),
            "duration_sec": round(duration, 3),
        }
