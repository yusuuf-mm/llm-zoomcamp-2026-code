# 01-agentic-rag

Module 1 of LLM Zoomcamp 2026: building a RAG system from scratch and making it agentic.

## What is in this folder?

| File | Purpose |
|------|---------|
| `notebook.ipynb` | Step-by-step tutorial notebook. It starts with a naive LLM call, then progressively builds a modular RAG pipeline with annotated explanations. |
| `ingest.py` | Scriptable data-loading layer. It fetches the FAQ JSON from the remote API and builds a search index. Use this for offline/batch indexing. |
| `rag_helper.py` | The reusable RAG class (`RAGBase`) that wires search, prompt building, and the LLM call together. Import this in notebooks or apps. |
| `sqlite-ingest.ipynb` | Ingestion notebook for the persistent `sqlitesearch` backend. Writes the FAQ into `faq.db`. |
| `persistent_rag.ipynb` | Query notebook that opens `faq.db` and runs `RAGBase` against the persistent index. |
| `persistent_rag.ipynb` | Same as above; kept for reference alongside the sqlite variant. |
| `app.py` | Streamlit study companion app with Learn, Sandbox, and Quiz phases. |
| `faq.db` | SQLite persistent index produced by `sqlite-ingest.ipynb`. |
| `note-dump.md` | Personal synthesis notes capturing mental models, OOP concepts, and study questions from the module. |
| `README.md` | This file. |

## How to run

```bash
# Install dependencies
uv add minsearch sqlitesearch openai python-dotenv streamlit

# Run the tutorial notebook
jupyter lab 01-agentic-rag/notebook.ipynb

# Or start the Streamlit study companion
streamlit run 01-agentic-rag/app.py
```

## Architecture overview

```
ingest.py  ──►  build_index  ──►  minsearch.Index
                                      │
notebook.ipynb / app.py               │
        │                             ▼
        │                     RAGBase.rag()
        │                             │
        └─────────────────────────────┘
                    search → build_prompt → llm
```

`ingest.py` is the **offline** step: it prepares the data.
`rag_helper.py` is the **online** step: it answers questions.
The notebooks and `app.py` wire them together.
