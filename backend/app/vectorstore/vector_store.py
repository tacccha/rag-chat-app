from app.core.config import (CHROMA_DB_PATH)
from langchain_chroma import Chroma
from app.vectorstore.embedder import get_embedding

def create_vectorstore(split_docs):
    """
    chunk分割したDocumentをEmbedding(ベクトル変換)し、
    ChromaDBへ保存する

    Args:
        split_docs (list):
            chunk分割後のDocument一覧

    Returns:
        Chroma:
            保存済みのVector Store
    """
    
    embeddings = get_embedding()
    
    # Chroma接続
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )
    
    # 追加対象
    new_docs = []
    new_ids = []
    
    # 登録済か確認
    for doc in split_docs:
        doc_id = doc.metadata["doc_id"]
        
        # 既存確認
        existing = vectorstore.get(
            ids=[doc_id]
        )
        
        # 未登録なら追加対象へ
        if len(existing["ids"]) == 0:
            new_docs.append(doc)
            new_ids.append(doc_id)
        
    # 新規だけ追加
    if new_docs:
        
        BATCH_SIZE = 5000
        
        for i in range(0, len(new_docs), BATCH_SIZE):
            batch_docs = new_docs[i:i + BATCH_SIZE]
            batch_ids = new_ids[i:i + BATCH_SIZE]
        
            vectorstore.add_documents(
                documents=batch_docs,
                ids= batch_ids
            )
        
        print(f"{len(new_docs)}件を登録しました。")
    
    else:
        print("新規Documentはありません。")
        
    return vectorstore