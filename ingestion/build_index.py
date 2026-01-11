from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_aws import BedrockEmbeddings
from langchain_community.vectorstores import FAISS
from pathlib import Path


# -----------------------------
# 1. PDF configuration
# -----------------------------
PDF_SOURCES = [
    {"path": "data/p1a.pdf", "paper": "Paper 1", "part": "A"},
    {"path": "data/p1b.pdf", "paper": "Paper 1", "part": "B"},
    {"path": "data/p2a.pdf", "paper": "Paper 2", "part": "A"},
    {"path": "data/p2b.pdf", "paper": "Paper 2", "part": "B"},
]


all_documents = []

for src in PDF_SOURCES:
    loader = PyPDFLoader(src["path"])
    docs = loader.load()

    # Attach PSIR-relevant metadata
    for d in docs:
        d.metadata.update({
            "paper": src["paper"],
            "part": src["part"],
            "source": Path(src["path"]).name
        })

    all_documents.extend(docs)

print(f"Total pages loaded: {len(all_documents)}")


# -----------------------------
# 2. Chunking (PSIR-optimized)
# -----------------------------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=350,
    chunk_overlap=60,
    separators=[
        "\n\n",          # Section / paragraph breaks
        "\n",            # Bullet end
        "•", "-", "*",   # Bullet symbols
        ".", " "         # Fallback
    ]
)

chunks = splitter.split_documents(all_documents)

print(f"Total chunks created: {len(chunks)}")


# -----------------------------
# 3. Embeddings
# -----------------------------
embeddings = BedrockEmbeddings(
    model_id="amazon.titan-embed-text-v1"
)


# -----------------------------
# 4. Build FAISS index
# -----------------------------
vectorstore = FAISS.from_documents(chunks, embeddings)


# -----------------------------
# 5. Persist index
# -----------------------------
vectorstore.save_local("faiss_index")

print("FAISS index built and saved successfully")
