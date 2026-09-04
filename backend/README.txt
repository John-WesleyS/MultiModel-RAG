# Traditional RAG Chatbot

A sophisticated **Retrieval-Augmented Generation (RAG) system** built from scratch in Python, supporting multimodal document processing, semantic search, and AI-powered response generation.

---

## 🎯 Project Overview

This project implements a complete Traditional RAG pipeline that ingests various document types (PDFs, Word documents, images, videos, audio files, and spreadsheets), processes them intelligently, generates embeddings, stores them in a vector database, and retrieves relevant context to provide accurate AI-generated responses.

**Key Features:**
- ✅ **Multimodal Support**: Process documents, images, videos, and audio files
- ✅ **Intelligent Processing**: Automatic file type detection and specialized handlers
- ✅ **Semantic Search**: Vector-based retrieval using state-of-the-art embeddings
- ✅ **Advanced Chunking**: Intelligent text segmentation with metadata preservation
- ✅ **Context-Aware Generation**: AI responses based on retrieved documents
- ✅ **RESTful API**: FastAPI-based endpoints for easy integration

---

## 🏗️ Tech Stack

### Core Framework
- **Python 3.8+** - Primary programming language
- **FastAPI** - High-performance web framework for building APIs
- **Pydantic** - Data validation and settings management

### AI & ML
- **Google Gemini API** - Embeddings generation and response generation
- **Google genai SDK** - Integration with Gemini models

### Vector Database & Storage
- **Qdrant** - Vector database for semantic search and similarity matching
- **PyMuPDF (fitz)** - PDF document processing and extraction

### Document Processing
- **python-docx** - Word document (.docx) handling
- **openpyxl** - Excel spreadsheet processing
- **pptx** - PowerPoint presentation handling
- **PIL (Pillow)** - Image processing
- **OpenCV** - Advanced image/video processing
- **librosa** - Audio processing

### Utilities
- **python-dotenv** - Environment variable management
- **python-multipart** - File upload handling

---

## 📁 Project Structure

```
Traditional-RAG/
│
├── main.py                          # FastAPI application entry point
├── requirements.txt                 # Project dependencies
├── README.txt                        # This file
│
├── app/                            # Main application package
│   ├── main.py                     # App initialization and exports
│   ├── llm.py                      # LLM configuration
│   │
│   ├── embeddings/                 # Embedding generation module
│   │   ├── __init__.py
│   │   └── embedder.py             # Gemini embedding functions
│   │                               # - generate_embeddings()
│   │                               # - generate_query_embedding()
│   │                               # - generate_image_embedding()
│   │
│   ├── ingestion/                  # Document ingestion pipeline
│   │   ├── __init__.py
│   │   ├── file_detector.py        # File type detection
│   │   ├── loader.py               # Document loading orchestration
│   │   ├── cleaner.py              # Text cleaning and normalization
│   │   ├── router.py               # Request routing
│   │   ├── splitter.py             # Text chunking/splitting logic
│   │   ├── metadata.py             # Metadata extraction
│   │   │
│   │   ├── extractors/             # Format-specific extractors
│   │   │   ├── pdf.py              # PDF text extraction
│   │   │   ├── docx.py             # Word document extraction
│   │   │   ├── excel.py            # Excel data extraction
│   │   │   ├── pptx.py             # PowerPoint extraction
│   │   │   └── vedio.py            # Video processing
│   │   │
│   │   ├── loaders/                # Format-specific loaders
│   │   │   ├── __init__.py
│   │   │   ├── loader.py           # Base loader class
│   │   │   ├── pdf_loader.py       # PDF file loader
│   │   │   ├── docx_loader.py      # Word file loader
│   │   │   ├── excel_loader.py     # Excel file loader
│   │   │   ├── csv_loader.py       # CSV file loader
│   │   │   ├── text_loader.py      # Text file loader
│   │   │   ├── pptx_loader.py      # PowerPoint loader
│   │   │   └── image_extractor.py  # Image extraction
│   │   │
│   │   └── processors/             # Content-specific processors
│   │       ├── document_processor.py  # Main document processor
│   │       ├── text_processor.py      # Text processing
│   │       ├── image_processor.py     # Image analysis & description
│   │       ├── video_processor.py     # Video analysis & extraction
│   │       ├── audio_processor.py     # Audio processing
│   │       └── table_processor.py     # Table extraction & processing
│   │
│   ├── llm/                        # Language Model Module
│   │   ├── __init__.py
│   │   ├── llm.py                  # LLM response generation
│   │   │                           # - generate_response()
│   │   │                           # - describe_media()
│   │   └── prompt.py               # Prompt engineering and construction
│   │
│   ├── retrieval/                  # Retrieval & Context Module
│   │   ├── __init__.py
│   │   ├── retriever.py            # Semantic search and retrieval
│   │   │                           # - retrieve_multimodal()
│   │   │                           # - understand_query()
│   │   ├── context_builder.py      # Build context for LLM
│   │   └── source_builder.py       # Build source citations
│   │
│   └── vectorstore/                # Vector Database Module
│       ├── __init__.py
│       └── qdrant.py               # Qdrant vector store operations
│                                   # - create_collection()
│                                   # - store_chunks()
│                                   # - search_similar_chunks()
│
├── media/                          # Processed media storage
│   ├── [UUID folders]/             # Organized by document ID
│   │   └── [chunk data files]
│   
├── qdrant_data/                    # Qdrant database storage
│   ├── meta.json
│   └── collection/
│       └── documents/
│
└── tests/                          # Comprehensive test suite
    ├── test_embeddings.py          # Embedding generation tests
    ├── test_retrieval.py           # Retrieval functionality tests
    ├── test_file_router.py         # File routing tests
    ├── test_rag_pipeline.py        # End-to-end pipeline tests
    ├── test_context.py             # Context building tests
    ├── test_gemini.py              # Gemini API integration tests
    ├── test_llm.py                 # LLM response generation tests
    ├── test_multimodal_api.py      # Multimodal API tests
    ├── test_prompt.py              # Prompt construction tests
    └── app/test_splitter.py        # Text splitting tests
```

---

## 📋 Supported File Types

The system intelligently detects and processes the following file formats:

### 📄 Documents
- **PDF** (.pdf) - Via PyMuPDF with text extraction
- **Word** (.docx) - Via python-docx library
- **Text** (.txt) - Plain text files
- **PowerPoint** (.pptx) - Presentation slides

### 📊 Spreadsheets & Data
- **Excel** (.xlsx, .xls) - Via openpyxl
- **CSV** (.csv) - Comma-separated values

### 🖼️ Images
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)
- **WebP** (.webp)

### 🎬 Multimedia
- **Video** (.mp4, .avi, .mov, .mkv) - Video frame extraction & analysis
- **Audio** (.mp3, .wav, .m4a) - Speech recognition & audio processing

---

## 🔄 Processing Pipeline

### Document Ingestion Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     File Upload                              │
│              (PDF, DOCX, Images, Video, Audio)              │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                  File Type Detection                          │
│         (file_detector.py) → Determine file format           │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│            Format-Specific Content Extraction                 │
│  • PDF: Text extraction via PyMuPDF                          │
│  • Images: Description via Gemini vision                     │
│  • Video: Frame extraction + temporal analysis               │
│  • Audio: Transcription via Gemini                           │
│  • Tables: Structured data extraction                        │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    Text Cleaning                              │
│   • Remove special characters & normalization                │
│   • Handle encoding issues                                   │
│   • Clean whitespace & formatting                            │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                  Intelligent Chunking                         │
│  • Semantic-aware text splitting                             │
│  • Preserve context boundaries                               │
│  • Configurable chunk size & overlap                         │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│               Metadata Extraction                             │
│  • Document source tracking                                  │
│  • Chunk position information                                │
│  • Temporal data (creation date, etc.)                       │
│  • Custom metadata fields                                    │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│          Embedding Generation (Gemini)                        │
│  • Dense vector representations (768-dim)                    │
│  • Semantic understanding of text                            │
│  • Image embeddings for visual content                       │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│            Vector Database Storage (Qdrant)                   │
│  • Store chunks with embeddings                              │
│  • Index for fast retrieval                                  │
│  • Organize by collection                                    │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                 Ready for Retrieval                           │
│         (Semantic search & RAG queries available)            │
└──────────────────────────────────────────────────────────────┘
```

### Query & Response Flow

```
┌──────────────────────────────────────────────────────────────┐
│                     User Query                                │
│              "What is the main topic?"                       │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                   Query Understanding                         │
│          • Cleaning and normalization                        │
│          • Intent extraction                                 │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│             Query Embedding Generation                        │
│  • Convert query to vector (Gemini)                          │
│  • 768-dimensional dense vector                              │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│           Semantic Search (Qdrant Vector DB)                  │
│  • Find K most similar chunks                                │
│  • Similarity scoring & ranking                              │
│  • Configurable threshold filtering                          │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                 Context Construction                          │
│  • Aggregate retrieved chunks                                │
│  • Preserve source information                               │
│  • Maintain document structure                               │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│              Prompt Engineering                               │
│  • Build multi-part prompt with context                      │
│  • Include system instructions                               │
│  • Format retrieved content                                  │
│  • Prepare for LLM consumption                               │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│         LLM Response Generation (Gemini 2.5-Flash)            │
│  • Generate contextual response                              │
│  • Maintain coherence & relevance                            │
│  • Include citations where applicable                        │
└─────────────────────────────┬────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                   Formatted Response                          │
│           • Citation tracking                                │
│           • Source references                                │
│           • Quality assurance                                │
└──────────────────────────────────────────────────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- Google Gemini API key
- Qdrant database instance

### Installation

1. **Clone the repository**
   ```bash
   cd c:\Users\LENOVO\Desktop\AI-Projects\Traditional-RAG
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or: source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```
   GEMINI_API_KEY=your_gemini_api_key_here
   QDRANT_URL=http://localhost:6333
   QDRANT_COLLECTION_NAME=documents
   ```

5. **Start Qdrant vector database**
   ```bash
   # Using Docker
   docker run -p 6333:6333 qdrant/qdrant:latest
   ```

6. **Run the application**
   ```bash
   python main.py
   ```

The FastAPI server will start at `http://localhost:8000`

---

## 📚 API Endpoints

### Core Endpoints

#### 1. Upload & Process Document
**POST** `/upload`
- Upload documents (PDF, DOCX, images, video, audio)
- Automatic processing and embedding
- Returns document ID and processing status

**Request:**
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@document.pdf"
```

#### 2. Chat/Query Endpoint
**POST** `/chat`
- Send query to retrieve relevant context and get AI response
- Returns: answer, sources, confidence scores

**Request:**
```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{"query": "What are the main topics?"}'
```

**Response:**
```json
{
  "query": "What are the main topics?",
  "response": "Based on the documents...",
  "sources": [
    {
      "document_id": "uuid-123",
      "chunk_id": 0,
      "text": "...",
      "score": 0.87
    }
  ]
}
```

---

## 🧪 Testing

Comprehensive test suite included for all components:

```bash
# Run all tests
pytest

# Run specific test suite
pytest test_embeddings.py          # Embedding generation
pytest test_retrieval.py           # Retrieval system
pytest test_rag_pipeline.py        # Full pipeline
pytest test_multimodal_api.py      # Multimodal support
pytest test_gemini.py              # Gemini API
pytest test_llm.py                 # LLM generation
pytest test_context.py             # Context building

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=app/
```

---

## 🔧 Core Components

### 1. Embeddings Module (`app/embeddings/`)
Handles all embedding generation using Google Gemini API:
- **generate_embeddings()** - Batch embedding for documents
- **generate_query_embedding()** - Query embedding for search
- **generate_image_embedding()** - Visual content embeddings
- **Dimension**: 768-dimensional dense vectors
- **Model**: Gemini Embedding 2

### 2. Ingestion Pipeline (`app/ingestion/`)
Orchestrates the complete document processing:
- **file_detector.py** - Identifies file types
- **loader.py** - Loads content based on format
- **cleaner.py** - Normalizes and cleans text
- **splitter.py** - Chunks text intelligently
- **metadata.py** - Extracts and tracks metadata
- **processors/** - Specialized handling per media type
- **loaders/** - Format-specific loaders

### 3. LLM Module (`app/llm/`)
Manages response generation and prompt engineering:
- **llm.py** - Calls Gemini 2.5-Flash for responses
- **prompt.py** - Builds optimized prompts with context
- **Media description** - Describes images/video for indexing

### 4. Retrieval System (`app/retrieval/`)
Performs semantic search and context preparation:
- **retriever.py** - Queries Qdrant for similar chunks
- **context_builder.py** - Aggregates context for LLM
- **source_builder.py** - Tracks source citations
- **Multi-modal retrieval** - Handles various content types

### 5. Vector Store (`app/vectorstore/`)
Manages Qdrant vector database operations:
- **qdrant.py** - Collection management
- **Index creation** - Optimized for similarity search
- **Batch operations** - Efficient chunk storage
- **Similarity search** - K-NN retrieval

---

## ⚙️ Configuration

### Environment Variables
```bash
GEMINI_API_KEY        # Google Gemini API authentication
QDRANT_URL            # Qdrant server URL (default: http://localhost:6333)
QDRANT_COLLECTION     # Collection name (default: documents)
EMBEDDING_DIM         # Embedding dimension (768 for Gemini)
CHUNK_SIZE            # Text chunk size (default: 512)
CHUNK_OVERLAP         # Chunk overlap (default: 50)
TOP_K                 # Retrieval results count (default: 5)
SCORE_THRESHOLD       # Minimum similarity threshold (default: 0.0)
```

### Processing Parameters
Adjust in respective module files:
- **Text Chunking** - `app/ingestion/splitter.py`
- **Embedding Model** - `app/embeddings/embedder.py`
- **Retrieval Settings** - `app/retrieval/retriever.py`
- **LLM Model Selection** - `app/llm/llm.py`

---

## 📊 Project Status

### Completed ✅
- [x] FastAPI server setup
- [x] File type detection
- [x] PDF text extraction
- [x] Word document processing
- [x] Image processing & analysis
- [x] Video processing & frame extraction
- [x] Audio transcription
- [x] Spreadsheet data extraction
- [x] Text cleaning & normalization
- [x] Intelligent text chunking
- [x] Metadata extraction
- [x] Gemini embeddings integration
- [x] Qdrant vector database setup
- [x] Multimodal embedding support
- [x] Semantic search retrieval
- [x] Context construction
- [x] Prompt engineering
- [x] LLM response generation
- [x] Comprehensive test suite
- [x] Citation tracking

### In Development 🔄
- [ ] Advanced query understanding
- [ ] Conversational memory/history
- [ ] Response ranking & re-ranking
- [ ] Semantic caching

### Planned Features 📝
- [ ] Web UI/Chat interface
- [ ] Batch document processing
- [ ] Custom embedding models
- [ ] Advanced filtering
- [ ] Document versioning
- [ ] Analytics & logging
- [ ] Performance optimization
- [ ] Multi-language support
- [ ] Fine-tuned models
- [ ] Feedback loop & learning

---

## 🎓 How It Works - Detailed Explanation

### Document Ingestion Process

1. **File Detection** - Analyzes file extension and magic bytes
2. **Content Extraction** - Uses specialized extractors per format
3. **Preprocessing** - Cleans, normalizes, and prepares text
4. **Intelligent Chunking** - Splits while maintaining semantic coherence
5. **Metadata Enrichment** - Adds document context and tracking info
6. **Embedding Generation** - Creates 768-dim vectors via Gemini
7. **Vector Storage** - Stores in Qdrant with indexed retrieval

### Query & Retrieval Process

1. **Query Input** - User asks a question
2. **Query Embedding** - Converts query to vector space
3. **Vector Search** - Finds K most similar chunks using cosine similarity
4. **Context Aggregation** - Combines relevant chunks into coherent context
5. **Prompt Construction** - Builds multi-part prompt with instructions + context
6. **LLM Generation** - Gemini 2.5-Flash generates contextual response
7. **Response Formatting** - Adds citations and source references
8. **Return to User** - Formatted response with provenance

### Multimodal Capabilities

- **Images**: Analyzed by Gemini Vision, descriptions indexed
- **Videos**: Frames extracted and analyzed, temporal context maintained
- **Audio**: Transcribed and indexed for searchability
- **Tables**: Structured data extracted and properly formatted
- **Mixed Content**: All modalities processed and unified in vector space

---

## 📦 Dependencies Summary

Key Python packages (see requirements.txt for complete list):

```
fastapi>=0.104.0              # Web framework
uvicorn>=0.24.0               # ASGI server
pydantic>=2.0.0               # Data validation
google-genai>=0.1.0            # Gemini API client
qdrant-client>=2.0.0           # Qdrant Python client
pymupdf>=1.23.0                # PDF processing
python-docx>=0.8.11            # Word doc processing
openpyxl>=3.1.0                # Excel processing
pillow>=10.0.0                 # Image processing
opencv-python>=4.8.0           # Computer vision
librosa>=0.10.0                # Audio processing
python-multipart>=0.0.6        # File upload support
python-dotenv>=1.0.0           # Environment variables
```

---

## 🔒 Security Considerations

- **API Key Protection**: Store GEMINI_API_KEY securely in .env
- **File Upload Limits**: Implement file size restrictions
- **Input Validation**: All uploads and queries validated via Pydantic
- **Rate Limiting**: Consider implementing for production
- **Authentication**: Add auth layer for production deployment

---

## 🚦 Production Deployment

For production use:

1. **Use production-grade Qdrant** (managed or self-hosted with persistence)
2. **Configure API authentication** (OAuth2, JWT tokens)
3. **Implement rate limiting** and request throttling
4. **Add request logging** and monitoring
5. **Use environment-specific configs**
6. **Deploy with uvicorn + Nginx** reverse proxy
7. **Enable HTTPS/TLS** for all connections
8. **Regular backups** of Qdrant database

---

## 📖 Example Usage

### Upload a Document
```python
import requests

with open('document.pdf', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/upload',
        files={'file': f}
    )
    print(response.json())
```

### Query the System
```python
import requests

response = requests.post(
    'http://localhost:8000/chat',
    json={'query': 'What is the main topic?'}
)
result = response.json()
print(f"Answer: {result['response']}")
print(f"Sources: {result['sources']}")
```

---

## 🤝 Contributing

Contributions welcome! Areas for enhancement:
- Additional document format support
- Query optimization techniques
- Advanced semantic understanding
- Performance improvements
- Web UI development

---

## 📝 License

MIT License - Free for personal and commercial use

---

## 📞 Support & Documentation

For issues or questions:
1. Check test files for usage examples
2. Review component docstrings
3. Examine API responses for debugging
4. Consult Gemini API documentation
5. Review Qdrant documentation for vector DB queries

---

## 🎯 Key Metrics

**Performance Targets:**
- Document ingestion: < 2 seconds per page
- Embedding generation: ~50-100 docs/sec
- Query response time: < 1 second
- Retrieval accuracy: High semantic relevance scores
- Storage efficiency: ~768 bytes per embedding + metadata

**Scalability:**
- Handles thousands of documents
- Supports batch processing
- Vector DB optimized for millions of vectors
- Multimodal content seamlessly integrated

---

**Last Updated**: August 29, 2026
**Project Status**: Active Development
**Python Version**: 3.8+
**API Version**: v1.0