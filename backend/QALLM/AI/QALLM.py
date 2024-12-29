from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import USearch
from usearch.index import Index
from langchain_community.document_loaders.pdf import PyPDFDirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_experimental.text_splitter import SemanticChunker
from langchain_community.docstore.in_memory import InMemoryDocstore
import json
import numpy as np
from langchain_core.documents import Document
import os
from langchain_core.documents import Document
import fitz 
import datetime

def load_pdf_from_memory(file_bytes, file_name):
    """
    Tải tài liệu từ bytes của file PDF và thêm tên file vào metadata.
    """
    documents = []
    pdf = fitz.open(stream=file_bytes, filetype="pdf")  # Mở file PDF từ bytes
    for page_number in range(len(pdf)):
        page = pdf[page_number]
        text = page.get_text()  # Lấy nội dung văn bản từ trang
        metadata = {"source": file_name, "page": page_number + 1}
        documents.append(Document(page_content=text, metadata=metadata))
    return documents

def calculate_chunk_ids(chunks):
   
    last_page_id = None
    current_chunk_index = 0

    for chunk in chunks:
        source = chunk.metadata.get("source")
        page = chunk.metadata.get("page")
        current_page_id = f"{source}:{page}"

        if current_page_id == last_page_id:
            current_chunk_index += 1
        else:
            current_chunk_index = 0

        chunk_id = f"{current_page_id}:{current_chunk_index}"
        last_page_id = current_page_id

        chunk.metadata["id"] = chunk_id

    return chunks
def add_files_to_usearch_from_memory(files):
    sources=[]

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        google_api_key="AIzaSyBwRi6f7aoxXxpwy5RhOThn0cOOV9_zI50"
    )

    print("Loading documents")
    documents = []
    for file in files:
        file_content = file["content"]
        file_name = file["name"]
        sources.append(
            {
                "file_name": file_name, 
                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
        )
        # Sử dụng PyMuPDF để tải dữ liệu từ bytes
        docs = load_pdf_from_memory(file_content, file_name)
        documents.extend(docs)

    print("Chunking")
    text_splitter = SemanticChunker(embeddings, breakpoint_threshold_amount=0.95)
    chunks = text_splitter.split_documents(documents)
    chunks_with_ids = calculate_chunk_ids(chunks)

    texts = [chunk.page_content for chunk in chunks_with_ids]
    metadatas = [chunk.metadata for chunk in chunks_with_ids]

    print("Adding to db")
    if not os.path.exists('metadata.json'):
        db = USearch.from_texts(embedding=embeddings, texts=texts, metadatas=metadatas)
        db.index.save("index.usearch")
    else:
        with open("metadata.json", "r") as f:
            loaded_docstore = json.load(f)
        data = loaded_docstore['docstore']
        documents = {
            doc_id: Document(metadata=item["metadata"], page_content=item["page_content"])
            for doc_id, item in zip(loaded_docstore['ids'], data)
        }
        docstore = InMemoryDocstore(documents)
        view = Index.restore("index.usearch", view=False)
        db = USearch(embedding=embeddings, index=view, docstore=docstore, ids=loaded_docstore['ids'])
        db.add_texts(texts=texts, metadatas=metadatas)
        db.index.save("index.usearch")
        sources = loaded_docstore["sources"] + sources
    serializable_docstore = [
        {
            "metadata": {"id": doc.metadata["id"]},
            "page_content": doc.page_content,
            "id": key,
        }
        for key, doc in db.docstore._dict.items()
    ]

    print("Các ID đã thêm:", db.docstore, db.index)

    with open("metadata.json", "w") as f:
        json.dump({"docstore": serializable_docstore, "ids": db.ids, "sources": sources}, f)

def get_sources():
    if not os.path.exists('metadata.json'):
        sources = []
    else:
        with open("metadata.json", "r") as f:
                loaded_docstore = json.load(f)
        sources = loaded_docstore["sources"]
        print(sources)
        # sources = [source["file_name"] for source in loaded_docstore["sources"]]
    return sources
               
def query_search(query):       
    PROMPT_TEMPLATE = """
    Answer the question based only on the following context:

    {context}

    ---

    Answer the question based on the above context: {question}.
    Answer by Vietnamese.
    """

    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key="AIzaSyBwRi6f7aoxXxpwy5RhOThn0cOOV9_zI50")
    with open("metadata.json", "r") as f:
            loaded_docstore = json.load(f)
    data = loaded_docstore['docstore']

    documents = {
        doc_id: Document(metadata=item["metadata"], page_content=item["page_content"])
        for doc_id, item in zip(loaded_docstore['ids'], data)
    }
    docstore = InMemoryDocstore(documents)
    view = Index.restore("index.usearch", view=False)
    db = USearch(embedding=embeddings, index=view, docstore=docstore, ids=loaded_docstore['ids'])

    results = db.similarity_search_with_score(query, k=10)
    context_text = "\n\n---\n\n".join([doc.page_content.strip() for doc, _score in results])
    print(context_text)
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    model = GoogleGenerativeAI(model="gemini-1.5-pro", google_api_key="AIzaSyBwRi6f7aoxXxpwy5RhOThn0cOOV9_zI50")
    response_text = model.invoke(prompt)

    sources = [doc.metadata.get("id", None) for doc, _score in results]
    print(response_text)
    formatted_response = f"Sources: {sources}"
    print(formatted_response)
    return(response_text, formatted_response)