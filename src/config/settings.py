from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    # App
    app_name: str = Field(default="AiResearchAndReportGenerationAgent", env="APP_NAME")
    app_env: str = Field(default="development", env="APP_ENV")
    debug: bool = Field(default=False, env="DEBUG")

    # Sarvam AI
    sarvam_api_key: str = Field(..., env="SARVAM_API_KEY")
    sarvam_api_base_url: str = Field(
        default="https://api.sarvam.ai/v1", env="SARVAM_API_BASE_URL"
    )
    sarvam_model: str = Field(default="sarvam-30b", env="SARVAM_MODEL")

    # Tavily
    tavily_api_key: str = Field(..., env="TAVILY_API_KEY")

    # Agent Config
    max_iterations: int = Field(default=10, env="MAX_ITERATIONS")
    max_search_results: int = Field(default=5, env="MAX_SEARCH_RESULTS")
    cost_budget_per_run: float = Field(default=1.0, env="COST_BUDGET_PER_RUN")

    # API
    api_host: str = Field(default="0.0.0.0", env="API_HOST")
    api_port: int = Field(default=8000, env="API_PORT")

    # Paths
    reports_dir: str = Field(default="data/reports", env="REPORTS_DIR")
    checkpoints_dir: str = Field(default="data/checkpoints", env="CHECKPOINTS_DIR")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Singleton
settings = Settings()

# Ensure data directories exist
os.makedirs(settings.reports_dir, exist_ok=True)
os.makedirs(settings.checkpoints_dir, exist_ok=True)