"""
Base harvester interface and shared data structures.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import json
from pathlib import Path


@dataclass
class RawCompanyRecord:
    legal_name: str
    trade_name: Optional[str]
    cage_code: Optional[str]
    duns_number: Optional[str]
    business_number: Optional[str]
    country: str  # ISO-3 (CAN, GBR, FRA, DEU, ITA, etc.)
    city: str
    website: Optional[str]
    tier: str  # Prime, Tier1, Tier2, SME
    controlled_goods: bool
    itar_compliant: bool
    certifications: List[str]
    domains: List[str]
    platforms: List[str]
    kics: List[str]  # Key Industrial Capabilities
    capabilities: List[Dict[str, Any]]
    products: List[Dict[str, Any]]
    services: List[Dict[str, Any]]
    province: Optional[str] = None  # Province / State (e.g. ON, QC, BC)
    parent_company: Optional[str] = None


class BaseHarvester(ABC):
    """Abstract base class for regional aerospace & defence data harvesters."""

    def __init__(self, region_name: str, output_dir: Optional[Path] = None):
        self.region_name = region_name
        self.output_dir = output_dir or Path(__file__).resolve().parent.parent / "data" / "raw"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def harvest(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Harvests records and returns a list of dictionaries matching RawCompanyRecord."""
        pass

    def save_raw(self, records: List[Dict[str, Any]], filename: Optional[str] = None) -> Path:
        """Serializes harvested records to a JSON file."""
        target_file = self.output_dir / (filename or f"{self.region_name.lower()}_raw.json")
        with open(target_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)
        return target_file
