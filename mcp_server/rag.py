from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings

DOCUMENT_DIR = Path("knowledge/documents")
VECTORSTORE_DIR = Path("knowledge/chroma")
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
TOPICS = ["math", "physics", "astronomy", "engineering", "chemistry", "computer_science"]

def load_documents(topic: str):
    documents = []
    topic_dir = DOCUMENT_DIR / topic
    for path in topic_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        documents.append(Document(page_content=text, metadata={"source": path.name}))
    return documents

_embeddings = None
_vector_stores = {}

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    return _embeddings

def get_vector_store(topic: str):
    if topic not in _vector_stores:
        _vector_stores[topic] = Chroma(
            collection_name=f"{topic}_knowledge",
            embedding_function=get_embeddings(),
            persist_directory=str(VECTORSTORE_DIR),
        )
    return _vector_stores[topic]

def create_vector_store(topic: str):
    vector_store = get_vector_store(topic)
    documents = load_documents(topic)
    existing = vector_store.get()
    if not existing["ids"]:
        vector_store.add_documents(documents, ids=[doc.metadata["source"] for doc in documents])
    return vector_store

def create_all_vector_stores():
    for topic in TOPICS:
        create_vector_store(topic)

def search_knowledge(topic: str, query: str, top_k: int = 3) -> str:
    try:
        vector_store = get_vector_store(topic)
        results = vector_store.similarity_search(query, k=top_k)
    except Exception as e:
        return f"Error searching {topic} knowledge: {e}"
    if not results:
        return f"No relevant {topic} knowledge found."
    formatted = []
    for result in results:
        source = result.metadata.get("source", "unknown")
        formatted.append(f"Source: {source}\n{result.page_content}")
    return "\n\n---\n\n".join(formatted)

def search_math_knowledge(query: str, top_k: int = 3) -> str:
    """Search mathematical knowledge for constants, definitions, formulas, and properties."""
    return search_knowledge("math", query, top_k)

def search_physics_knowledge(query: str, top_k: int = 3) -> str:
    """Search physics knowledge for laws, formulas, and definitions."""
    return search_knowledge("physics", query, top_k)

def search_astronomy_knowledge(query: str, top_k: int = 3) -> str:
    """Search astronomy knowledge for celestial bodies, laws, and definitions."""
    return search_knowledge("astronomy", query, top_k)

def search_engineering_knowledge(query: str, top_k: int = 3) -> str:
    """Search engineering knowledge for formulas, principles, and definitions."""
    return search_knowledge("engineering", query, top_k)

def search_chemistry_knowledge(query: str, top_k: int = 3) -> str:
    """Search chemistry knowledge for elements, reactions, and formulas."""
    return search_knowledge("chemistry", query, top_k)

def search_computer_science_knowledge(query: str, top_k: int = 3) -> str:
    """Search computer science knowledge for algorithms, data structures, and definitions."""
    return search_knowledge("computer_science", query, top_k)
