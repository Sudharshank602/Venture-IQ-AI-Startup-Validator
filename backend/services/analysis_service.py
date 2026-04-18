"""
Analysis Orchestrator
Coordinates LLM, scoring, and RAG services into a unified analysis pipeline.
"""

import time
from typing import Dict, Any

from backend.services.llm_service import llm_service
from backend.services.scoring_service import scoring_engine
from backend.services.vector_store import vector_store
from backend.models.schemas import (
    StartupValidationResponse, StartupIdeaRequest,
    MarketAnalysis, SWOTAnalysis, Competitor,
    RevenueModel, BusinessMoat, GrowthStrategy,
    GoToMarketStrategy, RiskFactor, RiskLevel
)
from backend.core.logger import logger


def _safe_list(data: Any, default=None) -> list:
    if isinstance(data, list):
        return data
    return default or []


def _safe_str(data: Any, default: str = "") -> str:
    return str(data) if data else default


class AnalysisOrchestrator:
    """End-to-end startup analysis pipeline."""

    async def run_full_analysis(self, request: StartupIdeaRequest) -> StartupValidationResponse:
        """Execute complete multi-step startup analysis."""
        start_time = time.time()
        logger.info(f"Starting full analysis for: {request.idea[:60]}...")

        # Step 1: Retrieve RAG context
        context = vector_store.retrieve_context(request.idea)
        if context:
            logger.info("RAG context retrieved successfully.")

        # Step 2: LLM multi-step analysis
        raw = await llm_service.analyze_startup_idea(
            idea=request.idea,
            industry=request.industry or "",
            target_market=request.target_market or "",
            location=request.location or "Global",
        )

        # Step 3: Scoring
        startup_score = scoring_engine.compute_scores(raw)

        # Step 4: Generate pitch
        pitch = await llm_service.generate_pitch(request.idea, raw)

        # Step 5: Assemble response
        response = self._assemble_response(request.idea, raw, startup_score, pitch)
        response.processing_time = round(time.time() - start_time, 2)

        logger.info(f"Analysis complete in {response.processing_time}s | Score: {startup_score.scores.overall_score}")
        return response

    def _assemble_response(self, idea: str, raw: Dict, score, pitch: str) -> StartupValidationResponse:
        """Map raw LLM output to typed Pydantic models."""

        # Market Analysis
        ma = raw.get("market_analysis", {})
        market = MarketAnalysis(
            market_size=_safe_str(ma.get("market_size"), "$1B+"),
            market_stage=_safe_str(ma.get("market_stage"), "Growing"),
            growth_rate=_safe_str(ma.get("growth_rate"), "15% CAGR"),
            target_audience=_safe_str(ma.get("target_audience"), "SMBs and enterprises"),
            pain_points=_safe_list(ma.get("pain_points"), ["Market inefficiency"]),
            market_trends=_safe_list(ma.get("market_trends"), ["AI adoption increasing"]),
            tam=_safe_str(ma.get("tam"), "$5B"),
            sam=_safe_str(ma.get("sam"), "$1B"),
            som=_safe_str(ma.get("som"), "$50M"),
        )

        # SWOT
        sw = raw.get("swot_analysis", {})
        swot = SWOTAnalysis(
            strengths=_safe_list(sw.get("strengths"), ["Innovative solution"]),
            weaknesses=_safe_list(sw.get("weaknesses"), ["Market awareness"]),
            opportunities=_safe_list(sw.get("opportunities"), ["Large market"]),
            threats=_safe_list(sw.get("threats"), ["Competition"]),
        )

        # Competitors
        competitors = []
        for c in _safe_list(raw.get("competitors"), []):
            try:
                competitors.append(Competitor(
                    name=_safe_str(c.get("name"), "Unknown"),
                    description=_safe_str(c.get("description"), ""),
                    strengths=_safe_list(c.get("strengths")),
                    weaknesses=_safe_list(c.get("weaknesses")),
                    funding=c.get("funding"),
                    market_share=c.get("market_share"),
                    pricing_model=c.get("pricing_model"),
                ))
            except Exception:
                continue

        # Revenue Models
        revenue_models = []
        for r in _safe_list(raw.get("revenue_models"), []):
            try:
                revenue_models.append(RevenueModel(
                    model_name=_safe_str(r.get("model_name"), "SaaS"),
                    description=_safe_str(r.get("description"), ""),
                    projected_monthly_revenue=_safe_str(r.get("projected_monthly_revenue"), "TBD"),
                    time_to_revenue=_safe_str(r.get("time_to_revenue"), "6 months"),
                    pros=_safe_list(r.get("pros")),
                    cons=_safe_list(r.get("cons")),
                ))
            except Exception:
                continue

        # Business Moats
        moats = []
        for m in _safe_list(raw.get("business_moats"), []):
            try:
                moats.append(BusinessMoat(
                    moat_type=_safe_str(m.get("moat_type"), "Technology"),
                    description=_safe_str(m.get("description"), ""),
                    strength=_safe_str(m.get("strength"), "Moderate"),
                    defensibility_score=float(m.get("defensibility_score", 60)),
                ))
            except Exception:
                continue

        # Growth Strategies
        strategies = []
        for g in _safe_list(raw.get("growth_strategies"), []):
            try:
                strategies.append(GrowthStrategy(
                    phase=_safe_str(g.get("phase"), "Launch"),
                    timeline=_safe_str(g.get("timeline"), "0-6 months"),
                    actions=_safe_list(g.get("actions")),
                    kpis=_safe_list(g.get("kpis")),
                    estimated_cost=_safe_str(g.get("estimated_cost"), "TBD"),
                ))
            except Exception:
                continue

        # GTM Strategy
        gtm_raw = raw.get("go_to_market", {})
        gtm = GoToMarketStrategy(
            launch_strategy=_safe_str(gtm_raw.get("launch_strategy"), "Direct sales and digital marketing"),
            primary_channels=_safe_list(gtm_raw.get("primary_channels"), ["Digital marketing"]),
            customer_acquisition=_safe_str(gtm_raw.get("customer_acquisition"), "Content marketing and SEO"),
            pricing_strategy=_safe_str(gtm_raw.get("pricing_strategy"), "Freemium model"),
            partnership_opportunities=_safe_list(gtm_raw.get("partnership_opportunities")),
            milestones=_safe_list(gtm_raw.get("milestones"), [{"month": "Month 6", "goal": "100 users"}]),
        )

        # Risk Factors
        risks = []
        for r in _safe_list(raw.get("risk_factors"), []):
            try:
                level_str = str(r.get("level", "Medium"))
                try:
                    level = RiskLevel(level_str)
                except ValueError:
                    level = RiskLevel.MEDIUM
                risks.append(RiskFactor(
                    risk=_safe_str(r.get("risk"), "Unknown risk"),
                    level=level,
                    probability=_safe_str(r.get("probability"), "30%"),
                    mitigation=_safe_str(r.get("mitigation"), "Monitor and adapt"),
                ))
            except Exception:
                continue

        return StartupValidationResponse(
            idea=idea,
            executive_summary=_safe_str(raw.get("executive_summary"), "Analysis complete."),
            scores=score,
            market_analysis=market,
            swot_analysis=swot,
            competitors=competitors,
            revenue_models=revenue_models,
            business_moats=moats,
            growth_strategies=strategies,
            go_to_market=gtm,
            risk_factors=risks,
            ai_pitch=pitch,
            ai_recommendations=_safe_list(raw.get("ai_recommendations"), ["Build MVP first", "Validate with real users"]),
        )


orchestrator = AnalysisOrchestrator()
