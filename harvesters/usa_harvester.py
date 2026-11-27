"""
United States Aerospace & Defence Harvester.
Loads the canonical verified US Aerospace & Defence supplier catalog
(harvesters/data/usa_verified_suppliers.json) covering Primes, Tier-1, Tier-2,
and specialized SMEs across all major US defence & aerospace hubs.
"""

from typing import List, Dict, Any, Optional
import json
from pathlib import Path
from harvesters.base import BaseHarvester


class USAHarvester(BaseHarvester):
    """Harvester for the United States Aerospace & Defence industrial base."""

    def __init__(
        self,
        data_file: Optional[Path] = None,
        output_dir: Optional[Path] = None,
    ):
        super().__init__(region_name="USA", output_dir=output_dir)
        self.data_file = data_file or (
            Path(__file__).resolve().parent / "data" / "usa_verified_suppliers.json"
        )

    def harvest(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Loads verified US supplier records and optionally serializes raw catalog."""
        if not self.data_file.exists():
            raise FileNotFoundError(
                f"Cannot find canonical US verified supplier catalog at {self.data_file}"
            )

        with open(self.data_file, "r", encoding="utf-8") as f:
            records: List[Dict[str, Any]] = json.load(f)

        if limit is not None:
            records = records[:limit]

        default_raw_dir = Path(__file__).resolve().parent.parent / "data" / "raw"
        target_raw = self.output_dir / "usa_aero_defence_catalog.json"
        # Protect full raw catalog against accidental truncation from limited test runs
        if limit is None or self.output_dir.resolve() != default_raw_dir.resolve() or not target_raw.exists():
            self.save_raw(records, "usa_aero_defence_catalog.json")

        return records
