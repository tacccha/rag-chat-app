from langchain_community.document_loaders import PyPDFLoader

def load_pdf(file_path: str):
    """
    指定したPDFファイルを読み込み、
    LangChainのDocument形式で返す

    Args:
        file_path (str):
            読み込むPDFファイルのパス

    Returns:
        list:
            PDFから読み込んだDocument一覧
    """
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents