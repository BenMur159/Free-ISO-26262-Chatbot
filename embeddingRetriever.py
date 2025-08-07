from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os
import pandas as pd




docs = []
#embeddings = OllamaEmbeddings(model="bge-m3")
embeddings = OllamaEmbeddings(model="mxbai-embed-large")
db_location = "./chrome_langchain_db"
data_folder = "./ISO26262"
add_documents = not os.path.exists(db_location)


if add_documents:
  for filename in os.listdir(data_folder):
      if filename.endswith(".txt"):
          path = os.path.join(data_folder, filename)
          with open(path, "r", encoding="utf-8") as f:
              content = f.read()
          doc = Document(
              page_content=content,
              metadata={"source": filename}  # Optional metadata
          )
          docs.append(doc)

  splitter = RecursiveCharacterTextSplitter(
      chunk_size=3200,
      chunk_overlap=1600
  )

  chunks = splitter.split_documents(docs)
  print(len(chunks))

  ids = []
  for i in range(len(chunks)):
    ids.append(str(i))

vector_store = Chroma(
    collection_name="ISO26262",
    persist_directory=db_location,
    embedding_function=embeddings
)

if add_documents:
  print("Embedding and adding documents to Chroma (this may take a while)...")
  vector_store.add_documents(documents=chunks, ids=ids)

retriever = vector_store.as_retriever(
    #search_type="mmr",
    #search_kwargs={'k': 40, 'fetch_k': 100}
    search_kwargs={'k': 20}
)