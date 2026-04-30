# PaperAI - Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1️⃣: Install (2 minutes)
```bash
cd PaperAI
pip install -r requirements.txt
```

### Step 2️⃣: Configure API Key (1 minute)
```bash
cp .env.example .env
# Edit .env and paste your Groq API key
# Get free key: https://console.groq.com/keys
```

### Step 3️⃣: Run (30 seconds)
```bash
python main.py
```

**That's it! 🎉 Upload a PDF and start asking questions!**

---

## 📖 What is RAG?

**RAG = Retrieval Augmented Generation**

Instead of relying on an LLM's training data, RAG:
1. **Retrieves** relevant chunks from YOUR specific paper
2. **Augments** the LLM prompt with those chunks
3. **Generates** answers grounded in YOUR document

**Why?**
- ✅ Accurate answers about your specific paper
- ✅ No hallucinations or made-up information
- ✅ Works with papers published after LLM training cutoff
- ✅ Cost-effective (only retrieve what's needed)

---

## 🎯 Use Cases

### Research Students
- Quick paper understanding without reading 50 pages
- Extract key concepts and methodologies
- Compare papers with specific questions

### Academics
- Review new papers efficiently
- Explain complex concepts to colleagues
- Prepare literature reviews

### Industry
- Understand technical papers
- Research competitors' publications
- Stay updated on latest research

---

## 📊 Architecture at a Glance

```
PDF Upload
    ↓
[PDF Processor]  ← Extract text, chunk into 1000-char pieces
    ↓
[Embeddings]     ← Convert chunks to vectors (384-dim)
    ↓
[Vector DB]      ← Store in FAISS for fast search
    ↓
┌─ User Question ─┐
│                 ↓
│          [Similarity Search]  ← Find top-5 relevant chunks
│                 ↓
│          [Groq LLM]  ← Generate answer with context
│                 ↓
└─ AI Answer ────┘
```

**Key Tech:**
- **Vector DB**: FAISS (Facebook AI similarity search)
- **Embeddings**: Sentence Transformers (all-MiniLM-L6-v2)
- **LLM**: Groq (llama-3.1-70b-versatile, super fast!)
- **UI**: PyQt5 (desktop application)

---

## 💡 How It Works

### Behind the Scenes

**When you upload a PDF:**
```
paper.pdf (40 pages)
    ↓
Text extracted: ~50,000 characters
    ↓
Split into chunks: ~50 chunks (1000 chars each)
    ↓
Embedding each chunk: 50 × 384-dimensional vectors
    ↓
Store in FAISS: Ready for fast search (~0.01ms per query)
```

**When you ask a question:**
```
Question: "What is the main contribution?"
    ↓
Convert to embedding: [0.12, -0.45, 0.78, ...]
    ↓
Search for similar chunks: Find top-5 matches
    ↓
Chunk 1: "The main contribution of this paper is..."
Chunk 2: "Our novel approach to..."
Chunk 3: "Unlike previous work..."
    ↓
Send to Groq: "Answer this based on these chunks"
    ↓
AI: "The paper presents a new method for..."
```

---

## 🎮 Using the Application

### GUI Mode (python main.py)

**Tabs:**
1. **Q&A** - Ask questions, get instant answers
2. **Explain Concepts** - "Explain transformer architecture"
3. **About** - How it works + documentation

**Features:**
- Click "📄 Upload PDF" to add papers
- Click "📋 Summarize Paper" for full summary
- Real-time processing with progress bar

### CLI Mode (python cli.py)

```bash
# Process PDF
python cli.py process papers/my_paper.pdf

# Ask question
python cli.py ask "How was the experiment conducted?"

# Summarize
python cli.py summarize

# Explain concept
python cli.py explain "Attention mechanism"

# Interactive chat
python cli.py interactive
```

---

## 🔐 API Key Management (Important!)

### Why Use .env?
- 🔒 Keeps your API key secret
- 🚫 Prevents accidental commits to GitHub
- 📁 Already configured in `.gitignore`

### Setup (Already Done!)
```bash
# Step 1: Copy template
cp .env.example .env

# Step 2: Edit .env
# Add your Groq API key:
# GROQ_API_KEY=gsk_your_key_here

# Step 3: It's automatic from here!
# The app loads it automatically
```

### Get Your Free API Key
1. Go to: https://console.groq.com
2. Sign up (free, no credit card)
3. Navigate to "API Keys"
4. Create new key
5. Copy it to `.env` file

**Your key is now secure and won't be exposed!**

---

## ⚙️ Customization

### Make it Faster
```python
# In config.py
MAX_CHUNK_SIZE = 500           # Smaller chunks
TOP_K_RESULTS = 3              # Fewer results to search
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Already optimized
```

### Make it More Accurate
```python
# In config.py
MAX_CHUNK_SIZE = 2000          # Larger context
CHUNK_OVERLAP = 500            # Better preservation
TOP_K_RESULTS = 10             # More results
LLM_TEMPERATURE = 0.5          # More deterministic
```

### Use Different LLM
```python
# In config.py - Groq models available:
"llama-3.1-70b-versatile"      # Most capable (default)
"llama-3.1-8b-instant"         # Faster but less capable
"mixtral-8x7b-32768"           # Mix of experts
```

---

## 📈 Features Explained

### 📋 Summarization
Generates comprehensive paper summary including:
- Main objective
- Methodology
- Key findings
- Implications and future work

### ❓ Q&A
Ask any question about the paper:
- "What datasets were used?"
- "How does this compare to X?"
- "What are the limitations?"

**Answers are always grounded in the actual paper content!**

### 💡 Concept Explanation
Get complex concepts explained simply:
- "Explain attention mechanism"
- "What is backpropagation?"
- "Explain ensemble methods"

Explanation includes relevant context from paper.

---

## 🐛 Quick Troubleshooting

| Problem | Solution |
|---------|----------|
| "GROQ_API_KEY not found" | Check `.env` file has your key |
| "ImportError: No module named 'groq'" | Run: `pip install -r requirements.txt` |
| "Permission denied main.py" | Run: `chmod +x main.py` or `python main.py` |
| Slow processing | Reduce `MAX_CHUNK_SIZE` in `config.py` |
| No database | Upload a PDF first via GUI or CLI |

---

## 📚 Project Files

```
PaperAI/
├── main.py              # GUI Application → python main.py
├── cli.py               # CLI Interface → python cli.py --help
├── config.py            # Configuration (adjust here)
├── pdf_processor.py     # PDF handling
├── embeddings.py        # Vector generation
├── vector_db.py         # FAISS database
├── rag_pipeline.py      # LLM integration
├── utils.py             # Helper functions
├── requirements.txt     # Install: pip install -r requirements.txt
├── .env.example         # Copy to .env and add API key
├── README.md            # Full documentation
├── SETUP_GUIDE.md       # Detailed setup guide
└── data/                # Data stored here (auto-created)
    ├── uploads/         # Your PDFs
    └── vector_store/    # Vector indices
```

---

## 🎓 Learning Path

### Beginner (Start Here!)
1. ✅ Install and run GUI
2. ✅ Upload a simple paper
3. ✅ Ask basic questions
4. ✅ Explore different concepts

### Intermediate
1. Try CLI mode: `python cli.py --help`
2. Experiment with config values
3. Process multiple papers
4. Read `README.md` for details

### Advanced
1. Modify `rag_pipeline.py` for custom prompts
2. Experiment with different embedding models
3. Integrate with your own application
4. Contribute improvements!

---

## 🚀 Next Steps

### Immediate
- [ ] Copy API key to `.env`
- [ ] Run `python main.py`
- [ ] Upload a paper
- [ ] Ask 5 questions

### Short Term
- [ ] Read `SETUP_GUIDE.md` for deep dive
- [ ] Try CLI mode: `python cli.py interactive`
- [ ] Customize `config.py`
- [ ] Process multiple papers

### Long Term
- [ ] Build web interface
- [ ] Integrate with your workflow
- [ ] Add more features
- [ ] Share with colleagues!

---

## 📞 Need Help?

### Check These First
1. **README.md** - Comprehensive documentation
2. **SETUP_GUIDE.md** - Detailed setup and troubleshooting
3. **config.py** - Comments explaining all options
4. **Code comments** - Every module is well-documented

### Common Questions

**Q: Is my API key safe?**
A: Yes! It's in `.env` which is in `.gitignore`. Never committed to git.

**Q: Can I process multiple papers?**
A: Yes! Each paper's chunks are added to the vector DB.

**Q: How much does Groq cost?**
A: Free tier available! Check console.groq.com for pricing.

**Q: Can I use this offline?**
A: No, Groq API requires internet. But FAISS search is local.

**Q: How long does processing take?**
A: ~10-30 seconds for typical paper depending on size.

---

## 🎉 You're All Set!

```bash
cd PaperAI
python main.py
```

**Start understanding papers better!** 📚✨

---

*Built with ❤️ using Groq, FAISS, and open-source tools*

**Have fun exploring!** 🚀
