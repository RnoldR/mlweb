# from langchain.llms import Ollama
import os
import time

from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders import UnstructuredEPubLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

def get_model(model_name: str) -> object:
    print(f'Creating model {model_name}')
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


def fast_answer(ollama, question: str) -> str:
    response = ollama.invoke(question)

    return response

### fast_answer ###


def ask(model, vectorstore, question: str) -> str:
    docs = vectorstore.similarity_search(question)
    qachain=RetrievalQA.from_chain_type(model, retriever=vectorstore.as_retriever())
    response = qachain.invoke({"query": question})

    return response['result'].strip()

### ask ###


doc_00 = 'https://www.gutenberg.org/files/1727/1727-h/1727-h.htm'
doc_01 = '/media/i-files/data/books/SF/Alastair Reynolds/Revelation Space 01 - Revelation Space (2000).epub'
model_01 = 'mistral'

# os.environ.setdefault("PYPANDOC_PANDOC", "/media/i-files/home/arnold/development/python/django/mlweb/.venv/lib64/python3.10/site-packages/pandoc")
print('\n[Started]\n')

ollama = get_model(model_01)
docs = get_epub(doc_01)

cpu = time.time()
print('Loading data')
data = docs.load() 
cpu = time.time() - cpu
print(f'Loaded in {cpu:.0f} seconds')

print('Splitting text')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=20)
all_splits = text_splitter.split_documents(data)

cpu = time.time()
print('Embedding...')
oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed)
cpu = time.time() - cpu
print(f'Embeddings generated in {cpu:.0f} seconds')

question = "Who is Anna Khouri and who is her husband?"
while question != 'q':
    response = ask(ollama, vectorstore, question)
    print(response)

    print('')
    question = input('Next question: ')
    print('')

# while
