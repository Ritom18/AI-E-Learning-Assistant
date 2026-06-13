import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# ---------------------------------
# Load Environment Variables
# ---------------------------------
load_dotenv()

# ---------------------------------
# Page Config
# ---------------------------------
st.set_page_config(
    page_title="BookGPT",
    page_icon="📚",
    layout="wide"
)

st.title("📚 BookGPT")
st.caption("Upload a PDF and chat with your book")

# ---------------------------------
# Session State
# ---------------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:

    st.header("📄 Upload Book")

    uploaded_file = st.file_uploader(
        "Choose PDF",
        type=["pdf"]
    )

    if uploaded_file:

        st.success(f"Uploaded: {uploaded_file.name}")

        if st.button("Process PDF"):

            with st.spinner("Creating embeddings..."):

                # Save uploaded PDF temporarily
                with tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".pdf"
                ) as tmp_file:

                    tmp_file.write(uploaded_file.read())
                    pdf_path = tmp_file.name

                # Load PDF
                loader = PyPDFLoader(pdf_path)
                docs = loader.load()

                # Split into chunks
                splitter = RecursiveCharacterTextSplitter(
                    chunk_size=1000,
                    chunk_overlap=200
                )

                chunks = splitter.split_documents(docs)

                # Embeddings
                embedding_model = OpenAIEmbeddings()

                # Create Chroma DB
                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embedding_model,
                    persist_directory="chroma-db"
                )

                st.session_state.vectorstore = vectorstore

                st.success(
                    f"Done! {len(chunks)} chunks created."
                )

# ---------------------------------
# Chat History
# ---------------------------------
for chat in st.session_state.chat_history:

    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

# ---------------------------------
# Ask Questions
# ---------------------------------
if st.session_state.vectorstore:

    query = st.chat_input(
        "Ask something about the book..."
    )

    if query:

        with st.chat_message("user"):
            st.write(query)

        # Retriever
        retriever = (
            st.session_state.vectorstore
            .as_retriever(
                search_type="mmr",
                search_kwargs={
                    "k": 4,
                    "fetch_k": 10,
                    "lambda_mult": 0.5
                }
            )
        )

        docs = retriever.invoke(query)

        if not docs:

            answer = (
                "I could not find any relevant "
                "information in the document."
            )

        else:

            context = "\n\n".join(
                doc.page_content
                for doc in docs
            )

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
You are a helpful AI assistant.

Use ONLY the provided context.

If the answer is not present in the context, say:

'I could not find the answer in the document.'

Do not make up information.
"""
                    ),
                    (
                        "human",
                        """
Context:
{context}

Question:
{question}
"""
                    )
                ]
            )

            final_prompt = prompt.invoke(
                {
                    "context": context,
                    "question": query
                }
            )

            llm = ChatMistralAI(
                model="mistral-small-2506"
            )

            response = llm.invoke(
                final_prompt
            )

            answer = response.content

        with st.chat_message("assistant"):
            st.write(answer)

        st.session_state.chat_history.append(
            {
                "question": query,
                "answer": answer
            }
        )

        if docs:
            with st.expander(
                "Retrieved Context"
            ):
                st.write(context)

else:

    st.info(
        "Upload a PDF and click "
        "'Process PDF' to begin."
    )