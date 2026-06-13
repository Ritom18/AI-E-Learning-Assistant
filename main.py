
from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma


embedding_model = OpenAIEmbeddings()


vectorstore = Chroma(
    persist_directory="chroma-db",
    embedding_function=embedding_model
)


retriever = vectorstore.as_retriever(
    search_type="mmr",
    search_kwargs={
        "k": 4,
        "fetch_k": 10,
        "lambda_mult": 0.5
    }
)
print("Chunks in DB:", vectorstore._collection.count())

llm = ChatMistralAI(
    model="mistral-small-2506"
)


prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a helpful AI assistant.

Use ONLY the provided context to answer the question.

If the answer is not present in the context, say:
"I could not find the answer in the document."

Do not make up information.
"""
        ),
        (
            "human",
            """Context:
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

    # Retrieve relevant documents
    docs = retriever.invoke(query)

    if not docs:
        print("\nAI: I could not find any relevant information in the document.\n")
        continue

  
    context = "\n\n".join(
        doc.page_content for doc in docs
    )


    
    final_prompt = prompt.invoke(
        {
            "context": context,
            "question": query
        }
    )

   
    response = llm.invoke(final_prompt)
    
    print(f"\nAI: {response.content}\n")

   
