PSIR RAG Assistant (DIY Retrieval-Augmented Generation)
Overview

This project implements a DIY Retrieval-Augmented Generation (RAG) system over personally compiled PSIR (Political Science & International Relations) notes.
The objective is to demonstrate correct RAG architecture, cost-aware design, and AWS-aligned GenAI implementation, rather than content completeness.

The system retrieves relevant note fragments using FAISS vector search and generates grounded answers using Amazon Bedrock models.

Architecture (High Level)
Streamlit (local UI)
        ↓ HTTP
Dockerized RAG Backend
        ├─ FAISS Vector Search
        ├─ Retrieval Logic (MMR)
        └─ Amazon Bedrock (LLM)


Frontend (Streamlit): Thin demo UI, local only

Backend: Containerized RAG runtime

Cloud Service: Amazon Bedrock for embeddings + generation

Vector Store: FAISS (offline-built, persisted)

Key Design Decisions
1. Offline Ingestion, Online Retrieval

PDFs are chunked and embedded once (offline)

FAISS index is saved and reused

Runtime performs only query embedding + retrieval + generation

This keeps latency low and cost predictable.

2. Content-Aware Chunking

Notes are crisp bullet points, not long prose

Smaller chunks preserve topic purity

Chunking parameters:

chunk_size: ~350 tokens

chunk_overlap: ~60 tokens

Chunk engineering is part of the ingestion pipeline, not runtime.

3. Explicit Retrieval Logic

FAISS uses Max Marginal Relevance (MMR) retrieval

Reduces redundancy while improving coverage

Retrieval is transparent and configurable (no black-box pipelines)

4. Grounded Prompting

LLM is instructed to answer only from retrieved context

Prevents hallucination

Output constrained to short, exam-style responses

5. Cost Control

No always-on services

Container is started only during demos/interviews

Amazon Bedrock is billed only per request

No managed vector database overhead

Tech Stack

Language: Python 3.10

LLM & Embeddings: Amazon Bedrock

Vector Store: FAISS (CPU)

Retrieval Framework: LangChain (modular usage)

Backend Runtime: Docker

Frontend: Streamlit (local)

Running the Project
1. Build FAISS Index (One-Time)
python build_index.py


This creates the persisted faiss_index/.

2. Build Docker Image
docker build -t psir-rag-backend .

3. Run Backend Container
docker run -p 8080:8080 \
  -e AWS_ACCESS_KEY_ID=XXXX \
  -e AWS_SECRET_ACCESS_KEY=YYYY \
  -e AWS_DEFAULT_REGION=us-east-1 \
  psir-rag-backend

4. Start Streamlit UI (Local)
streamlit run ui.py

Example Query
Explain realism in one sentence.


The answer is generated strictly from retrieved PSIR notes, not model priors.

Why This Project Matters

This project is designed to demonstrate:

Correct RAG mental model

Separation of offline ingestion vs online inference

Practical AWS GenAI integration

Cost-efficient system design

It intentionally avoids overengineering (ECS, OpenSearch, hosted UIs) to focus on core GenAI reasoning skills.

Future Extensions (Optional)

Metadata-aware retrieval (topic / thinker tags)

ECS or EC2 deployment

API Gateway in front of container

Source citation display in UI

Author’s Note:
This project prioritizes architectural correctness and explainability over scale or polish, in line with real GenAI interview expectations.
