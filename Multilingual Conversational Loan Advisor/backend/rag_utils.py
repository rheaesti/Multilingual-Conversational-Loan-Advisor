from langchain_google_vertexai import VertexAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from typing import List
from langchain_core.tools import tool

# Initialize embeddings model
embeddings = VertexAIEmbeddings(model_name="text-embedding-004")
pdf_paths = [
    "datasets\Loan-Manual-20200602154530.pdf",
]

# Split the documents into smaller chunks
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
all_splits = []

for pdf in pdf_paths:
    loader = PyPDFLoader(pdf)
    docs = loader.load()
    all_splits.extend(text_splitter.split_documents(docs))


# Initialize FAISS with the document chunks
vector_store = FAISS.from_documents(all_splits, embeddings)
_=vector_store.add_documents(documents=all_splits)
vector_store.save_local("ffais_index")



