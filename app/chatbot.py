from llama_index.core import StorageContext, load_index_from_storage
from llama_index.llms.ollama import Ollama
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Use the same embedding model used during ingestion
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

print("Loading vector index...")

# Load the saved index
storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)

print("Connecting to Llama3...")

# Connect to your local Ollama model
Settings.llm = Ollama(model="llama3")

# Create query engine
query_engine = index.as_query_engine()

print("Chatbot ready! Type 'exit' to quit.\n")

while True:
    question = input("Ask: ")

    if question.lower() == "exit":
        break

    response = query_engine.query(question)

    print("\nBot:", response, "\n")
