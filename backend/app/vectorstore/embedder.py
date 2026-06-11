from app.core.config import (EMBEDDING_MODEL)
from langchain_openai import OpenAIEmbeddings

def get_embedding():
    """
    OpenAIのEmbeddingモデルを生成して返す

    Returns:
        OpenAIEmbeddings:
            ベクトル化に使用するEmbeddingモデル
    """    
    embeddings = OpenAIEmbeddings(
        model = EMBEDDING_MODEL
    )
    
    return embeddings