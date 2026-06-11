from app.rag.retriever import get_retriever

def main():
    retriever = get_retriever()
    
    question = "VLANの設定方法を教えて"
    
    # 検索実行
    results = retriever.invoke(question)
    
    print(f"質問：{question}")
    print("=" * 50)
    
    # enumerate:番号付きで取り出す
    for i, doc in enumerate(results, 1):
        print(f"【結果】 {i}")
        # 最初の500文字だけ表示
        print(doc.page_content[:500])
        print(doc.metadata)
        print("=" * 50)
    
if __name__ == "__main__":
    main()