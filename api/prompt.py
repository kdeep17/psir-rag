def build_prompt(context, question, mode="STANDARD"):
    if mode == "ONE_SENTENCE":
        length_instruction = "Answer in exactly ONE sentence (max 25 words)."
    elif mode == "SHORT":
        length_instruction = "Answer in 40–60 words. Short Intro + core explanation if relevant."
    else:
        length_instruction = "Answer in 80–120 words with logical structure. Intro + core explanation if relevant."

    return f"""
You are a UPSC PSIR academic assistant.

Rules:
- Use ONLY ideas present in the notes.
- Do NOT introduce external facts or thinkers.
- Obey the answer length strictly.
- Maintain civil services answer tone.
Notes:
{context}

Question:
{question}

Answer instructions:
{length_instruction}
"""