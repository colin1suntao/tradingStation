from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"


class LLMConfig(BaseModel):
    provider: LLMProvider = Field(default=LLMProvider.OPENAI, description="LLM provider")
    model: str = Field(default="gpt-4o", description="Model name")
    api_key: Optional[str] = Field(default=None, description="API key (can also use env var)")
    temperature: float = Field(default=0.1, ge=0, le=2, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, description="Max tokens for generation")
    base_url: Optional[str] = Field(default=None, description="Base URL for API endpoint")


class LLMTestRequest(BaseModel):
    provider: LLMProvider = Field(default=LLMProvider.OPENAI)
    model: str = Field(default="gpt-4o")
    api_key: Optional[str] = None
    message: str = Field(default="Hello, how are you?")


class LLMTestResponse(BaseModel):
    success: bool
    response: str
    model: str
    provider: str
    latency_ms: Optional[float] = None
    error: Optional[str] = None


class AgentConfig(BaseModel):
    deep_think_model: str = Field(default="gpt-4o", description="Model for complex reasoning")
    quick_think_model: str = Field(default="gpt-4o-mini", description="Model for quick tasks")
    max_debate_rounds: int = Field(default=1, ge=1, le=10, description="Max debate rounds")
    max_risk_discuss_rounds: int = Field(default=1, ge=1, le=10, description="Max risk discuss rounds")


class TradingAgentsConfig(BaseModel):
    llm: LLMConfig = Field(default_factory=LLMConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    selected_analysts: List[str] = Field(
        default=["market", "social", "news", "fundamentals"],
        description="List of analysts to use"
    )
    checkpoint_enabled: bool = Field(default=False, description="Enable checkpoint resume")
    output_language: str = Field(default="English", description="Output language")