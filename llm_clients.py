from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings

import tracemalloc
tracemalloc.start()

load_dotenv()

llm = init_chat_model(
    model="gpt-4o",
    model_provider="azure_openai",
    temperature=0.5,
    configurable_fields=["temperature, model"],
    timeout=60,
    max_retries=2
)

# embeddings = init_embeddings(
#     provider="azure_openai",
#     model="text-embedding-3-large",
# )