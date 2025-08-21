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


class LLModel():
    
    def __init__(self, 
                 config: str = '', 
                 embeddings_store: str = False,
                 overwrite = False,
                ):
        self.model = None

        # create default embeddings function
        self.oembed = OllamaEmbeddings(
            base_url = "http://localhost:11434", 
            model = "nomic-embed-text",
        )

        # if a config is specified, read it and build the model
        if len(config) > 0:
            with open(
                'config/config.yaml', 
                encoding = 'utf8', 
                mode = "r"
            ) as infile:
                
                parameters = yaml.safe_load(infile)

                # read model
                model_name = parameters['model']
                self.model = self.get_model(model_name)

                # create the vector store
                if len(embeddings_store) > 0 \
                    and os.path.exists(embeddings_store) \
                    and not overwrite:

                    # Path exists, reload
                    print(f'vector_store load from {embeddings_store}')
                    self.vector_store = self.load_vector_store(embeddings_store)

                else:
                    # read all documents
                    data = self.get_documents(parameters['documents'])

                    self.vector_store = self.create_vector_store(
                        documents = data,
                        persistence = embeddings_store,
                    )

            # with
        # if

        return
    
    ### __init__ ###


    def get_model(self, model_name: str) -> object:
        print(f'Creating model: {model_name}')
        model = Ollama(
            base_url='http://localhost:11434',
            model = model_name,
        )

        return model

    ### get_model ###


    def get_documents(self, paths: list):
        cpu = time.time()

        # load all documents
        documents = []
        for filename in paths:
            # pick a loader
            if filename.endswith('.pdf'):
                print(f'Loading PDF: {filename}')
                loader = PyPDFLoader(filename)

            elif filename.endswith('.epub'):
                print(f'Loading epub: {filename}')
                loader = UnstructuredEPubLoader(filename)

            elif filename.endswith('.txt'):
                print(f'Loading text file: {filename}')
                loader = TextLoader(filename)

            elif filename.startswith('http'):
                print(f'Fetching url: {filename}')
                loader = WebBaseLoader(filename)

            # if

            # load the document
            documents.extend(loader.load())    
        # for

        cpu = time.time() - cpu
        print(f'{len(documents)} documents read in {cpu:.0f} seconds\n')
        
        return documents

    ### get_documents ###


    def create_vector_store(self, documents: list, persistence: str):
        print('Splitting text')
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = config['text_splitter']['chunk_size'], 
            chunk_overlap = config['text_splitter']['chunk_overlap'],
        )
        all_splits = text_splitter.split_documents(documents)

        cpu = time.time()
        print('Embedding...')
        vector_store = Chroma.from_documents(
            documents = all_splits, 
            embedding = self.oembed,
            persist_directory = persistence,
        )

        cpu = time.time() - cpu
        print(f'Embeddings generated in {cpu:.0f} seconds')

        return vector_store
    
    ### create_vector_store ###


    def load_vector_store(self, persistence: str):
        print(f'Loading embeddings from {persistence}')

        vector_store = Chroma(
            persist_directory = persistence, 
            embedding_function = self.oembed,
        )     

        return vector_store              

    ### load_vector_store ###


    def ask(self, question: str) -> str:
        self.vector_store.similarity_search(question)
        qachain = RetrievalQA.from_chain_type(
            self.model, 
            retriever = self.vector_store.as_retriever(),
        )
        
        response = qachain.invoke({"query": question})

        return response['result'].strip()

    ### ask ###

### Class: LLModel ###


os.environ.setdefault('CUDA_VISIBLE_DEVICES', '0,1')

config = common.load_parameters()

llm = LLModel('config/config.yaml', './data')

print('\n[Initialized from config.yaml]\n')

print('')
question = input('Your question: ')
while question != 'q':
    print('')
    response = llm.ask(question)
    print(response)

    print('')
    question = input('Next question: ')

# while
