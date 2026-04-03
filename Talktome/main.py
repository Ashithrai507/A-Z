from groq import Groq

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

# 🔑 API KEY
client = Groq(api_key="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")

# 🧠 MEMORY
chat_history = []
MAX_MEMORY = 10

# 📦 VECTOR STORE
vectorstore = None


# =========================
# 📄 LOAD PDF
# =========================
def load_pdf(file_path):
    global vectorstore

    try:
        loader = PyPDFLoader(file_path)
        documents = loader.load()

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )

        docs = splitter.split_documents(documents)

        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )

        vectorstore = FAISS.from_documents(docs, embeddings)

        print("✅ PDF loaded")
        return "✅ PDF loaded successfully!"

    except Exception as e:
        return f"❌ Error loading PDF: {str(e)}"


# =========================
# 🔍 GET CONTEXT
# =========================
def get_context(query):
    global vectorstore

    if vectorstore is None:
        return None

    results = vectorstore.similarity_search(query, k=3)

    if not results:
        return ""

    context = "\n".join([doc.page_content for doc in results])

    print("📄 Context Preview:", context[:200])

    return context


# =========================
# 🧠 MEMORY FUNCTIONS
# =========================
def update_memory(question, answer):
    chat_history.append({"user": question, "bot": answer})

    if len(chat_history) > MAX_MEMORY:
        chat_history.pop(0)


def get_memory_text():
    text = ""
    for chat in chat_history:
        text += f"User: {chat['user']}\nBot: {chat['bot']}\n"
    return text


# =========================
# 🎯 INTENT DETECTION
# =========================
def detect_intent(question):
    q = question.lower().strip()

    casual_phrases = [
        "hi", "hello", "hey", "bye",
        "thanks", "thank you",
        "who are you", "how are you"
    ]

    if q in casual_phrases:
        return "casual"

    return "academic"


# =========================
# 💬 COMMON RESPONSES
# =========================
def handle_common(question):
    q = question.lower()

    if q in ["hi", "hello", "hey"]:
        return "👋 Hello! Upload a PDF or ask me anything."

    if "how are you" in q:
        return "😄 I'm running smoothly!"

    if "who are you" in q:
        return "🤖 I'm your AI-powered smart chatbot."

    if "thank" in q:
        return "🙏 You're welcome!"

    if "bye" in q:
        return "👋 Goodbye!"

    return None


# =========================
# 🔎 RELEVANCE CHECK
# =========================
def is_context_relevant(context, question):
    if not context or len(context.strip()) < 50:
        return False

    keywords = question.lower().split()

    match_count = sum(1 for word in keywords if word in context.lower())

    return match_count >= 2


# =========================
# 🤖 MAIN FUNCTION
# =========================
def ask_llm(question):
    try:
        # Intent
        intent = detect_intent(question)

        if intent == "casual":
            reply = handle_common(question)
            if reply:
                return reply

        # Memory
        memory = get_memory_text()

        # Context
        context = get_context(question)

        use_rag = False

        if context:
            if is_context_relevant(context, question):
                use_rag = True

        # Prompt
        if use_rag:
            prompt = f"""
You are an intelligent AI assistant.

Conversation History:
{memory}

Relevant Document Context:
{context}

Instructions:
- Prefer document context if relevant
- Combine with general knowledge if needed
- Be clear and structured

Question:
{question}

Answer:
"""
        else:
            prompt = f"""
You are an intelligent AI assistant.

Conversation History:
{memory}

Instructions:
- Answer clearly and helpfully
- Use general knowledge

Question:
{question}

Answer:
"""

        print("🧠 Using RAG:", use_rag)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=500
        )

        answer = response.choices[0].message.content.strip()

        update_memory(question, answer)

        return answer

    except Exception as e:
        return f"❌ Error: {str(e)}"