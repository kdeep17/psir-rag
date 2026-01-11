FROM python:3.10-slim

WORKDIR /app

# System dependencies for FAISS
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY api/ ./api/
COPY faiss_index/ ./faiss_index/
COPY app.py .

EXPOSE 8080

CMD ["python", "app.py"]
