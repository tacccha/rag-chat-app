import os
from app.rag.similarity_search import similarity_search
from app.rag.generator import get_llm
from app.rag.prompt import get_prompt
from app.rag.memory import chat_history
from app.core.config import MAX_HISTORY

def run_rag(question: str):
    """
    質問に対してRAGを実行し、
    回答と参照元情報を返す

    Args:
        question (str):
            ユーザーからの質問

    Returns:
        dict:
            回答内容と参照元情報
    """
    # score付き検索
    results = similarity_search(question)
    
    # 関連Documentなしの場合
    if len(results) == 0:
        return {
            "answer": "マニュアルに記載がありません",
            "sources": []
        }
    
    # context生成    
    context = "\n\n".join(
        [doc.page_content for doc, _ in results]
    )
    
    # 会話履歴用に「Q: A: 」の形に変換
    history_text = "\n".join([
        f"Q: {item['question']}\nA: {item['answer']}"
        for item in chat_history   
    ])

    # Prompt埋め込み、LLMへ送信 
    chain = get_prompt() | get_llm()
    response = chain.invoke({
        "context": context,
        "history": history_text,
        "question": question
    })
    
    # 会話履歴へ追加
    chat_history.append({
        "question": question,
        "answer": response.content
    })
    
    # 会話履歴数の上限を超えたら古いものを削除
    if len(chat_history) > MAX_HISTORY:
        chat_history.pop(0)
    
    # source情報
    sources = []
    
    for doc, score in results:
        sources.append({
            "title": os.path.basename(doc.metadata.get("source", "")),
            "page": doc.metadata.get("page_number"),
            # "score": score
        })
            
    
    return {
        "answer": response.content,
        "sources": sources
    }