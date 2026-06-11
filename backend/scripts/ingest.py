from glob import glob
from app.ingestion.loader import load_pdf
from app.ingestion.chunker import create_chunks
from app.vectorstore.vector_store import create_vectorstore

def main():
    # PDFの読み込み
    pdf_files = glob("data/raw/*.pdf")
    all_documents = []
    for file_path in pdf_files:
        documents = load_pdf(file_path)
        all_documents.extend(documents)
        print(f"{file_path}を読み込みました。")
            
    print(f"総読み込み件数: {len(all_documents)}")
    
    # chunk生成
    split_docs = create_chunks(all_documents)  
    print(f"chunk数: {len(split_docs)}")
    print(split_docs[0].metadata)
    
    # DBへ登録
    create_vectorstore(split_docs)
    print("ChromaDBへ保存が完了しました。")
    
        
if __name__ == "__main__":
    main()