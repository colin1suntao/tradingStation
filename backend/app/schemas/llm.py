from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any, Callable
from enum import Enum


class LLMProvider(str, Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    OLLAMA = "ollama"
    OPENAI_COMPATIBLE = "openai_compatible"
    CUSTOM = "custom"


class LLMConfig(BaseModel):
    provider: LLMProvider = Field(default=LLMProvider.OPENAI, description="LLM provider")
    model: str = Field(default="gpt-4o", description="Model name")
    api_key: Optional[str] = Field(default=None, description="API key (can also use env var)")
    temperature: float = Field(default=0.1, ge=0, le=2, description="Temperature for generation")
    max_tokens: Optional[int] = Field(default=None, description="Max tokens for generation")
    base_url: Optional[str] = Field(default=None, description="Base URL for API endpoint")
    timeout: Optional[int] = Field(default=120, description="Request timeout in seconds")

    @field_validator('base_url')
    @classmethod
    def validate_base_url(cls, v, info):
        if v and not v.startswith(('http://', 'https://')):
            return f"http://{v}"
        return v


class LLMTestRequest(BaseModel):
    provider: str = Field(default="openai")
    model: str = Field(default="gpt-4o-mini")
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    message: str = Field(default="Hello, how are you?")
    temperature: float = Field(default=0.1)


class LLMTestResponse(BaseModel):
    success: bool
    response: str
    model: str
    provider: str
    latency_ms: Optional[float] = None
    error: Optional[str] = None


class CustomProviderConfig(BaseModel):
    name: str = Field(..., description="Unique name for the custom provider")
    base_url: str = Field(..., description="Base URL of the custom API endpoint")
    model: str = Field(default="", description="Default model name")
    api_key: Optional[str] = Field(default=None, description="API key if required")
    requires_api_key: bool = Field(default=False, description="Whether this provider requires an API key")
    extra_headers: Optional[Dict[str, str]] = Field(default=None, description="Extra headers to include in requests")


class CustomProviderRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')
    base_url: str = Field(..., description="Base URL of the custom API endpoint")
    model: str = Field(default="", description="Default model name")
    api_key: Optional[str] = Field(default=None)
    requires_api_key: bool = Field(default=False)
    extra_headers: Optional[Dict[str, str]] = None
    test_message: str = Field(default="Hello, this is a test. Please respond with 'OK' if you can read this message.")


class CustomProviderResponse(BaseModel):
    success: bool
    name: str
    message: str
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


class ProviderInfo(BaseModel):
    name: str
    display_name: str
    requires_api_key: bool
    requires_base_url: bool
    supports_streaming: bool
    models: List[str]
    description: str


class ProviderListResponse(BaseModel):
    providers: List[ProviderInfo]
    custom_providers: List[str]