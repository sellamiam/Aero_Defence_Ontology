"""
Swarm Orchestrator for the Aerospace & Defence Ontology & Matching Engine.
Coordinates data pipelines, agent execution, state management, and logging.
"""

from typing import Dict, Any, List, Optional
import time
import json
import logging
from pathlib import Path
from swarm.agents import (
    SwarmAgent,
    OntologyArchitectAgent,
    CanadianHarvesterAgent,
    EuUkHarvesterAgent,
    EntityResolutionAgent,
    KnowledgeGraphAgent,
    MatchingEngineAgent,
)

logger = logging.getLogger("SwarmOrchestrator")


class SwarmOrchestrator:
    """
    Central Orchestrator managing the multi-agent swarm pipeline.
    Ensures sequential and parallel stages run with integrity and observability.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        self.workspace_root = workspace_root or Path(__file__).resolve().parent.parent
        self.agents: Dict[str, SwarmAgent] = {
            "architect": OntologyArchitectAgent(),
            "harvester_ca": CanadianHarvesterAgent(),
            "harvester_eu_uk": EuUkHarvesterAgent(),
            "entity_resolution": EntityResolutionAgent(),
            "graph_store": KnowledgeGraphAgent(),
            "matcher": MatchingEngineAgent(),
        }
        self.execution_log: List[Dict[str, Any]] = []

    def run_full_pipeline(self, limit_per_region: Optional[int] = None) -> Dict[str, Any]:
        """
        Runs the full end-to-end swarm pipeline:
        1. Schema validation (OntologyArchitect)
        2. Data harvesting (CanadianHarvester + EuUkHarvester)
        3. Entity resolution & capability extraction (EntityResolutionSpecialist)
        4. Knowledge graph population & vector indexing (KnowledgeGraphStoreEngineer)
        5. Verification & matching benchmarks (MatchingEngineDeveloper)
        """
        overall_start = time.time()
        logger.info("=== Starting Aerospace & Defence Multi-Agent Swarm Pipeline ===")

        context: Dict[str, Any] = {
            "workspace_root": str(self.workspace_root),
            "limit_per_region": limit_per_region,
            "pipeline_state": {},
        }

        # Stage 1: Ontology Schema Verification
        logger.info("[Stage 1/5] Executing Ontology Architect schema validation...")
        stage1_res = self.agents["architect"].execute(context)
        self._record_step("OntologyArchitect", stage1_res)

        # Stage 2: Parallel / Sequential Regional Data Harvesting
        logger.info("[Stage 2/5] Executing Regional Data Harvesters (Canada, EU, UK)...")
        stage2_ca = self.agents["harvester_ca"].execute(context)
        self._record_step("CanadianHarvester", stage2_ca)

        stage2_eu_uk = self.agents["harvester_eu_uk"].execute(context)
        self._record_step("EuUkHarvester", stage2_eu_uk)

        # Stage 3: Entity Resolution & Information Extraction
        logger.info("[Stage 3/5] Executing Entity Resolution & Capability Extraction...")
        stage3_res = self.agents["entity_resolution"].execute(context)
        self._record_step("EntityResolutionSpecialist", stage3_res)

        # Stage 4: Knowledge Graph Triplestore & Vector Indexing
        logger.info("[Stage 4/5] Executing Graph Store Loading & Vector Indexing...")
        stage4_res = self.agents["graph_store"].execute(context)
        self._record_step("KnowledgeGraphStoreEngineer", stage4_res)

        # Stage 5: Matching Engine Verification & Benchmarks
        logger.info("[Stage 5/5] Executing Matching Engine Procurement Verification...")
        stage5_res = self.agents["matcher"].execute(context)
        self._record_step("MatchingEngineDeveloper", stage5_res)

        total_duration = round(time.time() - overall_start, 3)
        logger.info("=== Multi-Agent Swarm Pipeline Completed in %s seconds ===", total_duration)

        summary = {
            "status": "completed",
            "total_duration_sec": total_duration,
            "stages": self.execution_log,
            "summary_metrics": {
                "canada_records": stage2_ca.get("records_harvested", 0),
                "eu_uk_records": stage2_eu_uk.get("total_harvested", 0),
                "companies_resolved": stage3_res.get("companies_resolved", 0),
                "total_triples": stage4_res.get("total_triples", 0),
                "vectors_indexed": stage4_res.get("vectors_indexed", 0),
                "benchmarks_passed": stage5_res.get("all_passed", False),
            },
        }

        # Save run log
        log_path = self.workspace_root / "data" / "swarm_run_summary.json"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)

        return summary

    def _record_step(self, agent_name: str, result: Dict[str, Any]):
        entry = {
            "agent": agent_name,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "result": result,
        }
        self.execution_log.append(entry)

    def get_agent_metrics(self) -> Dict[str, Any]:
        """Returns performance metrics across all swarm members."""
        return {name: agent.metrics for name, agent in self.agents.items()}
