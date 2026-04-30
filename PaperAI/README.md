# Research Paper Assistant - RAG Based Paper Explainer

An AI-powered research paper assistant that helps you understand complex papers using Retrieval Augmented Generation (RAG), Groq LLM, and vector embeddings.

## 🎯 Features

- **📄 PDF Upload**: Upload any research paper in PDF format
- **📋 Paper Summarization**: Get comprehensive summaries of uploaded papers
- **❓ Q&A System**: Ask specific questions about the paper and get context-grounded answers
- **💡 Concept Explanation**: Get complex concepts explained in simple, beginner-friendly language
- **🔍 Semantic Search**: Find relevant content using vector embeddings
- **⚡ Fast Processing**: Powered by Groq's high-speed LLM API

## 🏗️ Architecture

### Data Flow:
```
User uploads PDF
        ↓
PDF → Text extraction (PyMuPDF)
        ↓
Text Chunking
        ↓
Embeddings Generation (Sentence Transformers)
        ↓
Vector Database Storage (FAISS)
        ↓
User asks question
        ↓
Semantic Search (similarity matching)
        ↓
Retrieve top-K relevant chunks
        ↓
Send to LLM (Groq) with context
        ↓
Generate Answer
```

## 🛠️ Technology Stack

### Backend
- **Python 3.8+**: Core programming language
- **LangChain**: LLM orchestration (optional)
- **Groq**: Fast LLM API (llama-3.1-70b-versatile model)

### Vector Database & Search
- **FAISS**: Efficient similarity search and dense vector clustering
- **Sentence Transformers**: Generate embeddings (all-MiniLM-L6-v2 model)

### PDF Processing
- **PyMuPDF**: PDF text extraction and manipulation
- **pdfplumber**: Alternative PDF library (optional)

### UI
- **PyQt5**: Cross-platform desktop GUI

### Dependencies
See `requirements.txt` for complete list

## 📦 Installation

### 1. Clone or navigate to the project
```bash
cd PaperAI
```

### 2. Create virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup environment variables
```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_api_key_here
```

Get your free API key from: https://console.groq.com/keys

### 5. Run the application
```bash
python main.py
```

## 🚀 Usage

### Getting Started
1. **Launch the Application**: Run `python main.py`
2. **Upload a PDF**: Click "📄 Upload PDF" and select a research paper
3. **Wait for Processing**: The system will extract, chunk, and embed the paper
4. **Start Interacting**:
   - Ask questions about the paper in the **Q&A** tab
   - Get concepts explained in the **Explain Concepts** tab
   - View paper summary by clicking **📋 Summarize Paper**

### Example Interactions

**Q&A Tab:**
- "What is the main contribution of this paper?"
- "How does the proposed method compare to existing approaches?"
- "What are the limitations mentioned in the paper?"

**Concepts Tab:**
- "Explain attention mechanisms"
- "What is backpropagation?"
- "Explain ensemble methods"

## ⚙️ Configuration

Edit `config.py` to customize:

```python
# LLM Configuration
LLM_MODEL = "llama-3.1-70b-versatile"
LLM_TEMPERATURE = 0.7
LLM_MAX_TOKENS = 2048

# Embeddings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chunking
MAX_CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

# Search
TOP_K_RESULTS = 5
SIMILARITY_THRESHOLD = 0.5
```

## 📁 Project Structure

```
PaperAI/
├── main.py              # Main GUI application
├── config.py            # Configuration management
├── pdf_processor.py     # PDF extraction & chunking
├── embeddings.py        # Embedding generation
├── vector_db.py         # FAISS vector database
├── rag_pipeline.py      # RAG pipeline with Groq LLM
├── requirements.txt     # Dependencies
├── .env.example         # Environment template
├── .gitignore           # Git ignore rules
└── data/
    ├── uploads/         # Uploaded PDFs
    └── vector_store/    # FAISS indices
```

## 🔐 API Key Security

### Best Practices:
1. **Never commit .env file** to version control (it's in .gitignore)
2. **Always use environment variables** for sensitive data
3. **Regenerate keys** if accidentally exposed
4. **Use .env.example** as a template for other users

### How to set API keys:
- Copy `.env.example` to `.env`
- Add your actual API key to `.env`
- Application loads it automatically via `python-dotenv`

### Alternative Methods:
```python
# Environment variable
import os
api_key = os.getenv("GROQ_API_KEY")

# Direct in code (NOT RECOMMENDED)
# api_key = "sk-..."  # DON'T DO THIS!
```

## 📊 How RAG Works

### 1. Document Processing
- PDF is uploaded and text is extracted
- Text is split into overlapping chunks
- Each chunk is converted to a vector embedding

### 2. Storage
- Embeddings are stored in FAISS index
- Metadata (chunk text, source, page info) is saved
- Database can be reused for multiple queries

### 3. Query Processing
- User question is converted to embedding
- FAISS performs similarity search
- Top-K most relevant chunks are retrieved

### 4. Generation
- Retrieved chunks are sent to Groq LLM as context
- LLM generates answer based on context
- Answer is grounded in the actual paper content

## 🧠 Customization

### Use Different LLM
```python
# In rag_pipeline.py
self.model = "llama-3.1-8b-instant"  # Faster but less capable
# or any other Groq model
```

### Use Different Embedding Model
```python
# In config.py
EMBEDDING_MODEL = "all-mpnet-base-v2"  # Larger, more powerful
```

### Use Different Vector DB
Instead of FAISS:
```python
# Chroma
from chromadb import Client

# Weaviate
import weaviate
```

## ⚠️ Limitations

- **PDF text extraction**: Works best with text-based PDFs (not scanned images)
- **Context window**: Limited by LLM's context size (8K for llama-70b)
- **Embedding dimension**: Fixed at 384 for all-MiniLM-L6-v2 model
- **Real-time processing**: Large PDFs may take time to process

## 🐛 Troubleshooting

### Common Issues

**"GROQ_API_KEY not found"**
- Solution: Make sure .env file exists with valid API key
- Check if python-dotenv is installed: `pip install python-dotenv`

**"PyMuPDF import error"**
- Solution: Install PyMuPDF: `pip install PyMuPDF`
- Alternative: `pip install pymupdf`

**"PDF processing slow"**
- Solution: Reduce MAX_CHUNK_SIZE in config.py
- Consider using larger embedding model for better accuracy

**"Out of memory"**
- Solution: Process smaller PDFs first
- Reduce TOP_K_RESULTS in config.py
- Use GPU-accelerated FAISS: `pip install faiss-gpu`

## 📈 Performance Tips

1. **Chunk size**: Smaller chunks (500) = more accurate, slower
2. **Overlap**: Higher overlap = better context preservation, slower
3. **Top K**: Retrieve 3-5 chunks for balance between quality and speed
4. **Model selection**: llama-3.1-8b-instant for speed, 70b for accuracy

## 🔄 Future Enhancements

- [ ] Multi-document support
- [ ] Streaming responses
- [ ] User history & saved conversations
- [ ] Custom RAG parameters UI
- [ ] Support for other file formats (DOCX, PPTX)
- [ ] Web interface with FastAPI
- [ ] Docker containerization
- [ ] Batch processing

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

## 📞 Support

For issues and questions:
1. Check the Troubleshooting section
2. Review the code comments
3. Check Groq documentation: https://console.groq.com/docs
4. Review LangChain docs: https://python.langchain.com/

---

**Made with ❤️ using Groq, FAISS, and open-source tools**
