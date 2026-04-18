"""
LLM Service - supports OpenAI (paid) and Groq (free) automatically.
"""

import json
import re
from typing import Dict, Any, Optional
from tenacity import retry, stop_after_attempt, wait_exponential

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.output_parsers import StrOutputParser

from backend.core.config import settings
from backend.core.logger import logger

GROQ_BASE_URL = "https://api.groq.com/openai/v1"


class LLMService:
    def __init__(self):
        extra = {}
        if settings.OPENAI_API_KEY.startswith("gsk_"):
            extra["base_url"] = GROQ_BASE_URL
            logger.info("Using Groq (free) API")
        else:
            logger.info("Using OpenAI API")

        self.llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0.3,
            api_key=settings.OPENAI_API_KEY,
            max_tokens=settings.MAX_TOKENS_PER_REQUEST,
            **extra,
        )
        self.creative_llm = ChatOpenAI(
            model=settings.OPENAI_MODEL,
            temperature=0.8,
            api_key=settings.OPENAI_API_KEY,
            max_tokens=1500,
            **extra,
        )
        logger.info(f"LLM Service initialized: {settings.OPENAI_MODEL}")

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def analyze_startup_idea(self, idea: str, industry: str = "", target_market: str = "", location: str = "Global") -> Dict[str, Any]:
        logger.info(f"Analyzing startup idea: {idea[:60]}...")

        system_prompt = """You are a world-class startup analyst and VC investor.
Return ONLY valid JSON. No markdown, no explanation, just pure JSON."""

        user_prompt = f"""Analyze this startup idea:

STARTUP IDEA: {idea}
INDUSTRY: {industry or 'Not specified'}
TARGET MARKET: {target_market or 'Not specified'}
LOCATION: {location}

Return this exact JSON structure:

{{
  "executive_summary": "2-3 sentence summary",
  "scores": {{
    "overall_score": 75,
    "market_demand_score": 80,
    "problem_solution_fit": 75,
    "monetization_potential": 70,
    "scalability_score": 75,
    "risk_score": 60,
    "investor_readiness_score": 65,
    "market_opportunity_score": 80,
    "success_probability": 70,
    "grade": "B+",
    "verdict": "One sentence verdict"
  }},
  "market_analysis": {{
    "market_size": "$X Billion",
    "market_stage": "Growing",
    "growth_rate": "X% CAGR",
    "target_audience": "Description",
    "pain_points": ["pain 1", "pain 2", "pain 3"],
    "market_trends": ["trend 1", "trend 2", "trend 3"],
    "tam": "$XB",
    "sam": "$XM",
    "som": "$XM"
  }},
  "swot_analysis": {{
    "strengths": ["s1", "s2", "s3"],
    "weaknesses": ["w1", "w2"],
    "opportunities": ["o1", "o2", "o3"],
    "threats": ["t1", "t2"]
  }},
  "competitors": [
    {{"name": "Competitor", "description": "What they do", "strengths": ["s1"], "weaknesses": ["w1"], "funding": "$XM", "market_share": "X%", "pricing_model": "$X/mo"}}
  ],
  "revenue_models": [
    {{"model_name": "SaaS Subscription", "description": "Monthly recurring", "projected_monthly_revenue": "$X-$Y by Month 12", "time_to_revenue": "3-6 months", "pros": ["p1"], "cons": ["c1"]}}
  ],
  "business_moats": [
    {{"moat_type": "Data Moat", "description": "Explanation", "strength": "Strong", "defensibility_score": 75}}
  ],
  "growth_strategies": [
    {{"phase": "Phase 1: Launch (0-6 months)", "timeline": "0-6 months", "actions": ["a1", "a2"], "kpis": ["k1", "k2"], "estimated_cost": "$10K-$25K"}},
    {{"phase": "Phase 2: Growth (6-18 months)", "timeline": "6-18 months", "actions": ["a1", "a2"], "kpis": ["k1", "k2"], "estimated_cost": "$50K-$150K"}},
    {{"phase": "Phase 3: Scale (18-36 months)", "timeline": "18-36 months", "actions": ["a1", "a2"], "kpis": ["k1", "k2"], "estimated_cost": "$500K+"}}
  ],
  "go_to_market": {{
    "launch_strategy": "Strategy description",
    "primary_channels": ["channel 1", "channel 2", "channel 3"],
    "customer_acquisition": "Acquisition strategy",
    "pricing_strategy": "Pricing rationale",
    "partnership_opportunities": ["partner 1", "partner 2"],
    "milestones": [
      {{"month": "Month 1", "goal": "goal"}},
      {{"month": "Month 3", "goal": "goal"}},
      {{"month": "Month 6", "goal": "goal"}},
      {{"month": "Month 12", "goal": "goal"}}
    ]
  }},
  "risk_factors": [
    {{"risk": "Risk description", "level": "Medium", "probability": "30%", "mitigation": "How to mitigate"}}
  ],
  "ai_recommendations": ["rec 1", "rec 2", "rec 3", "rec 4", "rec 5"]
}}

Fill in all values with realistic analysis for the idea provided."""

        try:
            messages = [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_prompt)
            ]
            response = await self.llm.ainvoke(messages)
            content = response.content.strip()
            content = re.sub(r"^```json\s*", "", content)
            content = re.sub(r"\s*```$", "", content)
            return json.loads(content)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {e}")
            raise ValueError(f"LLM returned invalid JSON: {e}")
        except Exception as e:
            logger.error(f"LLM analysis failed: {e}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def generate_pitch(self, idea: str, analysis: Dict[str, Any]) -> str:
        logger.info("Generating investor pitch...")
        scores = analysis.get("scores", {})
        market = analysis.get("market_analysis", {})

        prompt = f"""Write a 150-200 word investor pitch for this startup:

IDEA: {idea}
MARKET SIZE: {market.get('market_size', 'Large market')}
SUCCESS PROBABILITY: {scores.get('success_probability', 75)}%

Include: hook, solution, market size, competitive advantage, call-to-action.
Style: Y Combinator demo day. Passionate and data-driven."""

        messages = [HumanMessage(content=prompt)]
        response = await self.creative_llm.ainvoke(messages)
        return response.content.strip()

    async def get_quick_insights(self, idea: str) -> Dict[str, Any]:
        prompt = f"""Return JSON only, no markdown:
{{"one_liner": "10-word description", "market_category": "category", "initial_impression": "positive", "key_insight": "insight"}}

IDEA: {idea}"""
        try:
            messages = [HumanMessage(content=prompt)]
            response = await self.llm.ainvoke(messages)
            content = re.sub(r"```json\s*|\s*```", "", response.content.strip())
            return json.loads(content)
        except Exception:
            return {"one_liner": idea[:50], "market_category": "Technology", "initial_impression": "neutral", "key_insight": "Analysis in progress"}


llm_service = LLMService()