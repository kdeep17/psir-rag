from langchain_aws import ChatBedrock
from langchain_core.messages import SystemMessage, HumanMessage

_chat = None

def get_llm():
    global _chat
    if _chat is None:
        _chat = ChatBedrock(
            model_id="amazon.nova-lite-v1:0",
            model_kwargs={
                "temperature": 0.1,
                "maxTokens": 800
            }
        )
    return _chat

def generate(prompt):
    chat = get_llm()
    messages = [
        HumanMessage(content=prompt)
    ]
    return chat.invoke(messages).content