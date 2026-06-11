from app.core.config import (CHROMA_DB_PATH, TOP_K)
from langchain_chroma import Chroma
from app.vectorstore.embedder import get_embedding

def get_retriever():
    """
    不要
    
    保存済みのChromaDBを読み込み、
    類似検索用のRetrieverを生成して返す

    Returns:
        BaseRetriever:
            類似検索を行うRetriever
    """
    
    # embeddingモデル呼び出し
    embeddings = get_embedding();
    
    
    
    # 保存済みのDBを開く
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )
    
    # 検索専用にする
    retriever = vectorstore.as_retriever(
        # 上位3件
        search_kwargs={"k": TOP_K}
    )
    
    return retriever