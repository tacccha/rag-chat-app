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

以下の参考情報の中から、
質問に直接関係する内容だけを使って回答してください。

参考情報に書かれていない内容を
推測して回答してはいけません。

不明な場合は
「マニュアルに記載がありません」
と答えてください。

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