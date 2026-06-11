import os
from dotenv import load_dotenv

load_dotenv()

# OpenAI APIキー
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Embeddingで使用するモデル名
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL")

# 回答生成で使用するChatモデル名
CHAT_OPEN_AI_MODEL = os.getenv("CHAT_OPEN_AI_MODEL")

# ChromaDBの保存先ディレクトリ
CHROMA_DB_PATH = os.getenv("CHROMA_DB_PATH")

# アップロードしたPDFの保存先ディレクトリ
RAW_DATA_PATH = os.getenv("RAW_DATA_PATH")


# Retrieverで取得するDocument件数
TOP_K = 3

# 類似検索のscore閾値
# Chromaは低いほど類似度が高い
SCORE_THRESHOLD = 0.7

# 履歴保持件数
MAX_HISTORY = 5