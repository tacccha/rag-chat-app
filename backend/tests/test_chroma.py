import sys
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)

from langchain_chroma import Chroma
from app.vectorstore.embedder import get_embedding
from app.core.config import CHROMA_DB_PATH

embeddings = get_embedding()

vectorstore = Chroma(
    persist_directory=CHROMA_DB_PATH,
    embedding_function=embeddings
)

data = vectorstore.get()

print("===== Document Count =====")
print(len(data["ids"]))

print("\n===== First Metadata =====")
print(data["metadatas"][:5])