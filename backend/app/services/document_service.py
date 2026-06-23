import os
import shutil
from fastapi import UploadFile
from glob import glob
from collections import Counter
from langchain_chroma import Chroma
from app.core.config import (
    RAW_DATA_PATH,
    CHROMA_DB_PATH
)
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.vectorstore.embedder import get_embedding
from app.vectorstore.vector_store import create_vectorstore
from app.vectorstore.delete_vector import delete_vectors_by_filename

def get_raw_documents():
    """
    rawフォルダ内のPDF一覧取得

    Returns:
        list:
            PDFファイル名一覧
    """
    pdf_files = glob(
        f"{RAW_DATA_PATH}/*.pdf"
    )
    
    filenames = [os.path.basename(file) for file in pdf_files]
    
    return filenames


def get_vectorstore_documents():
    """
    VectorDB登録済みDocument一覧取得

    Returns:
        list:
            document一覧
    """
    embeddings = get_embedding()
    vectorstore = Chroma(
        persist_directory=CHROMA_DB_PATH,
        embedding_function=embeddings
    )
    
    data = vectorstore.get()
    titles = []
    for metadata in data["metadatas"]:
        title = metadata.get("title")
        if title:
            titles.append(title)
        
    counter = Counter(titles)
    documents = []
    for title, count in counter.items():
        documents.append({
            "title": title,
            "chunks": count
        })
    
    return documents


def upload_document(file: UploadFile):
    """
    PDFアップロードとVectorDB登録
    
    Args:
        file(UploadFile):
            アップロードファイル
    
    Returns:
        dict:
            実行結果
    """
    save_path = f"{RAW_DATA_PATH}/{file.filename}"
    
    # 同盟ファイル確認
    if os.path.exists(save_path):
        return {
            "filename": file.filename,
            "message": "同名ファイルが既に存在します"
        }
        
    try:
        # ファイル保存
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )
        
        # ファイル読み込み
        documents = load_pdf(save_path)
        
        # Chunk分割
        split_docs = create_chunks(documents)
        
        # VectorDB登録
        create_vectorstore(split_docs)
        
        return {
            "filename": file.filename,
            "message": "アップロードとChromaDB登録が完了しました"
        }
    
    except Exception as e:
        # Chroma登録失敗時はPDF削除
        if os.path.exists(save_path):
            os.remove(save_path)
        
        return {
            "filename": file.filename,
            "message": f"アップロード失敗: {str(e)}"
        }
  

def delete_raw_document(filename: str):
    """
    rawフォルダのPDF削除
    
    Args:
        filename(str):
            削除対象ファイル名
    
    Returns:
        dict:
            実行結果
    """
    file_path = f"{RAW_DATA_PATH}/{filename}"
    
    # ファイル存在確認
    if not os.path.exists(file_path):
        return {
            "message": "ファイルが存在しません"
        }
    
    # ファイル削除
    os.remove(file_path)
    
    # ChromaDB削除
    delete_vectors_by_filename(filename)
    
    return {
        "filename": filename,
        "message": "PDFとChromaDB削除完了"
    }
    