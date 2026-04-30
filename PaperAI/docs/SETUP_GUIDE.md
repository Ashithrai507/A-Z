# PaperAI - Complete Setup & Usage Guide

## 🎯 Quick Start (5 minutes)

### Step 1: Install Dependencies
```bash
cd PaperAI
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### Step 2: Setup Environment
```bash
cp .env.example .env
# Edit .env and add your Groq API key
# GROQ_API_KEY=your_key_here
```

Get free API key: https://console.groq.com/keys

### Step 3: Run Application
```bash
python main.py
```

---

## 🔐 Environment Variables & API Key Management

### ✅ BEST PRACTICE: Using .env File

**Why use .env?**
- ✓ Keeps secrets out of code
- ✓ Prevents accidental commits to git
- ✓ Easy to change per environment
- ✓ Professional practice

**Setup:**

1. **Copy template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit .env:**
   ```ini
   GROQ_API_KEY=gsk_your_actual_key_here
   ```

3. **Never commit .env:**
   ```bash
   # Already in .gitignore - safe!
   git add .
   git commit -m "Add PaperAI"
   # .env is ignored automatically
   ```

### ❌ DO NOT DO THIS:

```python
# ❌ WRONG - API key exposed in code!
api_key = "gsk_abc123xyz"

# ❌ WRONG - Hardcoded in main file
groq_client = Groq(api_key="sk_...")

# ❌ WRONG - In git history
git add .env  # Don't do this!
```

### ✅ DO THIS:

```python
# ✓ RIGHT - Load from environment
import os
from dotenv import load_dotenv

load_dotenv()  # Loads from .env file
api_key = os.getenv("GROQ_API_KEY")

# Application already does this in config.py!
```

### If You Accidentally Exposed Your Key:

1. **Immediately regenerate** in Groq console
   - https://console.groq.com/keys
   - Delete old key, create new one

2. **Update .env** with new key

3. **Don't commit** the old key to git

---

## 📊 Project Structure & Files

```
PaperAI/
│
├── main.py                 # GUI Application (PyQt5)
│   └── Launch: python main.py
│
├── cli.py                  # Command-line Interface
│   └── Launch: python cli.py --help
│
├── config.py               # Configuration Management
│   ├── Loads .env file
│   ├── Sets defaults
│   └── Manages paths
│
├── pdf_processor.py        # PDF Handling
│   ├── PDFProcessor class
│   │   ├── validate_pdf()
│   │   └── extract_text()
│   └── TextChunker class
│       ├── chunk_text()
│       └── chunk_by_sentences()
│
├── embeddings.py           # Vector Embeddings
│   └── EmbeddingGenerator class
│       ├── embed_text()
│       └── embed_chunks()
│
├── vector_db.py            # FAISS Vector Database
│   └── VectorDatabase class
│       ├── add_vectors()
│       ├── search()
│       ├── save()
│       └── load()
│
├── rag_pipeline.py         # RAG + Groq LLM
│   └── RAGPipeline class
│       ├── generate_answer()
│       ├── summarize_paper()
│       └── explain_concept()
│
├── utils.py                # Helper Functions
│   ├── setup_logging()
│   ├── save_results()
│   └── format_answer()
│
├── requirements.txt        # Python Dependencies
├── .env.example            # Environment Template
├── .env                    # Your Actual Config (NEVER COMMIT)
├── .gitignore              # Git Rules
├── setup.py                # Setup Script
├── README.md               # Main Documentation
│
├── data/                   # Data Directory (auto-created)
│   ├── uploads/            # Your uploaded PDFs
│   └── vector_store/       # FAISS indices
│
└── logs/                   # Log Files (optional)
```

---

## 🚀 How to Use

### Option 1: GUI Application (Recommended for users)

```bash
python main.py
```

**Features:**
- 📁 Upload PDFs with file dialog
- 📋 One-click summarization
- ❓ Ask questions in Q&A tab
- 💡 Explain concepts in Concepts tab
- 📊 Visual progress indicators

### Option 2: Command-Line Interface (Great for automation)

```bash
# Process a PDF
python cli.py process papers/research.pdf

# Ask a question
python cli.py ask "What is the main contribution?"

# Summarize the paper
python cli.py summarize

# Explain a concept
python cli.py explain "Attention Mechanism"

# Interactive mode
python cli.py interactive --pdf papers/research.pdf
```

### Option 3: Python Script (For integration)

```python
from pdf_processor import PDFProcessor, TextChunker
from embeddings import EmbeddingGenerator
from vector_db import VectorDatabase
from rag_pipeline import RAGPipeline
import config

# Setup
pdf_processor = PDFProcessor()
embedding_gen = EmbeddingGenerator(config.EMBEDDING_MODEL)
vector_db = VectorDatabase(config.EMBEDDING_DIMENSION)
rag = RAGPipeline(config.GROQ_API_KEY)

# Process PDF
text, metadata = pdf_processor.extract_text("paper.pdf")
chunker = TextChunker()
chunks = chunker.chunk_text(text)

# Embed and store
chunks = embedding_gen.embed_chunks(chunks)
embeddings = [c["embedding"] for c in chunks]
vector_db.add_vectors(embeddings)

# Ask question
query_embedding = embedding_gen.embed_text("Your question")[0]
results, _ = vector_db.search(query_embedding, k=5)
answer = rag.generate_answer("Your question", [r["text"] for r in results])
print(answer)
```

---

## ⚙️ Configuration Guide

### config.py Settings

```python
# 1. API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # Set in .env file

# 2. LLM Settings
LLM_MODEL = "llama-3.1-70b-versatile"     # Fast & accurate
LLM_TEMPERATURE = 0.7                      # 0=deterministic, 1=creative
LLM_MAX_TOKENS = 2048                      # Max response length

# 3. Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"      # Fast, 384 dimensions
EMBEDDING_DIMENSION = 384

# 4. PDF Chunking
MAX_CHUNK_SIZE = 1000                      # Characters per chunk
CHUNK_OVERLAP = 200                        # Overlap for context

# 5. Search
TOP_K_RESULTS = 5                          # Retrieved chunks
SIMILARITY_THRESHOLD = 0.5                 # Filter low matches
```

### Customization Examples

**For Speed (Faster Response):**
```python
LLM_MODEL = "llama-3.1-8b-instant"        # Smaller model
MAX_CHUNK_SIZE = 500                       # Smaller chunks
EMBEDDING_MODEL = "all-MiniLM-L6-v2"      # Already fast
TOP_K_RESULTS = 3                          # Fewer results
```

**For Accuracy (Better Answers):**
```python
LLM_MODEL = "llama-3.1-70b-versatile"     # Largest available
MAX_CHUNK_SIZE = 2000                      # Larger context
CHUNK_OVERLAP = 500                        # More overlap
TOP_K_RESULTS = 10                         # More results
LLM_TEMPERATURE = 0.5                      # More deterministic
```

**For Research Papers:**
```python
EMBEDDING_MODEL = "all-mpnet-base-v2"     # Better for papers
MAX_CHUNK_SIZE = 1500
CHUNK_OVERLAP = 300
TOP_K_RESULTS = 7
```

---

## 🔄 RAG Pipeline Explained

```
┌─────────────────────────────────────────────────────────────┐
│                    DOCUMENT PROCESSING                       │
└─────────────────────────────────────────────────────────────┘

1. PDF Upload
   ↓
2. Text Extraction (PyMuPDF)
   "The transformer architecture..."
   ↓
3. Chunking (overlapping segments)
   Chunk 1: "The transformer architecture is based on..."
   Chunk 2: "architecture is based on attention mechanisms..."
   Chunk 3: "attention mechanisms that allow..."
   ↓
4. Embedding Generation (Sentence Transformers)
   [0.12, -0.45, 0.78, ...] (384 dimensions)
   ↓
5. Vector Database Storage (FAISS)
   Index: {
     vector_id_0: embedding_0,
     vector_id_1: embedding_1,
     ...
   }
   Metadata: {
     vector_id_0: {text: "...", source: "paper.pdf"},
     ...
   }

┌─────────────────────────────────────────────────────────────┐
│                    QUERY PROCESSING                          │
└─────────────────────────────────────────────────────────────┘

1. User Question
   "How do attention mechanisms work?"
   ↓
2. Question Embedding
   [0.15, -0.42, 0.81, ...] (same 384 dimensions)
   ↓
3. Similarity Search (L2 Distance)
   Find vectors closest to question vector
   ↓
4. Retrieve Top-K Chunks
   [Chunk 5, Chunk 12, Chunk 3] (similarity score)
   ↓
5. Format Prompt with Context
   System: "You are a research paper assistant..."
   User: "Question: ... Context: [Chunk 5] ... [Chunk 12]..."
   ↓
6. LLM Generation (Groq)
   Processes with all context
   ↓
7. Return Answer
   Grounded in actual paper content!
```

---

## 📈 Performance Benchmarks

### Processing Time (per 1000 chunks)
| Operation | Time | Notes |
|-----------|------|-------|
| Text Extraction | ~2-5s | Depends on PDF size |
| Chunking | ~0.5s | CPU bound |
| Embedding | ~3-5s | Uses all CPU cores |
| FAISS Storage | ~0.1s | Very fast |
| **Total** | **~6-12s** | For typical paper |

### Query Response Time
| Step | Time |
|------|------|
| Question Embedding | ~50ms |
| Vector Search | ~10-50ms |
| LLM Generation | ~2-10s | Depends on answer length |
| **Total** | **~2-10s** | Mostly LLM time |

### Memory Usage
| Component | Memory |
|-----------|--------|
| FAISS Index (1M vectors) | ~1.5 GB |
| Embedding Model | ~300 MB |
| LLM Model (Groq cloud) | N/A (cloud) |
| Typical Paper (10K chunks) | ~50 MB |

---

## 🐛 Troubleshooting

### Issue: "GROQ_API_KEY not found"

**Cause:** Missing or incorrect .env file

**Solution:**
```bash
# Check .env exists
ls -la .env

# Check it has your key
cat .env | grep GROQ_API_KEY

# If missing, create it
cp .env.example .env
# Edit and add your key
```

### Issue: "ImportError: No module named 'groq'"

**Cause:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
# Or install specific package
pip install groq
```

### Issue: "PDF processing is very slow"

**Causes & Solutions:**
```python
# Solution 1: Reduce chunk size
MAX_CHUNK_SIZE = 500  # Was 1000

# Solution 2: Reduce overlap
CHUNK_OVERLAP = 100   # Was 200

# Solution 3: Use faster embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Already using it

# Solution 4: Use GPU if available
pip install faiss-gpu  # Instead of faiss-cpu
```

### Issue: "Scanned PDFs not working"

**Cause:** PyMuPDF can't extract text from images

**Solutions:**
1. Use OCR tool first:
   ```bash
   pip install pytesseract pdf2image
   # Convert PDF to images, then OCR, then save as text
   ```

2. Or use different extraction:
   ```python
   # Try pdfplumber instead
   pip install pdfplumber
   import pdfplumber
   ```

### Issue: "LLM responses are too short"

**Solution:** Increase max tokens
```python
# In config.py
LLM_MAX_TOKENS = 4096  # Was 2048
```

### Issue: "LLM responses are repetitive"

**Solution:** Increase temperature
```python
# In config.py
LLM_TEMPERATURE = 0.9  # Was 0.7
```

---

## 🔒 Security Best Practices

### 1. **Never Commit Secrets**
```bash
# Good - .env is ignored
git status
# On branch main
# Changes to be committed:
#   new file: pdf_processor.py
#   new file: config.py
# Untracked files:
#   .env  ← NOT INCLUDED

# Bad - Accidentally committed
git add .
git commit -am "Add all files"  # Includes .env!
```

### 2. **Rotate Keys Regularly**
```bash
# Every 3-6 months
# 1. Generate new key in Groq console
# 2. Update .env file
# 3. Delete old key
```

### 3. **Use Different Keys Per Environment**
```bash
.env                  # Development
.env.production       # Production
.env.test             # Testing

# Load appropriate one
from dotenv import load_dotenv
load_dotenv(".env.production")  # For production
```

### 4. **Don't Share Keys via Email**
- Use password manager (1Password, LastPass)
- Use secret management (AWS Secrets, HashiCorp Vault)
- For team: Use environment variables in CI/CD

### 5. **Monitor API Usage**
```bash
# Check Groq console regularly
# https://console.groq.com/usage
# Watch for unusual activity
# Set spending limits
```

---

## 🎓 Learning Resources

### Concepts
- [RAG Explained](https://www.promptingguide.ai/techniques/rag)
- [Vector Embeddings](https://www.cloudflare.com/learning/ai/what-are-embeddings/)
- [FAISS Guide](https://ai.meta.com/tools/faiss/)
- [Attention Mechanism](https://arxiv.org/abs/1706.03762)

### Tools
- [Groq API Docs](https://console.groq.com/docs)
- [LangChain Documentation](https://python.langchain.com/)
- [Sentence Transformers](https://www.sbert.net/)
- [PyQt5 Tutorial](https://www.tutorialspoint.com/pyqt5/)

### Papers
- [Attention is All You Need](https://arxiv.org/abs/1706.03762)
- [RAG: Retrieval-Augmented Generation](https://arxiv.org/abs/2005.11401)
- [FAISS: A library for efficient similarity search](https://arxiv.org/abs/1702.08734)

---

## 📝 Common Tasks

### Task 1: Process Multiple PDFs
```bash
python cli.py process papers/paper1.pdf
python cli.py process papers/paper2.pdf
python cli.py process papers/paper3.pdf

# All will be added to same vector DB
```

### Task 2: Batch Questions
```bash
# Create questions.txt
questions.txt:
What is the main contribution?
How does this compare to X?
What datasets were used?

# Process
while IFS= read -r q; do
  python cli.py ask "$q"
done < questions.txt
```

### Task 3: Export Results
```python
# Save answers to file
results = {
    "question": "What is...",
    "answer": "The paper shows...",
    "chunks_used": 5
}

import json
with open("results.json", "w") as f:
    json.dump(results, f, indent=2)
```

### Task 4: Customize UI
```python
# In main.py, modify colors/fonts
self.answer_display.setStyleSheet("""
    background-color: #ffffff;
    color: #333333;
    font-family: 'Courier New';
    font-size: 12px;
""")
```

---

## 📞 Getting Help

### Debug Mode
```python
# In config.py
DEBUG = True  # More logging

# Run with debug
python main.py
# Check console output
```

### Check Dependencies
```bash
pip list | grep -E "groq|faiss|torch|sentence|PyQt"

# Should show all installed
```

### Test Groq Connection
```python
from groq import Groq
import os

api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=api_key)

msg = client.chat.completions.create(
    model="llama-3.1-70b-versatile",
    messages=[{"role": "user", "content": "Hi!"}]
)
print(msg.choices[0].message.content)
```

### Test Vector DB
```python
import numpy as np
from vector_db import VectorDatabase

db = VectorDatabase(384)
test_vectors = np.random.rand(10, 384).astype('float32')
db.add_vectors(test_vectors)
print(f"Database has {db.get_size()} vectors")
```

---

## 🚀 Next Steps

1. ✅ Install dependencies
2. ✅ Add API key to .env
3. ✅ Run `python main.py`
4. ✅ Upload a research paper
5. ✅ Ask your first question
6. 📚 Read README.md for more features
7. 🔧 Customize config.py as needed
8. 🎯 Integrate into your workflow

**Happy researching! 🎓**
