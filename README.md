#  Smart E-Learning AI Chatbot

An intelligent document-based learning assistant that enables users to interact with educational PDF documents using natural language. The application combines **Retrieval-Augmented Generation (RAG)** with semantic search to deliver accurate, context-aware responses based on the uploaded documents instead of relying solely on the language model's internal knowledge.

Built with **Python**, **Streamlit**, **LangChain**, **ChromaDB**, **HuggingFace Embeddings**, and **Mistral AI**, the chatbot provides an interactive platform for students, educators, and researchers to quickly retrieve information from one or multiple PDF files.



#  Key Features

-  Upload and process one or more PDF documents
-  Ask questions in natural language
-  Semantic document retrieval using vector embeddings
-  Context-aware answers generated from uploaded PDFs
-  Displays the relevant document and page information
-  Interactive chat interface built with Streamlit
-  Fast document retrieval using Chroma Vector Database
-  Supports multiple PDF documents simultaneously



#  Technology Stack

 Component - Technology 

 Programming Language - Python 3.11 
 User Interface - Streamlit 
 Framework - LangChain 
 Large Language Model - Mistral Small (mistral-small-2506) 
 Embedding Model - HuggingFace all-MiniLM-L6-v2 
 Vector Database - ChromaDB 
 PDF Loader - PyPDFLoader 
 Text Splitter - Recursive Character Text Splitter 



#  System Architecture



A[Upload PDF Documents]
--> B[PyPDFLoader]

B --> C[Text Extraction]

C --> D[Text Chunking]

D --> E[HuggingFace Embeddings]

E --> F[Chroma Vector Database]

G[User Question]
--> H[Semantic Retriever (MMR)]

F --> H

H --> I[Relevant Document Chunks]

I --> J[Prompt Construction]

J --> K[Mistral AI]

K --> L[Generated Response]

L --> M[Streamlit Chat Interface]
 Workflow

The chatbot follows a Retrieval-Augmented Generation (RAG) pipeline:

Upload one or more PDF documents.
Extract textual content from each document.
Divide the extracted text into overlapping chunks.
Convert each chunk into vector embeddings.
Store embeddings in the Chroma vector database.
Accept a question from the user.
Retrieve the most relevant document chunks using semantic similarity.
Send the retrieved context along with the user query to the Mistral language model.
Generate a context-aware response.
Display the answer along with the corresponding document source.
 Project Structure:
Smart-E-Learning-Chatbot/
│
├── app.py
├── main.py
├── create_database.py
├── requirements.txt
├── .env
│
├── chroma-db/
│
├── pdf/
│
└── README.md
 Installation

Clone the repository

git clone https://github.com/your-username/Smart-E-Learning-Chatbot.git

Move to the project directory

cd Smart-E-Learning-Chatbot

Install the required packages

pip install -r requirements.txt
 Environment Setup

Create a .env file in the project directory.

MISTRAL_API_KEY=your_api_key

Replace your_api_key with your own Mistral API key.

 Running the Application

Launch the Streamlit application

streamlit run app.py

Alternatively, run the command-line version

python main.py
 Retrieval-Augmented Generation (RAG)

Unlike conventional chatbots, this application does not rely solely on the knowledge stored within the language model.

Instead, it follows a Retrieval-Augmented Generation approach:

The uploaded documents are converted into vector embeddings.
Relevant document sections are retrieved whenever a user asks a question.
Only the retrieved content is supplied to the language model.
The generated response is grounded in the uploaded documents, improving accuracy and reducing hallucinated answers.
 Application Overview

The application provides:

Home page for uploading PDF documents
PDF processing interface
Chat interface for question answering
Retrieved source display with page information
Context-aware AI-generated responses
 Future Enhancements

Several improvements can further extend the system:

 Voice-based interaction using speech recognition
 Automatic document summarization
 AI-generated quizzes and flashcards
 Learning analytics dashboard
 Multilingual document support
 Cloud deployment
 User authentication and personalized learning history
 Security

To protect sensitive information:

Store API keys in the .env file.
Never hard-code credentials.
Add .env to .gitignore.
Avoid committing private API keys to GitHub.
 License

This project is distributed under the MIT License.

 Author

Ritom Chakraborty

M.Sc. Computer Science (Data Science)

AI | Machine Learning | Natural Language Processing | Retrieval-Augmented Generation

 
