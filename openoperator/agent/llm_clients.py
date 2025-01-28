from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
import os

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings

import tracemalloc
tracemalloc.start()

load_dotenv()

llm = init_chat_model(
    model=os.getenv("MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0.5,
    configurable_fields=["temperature, model"],
    timeout=60,
    max_retries=2
)

# embeddings = init_embeddings(
#     provider="azure_openai",
#     model="text-embedding-3-large",
# )