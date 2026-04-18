"""
Test Suite for AI Startup Validator
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


class TestScoringEngine:
    def test_scoring_grades(self):
        from backend.services.scoring_service import ScoringEngine
        engine = ScoringEngine()
        assert engine._get_grade(95) == "A+"
        assert engine._get_grade(82) == "A"
        assert engine._get_grade(72) == "B+"
        assert engine._get_grade(62) == "B"
        assert engine._get_grade(52) == "C"
        assert engine._get_grade(30) == "D"

    def test_normalize(self):
        from backend.services.scoring_service import ScoringEngine
        engine = ScoringEngine()
        assert engine._normalize(150) == 100.0
        assert engine._normalize(-10) == 0.0
        assert engine._normalize(75.5) == 75.5


class TestSchemas:
    def test_startup_idea_request(self):
        from backend.models.schemas import StartupIdeaRequest
        req = StartupIdeaRequest(
            idea="An AI tool that helps students learn faster",
            industry="EdTech",
            target_market="College students",
            location="India"
        )
        assert req.idea.startswith("An AI tool")
        assert req.location == "India"

    def test_risk_level_enum(self):
        from backend.models.schemas import RiskLevel
        assert RiskLevel.LOW == "Low"
        assert RiskLevel.CRITICAL == "Critical"


class TestConfig:
    def test_settings_load(self):
        from backend.core.config import settings
        assert settings.APP_VERSION == "1.0.0"
        assert settings.API_PORT == 8000
        assert settings.OPENAI_MODEL == "gpt-4o"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
