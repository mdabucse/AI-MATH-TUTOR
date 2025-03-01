from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Initialize model
model = SentenceTransformer('all-MiniLM-L6-v2')

# FAISS index initialization
index_path = "faiss_index.index"
embedding_dim = 384  # Dimension of 'all-MiniLM-L6-v2'

def create_faiss_index():
    """Creates an empty FAISS index."""
    return faiss.IndexFlatL2(embedding_dim)

# Try loading an existing FAISS index
try:
    index = faiss.read_index(index_path)
except:
    index = create_faiss_index()

# Text Splitter
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

def make_chunks(text):
    """Split text into manageable chunks."""
    return text_splitter.split_text(text)

# Metadata storage
metadata_store = {}

def embed_and_store(chunks):
    """Embed text chunks and store them in FAISS with metadata."""
    global metadata_store
    embeddings = model.encode(chunks)
    faiss.normalize_L2(embeddings)  # Normalize for cosine similarity
    index.add(np.array(embeddings, dtype=np.float32))
    
    for i, chunk in enumerate(chunks):
        metadata_store[i] = chunk  # Store metadata separately
    
    # Save FAISS index
    faiss.write_index(index, index_path)

def get_context(query, top_k=3):
    """Retrieve relevant document chunks using FAISS."""
    query_emb = model.encode(query).reshape(1, -1)
    faiss.normalize_L2(query_emb)  # Normalize query
    distances, indices = index.search(np.array(query_emb, dtype=np.float32), top_k)
    
    context = [metadata_store[idx] for idx in indices[0] if idx in metadata_store]
    return " ".join(context)

def preprocess(values):
    """Convert JSON data into a single text string."""
    return "".join(values.values())

def rag_main(query):
    """Main function for RAG pipeline using FAISS."""
    pdf_path = r"A:\\Projects\\Edu_Pro\\backend\\data\\single.json"
    
    with open(pdf_path, 'r', encoding="utf-8") as f:
        values = json.load(f)
    
    print("Processing Text...")
    text_data = preprocess(values)
    
    if index.ntotal == 0:  # Check if index is empty
        print("Chunking and storing embeddings...")
        chunks = make_chunks(text_data)
        embed_and_store(chunks)
        print(f"Stored {len(chunks)} chunks.")
    else:
        print("Embeddings already exist, skipping storage.")
    
    # Retrieve relevant context
    retrieved_context = get_context(query)
    print("Retrieved Context:", retrieved_context)
    return retrieved_context

# Example Usage:
# query_result = rag_main("Your search query here")
