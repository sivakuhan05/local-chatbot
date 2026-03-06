# College AI Assistant

Local RAG chatbot for answering college event and exam queries.

## Setup

1. Install Python

2. Install Ollama

```
curl -fsSL https://ollama.com/install.sh | sh
```

3. Create virtual environment

```
python3 -m venv venv
source venv/bin/activate
```

4. Install dependencies

```
pip install -r requirements.txt
```

5. Download the Llama3 model

```
ollama run llama3
```

(The first run downloads the model. You can exit the chat with `/bye` once the download finishes.)

## Build the knowledge base

After adding or updating files in the `data/` folder, generate the vector index:

```
python app/ingest.py
```

This creates the `storage/` directory containing the vector database used for retrieval.

Note: `storage/` is generated automatically and is ignored by Git.

## Run the chatbot

Start the CLI chatbot:

```
python app/chatbot.py
```

Example questions you can try:

```
When is the next exam?
Where is the hackathon?
When do mid semester exams start?
```

Type `exit` to quit the chatbot.

## Project Structure

```
app/
  chatbot.py        # CLI chatbot interface
  ingest.py         # builds vector index from documents

data/
  events.txt
  exams.txt

storage/            # generated vector index (ignored by git)

requirements.txt
README.md
```

