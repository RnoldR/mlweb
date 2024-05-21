# from langchain.llms import Ollama
import os
import time
import yaml

from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import UnstructuredEPubLoader
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

import common

def get_model(model_name: str) -> object:
    print(f'Creating model: {model_name}')
    ollama = Ollama(
        base_url='http://localhost:11434',
        model = model_name,
        # model = "mistral",
    )

    return ollama

### get_model ###


def get_webdoc(url: str) -> object:
    print(f'Fetching url: {url}')
    doc = WebBaseLoader(url)
    
    return doc

### get_webdoc ###


def get_epub(doc_name: str) -> object:
    print(f'Fetching epub: {doc_name}')
    epub = UnstructuredEPubLoader(doc_name)

    return epub

### get_epub ###


def get_documents(paths: list):
    cpu = time.time()

    documents = []

    for filename in paths:
        if filename.endswith('.pdf'):
            print(f'Loading PDF: {filename}')
            loader = PyPDFLoader(filename)
            documents.extend(loader.load())

        elif filename.endswith('.epub'):
            print(f'Loading epub: {filename}')
            loader = UnstructuredEPubLoader(filename)
            documents.extend(loader.load())

        elif filename.endswith('.txt'):
            print(f'Loading text file: {filename}')
            loader = TextLoader(filename)
            documents.extend(loader.load())    

        # if
    # for

    cpu = time.time() - cpu
    print(f'{len(documents)} documents read in {cpu:.0f} seconds\n')
    
    return documents

### get_documents ###


def fast_answer(ollama, question: str) -> str:
    response = ollama.invoke(question)

    return response

### fast_answer ###


def create_vector_store(documents: list, persistence: str):
    print('Splitting text')
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = config['text_splitter']['chunk_size'], 
        chunk_overlap = config['text_splitter']['chunk_overlap'],
    )
    all_splits = text_splitter.split_documents(documents)

    cpu = time.time()
    print('Embedding...')
    oembed = OllamaEmbeddings(
        base_url = "http://localhost:11434", 
        model = "nomic-embed-text",
    )

    vectorstore = Chroma.from_documents(
        documents = all_splits, 
        embedding = oembed,
        persist_directory = persistence,
    )

    cpu = time.time() - cpu
    print(f'Embeddings generated in {cpu:.0f} seconds')

    return vectorstore

### create_vector_store ###


def ask(model, vectorstore, question: str) -> str:
    docs = vectorstore.similarity_search(question)
    qachain = RetrievalQA.from_chain_type(
        model, 
        retriever = vectorstore.as_retriever(),
    )
    
    response = qachain.invoke({"query": question})

    return response['result'].strip()

### ask ###


os.environ.setdefault('CUDA_VISIBLE_DEVICES', '0,1')

config = common.load_parameters()

print('\n[Initialized from config.yaml]\n')

# read model
model_name = config['model']
model = get_model(model_name)

# read all documents
documents = config['documents']
data = get_documents(documents)

# create the vector store
vector_store = create_vector_store(
    documents = data,
    persistence = './data',
)

print('')
question = input('Your question: ')
while question != 'q':
    print('')
    response = ask(model, vector_store, question)
    print(response)

    print('')
    question = input('Next question: ')

# while
