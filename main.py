from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Embeddings
embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Load Chroma DB
vectorstore = Chroma(
    persist_directory="chroma-db",
    embedding_function=embedding_model
)

print("Chunks in DB:", vectorstore._collection.count())

# Retriever
retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 25,
        "fetch_k": 80,
        "lambda_mult": 0.5
    }
)

# LLM
llm = ChatMistralAI(
    model="mistral-small-2506"
)

# Prompt
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

print("✅ RAG System Created")
print("Type 0 to exit\n")

while True:

    query = input("You: ")

    if query == "0":
        print("Exiting...")
        break

    docs = retriever.invoke(query)

    if not docs:
        print(
            "\nAI: I could not find any relevant information in the document.\n"
        )
        continue

    context = "\n\n".join(
        doc.page_content
        for doc in docs
    )

    final_prompt = prompt.invoke(
        {
            "context": context,
            "question": query
        }
    )

    response = llm.invoke(final_prompt)

    print(f"\nAI: {response.content}\n")

   
