<div align="center">

# 🚀 VentureIQ — AI Startup Validator & Business Intelligence Engine

<img src="https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/FastAPI-0.111-009688?style=for-the-badge&logo=fastapi&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-1.35-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/LangChain-0.2-1C3C3C?style=for-the-badge"/>
<img src="https://img.shields.io/badge/FAISS-Vector_DB-4285F4?style=for-the-badge"/>
<img src="https://img.shields.io/badge/LLaMA_3.3-70B-F55036?style=for-the-badge"/>
<img src="https://img.shields.io/badge/Tests-11%2F11_Passing-brightgreen?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>

<br/><br/>

**A production-grade, full-stack AI platform that validates startup ideas and generates VC-level business intelligence reports in under 30 seconds.**

*Powered by LLaMA 3.3 70B · LangChain · FAISS RAG · FastAPI · Streamlit*

<br/>

[🔴 Live Demo](#) · [📖 API Docs](http://localhost:8000/docs) · [⭐ Star this repo](#)

</div>

---

## 📌 What Makes This Project Stand Out

This is **not** a Jupyter notebook or a simple API wrapper.

VentureIQ is a complete, production-ready AI system featuring:

- 🏗️ **Clean modular architecture** — separated API, services, models, and UI layers
- 🔁 **Multi-step LLM reasoning** — structured chain-of-thought with validated JSON output
- 🗄️ **RAG pipeline** — FAISS vector database with 20+ curated business knowledge chunks
- 🔌 **Dual LLM support** — auto-detects OpenAI vs Groq (free) by API key prefix
- ⚡ **Async FastAPI backend** — with middleware, retry logic, and error handling
- 🧪 **11/11 unit tests passing** — scoring engine, JSON parsing, model validation
- 🎨 **Custom SaaS UI** — 900+ lines of Streamlit with production CSS

---

## 🎯 Core Features

| Module | Description |
|--------|-------------|
| 🧠 **AI Startup Validator** | 8-dimension scoring with success probability percentage |
| 📈 **Market Intelligence** | TAM / SAM / SOM sizing, growth rate, trends, pain points |
| ⚔️ **Competitor Analysis** | Real competitors mapped with funding, pricing, weakness gaps |
| 🔲 **SWOT Analysis** | AI-generated strategic analysis across all 4 quadrants |
| 🏰 **Business Moat Analysis** | Data moat, network effects, switching costs scored |
| 💰 **Revenue Model Engine** | 3+ monetization models with projected MRR timelines |
| 🗺️ **Growth Strategy Roadmap** | 3-phase plan: Launch → Growth → Scale with KPIs and budgets |
| 🎯 **Go-to-Market Strategy** | Channels, milestones, pricing strategy, partnerships |
| ⚠️ **Risk Analysis** | Risks with probability scores and mitigation strategies |
| 🎤 **AI Pitch Generator** | Y Combinator-style investor pitch auto-generated |
| 📥 **JSON Export** | Full analysis downloadable as structured JSON |

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      VENTUREIQ PLATFORM                          │
│                                                                   │
│   ┌─────────────────┐   REST API   ┌─────────────────────────┐  │
│   │    Streamlit     │◄────────────►│      FastAPI Backend     │  │
│   │    Frontend      │             │   /api/v1/analyze        │  │
│   │  (Custom CSS UI) │             │   /api/v1/health         │  │
│   └─────────────────┘             └────────────┬────────────┘  │
│                                                 │                │
│                                   ┌─────────────▼────────────┐  │
│                                   │   Analysis Orchestrator   │  │
│                                   │  (Pipeline Coordinator)   │  │
│                                   └──────┬──────────┬─────────┘  │
│                                          │          │             │
│                          ┌───────────────▼──┐  ┌───▼──────────┐ │
│                          │   LLM Service    │  │ Vector Store │ │
│                          │  LangChain +     │  │ FAISS + RAG  │ │
│                          │  LLaMA 3.3 70B   │  │ 20 KB chunks │ │
│                          └───────────────┬──┘  └──────────────┘ │
│                                          │                        │
│                          ┌───────────────▼──────────────────┐   │
│                          │       Scoring Engine              │   │
│                          │   VC-Weighted Algorithm           │   │
│                          │   8 dimensions → Grade A+ to D    │   │
│                          └──────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
ai-startup-validator/
│
├── 📂 backend/                        # FastAPI Backend
│   ├── 📂 api/
│   │   └── routes.py                  # REST endpoints with OpenAPI docs
│   ├── 📂 core/
│   │   ├── config.py                  # Pydantic Settings — type-safe env
│   │   └── logger.py                  # Loguru — rotating production logs
│   ├── 📂 models/
│   │   └── schemas.py                 # 15+ Pydantic data models
│   ├── 📂 services/
│   │   ├── llm_service.py             # LangChain + LLaMA 3.3 / GPT-4o
│   │   ├── scoring_service.py         # Proprietary VC-weighted scoring
│   │   ├── vector_store.py            # FAISS RAG knowledge base
│   │   └── analysis_service.py        # End-to-end pipeline orchestration
│   └── main.py                        # FastAPI app factory + middleware
│
├── 📂 frontend/
│   └── app.py                         # Streamlit SaaS UI (900+ lines)
│
├── 📂 data/
│   ├── embeddings/                    # FAISS index storage
│   └── knowledge_base/               # Business knowledge documents
│
├── 📂 tests/
│   ├── test_core.py                   # Unit tests
│   └── test_logic.py                  # Logic tests — 11/11 passing ✅
│
├── 📂 logs/                           # Auto-generated rotating logs
├── .env.example                       # Environment config template
├── .gitignore                         # Git ignore rules
├── requirements.txt                   # All Python dependencies
└── README.md                          # This file
```

---

## ⚙️ Technology Stack

### 🔧 Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| Python | 3.11+ | Core language |
| FastAPI | 0.111 | Async REST API with auto Swagger docs |
| Uvicorn | 0.29 | ASGI production server |
| Pydantic v2 | 2.7 | Type-safe data validation and settings |
| Loguru | 0.7 | Structured logging with rotation |
| Tenacity | 8.3 | Exponential backoff retry for LLM calls |

### 🤖 AI / LLM Layer
| Technology | Purpose |
|-----------|---------|
| LangChain 0.2 | LLM orchestration and prompt chaining |
| LLaMA 3.3 70B (Groq) | Free, fast primary reasoning model |
| OpenAI GPT-4o | Alternative paid LLM (auto-detected) |
| FAISS | Vector similarity search |
| SentenceTransformers | Text embeddings (`all-MiniLM-L6-v2`) |

### 🎨 Frontend
| Technology | Purpose |
|-----------|---------|
| Streamlit 1.35 | Interactive web UI |
| Custom CSS | Dark SaaS theme with animations and score rings |
| HTTPX | Async HTTP client for API communication |

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Free Groq API key from [console.groq.com](https://console.groq.com) *(no credit card required)*

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/ai-startup-validator.git
cd ai-startup-validator
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your API key:
```env
OPENAI_API_KEY=gsk_your_groq_key_here
OPENAI_MODEL=llama-3.3-70b-versatile
APP_ENV=development
LOG_LEVEL=INFO
API_PORT=8000
MAX_TOKENS_PER_REQUEST=4000
```

### 5. Run the Application

**Terminal 1 — Backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```

**Terminal 2 — Frontend:**
```bash
streamlit run frontend/app.py
```

### 6. Open in Browser
| Service | URL |
|---------|-----|
| 🎨 Frontend UI | http://localhost:8501 |
| 📖 API Swagger Docs | http://localhost:8000/docs |
| ❤️ Health Check | http://localhost:8000/api/v1/health |

---

## 🔌 API Reference

### `POST /api/v1/analyze`

**Request:**
```json
{
  "idea": "An AI platform that helps Indian restaurants reduce food waste using demand prediction",
  "industry": "FoodTech / AI",
  "target_market": "Small restaurants in India",
  "budget": "$25,000",
  "location": "India"
}
```

**Response:** Full `StartupValidationResponse` containing all 12 analysis sections, scores, and AI-generated pitch.

### `GET /api/v1/health`
```json
{
  "status": "operational",
  "version": "1.0.0",
  "environment": "development"
}
```

---

## 🤖 AI System Design

### Multi-Step LLM Reasoning
Each analysis runs a carefully engineered prompt that forces the LLM to reason across 12 output dimensions simultaneously — market sizing, competitive positioning, risk evaluation, and more — returning structured, validated JSON parsed by strict Pydantic models.

### RAG Knowledge Base
Before every analysis, the FAISS vector store retrieves the top-4 most relevant business knowledge chunks (from 20 curated entries covering VC criteria, PMF, unit economics, go-to-market frameworks) and injects them as context, significantly improving analysis quality.

### Proprietary Scoring Algorithm
```
Composite Score =
    Market Demand Score       × 0.25   ← Most critical VC signal
  + Problem-Solution Fit      × 0.20
  + Monetization Potential    × 0.20
  + Scalability Score         × 0.15
  + Market Opportunity Score  × 0.10
  + Investor Readiness Score  × 0.05
  + Risk Score                × 0.05
```

Grades: **A+ (≥90) · A (≥80) · B+ (≥70) · B (≥60) · C (≥50) · D (<50)**

### Auto Provider Detection
```python
# Zero config switching between free (Groq) and paid (OpenAI)
if api_key.startswith("gsk_"):
    base_url = "https://api.groq.com/openai/v1"  # Free LLaMA 3.3
else:
    base_url = None  # OpenAI GPT-4o
```

---

## ✅ Test Suite

```
=======================================================
  VentureIQ — Core Logic Test Suite
=======================================================

  ✓ Scoring: Grade calculation
  ✓ Scoring: Normalize values
  ✓ Scoring: Weighted composite
  ✓ LLM: JSON response parsing
  ✓ LLM: Fenced JSON parsing
  ✓ Utils: safe_list / safe_str helpers
  ✓ Model: Risk level enum mapping
  ✓ UI: Score color thresholds
  ✓ UI: Grade color mapping
  ✓ Model: Market analysis defaults
  ✓ Model: Verdict templates complete

=======================================================
  Results: 11 passed, 0 failed ✅
=======================================================
```

```bash
# Run tests yourself
python tests/test_logic.py
```

---

## 🌍 Deployment

### Docker
```bash
docker build -t ventureiq .
docker run -p 8000:8000 --env-file .env ventureiq
```

### Cloud (Free Tiers Available)
| Platform | Deploys | Notes |
|----------|---------|-------|
| **Railway** | Backend | Free $5 credit monthly |
| **Render** | Backend | Free tier available |
| **Streamlit Cloud** | Frontend | Completely free |
| **Hugging Face Spaces** | Full App | Free with GPU |

---

## 🗺️ Roadmap

- [x] Core AI validation engine
- [x] FAISS RAG knowledge base
- [x] Groq free LLM integration
- [x] Production Streamlit SaaS UI
- [x] 11/11 unit tests passing
- [ ] PDF report generation with ReportLab
- [ ] User auth and saved analyses history
- [ ] Live web scraping for real competitor data
- [ ] Multi-language support (Hindi, Tamil, Telugu)
- [ ] WhatsApp bot integration for idea submission

---

## 👤 About

**Sudha** — AI/ML Developer passionate about building production-grade intelligent systems.

**Skills demonstrated:**
- Full-stack AI application development (not just notebooks)
- LLM prompt engineering with structured output parsing
- RAG pipeline design with FAISS vector search
- REST API design with FastAPI and Pydantic
- Clean architecture with proper separation of concerns
- Error handling, retry logic, and logging at production scale
- Multi-provider LLM integration (OpenAI / Groq)
- Custom SaaS UI with Streamlit

📧 **Email:** your.email@gmail.com
💼 **LinkedIn:** linkedin.com/in/yourprofile
🐙 **GitHub:** github.com/yourusername

---

## 📄 License

MIT License — free to use, fork, and build upon with attribution.

---

<div align="center">

**If this project impressed you, please ⭐ star the repo!**

*Built end-to-end with Python · LangChain · FAISS · FastAPI · Streamlit*

</div>