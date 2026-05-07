from typing import Optional, Dict, Any, List, Callable, Type
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage


class LLMProviderRegistry:
    _providers: Dict[str, Type['BaseLLMClient']] = {}
    _custom_providers: Dict[str, Callable] = {}
    
    @classmethod
    def register(cls, name: str, client_class: Type['BaseLLMClient']):
        cls._providers[name.lower()] = client_class
    
    @classmethod
    def register_custom(cls, name: str, factory: Callable):
        cls._custom_providers[name.lower()] = factory
        cls._providers[name.lower()] = CustomProviderWrapper
    
    @classmethod
    def get_provider(cls, name: str) -> Optional[Type['BaseLLMClient']]:
        return cls._providers.get(name.lower())
    
    @classmethod
    def get_custom_provider(cls, name: str) -> Optional[Callable]:
        return cls._custom_providers.get(name.lower())
    
    @classmethod
    def list_providers(cls) -> List[str]:
        return list(cls._providers.keys())


class BaseLLMClient:
    def __init__(
        self,
        model: str,
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        **kwargs
    ):
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.extra_kwargs = kwargs
        self._client = None

    def get_client(self):
        raise NotImplementedError

    def invoke(self, messages: List[Dict[str, Any]]) -> str:
        raise NotImplementedError
    
    def _convert_messages(self, messages: List[Dict[str, Any]]) -> List:
        langchain_messages = []
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                langchain_messages.append(SystemMessage(content=content))
            elif role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
            else:
                langchain_messages.append(HumanMessage(content=content))
        return langchain_messages


class OpenAIClient(BaseLLMClient):
    def get_client(self):
        if self._client is None:
            self._client = ChatOpenAI(
                model=self.model,
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                base_url=self.extra_kwargs.get("base_url"),
            )
        return self._client

    def invoke(self, messages: List[Dict[str, Any]]) -> str:
        langchain_messages = self._convert_messages(messages)
        response = self.get_client().invoke(langchain_messages)
        return response.content


class AnthropicClient(BaseLLMClient):
    def get_client(self):
        if self._client is None:
            self._client = ChatAnthropic(
                model=self.model,
                anthropic_api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=self.max_tokens or 4096,
            )
        return self._client

    def invoke(self, messages: List[Dict[str, Any]]) -> str:
        langchain_messages = self._convert_messages(messages)
        response = self.get_client().invoke(langchain_messages)
        return response.content


class GoogleClient(BaseLLMClient):
    def get_client(self):
        if self._client is None:
            self._client = ChatGoogleGenerativeAI(
                model=self.model,
                google_api_key=self.api_key,
                temperature=self.temperature,
                max_output_tokens=self.max_tokens,
            )
        return self._client

    def invoke(self, messages: List[Dict[str, Any]]) -> str:
        langchain_messages = self._convert_messages(messages)
        response = self.get_client().invoke(langchain_messages)
        return response.content


class OllamaClient(BaseLLMClient):
    def get_client(self):
        if self._client is None:
            base_url = self.extra_kwargs.get("base_url", "http://localhost:11434")
            self._client = ChatOllama(
                model=self.model,
                base_url=base_url,
                temperature=self.temperature,
                num_predict=self.max_tokens,
            )
        return self._client

    def invoke(self, messages: List[Dict[str, Any]]) -> str:
        langchain_messages = self._convert_messages(messages)
        response = self.get_client().invoke(langchain_messages)
        return response.content


class OpenAICompatibleClient(BaseLLMClient):
    def get_client(self):
        if self._client is None:
            base_url = self.extra_kwargs.get("base_url")
            if not base_url:
                raise ValueError("base_url is required for OpenAI-compatible providers")
            
            self._client = ChatOpenAI(
                model=self.model,
                api_key=self.api_key or "not-needed",
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                base_url=base_url,
            )
        return self._client

    def invoke(self, messages: List[Dict[str, Any]]) -> str:
        langchain_messages = self._convert_messages(messages)
        response = self.get_client().invoke(langchain_messages)
        return response.content


class CustomProviderWrapper(BaseLLMClient):
    def __init__(self, model: str, factory: Callable, **kwargs):
        super().__init__(model=model, **kwargs)
        self.factory = factory
        self._client = None

    def get_client(self):
        if self._client is None:
            self._client = self.factory(
                model=self.model,
                api_key=self.api_key,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                **self.extra_kwargs
            )
        return self._client

    def invoke(self, messages: List[Dict[str, Any]]) -> str:
        client = self.get_client()
        if hasattr(client, 'invoke'):
            langchain_messages = self._convert_messages(messages)
            response = client.invoke(langchain_messages)
            return response.content
        else:
            return client(messages)


LLMProviderRegistry.register("openai", OpenAIClient)
LLMProviderRegistry.register("anthropic", AnthropicClient)
LLMProviderRegistry.register("google", GoogleClient)
LLMProviderRegistry.register("ollama", OllamaClient)
LLMProviderRegistry.register("openai_compatible", OpenAICompatibleClient)


class LLMClientFactory:
    @staticmethod
    def create_client(
        provider: str,
        model: str,
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        base_url: Optional[str] = None,
        **kwargs
    ) -> BaseLLMClient:
        provider = provider.lower()
        
        provider_class = LLMProviderRegistry.get_provider(provider)
        if provider_class is None:
            raise ValueError(
                f"Unsupported provider: {provider}. "
                f"Available providers: {LLMProviderRegistry.list_providers()}"
            )
        
        kwargs["base_url"] = base_url
        return provider_class(
            model=model,
            api_key=api_key,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )
    
    @staticmethod
    def register_custom_provider(
        name: str,
        factory: Callable,
        model: str,
        api_key: Optional[str] = None,
        **kwargs
    ) -> BaseLLMClient:
        LLMProviderRegistry.register_custom(name, factory)
        return LLMClientFactory.create_client(
            provider=name,
            model=model,
            api_key=api_key,
            **kwargs
        )


llm_factory = LLMClientFactory()

__all__ = [
    "LLMClientFactory",
    "BaseLLMClient",
    "OpenAIClient",
    "AnthropicClient",
    "GoogleClient",
    "OllamaClient",
    "OpenAICompatibleClient",
    "CustomProviderWrapper",
    "LLMProviderRegistry",
    "llm_factory",
]
