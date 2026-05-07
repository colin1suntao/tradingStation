from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.schemas.llm import (
    LLMTestRequest,
    LLMTestResponse,
    LLMProvider,
    TradingAgentsConfig,
    AgentConfig,
    LLMConfig
)
from app.services.llm_service import llm_service

router = APIRouter(prefix="/llm", tags=["LLM Configuration"])


@router.get("/models/{provider}", summary="List available models for provider")
async def list_models(provider: str):
    models = llm_service.list_available_models(provider)
    return {
        "provider": provider,
        "models": models
    }


@router.post("/test", response_model=LLMTestResponse, summary="Test LLM connection")
async def test_llm(request: LLMTestRequest):
    result = await llm_service.test_llm(
        provider=request.provider.value,
        model=request.model,
        api_key=request.api_key,
        message=request.message
    )
    return result


@router.post("/config/validate", summary="Validate LLM configuration")
async def validate_config(config: TradingAgentsConfig):
    try:
        result = await llm_service.test_llm(
            provider=config.llm.provider.value,
            model=config.llm.model,
            api_key=config.llm.api_key,
            message="Hello, this is a test message."
        )
        
        return {
            "valid": result.success,
            "provider": config.llm.provider.value,
            "model": config.llm.model,
            "message": "Connection successful" if result.success else result.error
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/providers", summary="List supported LLM providers")
async def list_providers():
    return {
        "providers": [
            {
                "name": "openai",
                "display_name": "OpenAI",
                "models": llm_service.list_available_models("openai"),
                "requires_api_key": True
            },
            {
                "name": "anthropic",
                "display_name": "Anthropic (Claude)",
                "models": llm_service.list_available_models("anthropic"),
                "requires_api_key": True
            },
            {
                "name": "google",
                "display_name": "Google (Gemini)",
                "models": llm_service.list_available_models("google"),
                "requires_api_key": True
            }
        ]
    }


@router.post("/config/save", summary="Save LLM configuration")
async def save_config(config: TradingAgentsConfig):
    return {
        "success": True,
        "config": {
            "provider": config.llm.provider.value,
            "model": config.llm.model,
            "deep_think_model": config.agent.deep_think_model,
            "quick_think_model": config.agent.quick_think_model,
            "max_debate_rounds": config.agent.max_debate_rounds,
            "max_risk_discuss_rounds": config.agent.max_risk_discuss_rounds,
            "selected_analysts": config.selected_analysts
        }
    }