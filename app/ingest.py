from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

print("Loading documents...")

documents = SimpleDirectoryReader("data").load_data()

print(f"Loaded {len(documents)} documents")

# Use local embedding model instead of OpenAI
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

index = VectorStoreIndex.from_documents(documents)

index.storage_context.persist("storage")

print("Index created and saved to storage/")
