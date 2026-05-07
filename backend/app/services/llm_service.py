import os
import time
from typing import Optional, Dict, Any
from app.llm import LLMClientFactory
from app.schemas.llm import LLMConfig, LLMTestResponse


class LLMService:
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
    ):
        cache_key = f"{provider}:{model}:{temperature}"
        
        if cache_key not in self._clients:
            resolved_api_key = api_key or self._get_api_key(provider)
            resolved_base_url = base_url or self._get_base_url(provider)
            
            self._clients[cache_key] = LLMClientFactory.create_client(
                provider=provider,
                model=model,
                api_key=resolved_api_key,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=resolved_base_url,
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
        env_vars = {
            "openai": "OPENAI_BASE_URL",
        }
        return os.getenv(env_vars.get(provider.lower(), ""))

    async def test_llm(
        self,
        provider: str,
        model: str,
        api_key: Optional[str] = None,
        message: str = "Hello, how are you?"
    ) -> LLMTestResponse:
        start_time = time.time()
        
        try:
            resolved_api_key = api_key or self._get_api_key(provider)
            
            if not resolved_api_key:
                return LLMTestResponse(
                    success=False,
                    response="",
                    model=model,
                    provider=provider,
                    error="API key not provided and not found in environment variables"
                )
            
            client = self.get_client(
                provider=provider,
                model=model,
                api_key=resolved_api_key,
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

    def list_available_models(self, provider: str = "openai") -> list:
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
        }
        return models.get(provider.lower(), [])


llm_service = LLMService()