from pymongo import MongoClient
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from datetime import datetime

# Set embedding model
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en")

# MongoDB connection
MONGO_URI = "mongodb+srv://eventadmin:Anbu12345@aicteproject.6gf5noy.mongodb.net/?appName=AicteProject"
DB_NAME = "eventverse"
COLLECTION_NAME = "events"


def load_events_from_mongo():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]

    docs = list(collection.find({
          "approvalStatus": "approved"     
    }))

    documents = []

    for doc in docs:
        # Format date nicely
        event_date = doc.get("eventDate")
        
        if event_date:
            formatted_date = event_date.strftime("%B %d, %Y")
            is_past = event_date < datetime.now()
        else:
            formatted_date = "Unknown"
            is_past = False

        status = "Past Event" if is_past else "Upcoming Event"

        text = f"""
Event: {doc.get('eventName')}
Category: {doc.get('category')}
Date: {formatted_date}
Status: {status}
Location: {doc.get('eventLocation')}
Organizer: {doc.get('organizerUsername')}
Club: {doc.get('clubAssociation')}
Description: {doc.get('eventDescription')}
"""

        documents.append(Document(text=text))

    return documents


if __name__ == "__main__":
    print("Fetching events from MongoDB...")

    documents = load_events_from_mongo()

    print(f"Loaded {len(documents)} events")

    index = VectorStoreIndex.from_documents(documents)

    index.storage_context.persist(persist_dir="storage")

    print("Index created and saved to storage/")
