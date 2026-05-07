import os
import time
from typing import Optional, Dict, Any, List
from app.llm import LLMClientFactory, LLMProviderRegistry, BaseLLMClient
from app.schemas.llm import LLMTestResponse, CustomProviderRequest, CustomProviderResponse


class LLMService:
    _custom_providers: Dict[str, Dict[str, Any]] = {}

    def __init__(self):
        self._clients: Dict[str, Any] = {}

    def get_client(
        self,
        provider: str = "openai",
        model: str = "gpt-4o",
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        base_url: Optional[str] = None,
        timeout: int = 120,
        **kwargs
    ):
        provider = provider.lower()
        cache_key = f"{provider}:{model}:{temperature}"
        
        if cache_key not in self._clients:
            resolved_api_key = api_key or self._get_api_key(provider)
            resolved_base_url = base_url or self._get_base_url(provider)
            
            if provider in self._custom_providers:
                custom_config = self._custom_providers[provider]
                resolved_base_url = resolved_base_url or custom_config.get("base_url")
                resolved_api_key = resolved_api_key or custom_config.get("api_key")
                model = model or custom_config.get("model", "")
            
            self._clients[cache_key] = LLMClientFactory.create_client(
                provider=provider,
                model=model,
                api_key=resolved_api_key,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=resolved_base_url,
                timeout=timeout,
                **kwargs
            )
        
        return self._clients[cache_key]

    def _get_api_key(self, provider: str) -> Optional[str]:
        env_vars = {
            "openai": "OPENAI_API_KEY",
            "anthropic": "ANTHROPIC_API_KEY",
            "google": "GOOGLE_API_KEY",
        }
        return os.getenv(env_vars.get(provider.lower(), ""))

    def _get_base_url(self, provider: str) -> Optional[str]:
        env_base_urls = {
            "openai": os.getenv("OPENAI_BASE_URL"),
            "ollama": os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        }
        return env_base_urls.get(provider.lower())

    async def test_llm(
        self,
        provider: str,
        model: str,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        message: str = "Hello, how are you?",
        temperature: float = 0.1
    ) -> LLMTestResponse:
        start_time = time.time()
        
        try:
            resolved_api_key = api_key
            resolved_base_url = base_url
            
            if provider in self._custom_providers:
                custom_config = self._custom_providers[provider]
                resolved_api_key = resolved_api_key or custom_config.get("api_key")
                resolved_base_url = resolved_base_url or custom_config.get("base_url")
                model = model or custom_config.get("model", "")
            else:
                resolved_api_key = resolved_api_key or self._get_api_key(provider)
                resolved_base_url = resolved_base_url or self._get_base_url(provider)
            
            client = self.get_client(
                provider=provider,
                model=model,
                api_key=resolved_api_key,
                base_url=resolved_base_url,
                temperature=temperature,
            )
            
            response = client.invoke([{"role": "user", "content": message}])
            
            latency_ms = (time.time() - start_time) * 1000
            
            return LLMTestResponse(
                success=True,
                response=response,
                model=model,
                provider=provider,
                latency_ms=round(latency_ms, 2),
            )
        except Exception as e:
            return LLMTestResponse(
                success=False,
                response="",
                model=model,
                provider=provider,
                error=str(e)
            )

    async def register_custom_provider(
        self, request: CustomProviderRequest
    ) -> CustomProviderResponse:
        try:
            test_client = self.get_client(
                provider="openai_compatible",
                model=request.model or "default",
                api_key=request.api_key,
                base_url=request.base_url,
            )
            
            response = test_client.invoke([
                {"role": "user", "content": request.test_message}
            ])
            
            self._custom_providers[request.name.lower()] = {
                "base_url": request.base_url,
                "model": request.model,
                "api_key": request.api_key,
                "requires_api_key": request.requires_api_key,
                "extra_headers": request.extra_headers,
            }
            
            return CustomProviderResponse(
                success=True,
                name=request.name,
                message=f"Custom provider '{request.name}' registered successfully. Test response: {response[:100]}..."
            )
        except Exception as e:
            return CustomProviderResponse(
                success=False,
                name=request.name,
                message="",
                error=str(e)
            )

    def unregister_custom_provider(self, name: str) -> bool:
        name = name.lower()
        if name in self._custom_providers:
            del self._custom_providers[name]
            
            keys_to_remove = [k for k in self._clients if k.startswith(f"{name}:")]
            for key in keys_to_remove:
                del self._clients[key]
            
            return True
        return False

    def list_custom_providers(self) -> List[str]:
        return list(self._custom_providers.keys())

    def list_available_models(self, provider: str = "openai") -> List[str]:
        models = {
            "openai": [
                "gpt-4o",
                "gpt-4o-mini",
                "gpt-4-turbo",
                "gpt-4",
                "gpt-3.5-turbo",
            ],
            "anthropic": [
                "claude-3-5-sonnet-latest",
                "claude-3-5-sonnet-20241022",
                "claude-3-opus-latest",
                "claude-3-opus-20240229",
                "claude-3-haiku-20240307",
            ],
            "google": [
                "gemini-1.5-pro",
                "gemini-1.5-flash",
                "gemini-1.5-pro-latest",
                "gemini-1.5-flash-latest",
                "gemini-1.0-pro",
            ],
            "ollama": [
                "llama3",
                "llama3.1",
                "llama3.2",
                "mistral",
                "mixtral",
                "codellama",
                "phi3",
                "qwen2",
                "qwen2.5",
                "deepseek-r1",
                "gemma2",
            ],
            "openai_compatible": [],
        }
        
        if provider.lower() in self._custom_providers:
            custom_model = self._custom_providers[provider.lower()].get("model")
            if custom_model:
                return [custom_model]
        
        return models.get(provider.lower(), [])

    def get_providers_info(self) -> Dict[str, Any]:
        providers = [
            {
                "name": "openai",
                "display_name": "OpenAI",
                "requires_api_key": True,
                "requires_base_url": False,
                "supports_streaming": True,
                "models": self.list_available_models("openai"),
                "description": "OpenAI's GPT models (GPT-4, GPT-3.5)"
            },
            {
                "name": "anthropic",
                "display_name": "Anthropic (Claude)",
                "requires_api_key": True,
                "requires_base_url": False,
                "supports_streaming": True,
                "models": self.list_available_models("anthropic"),
                "description": "Anthropic's Claude models"
            },
            {
                "name": "google",
                "display_name": "Google (Gemini)",
                "requires_api_key": True,
                "requires_base_url": False,
                "supports_streaming": True,
                "models": self.list_available_models("google"),
                "description": "Google's Gemini models"
            },
            {
                "name": "ollama",
                "display_name": "Ollama (Local)",
                "requires_api_key": False,
                "requires_base_url": True,
                "supports_streaming": True,
                "models": self.list_available_models("ollama"),
                "description": "Local LLM server via Ollama"
            },
            {
                "name": "openai_compatible",
                "display_name": "OpenAI Compatible",
                "requires_api_key": False,
                "requires_base_url": True,
                "supports_streaming": True,
                "models": [],
                "description": "Any OpenAI-compatible API endpoint (LM Studio, vLLM, LocalAI, etc.)"
            },
        ]
        
        return {
            "providers": providers,
            "custom_providers": list(self._custom_providers.keys())
        }


llm_service = LLMService()
