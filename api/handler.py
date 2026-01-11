import json
from api.retriever import retrieve
from api.prompt import build_prompt
from api.llm import generate


def detect_answer_length(question: str) -> str:
    q = question.lower()
    if "one sentence" in q or "in one line" in q:
        return "ONE_SENTENCE"
    if "short note" in q or "briefly" in q:
        return "SHORT"
    return "STANDARD"

def handler(event, context=None):
    # Extract query (supports API Gateway & local calls)
    if "body" in event and event["body"]:
        body = json.loads(event["body"])
        raw_question = body.get("query", "")
    else:
        raw_question = event.get("query", "")

    raw_question = raw_question.strip()
    normalized_question = raw_question.lower()

    if not raw_question:
        return {
            "statusCode": 400,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": "Missing query"})
        }

    # Retrieve documents
    docs = retrieve(normalized_question, final_k=4, fetch_k=12)

    if not docs:
        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "answer": "This concept is not covered in the notes.",
                "context": []
            })
        }

    # Extract clean text only (UI + debugging safe)
    context_chunks = [d.page_content for d in docs]

    # Build prompt using original question (important for UPSC directives)
    answer_mode = detect_answer_length(raw_question)
    context_text = "\n\n".join(context_chunks)
    prompt = build_prompt(context_text, raw_question, answer_mode)

    # Generate answer
    answer = generate(prompt)

    # Final response
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({
            "answer": answer,
            "context": context_chunks
        })
    }
