import sys
import os
sys.path.insert(0, '/workspace/backend')
os.environ.setdefault("OPENAI_API_KEY", "test-key")

from app.services.llm_service import llm_service
from app.schemas.llm import LLMConfig, LLMProvider

def test_llm_providers():
    print("=" * 60)
    print("Testing LLM Service")
    print("=" * 60)
    
    print("\n1. Available Models:")
    for provider in ["openai", "anthropic", "google"]:
        models = llm_service.list_available_models(provider)
        print(f"   {provider}: {models}")
    
    print("\n2. Testing API Keys:")
    for provider in ["openai", "anthropic", "google"]:
        api_key = llm_service._get_api_key(provider)
        print(f"   {provider}: {'Found' if api_key else 'Not Found'}")

    print("\n3. Testing Client Creation:")
    try:
        client = llm_service.get_client(
            provider="openai",
            model="gpt-4o-mini",
            api_key=os.getenv("OPENAI_API_KEY")
        )
        print(f"   OpenAI Client: {type(client)}")
    except Exception as e:
        print(f"   OpenAI Client Error: {e}")

    print("\n" + "=" * 60)
    print("LLM Service Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    test_llm_providers()