from app.core.config import (CHROMA_DB_PATH, TOP_K, SCORE_THRESHOLD)
from langchain_chroma import Chroma
from app.vectorstore.embedder import get_embedding

def similarity_search(question, filename=None, k=None):
    """
    類似度スコア付き類似検索
    
    Args:
        question(str):
            検索質問
        
        filename (str | None):
            検索対象PDF
        
        k(int):
            取得件数
    
    Returns:
        list:
            Documentとscore一覧
    """
    embeddings = get_embedding()
    
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )
    
    where = None
    # filename設定時だけフィルター
    if filename:
        where = {
            "title": filename
        }
        
    if k is None:
        k = TOP_K
    
    # 検索結果とスコアを返す
    results = vectorstore.similarity_search_with_score(
        question,
        k=k,
        filter=where
    )
    
    # 検索結果の精度確認
    filtered_results = []
    for doc, score in results:
        # scoreが低いほど近い
        if score <= SCORE_THRESHOLD:
            filtered_results.append(
                (doc, score)
            )
    
    return filtered_results