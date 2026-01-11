import streamlit as st
import requests

API_URL = "http://localhost:8080/rag"

st.set_page_config(page_title="PSIR RAG")
st.title("📘 PSIR Notes – RAG Assistant")

query = st.text_area(
    "Ask a question from your notes",
    placeholder="e.g. Explain realism in one sentence"
)

if st.button("Ask"):
    if not query.strip():
        st.warning("Enter a question")
    else:
        with st.spinner("Thinking..."):
            resp = requests.post(API_URL, json={"query": query})

            if resp.status_code != 200:
                st.error("Backend error")
            else:
                data = resp.json()
                answer = data.get("answer", "")
                context = data.get("context", [])

                st.subheader("Answer")
                st.write(answer)

                if context:
                    with st.expander("View notes used for answer"):
                        for i, chunk in enumerate(context, 1):
                            st.markdown(f"**Chunk {i}:**")
                            st.write(chunk)
