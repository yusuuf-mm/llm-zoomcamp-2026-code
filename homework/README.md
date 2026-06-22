# Homework: Agentic RAG

This folder contains the structured homework notebook for **Module 1 - Agentic RAG** of LLM Zoomcamp 2026.

## What's inside

- `homework.ipynb` — the completed homework notebook with all 6 questions answered and verified.

## How to run

1. Install dependencies:
   ```bash
   uv add minsearch gitsource openai python-dotenv
   ```

2. Make sure your `.env` file has the following keys:
   ```env
   OPENROUTER_API_KEY=sk-or-v1-...
   OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
   ```

3. Launch the notebook:
   ```bash
   jupyter lab homework/homework.ipynb
   ```

4. Run all cells in order. The notebook will:
   - Fetch 72 lesson markdown files from the course repo
   - Build a `minsearch` index and search it
   - Run a RAG pipeline and report input token counts
   - Chunk the documents and compare RAG token usage
   - Execute an agentic loop with tool calling and count search invocations
   - Print a summary of all answers at the end

## Notes

- The notebook uses `os.environ['OPENBLAS_NUM_THREADS'] = '1'` to prevent memory issues on some systems.
- Answers are printed directly in each cell; the final summary cell consolidates them.
- If you use a different model or provider, the exact token counts and tool-call numbers may vary slightly from the multiple-choice options.
