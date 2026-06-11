from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from app.core.config import (RAW_DATA_PATH)
from app.rag.pipeline import run_rag
from app.rag.similarity_search import similarity_search
from app.services.document_service import (
    get_raw_documents,
    get_vectorstore_documents,
    upload_document,
    delete_raw_document
)

app = FastAPI()

# middleware設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    """
    質問リクエスト 
    """
    # strのJSONの型
    question: str

class SearchRequest(BaseModel):
    """
    検索リクエスト
    """
    question: str
    filename: str | None = None
    

class DeleteRequest(BaseModel):
    """
    削除リクエスト
    """
    filename: str

@app.get("/")
def root():
    # APIが起動してるか確認のみ
    return {"message": "RAG API is running"}


@app.get("/documents/raw")
def raw_documents():
    """
    rawフォルダ内PDF一覧
    """
    documents = get_raw_documents()
        
    return { "documents": documents }


@app.get("/documents/vectorstore")
def vectorstore_documents():
    """
    VectorDB登録済みDocument一覧
    """
    documents = get_vectorstore_documents()

    return { "documents": documents }


@app.post("/ask")
def ask_question(request: QuestionRequest):
    """
    質問を受け取り
    RAGで回答を返す
    """
    answer = run_rag(request.question)
    
    return {
        "question": request.question,
        "answer": answer
    }


@app.post("/upload")
def upload_file(file: UploadFile = File(...)):
    """
    PDFをアップロードして保存し、
    ChromaDBへ登録する
    """
    result = upload_document(file)
        
    return result


@app.post("/search")
def score_document(request: SearchRequest):
    """
    score付き類似検索
    """
    results = similarity_search(
        question=request.question,
        filename=request.filename
    )
    
    response = []
    
    for doc, score in results:
        response.append({
            "score": score,
            "content": doc.page_content,
            "metadata": doc.metadata
        })
    
    return {
        "question": request.question,
        "results": response
    }
    

@app.delete("/delete")
def delete_document(request: DeleteRequest):
    """
    PDFを削除する
    """
    result = delete_raw_document(request.filename)
    
    return result