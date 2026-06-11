from app.core.config import (CHROMA_DB_PATH)
from langchain_chroma import Chroma
from app.vectorstore.embedder import get_embedding

def delete_vectors_by_filename(filename):
    """
    指定ファイルのVectorを削除する
    
    Args:
        filename (str):
            PDFファイル名
    """
    embeddings = get_embedding()
    
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )
    
    # metadata検索
    results = vectorstore.get(
        where={
            "title": filename
        }
    )
    
    ids = results["ids"]
    
    if ids:
        vectorstore.delete(ids=ids)
        
        print(f"{len(ids)}件削除しました。")
    
    else:
        print("削除対象なし")
    
