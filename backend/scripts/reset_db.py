import os
import shutil
from app.core.config import (CHROMA_DB_PATH)

def main():
    if os.path.exists(CHROMA_DB_PATH):
        shutil.rmtree(CHROMA_DB_PATH)
        print("ChromaDBを削除しました")
    else:
        print("ChromaDBは存在しません")


if __name__ == "__main__":
    main()