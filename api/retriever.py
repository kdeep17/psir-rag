from langchain_community.vectorstores import FAISS
from langchain_aws import BedrockEmbeddings

_embeddings = None
_db = None

def load_vectorstore():
    global _embeddings, _db
    if _db is None:
        _embeddings = BedrockEmbeddings(
            model_id="amazon.titan-embed-text-v1"
        )
        _db = FAISS.load_local(
            "faiss_index",
            _embeddings,
            allow_dangerous_deserialization=True
        )
    return _db

def retrieve(question, final_k=4, fetch_k=12):
    db = load_vectorstore()

    return db.max_marginal_relevance_search(
        question,
        k=final_k,
        fetch_k=fetch_k,
        lambda_mult=0.7
    )