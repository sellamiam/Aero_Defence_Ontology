"""
Entity Resolution & Corporate Hierarchy Linking Pipeline.
Deduplicates companies across data sources, resolves CAGE/NCAGE and DUNS keys,
and establishes parent-subsidiary relationships across international primes.
"""

from typing import List, Dict, Any, Optional
import json
import re
from pathlib import Path
import logging

logger = logging.getLogger("EntityResolutionPipeline")


class EntityResolutionPipeline:
    """Resolves and normalizes company entities, links multinational hierarchies, and unifies capabilities."""

    def __init__(self, data_dir: Optional[Path] = None):
        self.data_dir = data_dir or Path(__file__).resolve().parent.parent / "data"
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.processed_dir.mkdir(parents=True, exist_ok=True)

        # Corporate parent associations
        self.parent_subsidiary_rules = {
            "General Dynamics Land Systems-Canada": "General Dynamics Corporation",
            "L3Harris MAS Inc.": "L3Harris Technologies, Inc.",
            "Rheinmetall Canada Inc.": "Rheinmetall AG",
            "Pratt & Whitney Canada Corp.": "RTX Corporation",
            "Bell Textron Canada Ltd.": "Textron Inc.",
            "MBDA UK Ltd.": "MBDA",
        }

    def _normalize_name(self, name: str) -> str:
        """Strips common legal suffixes and punctuation for entity comparison."""
        cleaned = re.sub(r"\b(Inc|Corp|Corporation|Ltd|Limited|plc|SA|SE|GmbH|Co|LLC)\b\.?", "", name, flags=re.IGNORECASE)
        cleaned = re.sub(r"[^\w\s]", "", cleaned)
        return " ".join(cleaned.split()).lower()

    def process_and_resolve(self) -> Dict[str, Any]:
        """Loads raw regional catalogs, resolves identities and hierarchies, and writes processed output."""
        raw_files = list(self.raw_dir.glob("*_raw.json")) + list(self.raw_dir.glob("*_catalog.json"))
        
        # If no raw files exist yet, trigger harvesters
        if not raw_files:
            logger.info("No raw files found. Triggering harvesters...")
            from harvesters.canada_harvester import CanadaHarvester
            from harvesters.uk_harvester import UKHarvester
            from harvesters.eu_harvester import EUHarvester
            CanadaHarvester().harvest()
            UKHarvester().harvest()
            EUHarvester().harvest()
            raw_files = list(self.raw_dir.glob("*_catalog.json"))

        all_raw_records: List[Dict[str, Any]] = []
        for rf in raw_files:
            try:
                with open(rf, "r", encoding="utf-8") as f:
                    recs = json.load(f)
                    if isinstance(recs, list):
                        all_raw_records.extend(recs)
            except Exception as e:
                logger.error(f"Error reading {rf}: {e}")

        logger.info(f"Loaded {len(all_raw_records)} raw records across regions.")

        resolved_by_cage: Dict[str, Dict[str, Any]] = {}
        resolved_by_norm_name: Dict[str, str] = {}  # norm_name -> cage_code
        subsidiary_links_count = 0
        total_capabilities = 0

        for r in all_raw_records:
            cage = r.get("cage_code")
            norm_name = self._normalize_name(r.get("legal_name", ""))

            # Link corporate parent if applicable
            legal_name = r.get("legal_name", "")
            if legal_name in self.parent_subsidiary_rules:
                r["parent_company"] = self.parent_subsidiary_rules[legal_name]
                subsidiary_links_count += 1

            if cage and cage in resolved_by_cage:
                # Merge existing record
                existing = resolved_by_cage[cage]
                # Combine unique certs, capabilities, etc.
                existing["certifications"] = list(set(existing["certifications"] + r.get("certifications", [])))
                existing["kics"] = list(set(existing["kics"] + r.get("kics", [])))
                existing["platforms"] = list(set(existing["platforms"] + r.get("platforms", [])))
                continue

            if norm_name in resolved_by_norm_name:
                prior_cage = resolved_by_norm_name[norm_name]
                existing = resolved_by_cage[prior_cage]
                existing["certifications"] = list(set(existing["certifications"] + r.get("certifications", [])))
                continue

            # Register record
            if not cage:
                cage = f"GEN{len(resolved_by_cage)+1:05d}"
                r["cage_code"] = cage

            resolved_by_cage[cage] = r
            resolved_by_norm_name[norm_name] = cage
            total_capabilities += len(r.get("capabilities", []))

        resolved_list = list(resolved_by_cage.values())
        logger.info(f"Resolved {len(resolved_list)} unique companies ({subsidiary_links_count} parent links).")

        out_path = self.processed_dir / "normalized_companies.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(resolved_list, f, indent=2, ensure_ascii=False)

        return {
            "companies_resolved": len(resolved_list),
            "subsidiaries_linked": subsidiary_links_count,
            "capabilities_extracted": total_capabilities,
            "output_path": str(out_path),
        }
