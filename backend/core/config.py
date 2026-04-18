"""
Core Configuration Module
Centralized settings management using Pydantic BaseSettings.
"""

from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    # App
    APP_NAME: str = "AI Startup Validator & Business Intelligence Engine"
    APP_VERSION: str = "1.0.0"
    APP_ENV: str = "development"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"

    # OpenAI
    OPENAI_API_KEY: str = Field(default="", env="OPENAI_API_KEY")
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_EMBEDDING_MODEL: str = "text-embedding-3-small"

    # API Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000

    # Paths
    FAISS_INDEX_PATH: str = "data/embeddings/startup_knowledge.index"
    KNOWLEDGE_BASE_PATH: str = "data/knowledge_base/"
    REPORT_OUTPUT_DIR: str = "reports/"

    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE: int = 20
    MAX_TOKENS_PER_REQUEST: int = 4000

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
