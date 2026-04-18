"""
AI Startup Validator & Business Intelligence Engine
Streamlit Frontend - Production SaaS UI
"""

import streamlit as st
import httpx
import json
import asyncio
import time
from typing import Dict, Any, Optional

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VentureIQ — AI Startup Intelligence",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)

API_BASE = "http://localhost:8000/api/v1"

# ─── Styles ───────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --bg: #0a0a0f;
    --surface: #111118;
    --border: #1e1e2e;
    --accent: #6c63ff;
    --accent2: #00d4aa;
    --accent3: #ff6b6b;
    --gold: #f5c518;
    --text: #e8e8f0;
    --muted: #6b6b85;
    --card: #13131f;
}

* { font-family: 'DM Sans', sans-serif; }
h1, h2, h3, .brand { font-family: 'Syne', sans-serif !important; }

.stApp { background: var(--bg); color: var(--text); }
.block-container { padding: 2rem 3rem; max-width: 1400px; }

/* Hide Streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* Hero */
.hero {
    background: linear-gradient(135deg, #0a0a0f 0%, #12112a 50%, #0a0a0f 100%);
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 4rem 3rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}
.hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -20%;
    width: 500px;
    height: 500px;
    background: radial-gradient(circle, rgba(108,99,255,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.hero::after {
    content: '';
    position: absolute;
    bottom: -30%;
    right: -10%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(0,212,170,0.08) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge {
    display: inline-block;
    background: rgba(108,99,255,0.15);
    border: 1px solid rgba(108,99,255,0.4);
    color: #9d97ff;
    padding: 4px 14px;
    border-radius: 100px;
    font-size: 12px;
    font-weight: 500;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}
.hero-title {
    font-family: 'Syne', sans-serif !important;
    font-size: clamp(2.4rem, 4vw, 3.6rem);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #ffffff 0%, #9d97ff 50%, #00d4aa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 1rem;
}
.hero-sub {
    font-size: 1.1rem;
    color: var(--muted);
    font-weight: 300;
    max-width: 600px;
    line-height: 1.7;
}

/* Stats row */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 6px 16px;
    font-size: 13px;
    color: var(--muted);
    margin: 4px;
}
.stat-pill strong { color: var(--text); }

/* Score ring */
.score-ring-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 2rem;
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
}
.score-ring {
    width: 160px;
    height: 160px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 2.8rem;
    font-weight: 800;
    margin: 1rem 0;
    position: relative;
}
.grade-badge {
    font-family: 'Syne', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    padding: 4px 16px;
    border-radius: 100px;
    letter-spacing: 0.05em;
}

/* Cards */
.info-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: border-color 0.2s;
}
.info-card:hover { border-color: rgba(108,99,255,0.4); }
.card-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.8rem;
}

/* Metric bars */
.metric-bar-wrap { margin: 10px 0; }
.metric-label { display: flex; justify-content: space-between; font-size: 13px; margin-bottom: 4px; }
.metric-label span:last-child { color: var(--accent); font-weight: 600; }
.metric-bar-bg { background: rgba(255,255,255,0.05); border-radius: 100px; height: 6px; }
.metric-bar-fill { height: 6px; border-radius: 100px; transition: width 1s ease; }

/* Tags */
.tag {
    display: inline-block;
    background: rgba(108,99,255,0.12);
    border: 1px solid rgba(108,99,255,0.25);
    color: #9d97ff;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 12px;
    font-weight: 500;
    margin: 3px;
}
.tag-green {
    background: rgba(0,212,170,0.1);
    border-color: rgba(0,212,170,0.25);
    color: #00d4aa;
}
.tag-red {
    background: rgba(255,107,107,0.1);
    border-color: rgba(255,107,107,0.25);
    color: #ff6b6b;
}
.tag-gold {
    background: rgba(245,197,24,0.1);
    border-color: rgba(245,197,24,0.3);
    color: var(--gold);
}

/* SWOT grid */
.swot-cell {
    border-radius: 14px;
    padding: 1.2rem;
    margin: 6px;
}
.swot-s { background: rgba(0,212,170,0.08); border: 1px solid rgba(0,212,170,0.2); }
.swot-w { background: rgba(255,107,107,0.08); border: 1px solid rgba(255,107,107,0.2); }
.swot-o { background: rgba(108,99,255,0.08); border: 1px solid rgba(108,99,255,0.2); }
.swot-t { background: rgba(245,197,24,0.08); border: 1px solid rgba(245,197,24,0.2); }
.swot-title { font-family: 'Syne', sans-serif; font-size: 0.9rem; font-weight: 700; margin-bottom: 0.6rem; }
.swot-item { font-size: 13px; color: #b0b0c8; margin: 4px 0; padding-left: 12px; position: relative; }
.swot-item::before { content: '→'; position: absolute; left: 0; color: var(--muted); }

/* Risk badges */
.risk-badge {
    display: inline-block;
    padding: 2px 10px;
    border-radius: 100px;
    font-size: 11px;
    font-weight: 600;
}
.risk-low { background: rgba(0,212,170,0.15); color: #00d4aa; }
.risk-medium { background: rgba(245,197,24,0.15); color: var(--gold); }
.risk-high { background: rgba(255,107,107,0.15); color: #ff6b6b; }
.risk-critical { background: rgba(255,50,50,0.2); color: #ff3232; }

/* Competitor table */
.comp-row {
    display: grid;
    grid-template-columns: 1.5fr 2fr 1fr 1fr;
    gap: 1rem;
    padding: 14px 16px;
    border-bottom: 1px solid var(--border);
    align-items: start;
    font-size: 14px;
}
.comp-row:last-child { border-bottom: none; }
.comp-header {
    font-size: 11px;
    font-weight: 600;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* Timeline */
.timeline-item {
    display: flex;
    gap: 16px;
    margin-bottom: 1.5rem;
    position: relative;
}
.timeline-dot {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 14px;
    flex-shrink: 0;
}
.timeline-content { flex: 1; }

/* Pitch box */
.pitch-box {
    background: linear-gradient(135deg, rgba(108,99,255,0.08) 0%, rgba(0,212,170,0.05) 100%);
    border: 1px solid rgba(108,99,255,0.3);
    border-radius: 16px;
    padding: 2rem;
    position: relative;
}
.pitch-box::before {
    content: '"';
    position: absolute;
    top: -10px;
    left: 20px;
    font-size: 5rem;
    color: rgba(108,99,255,0.3);
    font-family: Georgia, serif;
    line-height: 1;
}
.pitch-text {
    font-size: 1.05rem;
    line-height: 1.8;
    color: #d0d0e8;
    font-style: italic;
    margin-top: 1rem;
}

/* Input section */
.input-section {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 2rem;
    margin-bottom: 2rem;
}

/* Section headers */
.section-header {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 1.5rem;
}
.section-title {
    font-family: 'Syne', sans-serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: var(--text);
}
.section-line {
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, var(--border), transparent);
}

/* Streamlit overrides */
.stTextArea textarea {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 15px !important;
}
.stTextArea textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 2px rgba(108,99,255,0.15) !important;
}
.stTextInput input {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: 'DM Sans', sans-serif !important;
}
.stSelectbox > div > div {
    background: rgba(255,255,255,0.03) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
}
.stButton > button {
    background: linear-gradient(135deg, #6c63ff, #5a52e0) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.75rem 2rem !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    transition: all 0.2s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #7c74ff, #6c63ff) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 8px 24px rgba(108,99,255,0.35) !important;
}
.stExpander {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
}
.stProgress > div > div { background: var(--accent) !important; border-radius: 100px !important; }
.stSpinner { color: var(--accent) !important; }

/* Recommendation items */
.rec-item {
    display: flex;
    gap: 12px;
    align-items: flex-start;
    padding: 12px 0;
    border-bottom: 1px solid rgba(255,255,255,0.04);
}
.rec-num {
    width: 28px;
    height: 28px;
    border-radius: 8px;
    background: rgba(108,99,255,0.2);
    color: #9d97ff;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 700;
    flex-shrink: 0;
}
.rec-text { font-size: 14px; color: #c0c0d8; line-height: 1.6; padding-top: 4px; }

/* Processing time */
.proc-time {
    text-align: center;
    font-size: 12px;
    color: var(--muted);
    margin-top: 1rem;
}
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ──────────────────────────────────────────────────────────

def score_color(score: float) -> str:
    if score >= 80: return "#00d4aa"
    if score >= 60: return "#6c63ff"
    if score >= 40: return "#f5c518"
    return "#ff6b6b"

def score_ring_style(score: float) -> str:
    color = score_color(score)
    pct = int(score)
    return f"background: conic-gradient({color} {pct * 3.6}deg, rgba(255,255,255,0.05) 0deg); color: {color};"

def grade_color(grade: str) -> tuple:
    colors = {
        "A+": ("#00d4aa", "rgba(0,212,170,0.15)"),
        "A":  ("#6c63ff", "rgba(108,99,255,0.15)"),
        "B+": ("#9d97ff", "rgba(157,151,255,0.15)"),
        "B":  ("#f5c518", "rgba(245,197,24,0.15)"),
        "C":  ("#ff9f43", "rgba(255,159,67,0.15)"),
        "D":  ("#ff6b6b", "rgba(255,107,107,0.15)"),
    }
    return colors.get(grade, ("#6c63ff", "rgba(108,99,255,0.15)"))

def risk_badge(level: str) -> str:
    cls = {"Low": "risk-low", "Medium": "risk-medium", "High": "risk-high", "Critical": "risk-critical"}.get(level, "risk-medium")
    return f'<span class="risk-badge {cls}">{level}</span>'

def metric_bar(label: str, value: float, color: str = None):
    c = color or score_color(value)
    st.markdown(f"""
    <div class="metric-bar-wrap">
        <div class="metric-label"><span>{label}</span><span>{value:.0f}</span></div>
        <div class="metric-bar-bg"><div class="metric-bar-fill" style="width:{value}%;background:{c};"></div></div>
    </div>
    """, unsafe_allow_html=True)

def section_header(icon: str, title: str):
    st.markdown(f"""
    <div class="section-header">
        <span style="font-size:1.3rem">{icon}</span>
        <span class="section-title">{title}</span>
        <div class="section-line"></div>
    </div>
    """, unsafe_allow_html=True)


# ─── API Call ─────────────────────────────────────────────────────────────────

def call_api(payload: dict) -> Optional[Dict]:
    try:
        with httpx.Client(timeout=120.0) as client:
            response = client.post(f"{API_BASE}/analyze", json=payload)
            response.raise_for_status()
            return response.json()
    except httpx.ConnectError:
        st.error("⚠️ Cannot connect to API server. Make sure the backend is running on port 8000.")
        return None
    except httpx.TimeoutException:
        st.error("⏱️ Analysis timed out. Please try again.")
        return None
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return None


# ─── Render Functions ──────────────────────────────────────────────────────────

def render_hero():
    st.markdown("""
    <div class="hero">
        <div class="hero-badge">✦ AI-Powered Business Intelligence</div>
        <div class="hero-title">Validate Your Startup.<br>Intelligence, Instantly.</div>
        <div class="hero-sub">
            Enter your idea. Get a full VC-grade analysis in seconds — market sizing, 
            competitor mapping, revenue models, growth strategy, and your startup's 
            success probability score.
        </div>
        <div style="margin-top:2rem;">
            <span class="stat-pill">🤖 <strong>GPT-4o</strong> Powered</span>
            <span class="stat-pill">🔍 <strong>RAG</strong> Knowledge Base</span>
            <span class="stat-pill">📊 <strong>8-Dimension</strong> Scoring</span>
            <span class="stat-pill">⚡ <strong>Real-time</strong> Analysis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_input_form():
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    section_header("💡", "Describe Your Startup Idea")

    idea = st.text_area(
        "Startup Idea *",
        placeholder="e.g. An AI-powered platform that helps Indian small businesses automate GST filing and financial compliance using WhatsApp...",
        height=120,
        help="Be specific. Include the problem, solution, and target customer.",
    )

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        industry = st.text_input("Industry / Vertical", placeholder="e.g. FinTech, HealthTech")
    with c2:
        target_market = st.text_input("Target Market", placeholder="e.g. SMBs in India")
    with c3:
        budget = st.text_input("Initial Budget", placeholder="e.g. $25,000")
    with c4:
        location = st.selectbox("Market", ["India", "Global", "US", "Southeast Asia", "Europe", "Middle East", "Africa"])

    st.markdown("</div>", unsafe_allow_html=True)

    submit = st.button("🚀 Analyze My Startup Idea", use_container_width=True)
    return submit, idea, industry, target_market, budget, location


def render_score_overview(data: dict):
    scores = data.get("scores", {}).get("scores", {})
    startup_score = data.get("scores", {})

    overall = scores.get("overall_score", 0)
    success_prob = startup_score.get("success_probability", 0)
    grade = startup_score.get("grade", "B")
    verdict = startup_score.get("verdict", "")
    gcolor, gbg = grade_color(grade)

    section_header("📊", "Startup Intelligence Score")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown(f"""
        <div class="score-ring-container">
            <div style="font-size:12px;color:var(--muted);text-transform:uppercase;letter-spacing:0.1em;">Overall Score</div>
            <div class="score-ring" style="{score_ring_style(overall)}">
                {overall:.0f}
            </div>
            <div class="grade-badge" style="background:{gbg};color:{gcolor};">Grade {grade}</div>
            <div style="margin-top:1rem;font-size:13px;color:var(--muted);text-align:center;line-height:1.6;">{verdict}</div>
            <div style="margin-top:1rem;width:100%;padding-top:1rem;border-top:1px solid var(--border);">
                <div style="font-size:11px;color:var(--muted);text-align:center;margin-bottom:4px;">SUCCESS PROBABILITY</div>
                <div style="font-size:2rem;font-family:'Syne',sans-serif;font-weight:800;color:{score_color(success_prob)};text-align:center;">{success_prob:.0f}%</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown('<div class="card-title">Score Breakdown</div>', unsafe_allow_html=True)
        metric_bar("Market Demand", scores.get("market_demand_score", 0))
        metric_bar("Problem-Solution Fit", scores.get("problem_solution_fit", 0))
        metric_bar("Monetization Potential", scores.get("monetization_potential", 0))
        metric_bar("Scalability", scores.get("scalability_score", 0))
        metric_bar("Market Opportunity", scores.get("market_opportunity_score", 0))
        metric_bar("Investor Readiness", scores.get("investor_readiness_score", 0))
        metric_bar("Risk Score (Higher = Less Risk)", scores.get("risk_score", 0))
        st.markdown("</div>", unsafe_allow_html=True)

    # Executive Summary
    st.markdown(f"""
    <div class="info-card" style="border-left: 3px solid var(--accent);">
        <div class="card-title">Executive Summary</div>
        <div style="font-size:15px;line-height:1.8;color:#c0c0d8;">{data.get('executive_summary','')}</div>
    </div>
    """, unsafe_allow_html=True)


def render_market_analysis(data: dict):
    ma = data.get("market_analysis", {})
    section_header("📈", "Market Analysis")

    c1, c2, c3 = st.columns(3)
    for col, label, key, icon in [
        (c1, "Total Addressable Market", "tam", "🌐"),
        (c2, "Serviceable Market", "sam", "🎯"),
        (c3, "Obtainable Market", "som", "⚡"),
    ]:
        with col:
            st.markdown(f"""
            <div class="info-card" style="text-align:center;">
                <div style="font-size:2rem;margin-bottom:4px;">{icon}</div>
                <div class="card-title" style="text-align:center;">{label}</div>
                <div style="font-family:'Syne',sans-serif;font-size:1.6rem;font-weight:800;color:var(--accent2);">{ma.get(key,'—')}</div>
            </div>
            """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class="info-card">
            <div class="card-title">Market Overview</div>
            <div style="font-size:13px;margin-bottom:8px;"><span style="color:var(--muted);">Market Size:</span> <strong>{ma.get('market_size','—')}</strong></div>
            <div style="font-size:13px;margin-bottom:8px;"><span style="color:var(--muted);">Growth Rate:</span> <strong style="color:var(--accent2);">{ma.get('growth_rate','—')}</strong></div>
            <div style="font-size:13px;margin-bottom:8px;"><span style="color:var(--muted);">Stage:</span> <span class="tag">{ma.get('market_stage','—')}</span></div>
            <div style="font-size:13px;"><span style="color:var(--muted);">Target Audience:</span><br><span style="color:#c0c0d8;">{ma.get('target_audience','—')}</span></div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        pains = ma.get("pain_points", [])
        pain_html = "".join(f'<div class="swot-item">{p}</div>' for p in pains)
        st.markdown(f"""
        <div class="info-card">
            <div class="card-title">Key Pain Points</div>
            {pain_html}
        </div>
        """, unsafe_allow_html=True)

    trends = ma.get("market_trends", [])
    trend_tags = "".join(f'<span class="tag tag-green">{t}</span>' for t in trends)
    st.markdown(f"""
    <div class="info-card">
        <div class="card-title">Market Trends</div>
        {trend_tags}
    </div>
    """, unsafe_allow_html=True)


def render_swot(data: dict):
    swot = data.get("swot_analysis", {})
    section_header("🔲", "SWOT Analysis")

    c1, c2 = st.columns(2)
    for col, key, label, cls, color in [
        (c1, "strengths", "💪 Strengths", "swot-s", "#00d4aa"),
        (c2, "weaknesses", "⚠️ Weaknesses", "swot-w", "#ff6b6b"),
    ]:
        items = swot.get(key, [])
        items_html = "".join(f'<div class="swot-item">{i}</div>' for i in items)
        with col:
            st.markdown(f'<div class="swot-cell {cls}"><div class="swot-title" style="color:{color};">{label}</div>{items_html}</div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    for col, key, label, cls, color in [
        (c1, "opportunities", "🚀 Opportunities", "swot-o", "#9d97ff"),
        (c2, "threats", "⚡ Threats", "swot-t", "#f5c518"),
    ]:
        items = swot.get(key, [])
        items_html = "".join(f'<div class="swot-item">{i}</div>' for i in items)
        with col:
            st.markdown(f'<div class="swot-cell {cls}"><div class="swot-title" style="color:{color};">{label}</div>{items_html}</div>', unsafe_allow_html=True)


def render_competitors(data: dict):
    competitors = data.get("competitors", [])
    if not competitors:
        return
    section_header("⚔️", "Competitor Analysis")
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.markdown("""
    <div class="comp-row comp-header">
        <div>Company</div><div>Description</div><div>Funding</div><div>Pricing</div>
    </div>
    """, unsafe_allow_html=True)
    for c in competitors:
        weaknesses = ", ".join(c.get("weaknesses", []))
        st.markdown(f"""
        <div class="comp-row">
            <div>
                <div style="font-weight:600;font-family:'Syne',sans-serif;font-size:15px;">{c.get('name','')}</div>
                <div style="font-size:11px;color:var(--muted);margin-top:4px;">🔓 Gap: {weaknesses[:60] + '...' if len(weaknesses) > 60 else weaknesses}</div>
            </div>
            <div style="color:#b0b0c8;font-size:13px;">{c.get('description','')}</div>
            <div><span class="tag tag-gold">{c.get('funding','N/A')}</span></div>
            <div style="font-size:13px;color:#b0b0c8;">{c.get('pricing_model','N/A')}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_revenue_models(data: dict):
    models = data.get("revenue_models", [])
    if not models:
        return
    section_header("💰", "Revenue Models")
    cols = st.columns(min(len(models), 3))
    for i, model in enumerate(models[:3]):
        with cols[i]:
            pros = "".join(f'<div style="font-size:12px;color:#00d4aa;margin:3px 0;">✓ {p}</div>' for p in model.get("pros", []))
            cons = "".join(f'<div style="font-size:12px;color:#ff6b6b;margin:3px 0;">✗ {c}</div>' for c in model.get("cons", []))
            st.markdown(f"""
            <div class="info-card">
                <div class="card-title">{model.get('model_name','')}</div>
                <div style="font-size:13px;color:#b0b0c8;margin-bottom:12px;">{model.get('description','')}</div>
                <div style="margin-bottom:8px;">
                    <span style="font-size:11px;color:var(--muted);">PROJECTED MRR</span>
                    <div style="font-family:'Syne',sans-serif;font-size:1.1rem;font-weight:700;color:var(--accent2);">{model.get('projected_monthly_revenue','—')}</div>
                </div>
                <div style="font-size:12px;color:var(--muted);margin-bottom:8px;">⏱ {model.get('time_to_revenue','—')}</div>
                {pros}
                {cons}
            </div>
            """, unsafe_allow_html=True)


def render_moats(data: dict):
    moats = data.get("business_moats", [])
    if not moats:
        return
    section_header("🏰", "Business Moat Analysis")
    for m in moats:
        strength_color = {"Strong": "#00d4aa", "Moderate": "#6c63ff", "Weak": "#f5c518"}.get(m.get("strength", "Moderate"), "#6c63ff")
        score = m.get("defensibility_score", 60)
        st.markdown(f"""
        <div class="info-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                <div>
                    <div style="font-family:'Syne',sans-serif;font-size:1rem;font-weight:700;">{m.get('moat_type','')}</div>
                    <span class="tag" style="background:rgba(255,255,255,0.05);color:{strength_color};border-color:{strength_color}33;">{m.get('strength','')}</span>
                </div>
                <div style="font-family:'Syne',sans-serif;font-size:2rem;font-weight:800;color:{strength_color};">{score:.0f}</div>
            </div>
            <div style="font-size:13px;color:#b0b0c8;">{m.get('description','')}</div>
        </div>
        """, unsafe_allow_html=True)


def render_growth_strategy(data: dict):
    strategies = data.get("growth_strategies", [])
    if not strategies:
        return
    section_header("🗺️", "Growth Strategy Roadmap")
    colors = ["#6c63ff", "#00d4aa", "#f5c518"]
    for i, s in enumerate(strategies):
        color = colors[i % len(colors)]
        actions_html = "".join(f'<div class="swot-item">{a}</div>' for a in s.get("actions", []))
        kpis_html = "".join(f'<span class="tag">{k}</span>' for k in s.get("kpis", []))
        st.markdown(f"""
        <div class="timeline-item">
            <div class="timeline-dot" style="background:rgba({','.join(str(int(color.lstrip('#')[i:i+2], 16)) for i in (0,2,4))},0.15);color:{color};">
                {i+1}
            </div>
            <div class="timeline-content">
                <div class="info-card">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <div style="font-family:'Syne',sans-serif;font-weight:700;color:{color};">{s.get('phase','')}</div>
                        <div style="font-size:12px;color:var(--muted);">💰 {s.get('estimated_cost','')}</div>
                    </div>
                    {actions_html}
                    <div style="margin-top:10px;">{kpis_html}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)


def render_gtm(data: dict):
    gtm = data.get("go_to_market", {})
    if not gtm:
        return
    section_header("🎯", "Go-to-Market Strategy")
    c1, c2 = st.columns(2)
    with c1:
        channels = "".join(f'<span class="tag tag-green">{ch}</span>' for ch in gtm.get("primary_channels", []))
        partners = "".join(f'<span class="tag">{p}</span>' for p in gtm.get("partnership_opportunities", []))
        st.markdown(f"""
        <div class="info-card">
            <div class="card-title">Launch Strategy</div>
            <div style="font-size:13px;color:#b0b0c8;margin-bottom:12px;">{gtm.get('launch_strategy','')}</div>
            <div class="card-title" style="margin-top:12px;">Primary Channels</div>
            {channels}
            <div class="card-title" style="margin-top:12px;">Partnership Opportunities</div>
            {partners}
        </div>
        """, unsafe_allow_html=True)
    with c2:
        milestones = gtm.get("milestones", [])
        ms_html = "".join(f"""
        <div style="display:flex;gap:12px;padding:10px 0;border-bottom:1px solid var(--border);">
            <span class="tag tag-gold" style="white-space:nowrap;">{m.get('month','')}</span>
            <div style="font-size:13px;color:#b0b0c8;">{m.get('goal','')}</div>
        </div>
        """ for m in milestones)
        st.markdown(f"""
        <div class="info-card">
            <div class="card-title">Milestone Roadmap</div>
            {ms_html}
            <div style="margin-top:12px;"><div class="card-title">Pricing Strategy</div><div style="font-size:13px;color:#b0b0c8;">{gtm.get('pricing_strategy','')}</div></div>
        </div>
        """, unsafe_allow_html=True)


def render_risks(data: dict):
    risks = data.get("risk_factors", [])
    if not risks:
        return
    section_header("⚠️", "Risk Analysis")
    for r in risks:
        st.markdown(f"""
        <div class="info-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px;">
                <div style="font-size:14px;font-weight:500;max-width:70%;">{r.get('risk','')}</div>
                <div style="display:flex;gap:8px;align-items:center;">
                    <span style="font-size:12px;color:var(--muted);">{r.get('probability','')}</span>
                    {risk_badge(r.get('level','Medium'))}
                </div>
            </div>
            <div style="font-size:13px;color:#8888aa;">🛡️ <em>{r.get('mitigation','')}</em></div>
        </div>
        """, unsafe_allow_html=True)


def render_pitch(data: dict):
    pitch = data.get("ai_pitch", "")
    if not pitch:
        return
    section_header("🎤", "AI-Generated Investor Pitch")
    st.markdown(f"""
    <div class="pitch-box">
        <div class="pitch-text">{pitch}</div>
    </div>
    """, unsafe_allow_html=True)


def render_recommendations(data: dict):
    recs = data.get("ai_recommendations", [])
    if not recs:
        return
    section_header("🧠", "AI Recommendations")
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    for i, rec in enumerate(recs, 1):
        st.markdown(f"""
        <div class="rec-item">
            <div class="rec-num">{i}</div>
            <div class="rec-text">{rec}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


# ─── Main App ──────────────────────────────────────────────────────────────────

def main():
    render_hero()

    submit, idea, industry, target_market, budget, location = render_input_form()

    if submit:
        if not idea or len(idea.strip()) < 10:
            st.warning("Please describe your startup idea in at least 10 characters.")
            return

        with st.spinner("🔬 Running AI analysis... This takes 15-30 seconds."):
            t0 = time.time()
            data = call_api({
                "idea": idea.strip(),
                "industry": industry,
                "target_market": target_market,
                "budget": budget,
                "location": location,
            })

        if data:
            elapsed = time.time() - t0
            st.markdown(f'<div class="proc-time">⚡ Analysis completed in {elapsed:.1f}s</div>', unsafe_allow_html=True)
            st.divider()

            render_score_overview(data)
            st.divider()
            render_market_analysis(data)
            st.divider()
            render_swot(data)
            st.divider()
            render_competitors(data)
            st.divider()
            render_revenue_models(data)
            st.divider()
            render_moats(data)
            st.divider()
            render_growth_strategy(data)
            st.divider()
            render_gtm(data)
            st.divider()
            render_risks(data)
            st.divider()
            render_pitch(data)
            st.divider()
            render_recommendations(data)

            # JSON download
            st.divider()
            section_header("📥", "Export Report")
            st.download_button(
                label="⬇️ Download Full Analysis (JSON)",
                data=json.dumps(data, indent=2),
                file_name=f"startup_analysis_{int(time.time())}.json",
                mime="application/json",
            )

    else:
        # Landing state
        st.markdown("""
        <div style="text-align:center;padding:4rem 2rem;color:var(--muted);">
            <div style="font-size:4rem;margin-bottom:1rem;">🚀</div>
            <div style="font-family:'Syne',sans-serif;font-size:1.3rem;font-weight:700;color:var(--text);margin-bottom:0.5rem;">Ready to Validate Your Vision?</div>
            <div style="max-width:500px;margin:0 auto;line-height:1.8;">
                Enter your startup idea above and get a comprehensive VC-grade analysis powered by GPT-4o and RAG technology.
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
