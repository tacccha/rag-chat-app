from app.rag.pipeline import run_rag

def main():
    question = "VLANの設定方法を教えて"
    
    answer = run_rag(question)
    
    print(f"質問：{question}")
    print("=" * 50)
    print("【回答】")
    print(answer)
    
if __name__ == "__main__":
    main()