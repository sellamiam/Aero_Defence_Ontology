"""
Pydantic data models for the Procurement Matching Engine.
"""

from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class MatchingCriteria(BaseModel):
    """Specification of procurement or partnering requirements."""

    query_text: str = Field(..., description="Natural language capability or RFP description.")
    required_country: Optional[str] = Field(None, description="ISO-3 Country code (e.g., 'CAN', 'GBR', 'FRA').")
    required_region: Optional[str] = Field(None, description="Province / State code (e.g. 'ON', 'QC').")
    required_certifications: List[str] = Field(default_factory=list, description="Mandatory certification IDs.")
    require_controlled_goods: Optional[bool] = Field(None, description="Must be Controlled Goods (CGP) certified.")
    require_itar_compliant: Optional[bool] = Field(None, description="Must be ITAR/EAR compliant.")
    min_trl: Optional[int] = Field(None, ge=1, le=9, description="Minimum Technology Readiness Level.")
    target_platform: Optional[str] = Field(None, description="Specific platform filter.")
    target_kic: Optional[str] = Field(None, description="Target Key Industrial Capability.")
    top_k: int = Field(default=10, ge=1, le=100, description="Number of results to return.")

    # Weight configuration for composite scoring (sum typically = 1.0)
    weight_semantic: float = Field(default=0.50, ge=0.0, le=1.0)
    weight_cert: float = Field(default=0.20, ge=0.0, le=1.0)
    weight_trl: float = Field(default=0.15, ge=0.0, le=1.0)
    weight_geo: float = Field(default=0.15, ge=0.0, le=1.0)


class ScoreBreakdown(BaseModel):
    semantic_score: float
    certification_score: float
    trl_score: float
    geographic_score: float
    active_weights: Dict[str, float]


class CompanyMatch(BaseModel):
    rank: int
    overall_score: float
    confidence_level: str  # HIGH, MODERATE, LOW_ADJACENT
    cage_code: str
    legal_name: str
    country: str
    province: Optional[str] = None
    city: str
    tier: str
    controlled_goods: bool
    certifications: List[str]
    matched_capability_title: Optional[str] = None
    matched_capability_description: Optional[str] = None
    breakdown: ScoreBreakdown
    justification: str


class MatchResponse(BaseModel):
    query: str
    parsed_intent: Optional[Dict[str, Any]] = None
    confidence_summary: Optional[str] = None
    total_matches_found: int
    top_matches: List[CompanyMatch]
    execution_time_ms: float
