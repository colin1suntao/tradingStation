from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.schemas.llm import (
    LLMTestRequest,
    LLMTestResponse,
    LLMProvider,
    TradingAgentsConfig,
    AgentConfig,
    LLMConfig,
    CustomProviderRequest,
    CustomProviderResponse,
)
from app.services.llm_service import llm_service

router = APIRouter(prefix="/llm", tags=["LLM Configuration"])


@router.get("/providers", summary="List all LLM providers")
async def list_providers():
    info = llm_service.get_providers_info()
    return {
        "standard_providers": info["providers"],
        "custom_providers": info["custom_providers"]
    }


@router.get("/models/{provider}", summary="List available models for provider")
async def list_models(provider: str):
    models = llm_service.list_available_models(provider)
    custom_providers = llm_service.list_custom_providers()
    
    return {
        "provider": provider,
        "models": models,
        "is_custom": provider.lower() in custom_providers
    }


@router.post("/test", response_model=LLMTestResponse, summary="Test LLM connection")
async def test_llm(request: LLMTestRequest):
    result = await llm_service.test_llm(
        provider=request.provider,
        model=request.model,
        api_key=request.api_key,
        base_url=request.base_url,
        message=request.message,
        temperature=request.temperature
    )
    return result


@router.post("/config/validate", summary="Validate LLM configuration")
async def validate_config(config: TradingAgentsConfig):
    try:
        result = await llm_service.test_llm(
            provider=config.llm.provider.value,
            model=config.llm.model,
            api_key=config.llm.api_key,
            base_url=config.llm.base_url,
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


@router.post("/custom/register", response_model=CustomProviderResponse, summary="Register a custom LLM provider")
async def register_custom_provider(request: CustomProviderRequest):
    result = await llm_service.register_custom_provider(request)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result


@router.delete("/custom/{provider_name}", summary="Unregister a custom LLM provider")
async def unregister_custom_provider(provider_name: str):
    success = llm_service.unregister_custom_provider(provider_name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Custom provider '{provider_name}' not found")
    return {
        "success": True,
        "message": f"Custom provider '{provider_name}' unregistered successfully"
    }


@router.get("/custom", summary="List registered custom providers")
async def list_custom_providers():
    custom_providers = llm_service.list_custom_providers()
    return {
        "custom_providers": custom_providers,
        "count": len(custom_providers)
    }


@router.post("/custom/{provider_name}/test", summary="Test a custom provider connection")
async def test_custom_provider(provider_name: str, model: str = "default"):
    custom_providers = llm_service.list_custom_providers()
    if provider_name.lower() not in custom_providers:
        raise HTTPException(status_code=404, detail=f"Custom provider '{provider_name}' not found")
    
    result = await llm_service.test_llm(
        provider=provider_name,
        model=model,
        message="Hello, this is a test message."
    )
    return result


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


@router.get("/ollama/list", summary="List available models from Ollama")
async def list_ollama_models(base_url: str = "http://localhost:11434"):
    try:
        import requests
        response = requests.get(f"{base_url}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                "success": True,
                "models": [m.get("name") for m in data.get("models", [])],
                "base_url": base_url
            }
        else:
            return {
                "success": False,
                "error": f"Ollama returned status {response.status_code}",
                "base_url": base_url
            }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "base_url": base_url
        }