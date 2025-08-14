import os

from dotenv import load_dotenv
from langchain_core.language_models.chat_models import BaseChatModel

from openoperator.agent.pollinations_llm import PollinationsChatModel

import tracemalloc
tracemalloc.start()

load_dotenv()

def get_llm() -> BaseChatModel:
    """Get the configured LLM based on environment variables."""
    model_provider = os.getenv("MODEL_PROVIDER", "").lower()
    model = os.getenv("MODEL", "openai")
    
    if model_provider == "pollinations":
        return PollinationsChatModel(
            model_name=model,
            temperature=0.5,
            max_tokens=1500,
            timeout=60
        )
    else:
        # Use LangChain's init_chat_model for other providers
        from langchain.chat_models import init_chat_model
        return init_chat_model(
            model=model,
            model_provider=model_provider,
            temperature=0.5,
            configurable_fields=["temperature", "model"],
            timeout=60,
            max_retries=2
        )

# Initialize the LLM
llm = get_llm()

# embeddings = init_embeddings(
#     provider="azure_openai",
#     model="text-embedding-3-large",
# )