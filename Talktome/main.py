from groq import Groq

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import WebBaseLoader

client = Groq(api_key="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")

chat_history = []
MAX_MEMORY = 10
vectorstore = None
website_store = None

def load_website(url):
    global website_store
    try:
        loader = WebBaseLoader(url)
        documents = loader.load()
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        docs = splitter.split_documents(documents)
        embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        website_store = FAISS.from_documents(docs, embeddings)

        return " Website data loaded successfully!"
    except Exception as e:
        return f"Website load error: {str(e)}"

def get_website_context(query):
    global website_store
    if website_store is None:
        return None
    results = website_store.similarity_search(query, k=3)
    if not results:
        return ""
    return "\n".join([doc.page_content for doc in results])

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
        print("PDF loaded")
        return "PDF loaded successfully!"
    except Exception as e:
        return f" Error loading PDF: {str(e)}"

def get_context(query):
    global vectorstore
    if vectorstore is None:
        return None
    results = vectorstore.similarity_search(query, k=3)
    if not results:
        return ""
    context = "\n".join([doc.page_content for doc in results])
    print("Context Preview:", context[:200])
    return context

def update_memory(question, answer):
    chat_history.append({"user": question, "bot": answer})
    if len(chat_history) > MAX_MEMORY:
        chat_history.pop(0)

def get_memory_text():
    text = ""
    for chat in chat_history:
        text += f"User: {chat['user']}\nBot: {chat['bot']}\n"
    return text

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

def handle_common(question):
    q = question.lower()
    if q in ["hi", "hello", "hey"]:
        return "Hello! Upload a PDF or ask me anything."

    if "how are you" in q:
        return " I'm running smoothly!"
    if "who are you" in q:
        return " I'm your AI-powered smart chatbot."

    if "thank" in q:
        return " You're welcome!"

    if "bye" in q:
        return " Goodbye!"

    return None


def is_context_relevant(context, question):
    if not context or len(context.strip()) < 50:
        return False
    keywords = question.lower().split()
    match_count = sum(1 for word in keywords if word in context.lower())
    return match_count >= 2

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

        # 🔥 MULTI SOURCE CONTEXT
        pdf_context = get_context(question)
        web_context = get_website_context(question)
        use_pdf = False
        use_web = False

        if pdf_context and is_context_relevant(pdf_context, question):
            use_pdf = True
        if web_context and is_context_relevant(web_context, question):
            use_web = True
        if use_pdf:
            print("Using PDF")

            prompt = f"""
You are an intelligent AI assistant.

Conversation History:
{memory}

PDF Context:
{pdf_context}

Instructions:
- Answer using PDF context
- If partially relevant, combine with general knowledge
- Be clear and structured

Question:
{question}

Answer:
"""

        elif use_web:
            print(" Using Website")

            prompt = f"""
You are a college assistant.

Conversation History:
{memory}

Website Data:
{web_context}

Instructions:
- Answer using website information
- Be accurate and concise

Question:
{question}

Answer:
"""

        else:
            print(" Using General AI")

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

        # LLM CALL
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
            max_tokens=500
        )

        answer = response.choices[0].message.content.strip()

        # Save memory
        update_memory(question, answer)

        return answer

    except Exception as e:
        return f"❌ Error: {str(e)}"