# -*- coding: utf-8 -*-

import tempfile
import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate

# -----------------------------
# Load Environment Variables
# -----------------------------
load_dotenv()

# -----------------------------
# Page Config
# -----------------------------
st.set_page_config(
    page_title="Smart E-Learning AI Chatbot",
    page_icon="💬",
    layout="wide"
)

st.title("📖 Smart E-Learning AI Chatbot 🎓")
st.caption("Upload one or more PDFs and chat with them")

# -----------------------------
# Session State
# -----------------------------
if "vectorstore" not in st.session_state:
    st.session_state.vectorstore = None

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.header("📄 Upload PDFs")

    uploaded_files = st.file_uploader(
        "Choose PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} PDF(s) uploaded"
        )

        if st.button("Process PDFs"):

            with st.spinner("Processing PDFs..."):

                all_docs = []

                # Load all PDFs
                for uploaded_file in uploaded_files:

                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as tmp_file:
                        
                        uploaded_file.seek(0)

                        tmp_file.write(
                            uploaded_file.getvalue()
                        )

                        # tmp_file.write(
                        #     uploaded_file.read()
                        # )

                        pdf_path = tmp_file.name

                    loader = PyPDFLoader(pdf_path)

                    docs = loader.load()

                    st.write(
                        f"{uploaded_file.name} -> {len(docs)} pages"
                    )

                    # # Store PDF filename
                    # for doc in docs:
                    #     doc.metadata[
                    #         "source_file"
                    #     ] = uploaded_file.name

                    # all_docs.extend(docs)

                    # Store PDF filename and page number
                    for page_num, doc in enumerate(docs, start=1):
                         doc.metadata["source_file"] = uploaded_file.name
                         doc.metadata["page"] = page_num
                    
                    all_docs.extend(docs)

                    st.write(f"Total pages loaded: {len(all_docs)}")
                
                if len(all_docs) == 0:
                    st.error(
                         "No pages could be extracted from the PDF."
                    )
                    st.stop()
                # Split documents
                splitter = RecursiveCharacterTextSplitter(
                    # chunk_size=1000,
                    # chunk_overlap=200
                    chunk_size=1500,
                    chunk_overlap=300
                )

                chunks = splitter.split_documents(
                    all_docs
                )

                # Free embeddings
                embedding_model = HuggingFaceEmbeddings(
                    model_name=
                    "sentence-transformers/all-MiniLM-L6-v2"
                    #"sentence-transformers/all-mpnet-base-v2"

                )

                st.write(f"Pages loaded: {len(all_docs)}")
                st.write(f"Chunks created: {len(chunks)}")

                if len(chunks) > 0:
                     st.write("First chunk:")
                     st.write(chunks[0].page_content[:300])

                test_embedding = embedding_model.embed_query("hello")
                st.write(f"Embedding dimension: {len(test_embedding)}")

                # Create Chroma vector DB
                vectorstore = Chroma.from_documents(
                    documents=chunks,
                    embedding=embedding_model
                )

                st.session_state.vectorstore = (
                    vectorstore
                )

                st.success(
                    f"Processed "
                    f"{len(uploaded_files)} PDFs | "
                    f"{len(all_docs)} pages | "
                    f"{len(chunks)} chunks"
                )

# -----------------------------
# Display Chat History
# -----------------------------
for chat in st.session_state.chat_history:

    with st.chat_message("user"):
        st.write(chat["question"])

    with st.chat_message("assistant"):
        st.write(chat["answer"])

# -----------------------------
# Chat Interface
# -----------------------------
selected_pdf = None

if st.session_state.vectorstore:

    # uploaded_pdf_names = list(
    #     set(
    #         chat_doc.metadata.get("source_file")
    #         for chat_doc in st.session_state.vectorstore.get()["metadatas"]
    #     )
    # )

    uploaded_pdf_names = list(
        set(
            meta.get("source_file")
            for meta in st.session_state.vectorstore.get()["metadatas"]
            if meta.get("source_file")
        )
    )



    selected_pdf = st.selectbox(
        "📄 Select PDF to chat",
        uploaded_pdf_names
    )


    query = st.chat_input(
        "Ask something about your PDFs..."
    )

    if query:

        with st.chat_message("user"):
            st.write(query)

        # retriever = (
        #     st.session_state.vectorstore
        #     .as_retriever(
        #         # search_type="mmr",
        #         # search_kwargs={
        #         #     "k": 4,
        #         #     "fetch_k": 10,
        #         #     "lambda_mult": 0.5
        #         # }
        #         retriever = st.session_state.vectorstore.as_retriever(
        #             search_type="similarity",
        #             search_kwargs={
        #                 "k": 8,
        #                 "fetch_k": 20
        #             }
        #         )
        #     )
        # )

        retriever = st.session_state.vectorstore.as_retriever(
            search_type="mmr",
            search_kwargs={
                "k": 25,
                "fetch_k": 80,
                "lambda_mult": 0.5,

                # "filter": {
                #     "source_file": selected_pdf
                # }
            }
        )

        #docs = retriever.invoke(query)

        docs = retriever.invoke(query)

        if selected_pdf:
            docs = [
                doc for doc in docs
                if doc.metadata.get("source_file") == selected_pdf
        ]

        print("\n" + "="*80)
        print("QUERY:", query)
        print("="*80)

        for i, doc in enumerate(docs):
            print(f"\nCHUNK {i+1}\n")
            print(doc.page_content[:1000])

        # docs = st.session_state.vectorstore.similarity_search_with_score(query, k=4)
        # filtered_docs = [doc for doc, score in docs if score < 1.0]

        if not docs:

            answer = (
                "I could not find any relevant "
                "information in the documents."
            )

        else:

            # context = "\n\n".join(
            #     doc.page_content
            #     for doc in docs
            # )

            context = "\n\n---\n\n".join(
                 f"Source {i+1}:\n{doc.page_content}"
                 for i, doc in enumerate(docs)
            )

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """
You are a helpful AI assistant.

Answer ONLY from the provided context.

When the question asks for:
- names
- committee members
- convenors of AILS 2026
- convenors
- lists

extract and return all matching names exactly as written.

The context may come from multiple PDFs.

When answering, mention the source document if available.


If the answer is not present in the context,
say:

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
                model="mistral-small-2603"
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

        # Show retrieved chunks
        if docs:

            with st.expander(
                "📚 Retrieved Sources"
            ):

                for doc in docs:

                    # st.write(
                    #     f"📄 Source: "
                    #     f"{doc.metadata.get('source_file', 'Unknown')}"
                    # )

                    st.write(
                        f"📄 Source: {doc.metadata.get('source_file', 'Unknown')} | "
                        f"Page: {doc.metadata.get('page', 'N/A')}"
                    )

                    st.write(
                        doc.page_content[:500]
                    )

                    st.divider()

else:

    st.info(
        "Upload PDFs and click "
        "'Process PDFs' to begin."
    )