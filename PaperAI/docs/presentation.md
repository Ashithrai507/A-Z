# PaperAI — RAG‑Based Research Paper Assistant

## 1. Title Slide
**PaperAI: AI Research Paper Assistant**  
RAG + LLM + Vector Search for fast, grounded paper understanding

**Presenter:** [Ashith Rai]  
**Date:** 29 Apr 2026

---

## 2. Problem Statement
- Research papers are long, dense, and time‑consuming to understand
- Traditional LLMs can hallucinate or miss paper‑specific details
- We need fast, accurate, paper‑grounded explanations

**Goal:** Help users understand papers quickly with summaries, Q&A, and concept explanations.

---

## 3. What is RAG (Retrieval‑Augmented Generation)
- **Retrieve** relevant content from the paper
- **Augment** the LLM prompt with those passages
- **Generate** an answer grounded in the paper

**Why RAG?**
- Reduces hallucinations
- Uses paper‑specific evidence
- Works for new papers beyond model training data

---

## 4. System Overview
**User uploads PDF → System extracts text → chunks → embeddings → vector DB → Q&A via LLM**

Core features:
- **Summarize** research papers
- **Answer** questions about the paper
- **Explain** difficult concepts in simple language

---

## 5. Architecture (High‑Level)
**UI → Processing → Embeddings → Vector DB → LLM → Answer**

Layers:
1. **UI Layer** (PyQt5 GUI)
2. **PDF Processing Layer** (PyMuPDF)
3. **Chunking Layer** (overlapping text chunks)
4. **Embedding Layer** (Sentence Transformers)
5. **Vector DB Layer** (FAISS)
6. **LLM Layer** (Groq API)

---

## 6. End‑to‑End Pipeline (Step‑by‑Step)
1. **Upload PDF**
2. **Extract text** (page by page)
3. **Chunk text** (overlap for context)
4. **Create embeddings** (vector representation)
5. **Store vectors** in FAISS
6. **User question**
7. **Similarity search** (top‑K chunks)
8. **Send context + question** to Groq LLM
9. **Generate answer** (grounded)

---

## 7. Data Flow Diagram (Narrative)
**PDF → Text → Chunks → Embeddings → FAISS → Query → Top‑K → LLM → Response**

Key benefit: Only **relevant chunks** are passed to LLM (cost & accuracy).

---

## 8. Chunking Strategy
- Fixed‑size chunks (default 1000 chars)
- Overlap (default 200 chars) preserves context
- Optional sentence‑aware chunking available

**Why overlap?**
- Prevents cutting important ideas mid‑sentence
- Improves retrieval quality

---

## 9. Embeddings
- **Model:** sentence-transformers `all-MiniLM-L6-v2`
- **Dimension:** 384
- Converts text into dense vectors

**Why this model?**
- Fast and lightweight
- Good semantic retrieval quality

---

## 10. Vector Database
- **FAISS** (Facebook AI Similarity Search)
- Uses L2 distance for nearest‑neighbor search

**Why FAISS?**
- Fast retrieval
- Scales to large documents
- Easy to save/load indices

---

## 11. LLM & Prompting
- **LLM Provider:** Groq API
- **Current model:** `llama-3.1-8b-instant`

Prompt includes:
- System prompt (role guidance)
- User question
- Retrieved chunks

**Why Groq?**
- Fast inference
- Free tier available

---

## 12. Summarization Flow
- Uses **first N chunks** or **char‑budgeted context**
- Produces:
  - Objective & research question
  - Methodology
  - Key findings
  - Implications/future work

---

## 13. Q&A Flow
- Embed user question
- Top‑K FAISS search
- Pass relevant chunks to LLM
- Generate answer with citations

---

## 14. Concept Explanation Flow
- Embed the concept phrase
- Retrieve relevant chunks
- Ask LLM to explain in simple terms

---

## 15. Tech Stack
**Frontend**
- PyQt5 GUI

**Backend**
- Python 3.8+

**LLM**
- Groq API (Llama/Mixtral)

**Embeddings**
- Sentence Transformers (all‑MiniLM‑L6‑v2)

**Vector DB**
- FAISS

**PDF Handling**
- PyMuPDF

---

## 16. Project Structure (Key Modules)
- `main.py` — GUI application
- `pdf_processor.py` — PDF extraction + chunking
- `embeddings.py` — embedding generation
- `vector_db.py` — FAISS operations
- `rag_pipeline.py` — LLM calls
- `config.py` — configuration

---

## 17. Security & Configuration
- API keys stored in `.env`
- `.gitignore` prevents committing secrets
- Modular config for model selection

---

## 18. Limitations & Risks
- Scanned PDFs require OCR (not included)
- Model context limits (TPM / tokens)
- Large papers may need summarization chaining

**Mitigation:**
- Context size capping
- Chunking with overlap
- Optional multi‑pass summarization

---

## 19. Demo Script (Live Flow)
1. Launch app
2. Upload a research PDF
3. Click “Summarize Paper”
4. Ask: “What is the main contribution?”
5. Ask: “Explain [complex concept]”

---

## 20. Why This Project Matters
- Accelerates research understanding
- Reduces manual reading time
- Enables non‑experts to access research
- Promotes evidence‑grounded AI answers

---

## 21. Future Enhancements
- OCR support for scanned PDFs
- Multi‑paper comparison
- Web app / API
- Conversation history & export
- Citation highlighting in UI

---

## 22. Quick Q&A Prep (Possible Questions)
**Q:** Why not just use an LLM directly?  
**A:** RAG grounds answers in the actual paper and avoids hallucinations.

**Q:** How do you avoid large‑token errors?  
**A:** Cap context size and retrieve only top‑K chunks.

**Q:** How scalable is it?  
**A:** FAISS scales to millions of vectors; more scaling can be done with cloud DBs.

---

## 23. Closing Slide
**PaperAI = Faster, grounded research understanding**  
RAG + LLM + vector search in a clean desktop workflow

**Thank you!**

---

# Speaker Notes (Use During Presentation)

## Key Talking Points
- Stress the *pipeline* and how each part improves quality
- Emphasize **grounded answers** (no hallucinations)
- Mention **Groq speed** and why it is practical for demo

## Risks & Answers
- **Model deprecations:** configurable model in `config.py`
- **Token limits:** context cap and summarization window
- **Scanned PDFs:** future OCR support

## Demo Tips
- Prepare a short PDF (5–10 pages) for quick demo
- Ask a simple question first to show responsiveness
- Summarize after Q&A to show multi‑feature support
