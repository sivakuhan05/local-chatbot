from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from datetime import datetime

# Use same embedding model as ingestion
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

# Connect to local Llama3
Settings.llm = Ollama(model="llama3")

print("Loading vector index...")

storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)

# Retrieve multiple relevant chunks
query_engine = index.as_query_engine(similarity_top_k=3)

print("Chatbot ready! Type 'exit' to quit.\n")

while True:
    question = input("Ask: ")

    if question.lower() == "exit":
        break

    # Inject current date
    today = datetime.now().strftime("%B %d, %Y")

    enhanced_query = f"""
You are a helpful college assistant that answers student questions about exams and events.

Today's date is {today}.

Use the provided context to answer the question clearly and naturally in a full sentence.

Question: {question}
"""

    response = query_engine.query(enhanced_query)

    print("\nBot:", response, "\n")
