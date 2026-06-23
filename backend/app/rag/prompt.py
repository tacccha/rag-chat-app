from langchain_core.prompts import ChatPromptTemplate

def get_prompt():
    """
    RAG用の回答生成プロンプトを作成して返す

    Returns:
        ChatPromptTemplate:
            回答生成に使用するPrompt
    """
    
    template = """
あなたは社内マニュアル回答アシスタントです。

以下のルールに従って回答してください。

* 日本語で回答
* 回答は簡潔に
* 箇条書きを使う
* 設定値やコマンドはコードブロックで表示
* 参考情報にない内容を推測しない
* 不明な場合は「マニュアルに記載がありません」と回答

過去の会話：
{history}

参考情報：
{context}

質問：
{question}

回答：
"""

    prompt = ChatPromptTemplate.from_template(
        template      
    )
    
    return prompt