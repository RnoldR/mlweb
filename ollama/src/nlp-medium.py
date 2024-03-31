# from langchain.llms import Ollama
from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader, TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

# get a simple answer from a question
ollama = Ollama(
    base_url='http://localhost:11434',
    model = "mistral",
    # model="llama2",
)

# response = ollama.invoke("why is the sky blue")
# print(response)

print('Reading the Ilias')
# loader = WebBaseLoader("https://www.gutenberg.org/files/1727/1727-h/1727-h.htm")
loader = TextLoader("texts/odessy.htm")
data = loader.load()

print('Splitting the text')
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

# Embed the text
oembed = OllamaEmbeddings(base_url="http://localhost:11434", model="nomic-embed-text")
vectorstore = Chroma.from_documents(documents=all_splits, embedding=oembed, persist_directory="./chroma_db")

# load from disk
# db3 = Chroma(persist_directory="./chroma_db")
# docs = db.similarity_search(query)
# print(docs[0].page_content)

question = "Who is Neptune?" # "Who is Neleus and who is in Neleus' family?"
print(f'Question: {question}')

docs = vectorstore.similarity_search(question)
qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
response = qachain.invoke({"query": question})
print(f"Response: {response['result']}")

n = 10
while n > 0:
    question = response['result'] + '?'
    docs = vectorstore.similarity_search(question)
    qachain=RetrievalQA.from_chain_type(ollama, retriever=vectorstore.as_retriever())
    response = qachain.invoke({"query": question})
    print(f"Response: {response['result']}")

    n = n - 1


