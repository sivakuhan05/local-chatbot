from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from datetime import datetime

# Use same embedding model as ingestion
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

# Connect to local Llama3
llm = Ollama(model="llama3")
Settings.llm = llm

print("Loading vector index...")

storage_context = StorageContext.from_defaults(persist_dir="storage")
index = load_index_from_storage(storage_context)

# Retrieve multiple relevant chunks
query_engine = index.as_query_engine(
    similarity_top_k=3,
    streaming=True
)

print("Chatbot ready! Type 'exit' to quit.\n")

while True:
    question = input("Ask: ")

    if question.strip().lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break

    # Inject current date
    today = datetime.now().strftime("%B %d, %Y")

    # Simple keyword trigger for RAG
    keywords = ["exam", "event", "hackathon", "fest", "schedule", "date"]
    use_rag = any(word in question.lower() for word in keywords)

    print("\nBot: ", end="", flush=True)

    if use_rag:
        enhanced_query = f"""
You are a college assistant chatbot.

Today's date is {today}.

Answer in a natural and friendly tone, but keep it concise.
Avoid being overly robotic or overly verbose.

Only consider events marked as "Upcoming Event".
Ignore events marked as "Past Event".

If there are upcoming events:
- Briefly mention them in a natural sentence
- Include event name, date, and location

If there are no upcoming events, say:
"There are currently no upcoming events."

Question: {question}
"""

        response = query_engine.query(enhanced_query)

        full_response = ""

        for token in response.response_gen:
            print(token, end="", flush=True)
            full_response += token

        # Only fallback if nothing was generated at all
        if not full_response.strip():
            print("There are currently no upcoming events.", end="")

        print("\n")

    else:
        stream = llm.stream_complete(question)

        full_response = ""

        for token in stream:
            new_text = token.delta
            print(new_text, end="", flush=True)
            full_response += new_text

        print("\n")
