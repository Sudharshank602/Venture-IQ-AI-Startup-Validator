"""
Vector Store Service (RAG)
FAISS-based vector database for business knowledge retrieval.
Enables Retrieval-Augmented Generation for richer analysis.
"""

import os
import json
from pathlib import Path
from typing import List, Optional

from backend.core.config import settings
from backend.core.logger import logger

# Graceful import handling for deployment flexibility
try:
    import faiss
    import numpy as np
    from sentence_transformers import SentenceTransformer
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    logger.warning("FAISS/SentenceTransformers not available. RAG features disabled.")


BUSINESS_KNOWLEDGE_BASE = [
    # Market sizing frameworks
    "Total Addressable Market (TAM) represents the total revenue opportunity for a product or service. SAM (Serviceable Addressable Market) is the portion you can realistically serve. SOM (Serviceable Obtainable Market) is what you can capture in the near term.",
    "Product-Market Fit (PMF) is achieved when at least 40% of surveyed users say they would be 'very disappointed' if they could no longer use your product (Sean Ellis test).",
    "Network effects occur when a product becomes more valuable as more people use it. Examples: Uber, Airbnb, LinkedIn. Network effects create powerful moats.",
    "SaaS metrics: MRR (Monthly Recurring Revenue), ARR (Annual Recurring Revenue), Churn Rate, LTV (Lifetime Value), CAC (Customer Acquisition Cost), LTV:CAC ratio should be 3:1 or higher.",
    "Venture capital investment stages: Pre-seed ($50K-$500K), Seed ($500K-$3M), Series A ($3M-$15M), Series B ($15M-$50M), Series C ($50M-$100M+).",
    "Customer segments: B2B (Business to Business), B2C (Business to Consumer), B2B2C (platform selling through businesses to consumers), D2C (Direct to Consumer).",
    "Unit economics: Gross margin should be 60%+ for software, 40%+ for marketplace. Payback period should be under 18 months for healthy SaaS.",
    "Lean Startup methodology: Build-Measure-Learn loop. Create MVP (Minimum Viable Product), validate assumptions quickly, pivot or persevere based on data.",
    "Go-to-market strategies: Product-Led Growth (PLG), Sales-Led Growth (SLG), Marketing-Led Growth (MLG). PLG companies like Slack and Dropbox use the product itself as main acquisition channel.",
    "Competitive moats: Brand, Network Effects, Switching Costs, Cost Advantages, Efficient Scale, Intangible Assets (patents, licenses, regulatory approvals).",
    "Startup failure reasons: 35% no market need, 20% ran out of cash, 14% wrong team, 14% outcompeted, 10% pricing/cost issues, 8% poor product, 7% need business model.",
    "Revenue models: Subscription (SaaS), Transaction fee (marketplace 5-30%), Freemium (2-5% conversion), Advertising, Licensing, Professional services.",
    "Indian startup ecosystem: India has 100+ unicorns. Key sectors: Fintech, EdTech, HealthTech, AgriTech, SaaS. Peak funding was 2021-2022, now more disciplined.",
    "AI startup trends 2024-2025: Vertical AI (industry-specific), AI agents, RAG applications, AI infrastructure, multimodal AI, edge AI. Enterprise AI adoption accelerating.",
    "Pricing strategies: Cost-plus, Value-based, Competitive, Penetration (low entry price), Premium/Luxury, Freemium, Usage-based. Value-based pricing maximizes revenue.",
    "Growth hacking: Viral loops, referral programs, SEO, content marketing, community building, product integrations, partnership channels.",
    "Investor readiness checklist: Clear problem statement, proven market demand, working MVP or prototype, early traction (revenue or users), scalable business model, strong founding team.",
    "SWOT Analysis: Internal factors (Strengths, Weaknesses), External factors (Opportunities, Threats). Essential strategic planning tool for startups.",
    "Customer Development: Steve Blank's method of interviewing customers before building. Validate problem, solution, and business model assumptions through 100+ customer conversations.",
    "Platform vs Product: Platforms create network effects and can monetize third-party developers. Products are standalone. Platforms typically have higher valuations.",
]


class VectorStoreService:
    """FAISS-backed knowledge base for RAG-enhanced startup analysis."""

    def __init__(self):
        self.available = FAISS_AVAILABLE
        self.index = None
        self.encoder = None
        self.documents = BUSINESS_KNOWLEDGE_BASE

        if self.available:
            self._initialize()

    def _initialize(self):
        """Initialize encoder and FAISS index."""
        try:
            logger.info("Initializing Vector Store...")
            self.encoder = SentenceTransformer('all-MiniLM-L6-v2')
            self._build_index()
            logger.info(f"Vector Store ready with {len(self.documents)} knowledge chunks.")
        except Exception as e:
            logger.error(f"Vector Store initialization failed: {e}")
            self.available = False

    def _build_index(self):
        """Build FAISS index from knowledge base."""
        embeddings = self.encoder.encode(self.documents)
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype(np.float32))

    def retrieve_context(self, query: str, top_k: int = 4) -> str:
        """Retrieve relevant business knowledge for a query."""
        if not self.available or self.index is None:
            return ""
        try:
            query_vec = self.encoder.encode([query]).astype(np.float32)
            distances, indices = self.index.search(query_vec, top_k)
            retrieved = [self.documents[i] for i in indices[0] if i < len(self.documents)]
            return "\n\n".join(retrieved)
        except Exception as e:
            logger.error(f"Vector retrieval failed: {e}")
            return ""

    def get_status(self) -> dict:
        return {
            "available": self.available,
            "document_count": len(self.documents),
            "index_type": "FAISS FlatL2" if self.available else "Disabled",
        }


vector_store = VectorStoreService()
