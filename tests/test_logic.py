"""
Core logic validation tests — runs without external dependencies.
"""

import json
import re
import sys

PASS = 0
FAIL = 0


def test(name, fn):
    global PASS, FAIL
    try:
        fn()
        print(f"  ✓ {name}")
        PASS += 1
    except Exception as e:
        print(f"  ✗ {name}: {e}")
        FAIL += 1


# ─── Grade logic ─────────────────────────────────────────────────────────────

GRADE_THRESHOLDS = [(90, "A+"), (80, "A"), (70, "B+"), (60, "B"), (50, "C"), (0, "D")]


def get_grade(score):
    for threshold, grade in GRADE_THRESHOLDS:
        if score >= threshold:
            return grade
    return "D"


def test_grades():
    assert get_grade(95) == "A+"
    assert get_grade(85) == "A"
    assert get_grade(73) == "B+"
    assert get_grade(62) == "B"
    assert get_grade(53) == "C"
    assert get_grade(30) == "D"


# ─── Normalize ────────────────────────────────────────────────────────────────

def normalize(value):
    return round(max(0.0, min(100.0, float(value))), 2)


def test_normalize():
    assert normalize(150) == 100.0
    assert normalize(-10) == 0.0
    assert normalize(75.5) == 75.5
    assert normalize(0) == 0.0
    assert normalize(100) == 100.0


# ─── Weighted composite ───────────────────────────────────────────────────────

def weighted_composite(s):
    return round(
        s["market_demand"] * 0.25
        + s["fit"] * 0.20
        + s["monetization"] * 0.20
        + s["scalability"] * 0.15
        + s["opportunity"] * 0.10
        + s["investor"] * 0.05
        + s["risk"] * 0.05,
        2,
    )


def test_composite():
    scores = {
        "market_demand": 80, "fit": 75, "monetization": 70,
        "scalability": 85, "opportunity": 90, "investor": 65, "risk": 60,
    }
    composite = weighted_composite(scores)
    assert 60 <= composite <= 100
    grade = get_grade(composite)
    assert grade in ("A+", "A", "B+", "B", "C", "D")


# ─── JSON parsing (LLM response) ─────────────────────────────────────────────

MOCK_LLM = """{
  "executive_summary": "A compelling fintech solution targeting underserved SMBs.",
  "scores": {
    "overall_score": 78.5,
    "market_demand_score": 82,
    "problem_solution_fit": 76,
    "monetization_potential": 74,
    "scalability_score": 80,
    "risk_score": 65,
    "investor_readiness_score": 70,
    "market_opportunity_score": 85,
    "success_probability": 72,
    "grade": "B+",
    "verdict": "Strong market opportunity with solid fundamentals."
  },
  "ai_recommendations": ["Build MVP first", "Talk to 100 customers", "Focus on one market"]
}"""


def parse_llm_json(content):
    content = content.strip()
    content = re.sub(r"^```json\s*", "", content)
    content = re.sub(r"\s*```$", "", content)
    return json.loads(content)


def test_json_parsing():
    data = parse_llm_json(MOCK_LLM)
    assert data["scores"]["overall_score"] == 78.5
    assert data["scores"]["grade"] == "B+"
    assert len(data["ai_recommendations"]) == 3


def test_json_parsing_with_fences():
    fenced = "```json\n" + MOCK_LLM + "\n```"
    data = parse_llm_json(fenced)
    assert data["executive_summary"] != ""


# ─── Helper functions ─────────────────────────────────────────────────────────

def safe_list(data, default=None):
    return data if isinstance(data, list) else (default or [])


def safe_str(data, default=""):
    return str(data) if data else default


def test_helpers():
    assert safe_list([1, 2, 3]) == [1, 2, 3]
    assert safe_list(None, ["x"]) == ["x"]
    assert safe_list("bad", ["fallback"]) == ["fallback"]
    assert safe_str("hello") == "hello"
    assert safe_str(None, "default") == "default"
    assert safe_str(0, "zero") == "zero"


# ─── Risk level mapping ───────────────────────────────────────────────────────

RISK_CSS = {
    "Low": "risk-low",
    "Medium": "risk-medium",
    "High": "risk-high",
    "Critical": "risk-critical",
}


def test_risk_levels():
    for level in ["Low", "Medium", "High", "Critical"]:
        assert level in RISK_CSS


# ─── Score color logic ────────────────────────────────────────────────────────

def score_color(score):
    if score >= 80:
        return "#00d4aa"
    if score >= 60:
        return "#6c63ff"
    if score >= 40:
        return "#f5c518"
    return "#ff6b6b"


def test_score_colors():
    assert score_color(90) == "#00d4aa"
    assert score_color(70) == "#6c63ff"
    assert score_color(50) == "#f5c518"
    assert score_color(20) == "#ff6b6b"


# ─── Grade color mapping ──────────────────────────────────────────────────────

GRADE_COLORS = {
    "A+": ("#00d4aa", "rgba(0,212,170,0.15)"),
    "A":  ("#6c63ff", "rgba(108,99,255,0.15)"),
    "B+": ("#9d97ff", "rgba(157,151,255,0.15)"),
    "B":  ("#f5c518", "rgba(245,197,24,0.15)"),
    "C":  ("#ff9f43", "rgba(255,159,67,0.15)"),
    "D":  ("#ff6b6b", "rgba(255,107,107,0.15)"),
}


def test_grade_colors():
    for grade in ["A+", "A", "B+", "B", "C", "D"]:
        color, bg = GRADE_COLORS[grade]
        assert color.startswith("#")
        assert "rgba" in bg


# ─── Market analysis defaults ─────────────────────────────────────────────────

def test_market_defaults():
    ma = {}
    market_size = ma.get("market_size") or "$1B+"
    market_stage = ma.get("market_stage") or "Growing"
    growth_rate = ma.get("growth_rate") or "15% CAGR"
    pain_points = safe_list(ma.get("pain_points"), ["Market inefficiency"])

    assert market_size == "$1B+"
    assert market_stage == "Growing"
    assert growth_rate == "15% CAGR"
    assert len(pain_points) == 1


# ─── Startup score verdict templates ─────────────────────────────────────────

VERDICT_TEMPLATES = {
    "A+": "Exceptional opportunity — investor-ready with strong fundamentals.",
    "A":  "High-potential idea with solid market validation.",
    "B+": "Promising concept — refine execution strategy before pitching.",
    "B":  "Viable idea needing stronger differentiation and market fit.",
    "C":  "Early-stage concept with significant validation gaps.",
    "D":  "High-risk idea requiring fundamental rethinking.",
}


def test_verdicts():
    for grade in GRADE_COLORS.keys():
        assert grade in VERDICT_TEMPLATES
        assert len(VERDICT_TEMPLATES[grade]) > 20


# ─── Run all tests ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n" + "=" * 55)
    print("  VentureIQ — Core Logic Test Suite")
    print("=" * 55)

    suites = [
        ("Scoring: Grade calculation", test_grades),
        ("Scoring: Normalize values", test_normalize),
        ("Scoring: Weighted composite", test_composite),
        ("LLM: JSON response parsing", test_json_parsing),
        ("LLM: Fenced JSON parsing", test_json_parsing_with_fences),
        ("Utils: safe_list / safe_str", test_helpers),
        ("Model: Risk level mapping", test_risk_levels),
        ("UI: Score color thresholds", test_score_colors),
        ("UI: Grade color mapping", test_grade_colors),
        ("Model: Market analysis defaults", test_market_defaults),
        ("Model: Verdict templates", test_verdicts),
    ]

    print()
    for name, fn in suites:
        test(name, fn)

    print()
    print("=" * 55)
    print(f"  Results: {PASS} passed, {FAIL} failed")
    print("=" * 55 + "\n")

    sys.exit(0 if FAIL == 0 else 1)
