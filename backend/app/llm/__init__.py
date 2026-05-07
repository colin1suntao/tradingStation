from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

class LLMClientFactory:
    PROVIDERS = {
        "openai": "openai",
        "anthropic": "anthropic",
        "google": "google",
    }

    @staticmethod
    def create_client(
        provider: str,
        model: str,
        api_key: Optional[str] = None,
        temperature: float = 0.1,
        max_tokens: Optional[int] = None,
        base_url: Optional[str] = None,
        **kwargs
    ):
        provider = provider.lower()
        
        if provider == "openai":
            return OpenAIClient(
                model=model,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
                base_url=base_url,
                **kwargs
            )
        elif provider == "anthropic":
            return AnthropicClient(
                model=model,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
        elif provider == "google":
            return GoogleClient(
                model=model,
                api_key=api_key,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )
        else:
            raise ValueError(f"Unsupported provider: {provider}")


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
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
        from langchain_core.outputs import ChatGeneration, ChatResult
        
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
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
        
        langchain_messages = []
        system_message = ""
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role == "system":
                system_message = content
            elif role == "user":
                langchain_messages.append(HumanMessage(content=content))
            elif role == "assistant":
                langchain_messages.append(AIMessage(content=content))
        
        if system_message:
            self.get_client().bind_tools = lambda tools: self.get_client()
            response = self.get_client().invoke(langchain_messages)
        else:
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
        from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
        
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
        
        response = self.get_client().invoke(langchain_messages)
        return response.content


llm_factory = LLMClientFactory()

__all__ = [
    "LLMClientFactory",
    "BaseLLMClient",
    "OpenAIClient",
    "AnthropicClient",
    "GoogleClient",
    "llm_factory",
]