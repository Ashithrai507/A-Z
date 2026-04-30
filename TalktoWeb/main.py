from groq import Groq
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

client = Groq(api_key="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")
chat_history = []
MAX_MEMORY = 10
website_store = None
# Priority pages to always crawl first
PRIORITY_PATHS = [
    "/", "/about", "/academics", "/departments", "/courses",
    "/admissions", "/faculty", "/contact", "/facilities",
    "/placement", "/events", "/news", "/research"
]

def crawl_website(base_url, max_pages=40):
    base_url = base_url.rstrip("/")
    visited = set()
    documents = []
    # Start with priority pages first
    priority_urls = [base_url + path for path in PRIORITY_PATHS]
    discovered_urls = []
    to_visit = priority_urls + discovered_urls
    while to_visit and len(visited) < max_pages:
        url = to_visit.pop(0)
        if url in visited:
            continue
        try:
            print(f"Crawling ({len(visited)+1}/{max_pages}): {url}")
            response = requests.get(url, timeout=8, headers={
                "User-Agent": "Mozilla/5.0 (compatible; CollegeBot/1.0)"
            })
            if response.status_code != 200:
                visited.add(url)
                continue
            soup = BeautifulSoup(response.text, "html.parser")
            #  Remove nav/footer noise before extracting text
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()
            #  Extract meaningful text with structure
            page_text = ""
            title = soup.find("title")
            if title:
                page_text += f"Page Title: {title.get_text(strip=True)}\n\n"
            for tag in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "td", "th"]):
                text = tag.get_text(strip=True)
                if len(text) > 20:  # skip tiny fragments
                    page_text += text + "\n"
            if page_text.strip():
                from langchain_core.documents import Document
                documents.append(Document(
                    page_content=page_text,
                    metadata={"source": url}
                ))
            visited.add(url)
            #  Discover new links (same domain only)
            for link in soup.find_all("a", href=True):
                href = link["href"].strip()
                full_url = urljoin(base_url, href)
                parsed = urlparse(full_url)
                # Keep only same-domain, clean HTTP links
                if (parsed.scheme in ("http", "https")
                        and urlparse(base_url).netloc in parsed.netloc
                        and full_url not in visited
                        and "#" not in full_url
                        and full_url not in to_visit):
                    to_visit.append(full_url)
        except Exception as e:
            print(f"Skipped {url}: {e}")
            visited.add(url)
            continue
    print(f" Done. Crawled {len(documents)} pages.")
    return documents

def load_college_data():
    global website_store
    base_url = "https://vcetputtur.ac.in"
    documents = crawl_website(base_url, max_pages=40)
    if not documents:
        return "No pages could be crawled. Check network/URL."
    #  Larger chunks = more context per retrieval
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        separators=["\n\n", "\n", ".", " "]
    )
    docs = splitter.split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    website_store = FAISS.from_documents(docs, embeddings)
    return f"Loaded {len(docs)} chunks from {len(documents)} pages!"

def expand_query(query):
    """Add domain-specific keywords to improve retrieval."""
    expansions = {
        "department": "departments courses branches engineering",
        "fee": "fees tuition cost payment admission charges",
        "faculty": "faculty staff professors teachers lecturers",
        "placement": "placement companies jobs recruiter salary package",
        "admission": "admission eligibility criteria cutoff rank",
        "hostel": "hostel accommodation boarding facilities",
        "contact": "contact address phone email location",
    }
    q_lower = query.lower()
    for key, extra in expansions.items():
        if key in q_lower:
            return query + " " + extra
    return query

def get_context(query):
    global website_store
    if website_store is None:
        return None
    expanded = expand_query(query)
    # Retrieve more chunks (k=8) and deduplicate
    results = website_store.similarity_search(expanded, k=8)
    seen = set()
    unique_results = []
    for doc in results:
        snippet = doc.page_content[:100]
        if snippet not in seen:
            seen.add(snippet)
            unique_results.append(doc)
    if not unique_results:
        return ""
    context_parts = []
    for i, doc in enumerate(unique_results):
        source = doc.metadata.get("source", "unknown")
        context_parts.append(f"[Source {i+1}: {source}]\n{doc.page_content}")
    return "\n\n---\n\n".join(context_parts)

def update_memory(question, answer):
    chat_history.append({"user": question, "bot": answer})
    if len(chat_history) > MAX_MEMORY:
        chat_history.pop(0)

def get_memory_text():
    return "".join(
        f"User: {c['user']}\nBot: {c['bot']}\n"
        for c in chat_history
    )

def ask_llm(question):
    try:
        if website_store is None:
            return "Please click 'Load College Data' first."
        memory = get_memory_text()
        context = get_context(question)
        if context is None:
            return " Please load college data first."
        if not context.strip():
            return " Couldn't find relevant info. Try rephrasing your question."
        prompt = f"""You are a helpful assistant for VCET Puttur college.
Previous conversation:
{memory}
Website context (from multiple pages):
{context}
Instructions:
- Answer using ONLY the context provided above
- Be detailed and structured — use bullet points or sections where helpful
- Include specific numbers, names, dates when present in the context
- If info spans multiple sources, combine them for a complete answer
- If something is partially found, share what is available and note what's missing
- Never say "not found" without first checking all context sections
Question: {question}
Answer:"""
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=1024
        )
        answer = response.choices[0].message.content.strip()
        if not answer:
            return "No response generated. Try again."
        update_memory(question, answer)
        return answer
    except Exception as e:
        return f"Error: {str(e)}"