# 📚 DocTutor AI

An intelligent PDF chat application that allows you to upload PDFs and interact with them using AI. Built with LangChain, Streamlit, and powered by Mistral AI and OpenAI.
<br>
[visit website](https://doctutor-ai-32bwkdtsk5ah6jbtlnst4u.streamlit.app/)
<br><hr>
[demo](https://youtu.be/eVZEgZwXYrk?si=X1Qq_ysNKIL807_Z)

## Features

- 📄 **PDF Upload & Processing** - Upload PDF files and automatically split them into manageable chunks
- 🔍 **Semantic Search** - Uses embeddings to find relevant content from your documents
- 💬 **AI Chat Interface** - Chat with your documents using an intuitive web interface
- 🧠 **RAG System** - Retrieval-Augmented Generation for accurate, context-aware responses
- 💾 **Vector Database** - Persistent storage of embeddings using ChromaDB
- 🚀 **Two Interfaces** - Web UI with Streamlit and CLI interface for flexibility

## Tech Stack

- **LangChain** - LLM orchestration and RAG implementation
- **Streamlit** - Web application framework
- **ChromaDB** - Vector database for embeddings
- **Mistral AI** - LLM for chat responses
- **OpenAI** - Embeddings generation
- **PyPDF** - PDF loading and processing

## Prerequisites

- Python 3.9+
- Mistral AI API key
- OpenAI API key

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DocTutor AI
   ```

2. **Create a virtual environment**
   ```bash
   uv venv 
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and add your API keys:
   ```
   MISTRAL_API_KEY=your_mistral_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

## Usage

### Web Interface (Streamlit)

```bash
streamlit run app.py
```

Then:
1. Open http://localhost:8501 in your browser
2. Upload a PDF file using the sidebar
3. Click "Process PDF" to create embeddings
4. Start chatting with your document!

### CLI Interface

```bash
python main.py
```

Then:
1. Type your questions in the terminal
2. Get AI-powered answers based on your document
3. Type `0` to exit

### Create Vector Database

To pre-process a PDF and create embeddings:

```bash
python create_database.py
```

Edit the file path in `create_database.py` to process different PDFs.

## Project Structure

```
DocTutor AI/
├── app.py                 # Streamlit web interface
├── main.py               # CLI interface with RAG system
├── create_database.py    # Database initialization script
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables (NOT tracked by git)
├── .env.example          # Example environment file
├── .gitignore           # Git ignore rules
├── pdf/                 # PDF files directory
└── chroma-db/           # Vector database storage
```

## Environment Variables

Create a `.env` file in the root directory:

```
MISTRAL_API_KEY=your_mistral_api_key
OPENAI_API_KEY=your_openai_api_key
```

**Note**: The `.env` file is git-ignored for security. Never commit API keys.

## How It Works

1. **Document Loading** - PDFs are loaded and parsed using PyPDFLoader
2. **Chunking** - Documents are split into overlapping chunks for better context
3. **Embeddings** - Each chunk is converted to embeddings using OpenAI's embedding model
4. **Storage** - Embeddings are stored in ChromaDB for efficient retrieval
5. **Retrieval** - When you ask a question, relevant chunks are retrieved using similarity search
6. **Generation** - Mistral AI generates responses based on the retrieved context

## Configuration

### Text Splitting
- **Chunk Size**: 1000 characters
- **Chunk Overlap**: 200 characters

### Retriever Settings
- **Search Type**: Maximum Marginal Relevance (MMR)
- **K**: 4 relevant documents
- **Fetch K**: 10 initial candidates
- **Lambda Multiplier**: 0.5

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue on the GitHub repository.
