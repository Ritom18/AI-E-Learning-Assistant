from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# Load PDF
loader = PyPDFLoader("pdf/Numpy.pdf")
docs = loader.load()

# Split PDF
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=300
)

chunks = splitter.split_documents(docs)

# Free local embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create vector DB
vectorstore = Chroma.from_documents(
    documents=chunks,
    embedding=embedding_model,
    persist_directory="chroma-db"
)

print(f"Pages loaded: {len(docs)}")
print(f"Chunks created: {len(chunks)}")
print("Database created successfully.")