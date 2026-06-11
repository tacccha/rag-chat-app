from langchain_text_splitters import RecursiveCharacterTextSplitter

def create_chunks(documents):
    """
    PDFから読み込んだDocumentを
    chunk単位に分割し、
    metadataを付与して返す

    Args:
        documents (list):
            loader.pyで読み込んだDocument一覧

    Returns:
        list:
            chunk分割後のDocument一覧
    """
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 700,
        chunk_overlap = 100,
        separators = ["\n\n", "\n", "。", " ", ""]
    )
    # 分割実行
    split_docs = text_splitter.split_documents(documents)
    
    # 情報追加
    for i,  doc in enumerate(split_docs):
        # ファイル名、ページ番号取得
        source = doc.metadata.get("source", "")
        page = doc.metadata.get("page", 0)
        
        title = source.split("/")[-1]
        
        doc.metadata["document_type"] = "manual"
        doc.metadata["title"] = title
        doc.metadata["page_number"] = page
        
        # chunk番号
        doc.metadata["chunk_index"] = i
        
        # document識別ID
        doc.metadata["doc_id"] = f"{title}_{page}_{i}"
    
    return split_docs