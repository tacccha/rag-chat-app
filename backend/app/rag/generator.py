from app.core.config import (CHAT_OPEN_AI_MODEL)
from langchain_openai import ChatOpenAI

def get_llm():
    """
    回答生成用のLLMを生成して返す
    
    Returns:
        ChatOpenAI:
            回答生成に使用するLLM
    """

    llm = ChatOpenAI(
        model=CHAT_OPEN_AI_MODEL,
        # 安定、事実重視。RAGでは0が基本
        temperature=0
    )
    
    return llm