"""
Startup Scoring Algorithm
Advanced multi-dimensional scoring engine for startup validation.
"""

from typing import Dict, Any
from backend.models.schemas import ValidationScore, StartupScore
from backend.core.logger import logger


class ScoringEngine:
    """
    Proprietary startup scoring algorithm.
    Weights based on VC investment criteria research.
    """

    GRADE_THRESHOLDS = [
        (90, "A+"), (80, "A"), (70, "B+"),
        (60, "B"), (50, "C"), (0, "D")
    ]

    VERDICT_TEMPLATES = {
        "A+": "🚀 Exceptional opportunity — investor-ready with strong fundamentals.",
        "A":  "⭐ High-potential idea with solid market validation.",
        "B+": "✅ Promising concept — refine execution strategy before pitching.",
        "B":  "🔄 Viable idea needing stronger differentiation and market fit.",
        "C":  "⚠️ Early-stage concept with significant validation gaps.",
        "D":  "🔴 High-risk idea requiring fundamental rethinking.",
    }

    def compute_scores(self, raw_analysis: Dict[str, Any]) -> StartupScore:
        """Compute final startup scores from LLM analysis."""
        logger.info("Computing startup scores...")

        raw_scores = raw_analysis.get("scores", {})

        scores = ValidationScore(
            overall_score=self._normalize(raw_scores.get("overall_score", 60)),
            market_demand_score=self._normalize(raw_scores.get("market_demand_score", 60)),
            problem_solution_fit=self._normalize(raw_scores.get("problem_solution_fit", 60)),
            monetization_potential=self._normalize(raw_scores.get("monetization_potential", 60)),
            scalability_score=self._normalize(raw_scores.get("scalability_score", 60)),
            risk_score=self._normalize(raw_scores.get("risk_score", 50)),
            investor_readiness_score=self._normalize(raw_scores.get("investor_readiness_score", 50)),
            market_opportunity_score=self._normalize(raw_scores.get("market_opportunity_score", 60)),
        )

        # Weighted composite score
        weighted_score = self._weighted_composite(scores)
        success_probability = self._normalize(raw_scores.get("success_probability", weighted_score))

        grade = self._get_grade(weighted_score)
        verdict = raw_scores.get("verdict") or self.VERDICT_TEMPLATES[grade]

        return StartupScore(
            scores=scores,
            success_probability=success_probability,
            grade=grade,
            verdict=verdict,
        )

    def _weighted_composite(self, scores: ValidationScore) -> float:
        """VC-weighted composite scoring formula."""
        weights = {
            "market_demand_score": 0.25,
            "problem_solution_fit": 0.20,
            "monetization_potential": 0.20,
            "scalability_score": 0.15,
            "market_opportunity_score": 0.10,
            "investor_readiness_score": 0.05,
            "risk_score": 0.05,
        }
        total = (
            scores.market_demand_score * weights["market_demand_score"] +
            scores.problem_solution_fit * weights["problem_solution_fit"] +
            scores.monetization_potential * weights["monetization_potential"] +
            scores.scalability_score * weights["scalability_score"] +
            scores.market_opportunity_score * weights["market_opportunity_score"] +
            scores.investor_readiness_score * weights["investor_readiness_score"] +
            scores.risk_score * weights["risk_score"]
        )
        return round(total, 2)

    def _get_grade(self, score: float) -> str:
        for threshold, grade in self.GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return "D"

    def _normalize(self, value: float) -> float:
        return round(max(0.0, min(100.0, float(value))), 2)


scoring_engine = ScoringEngine()
