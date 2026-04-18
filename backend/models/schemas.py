"""
Data Models
Pydantic schemas for all API requests, responses, and internal data structures.
"""

from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


# ─── Enums ────────────────────────────────────────────────────────────────────

class RiskLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class MarketStage(str, Enum):
    EMERGING = "Emerging"
    GROWING = "Growing"
    MATURE = "Mature"
    DECLINING = "Declining"


# ─── Request Models ───────────────────────────────────────────────────────────

class StartupIdeaRequest(BaseModel):
    idea: str = Field(..., min_length=10, max_length=2000, description="Startup idea description")
    industry: Optional[str] = Field(None, description="Industry category")
    target_market: Optional[str] = Field(None, description="Target market/audience")
    budget: Optional[str] = Field(None, description="Estimated initial budget")
    location: Optional[str] = Field("Global", description="Target geographic market")

    class Config:
        json_schema_extra = {
            "example": {
                "idea": "An AI-powered platform that helps small restaurants optimize their menu pricing and reduce food waste using real-time demand prediction.",
                "industry": "FoodTech / AI",
                "target_market": "Small to medium restaurants",
                "budget": "$50,000",
                "location": "India / Southeast Asia"
            }
        }


class CompetitorAnalysisRequest(BaseModel):
    idea: str = Field(..., description="Startup idea")
    industry: str = Field(..., description="Industry vertical")


class ReportRequest(BaseModel):
    idea: str
    analysis_data: Dict[str, Any]


# ─── Score Models ─────────────────────────────────────────────────────────────

class ValidationScore(BaseModel):
    overall_score: float = Field(..., ge=0, le=100)
    market_demand_score: float = Field(..., ge=0, le=100)
    problem_solution_fit: float = Field(..., ge=0, le=100)
    monetization_potential: float = Field(..., ge=0, le=100)
    scalability_score: float = Field(..., ge=0, le=100)
    risk_score: float = Field(..., ge=0, le=100)
    investor_readiness_score: float = Field(..., ge=0, le=100)
    market_opportunity_score: float = Field(..., ge=0, le=100)


class StartupScore(BaseModel):
    scores: ValidationScore
    success_probability: float = Field(..., ge=0, le=100)
    grade: str  # A+, A, B+, B, C, D
    verdict: str


# ─── Analysis Models ──────────────────────────────────────────────────────────

class MarketAnalysis(BaseModel):
    market_size: str
    market_stage: str
    growth_rate: str
    target_audience: str
    pain_points: List[str]
    market_trends: List[str]
    tam: str  # Total Addressable Market
    sam: str  # Serviceable Addressable Market
    som: str  # Serviceable Obtainable Market


class Competitor(BaseModel):
    name: str
    description: str
    strengths: List[str]
    weaknesses: List[str]
    funding: Optional[str] = None
    market_share: Optional[str] = None
    pricing_model: Optional[str] = None


class SWOTAnalysis(BaseModel):
    strengths: List[str]
    weaknesses: List[str]
    opportunities: List[str]
    threats: List[str]


class BusinessMoat(BaseModel):
    moat_type: str
    description: str
    strength: str  # Strong / Moderate / Weak
    defensibility_score: float


class RevenueModel(BaseModel):
    model_name: str
    description: str
    projected_monthly_revenue: str
    time_to_revenue: str
    pros: List[str]
    cons: List[str]


class GrowthStrategy(BaseModel):
    phase: str
    timeline: str
    actions: List[str]
    kpis: List[str]
    estimated_cost: str


class GoToMarketStrategy(BaseModel):
    launch_strategy: str
    primary_channels: List[str]
    customer_acquisition: str
    pricing_strategy: str
    partnership_opportunities: List[str]
    milestones: List[Dict[str, str]]


class RiskFactor(BaseModel):
    risk: str
    level: RiskLevel
    probability: str
    mitigation: str


# ─── Main Response Models ─────────────────────────────────────────────────────

class StartupValidationResponse(BaseModel):
    idea: str
    executive_summary: str
    scores: StartupScore
    market_analysis: MarketAnalysis
    swot_analysis: SWOTAnalysis
    competitors: List[Competitor]
    revenue_models: List[RevenueModel]
    business_moats: List[BusinessMoat]
    growth_strategies: List[GrowthStrategy]
    go_to_market: GoToMarketStrategy
    risk_factors: List[RiskFactor]
    ai_pitch: str
    ai_recommendations: List[str]
    processing_time: Optional[float] = None


class HealthResponse(BaseModel):
    status: str
    version: str
    environment: str
