"""
Aerospace & Defence Procurement & Capability Matching Engine.
Features:
- Leak-proof Geographic Gating (Country, Province, City)
- Automatic Intent Parsing & Domain Synonym Expansion
- Dynamic Weight Normalization (Eliminates Score Inflation)
- Calibrated Semantic Confidence & Gap Analysis
"""

from typing import List, Dict, Any, Optional, Set
import time
import logging
from pathlib import Path

from store.graph_store import GraphStore
from store.vector_store import VectorStore
from matching.models import MatchingCriteria, MatchResponse, CompanyMatch, ScoreBreakdown
from matching.parser import QueryParser, CANADIAN_CITY_PROVINCE

logger = logging.getLogger("MatchingEngine")


class MatchingEngine:
    """Core matching engine for Aerospace and Defence procurement & partnering."""

    def __init__(self, graph_store: Optional[GraphStore] = None, vector_store: Optional[VectorStore] = None):
        self.workspace_root = Path(__file__).resolve().parent.parent
        self.graph_store = graph_store or GraphStore()
        self.vector_store = vector_store or VectorStore()

        self._company_cache: Dict[str, Dict[str, Any]] = {}
        self._initialize_stores()

    def _initialize_stores(self):
        """Ensures graph store and vector store are populated."""
        if len(self.graph_store.store) == 0:
            logger.info("Initializing GraphStore...")
            self.graph_store.build_and_populate()

        if self.vector_store.tfidf_matrix is None:
            if not self.vector_store.load_index():
                logger.info("Building VectorStore index...")
                self.vector_store.build_index_from_graph(self.graph_store)

    def _get_company_data(self, cage_code: str) -> Optional[Dict[str, Any]]:
        if cage_code not in self._company_cache:
            profile = self.graph_store.get_company_profile(cage_code)
            if profile:
                # Infer Canadian province if missing
                if profile.get("country") == "CAN" and not profile.get("province"):
                    city_lower = (profile.get("city") or "").lower()
                    profile["province"] = CANADIAN_CITY_PROVINCE.get(city_lower)
                self._company_cache[cage_code] = profile
        return self._company_cache.get(cage_code)

    def match(self, criteria: MatchingCriteria) -> MatchResponse:
        """Executes leak-proof multi-criteria hybrid matching algorithm."""
        start_time = time.time()
        
        # 1. NLP Query Parsing & Intent Extraction
        parsed = QueryParser.parse(criteria.query_text)
        logger.info(f"Query parsed: clean='{parsed.cleaned_query}', geo={parsed.target_country}/{parsed.target_region}")

        # Resolve active effective constraints
        effective_country = criteria.required_country or parsed.target_country
        effective_region = criteria.required_region or parsed.target_region
        effective_certs = list(set(criteria.required_certifications + parsed.extracted_certs))
        effective_cgp = criteria.require_controlled_goods if criteria.require_controlled_goods is not None else parsed.require_cgp
        effective_min_trl = criteria.min_trl or parsed.min_trl
        search_query = parsed.expanded_query

        # 2. Dynamic Weight Normalization (Eliminates Free Points)
        raw_weights = {"semantic": 0.50}
        if effective_certs:
            raw_weights["cert"] = 0.20
        if effective_min_trl:
            raw_weights["trl"] = 0.15
        if effective_country or effective_region:
            raw_weights["geo"] = 0.15

        total_weight = sum(raw_weights.values())
        norm_weights = {k: round(v / total_weight, 4) for k, v in raw_weights.items()}

        # 3. Semantic Candidate Retrieval
        semantic_candidates = self.vector_store.query_semantic(search_query, top_k=300)

        evaluated_candidates: List[CompanyMatch] = []
        seen_companies: Set[str] = set()

        for cand in semantic_candidates:
            cage = cand["cage_code"]
            if cage in seen_companies:
                continue
            seen_companies.add(cage)

            comp = self._get_company_data(cage)
            if not comp:
                continue

            comp_country = comp.get("country", "")
            comp_city = comp.get("city", "")
            comp_province = comp.get("province") or CANADIAN_CITY_PROVINCE.get(comp_city.lower())

            # LEAK-PROOF GATE 1: Geographic Country Filter
            if effective_country:
                req_c = effective_country.upper()
                if comp_country != req_c:
                    # Check if foreign company has an active direct subsidiary in target country
                    has_sub = any(
                        sub.get("country") == req_c for sub in comp.get("subsidiaries", [])
                    )
                    if not has_sub:
                        # Strictly eliminate: Leak-proof
                        continue

            # LEAK-PROOF GATE 2: Geographic Region / Province Filter
            if effective_region:
                req_r = effective_region.upper()
                if comp_province != req_r:
                    # If user asked for Ontario, companies in France, UK, Quebec, etc. are eliminated
                    continue

            # LEAK-PROOF GATE 3: Controlled Goods Registration (CGP)
            if effective_cgp is True and not comp.get("controlled_goods", False):
                continue

            # LEAK-PROOF GATE 4: ITAR Compliance
            if criteria.require_itar_compliant is True and not comp.get("itar_compliant", False):
                continue

            # Dimension 1: Calibrated Semantic Score
            raw_sim = cand.get("similarity_score", 0.0)
            if raw_sim >= 0.35:
                s_semantic = min(1.0, 0.70 + (raw_sim - 0.35) * 0.75)
                confidence = "HIGH"
            elif raw_sim >= 0.18:
                s_semantic = 0.35 + (raw_sim - 0.18) * 1.8
                confidence = "MODERATE"
            else:
                s_semantic = max(0.05, raw_sim * 1.8)
                confidence = "LOW_ADJACENT"

            # Dimension 2: Geographic Fit
            s_geo = 1.0
            if effective_region and comp_province == effective_region.upper():
                s_geo = 1.0
            elif effective_country and comp_country == effective_country.upper():
                s_geo = 1.0
            else:
                s_geo = 0.65 if comp.get("subsidiaries") else 0.0

            # Dimension 3: Certification Compliance
            s_cert = 1.0
            comp_certs = set(comp.get("certifications", []))
            if effective_certs:
                matched_certs = [
                    rc for rc in effective_certs
                    if any(rc in cc for cc in comp_certs)
                ]
                s_cert = len(matched_certs) / len(effective_certs)

            # Dimension 4: Readiness Level (TRL) Fit
            s_trl = 1.0
            cand_trl = cand.get("trl") or 8
            if effective_min_trl:
                if cand_trl >= effective_min_trl:
                    s_trl = 1.0
                else:
                    deficit = effective_min_trl - cand_trl
                    s_trl = max(0.0, 1.0 - (deficit * 0.35))

            # Composite Score using strictly normalized active weights
            overall = (
                (norm_weights.get("semantic", 0.0) * s_semantic)
                + (norm_weights.get("cert", 0.0) * s_cert)
                + (norm_weights.get("trl", 0.0) * s_trl)
                + (norm_weights.get("geo", 0.0) * s_geo)
            )

            # Human-Readable Justification & Gap Analysis
            justification_parts = []
            loc_label = f"{comp_country}"
            if comp_province:
                loc_label += f" ({comp_province} - {comp_city})"
            elif comp_city:
                loc_label += f" ({comp_city})"

            justification_parts.append(f"Location: {loc_label}")

            if confidence == "HIGH":
                justification_parts.append(f"Strong capability match for '{cand['matched_capability_title']}'")
            elif confidence == "MODERATE":
                justification_parts.append(f"Moderate match: '{cand['matched_capability_title']}'")
            else:
                justification_parts.append(f"Adjacent capability: '{cand['matched_capability_title']}'")

            if effective_certs:
                if s_cert >= 1.0:
                    justification_parts.append(f"Certified: {', '.join(effective_certs)}")
                else:
                    justification_parts.append(f"Missing some requested certifications")

            if comp.get("controlled_goods"):
                justification_parts.append("CGP Registered")

            justification = " | ".join(justification_parts)

            breakdown = ScoreBreakdown(
                semantic_score=round(s_semantic, 3),
                certification_score=round(s_cert, 3),
                trl_score=round(s_trl, 3),
                geographic_score=round(s_geo, 3),
                active_weights=norm_weights,
            )

            evaluated_candidates.append(
                CompanyMatch(
                    rank=0,
                    overall_score=round(overall, 4),
                    confidence_level=confidence,
                    cage_code=cage,
                    legal_name=comp["legal_name"],
                    country=comp["country"],
                    province=comp_province,
                    city=comp["city"],
                    tier=comp["tier"],
                    controlled_goods=comp.get("controlled_goods", False),
                    certifications=comp.get("certifications", []),
                    matched_capability_title=cand.get("matched_capability_title"),
                    matched_capability_description=cand.get("matched_capability_description"),
                    breakdown=breakdown,
                    justification=justification,
                )
            )

        # Sort descending by overall score
        evaluated_candidates.sort(key=lambda x: x.overall_score, reverse=True)

        for i, item in enumerate(evaluated_candidates[: criteria.top_k]):
            item.rank = i + 1

        top_results = evaluated_candidates[: criteria.top_k]
        elapsed_ms = round((time.time() - start_time) * 1000, 2)

        # Confidence summary
        if not top_results:
            conf_summary = "NO_MATCH: No qualified suppliers found matching all strict criteria."
        elif top_results[0].confidence_level == "HIGH":
            conf_summary = f"HIGH_CONFIDENCE: Found {len(top_results)} direct qualified suppliers."
        elif top_results[0].confidence_level == "MODERATE":
            conf_summary = f"MODERATE_CONFIDENCE: Found {len(top_results)} qualified suppliers with relevant capabilities."
        else:
            conf_summary = f"LOW_CONFIDENCE_ADJACENT: Showing closest adjacent capabilities in requested region."

        return MatchResponse(
            query=criteria.query_text,
            parsed_intent={
                "cleaned_query": parsed.cleaned_query,
                "target_country": effective_country,
                "target_region": effective_region,
                "effective_certs": effective_certs,
                "effective_cgp": effective_cgp,
                "effective_min_trl": effective_min_trl,
            },
            confidence_summary=conf_summary,
            total_matches_found=len(evaluated_candidates),
            top_matches=top_results,
            execution_time_ms=elapsed_ms,
        )

    def run_benchmark_scenarios(self) -> Dict[str, Any]:
        """Runs automated evaluation benchmarks testing real-world procurement queries."""
        logger.info("Running procurement matching evaluation benchmarks...")
        scenarios = [
            {
                "id": "scenario_1_ca_iss",
                "name": "Canadian In-Service Support & Aircraft Structural Life Extension",
                "criteria": MatchingCriteria(
                    query_text="Maritime patrol aircraft depot-level overhaul, structural life extension, and mission avionics integration in Canada with CGP and TRL 8",
                    top_k=5,
                ),
                "expected_top_companies": ["IMP Aerospace & Defence", "L3Harris MAS Inc.", "Bombardier Inc."],
            },
            {
                "id": "scenario_2_simulation",
                "name": "Synthetic Combat Flight Training & Level D Simulators",
                "criteria": MatchingCriteria(
                    query_text="Full flight simulator Level D and distributed synthetic mission training environments",
                    min_trl=8,
                    top_k=5,
                ),
                "expected_top_companies": ["CAE Inc."],
            },
            {
                "id": "scenario_3_space_radar",
                "name": "Space-Based Synthetic Aperture Radar (SAR) & Robotics",
                "criteria": MatchingCriteria(
                    query_text="Space-based Synthetic Aperture Radar SAR satellites, space robotics, and orbital servicing",
                    min_trl=8,
                    top_k=5,
                ),
                "expected_top_companies": ["MDA Space Ltd."],
            },
            {
                "id": "scenario_4_ontario_drones",
                "name": "Tactical Drone Motors & UAS Electric Powertrains in Ontario",
                "criteria": MatchingCriteria(
                    query_text="Drone motors mid size drones in Ontario",
                    top_k=5,
                ),
                "expected_top_companies": [
                    "Volatus Aerospace Corp.",
                    "Pegasus Imagery Ltd.",
                    "MicroPilot Systems Canada Ltd.",
                    "SkyX Systems Corp.",
                    "Draganfly Innovations Canada Inc.",
                ],
            },
        ]

        benchmark_results = []
        all_passed = True

        for sc in scenarios:
            res = self.match(sc["criteria"])
            top_names = [m.legal_name for m in res.top_matches]
            passed = any(exp in top_names for exp in sc["expected_top_companies"])
            if not passed:
                all_passed = False

            benchmark_results.append({
                "scenario_id": sc["id"],
                "name": sc["name"],
                "passed": passed,
                "top_matched_company": top_names[0] if top_names else None,
                "expected_any_of": sc["expected_top_companies"],
                "latency_ms": res.execution_time_ms,
            })

        logger.info(f"Benchmarks completed. All passed: {all_passed}")
        return {"all_passed": all_passed, "scenarios": benchmark_results}
