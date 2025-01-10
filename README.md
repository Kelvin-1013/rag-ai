# RAG (Retrieval Augmented Generation) System

## Table of Contents
1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture](#architecture)
4. [Installation](#installation)
5. [Usage](#usage)
6. [API Endpoints](#api-endpoints)
7. [Security Features](#security-features)
8. [Vector Database Integration](#vector-database-integration)
9. [Document Processing](#document-processing)
10. [Query System](#query-system)
11. [Configuration](#configuration)
12. [Dependencies](#dependencies)
13. [File Structure](#file-structure)
14. [Contributing](#contributing)
15. [License](#license)
16. [Contact](#contact)

## Project Overview

This project implements a sophisticated Retrieval Augmented Generation (RAG) system designed to process, store, and query various document types while maintaining a high level of data security. The system integrates multiple embedding models, supports various document formats, and implements advanced security features such as data masking and unmasking.

## Features

- Multi-format document processing (PDF, JSON, TXT)
- Secure data handling with masking of sensitive information
- Multiple embedding models for different use cases
- Namespace support for multi-tenant or categorized data storage
- Flexible querying system with masked and unmasked options
- Integration with external Language Model (LLM) API
- Modular and extensible architecture

## Architecture

The system is built on a modular architecture with the following main components:

1. **Document Ingestion**: Handles the processing of various document types.
2. **Security Layer**: Implements data masking and unmasking.
3. **Vector Database**: Stores document embeddings for efficient retrieval.
4. **Query Processing**: Manages document retrieval and interaction with LLM.
5. **API Layer**: Provides RESTful endpoints for system interaction.


```mermaid
graph TB
    A[Client] --> B[API Layer]
    B --> C[Document Ingestion]
    B --> D[Query Processing]
    B --> E[Database Management]
    C --> F[Security Layer]
    D --> F
    F --> G[Vector Database]
    D --> H[External LLM API]
    
    subgraph "Document Ingestion"
    C --> I[PDF Processor]
    C --> J[JSON Processor]
    C --> K[TXT Processor]
    end
    
    subgraph "Security Layer"
    F --> L[Data Masking]
    F --> M[Data Unmasking]
    end
    
    subgraph "Vector Database"
    G --> N[ChromaDB]
    N --> O[Embedding Models]
    end

Key Components:

1. **API Layer**: Handles incoming requests and routes them to appropriate modules.
2. **Document Ingestion**: Processes various document types and prepares them for storage.
3. **Security Layer**: Manages data masking and unmasking operations.
4. **Vector Database**: Stores and retrieves document embeddings efficiently.
5. **Query Processing**: Manages document retrieval and interaction with external LLM.
6. **Database Management**: Handles operations like deletion of specific or all databases.


## Installation

Follow these steps to set up the RAG system:

1. Clone the repository:
```
git clone [https://github.com/Kelvin-1013/rag.git](https://github.com/Kelvin-1013/rag.git)
cd rag-system
```
2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
3. Install the required dependencies:
```
pip install -r requirements.txt
```
4. Download the spaCy English language model:
```
python -m spacy download en_core_web_sm
```
5. Set up the necessary directories:
```
mkdir -p Databases sqliteDB Uploaded_files
```
6. Configure the external LLM API endpoint in the `app.py` file.
7. (Optional) Adjust any configuration parameters in the individual processing files as needed.


## Usage

To start the RAG system server:

1. Ensure you're in the project directory and your virtual environment is activated.
2. Run the following command:
```
python app.py
```
3. The server will start, by default on `[http://localhost:5000\`](http://localhost:5000\`).
4. Use the provided API endpoints to interact with the system for document ingestion, querying, and database management.


Example usage with curl:

1. Ingest a PDF document:
```
curl -X POST -F "files=@/path/to/document.pdf" -F "Vectordb_name=mydb" -F "Namespace=docs" -F "Chunk_size=1000" -F "Chunk_overlap=200" -F "Embed_method=wide_range_NLP" [http://localhost:5000/PDF_injest](http://localhost:5000/PDF_injest)
```
2. Query the system:
```
curl -X POST -F "vectordb_name=mydb" -F "namespace=docs" -F "prompt=What is RAG?" -F "model_max_array_lenth=10" -F "model_max_number_token=100" -F "model_temperature=0.7" -F "model_max_string_token_length=50" [http://localhost:5000/query](http://localhost:5000/query)
```


## API Endpoints

The RAG system provides the following RESTful API endpoints:

### Document Ingestion

- `POST /PDF_injest`: Ingest PDF documents

- Parameters:

- `files`: PDF file(s) to ingest
- `Vectordb_name`: Name of the vector database
- `Namespace`: Namespace for the documents
- `Chunk_size`: Size of text chunks
- `Chunk_overlap`: Overlap between chunks
- `Embed_method`: Embedding method to use






- `POST /PDF_injest_mask`: Ingest PDF documents with data masking

- Parameters: Same as `/PDF_injest`



- `POST /Text_injest`: Ingest text documents

- Parameters: Same as `/PDF_injest`



- `POST /Text_injest_mask`: Ingest text documents with data masking

- Parameters: Same as `/PDF_injest`



- `POST /json_injest`: Ingest JSON documents

- Parameters: Same as `/PDF_injest`



- `POST /json_injest_mask`: Ingest JSON documents with data masking

- Parameters: Same as `/PDF_injest`





### Querying

- `POST /query`: Query the system

- Parameters:

- `vectordb_name`: Name of the vector database to query
- `namespace`: Namespace to query (optional)
- `prompt`: Query prompt
- `model_max_array_lenth`: Maximum array length for the model
- `model_max_number_token`: Maximum number of tokens
- `model_temperature`: Model temperature
- `model_max_string_token_length`: Maximum string token length
- `POST /query_unmask`: Query the system with unmasking of sensitive data
- Parameters: Same as `/query`

### Database Management

- `DELETE /delete_one_db`: Delete a specific database

- Parameters:

- `vectordb_name`: Name of the vector database to delete






- `DELETE /delete_all_dbs`: Delete all databases

- No parameters required





## Security Features

The RAG system implements robust security measures to protect sensitive information:

### Data Masking

1. **Detection**: The system uses a combination of Named Entity Recognition (NER) and regular expressions to detect sensitive information:

1. Personal Names: Using spaCy's NER capabilities
2. Email Addresses: Regex pattern `\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b`
3. Credit Card Numbers: Regex pattern `\b\d{16}\b`
4. Phone Numbers: Regex pattern `\b\d{3}-\d{3}-\d{4}\b`



2. **Masking Process**:

1. Detected sensitive information is replaced with UUIDs
2. The original data and corresponding UUIDs are stored in a secure SQLite database



3. **Unmasking**:

1. Unmasking is performed only when explicitly requested through the `query_unmask` endpoint
2. The system retrieves the original data using the UUIDs stored in the SQLite database





### UUID Mapping Database

Sensitive data mappings are stored in a SQLite database with the following schema:

```sql
CREATE TABLE uuid_info(
vectordb_name TEXT,
namespace TEXT,
style TEXT,
real TEXT,
uuid TEXT
)
```

- `vectordb_name`: Name of the vector database
- `namespace`: Namespace of the document
- `style`: Type of sensitive data (e.g., 'name', 'email', 'credit_card', 'phone_number')
- `real`: The original sensitive data
- `uuid`: The UUID used to replace the sensitive data in the vector database


### Secure Data Handling

- Sensitive data is never stored in plain text in the vector database
- All communication with the external LLM API is done over HTTPS
- Temporary files in the `Uploaded_files` directory are deleted after processing


## Vector Database Integration

The RAG system uses ChromaDB for efficient storage and retrieval of document embeddings:

### Embedding Models

The system supports multiple embedding models to cater to different use cases:

1. `roberta-base`: For improved language understanding
2. `all-MiniLM-L6-v2`: For wide-range NLP tasks
3. `squeezebert/squeezebert-uncased`: For resource-constrained environments


### Storage

- Embeddings are stored persistently in the `./Databases/{model}` directory
- Each embedding model has its own separate storage to optimize retrieval based on the chosen model


### Retrieval

- The system uses a similarity search to retrieve relevant documents
- The `k` parameter in the retriever can be adjusted to control the number of similar documents retrieved


### Namespace Support

- Documents can be organized into namespaces
- Queries can be restricted to specific namespaces for more targeted results


## Document Processing

The RAG system supports processing of various document types:

### PDF Processing

- Utilizes `PyPDFLoader` for loading PDF documents
- Implements text chunking using `CharacterTextSplitter`
- Supports both masked and unmasked ingestion


### JSON Processing

- Uses a custom `JSONLoader` with `jq_schema` for flexible JSON parsing
- Capable of handling nested JSON structures
- Supports both masked and unmasked ingestion


### Text Processing

- Employs `TextLoader` with UTF-8 encoding for plain text documents
- Implements text chunking for efficient processing
- Supports both masked and unmasked ingestion


### Common Processing Steps

1. Document loading
2. Text extraction and chunking
3. Metadata addition (namespace, vector database name)
4. Data masking (if applicable)
5. Embedding generation
6. Storage in ChromaDB


## Query System

The RAG system provides two main querying mechanisms:

### Standard Query

- Endpoint: `/query`
- Process:

1. Receives query parameters including the prompt and model settings
2. Retrieves relevant documents from the vector database
3. Constructs a context-enhanced prompt
4. Sends the prompt to the external LLM API
5. Returns the LLM-generated response





### Unmasking Query

- Endpoint: `/query_unmask`
- Process:

1. Follows the same steps as the standard query
2. After receiving the LLM-generated response, it unmasks any UUIDs
3. Replaces UUIDs with the original sensitive data from the SQLite database
4. Returns the unmasked response





### Query Parameters

- `vectordb_name`: Name of the vector database to query
- `namespace`: Optional namespace to restrict the query
- `prompt`: The user's query prompt
- `model_max_array_lenth`: Maximum array length for the LLM
- `model_max_number_token`: Maximum number of tokens for the LLM response
- `model_temperature`: Temperature setting for the LLM (controls randomness)
- `model_max_string_token_length`: Maximum string token length for the LLM


## Configuration

The RAG system uses a combination of hardcoded values and runtime parameters. Future improvements could include:

### Current Configuration

- Embedding models are hardcoded in the ingestion and query files
- Database paths are hardcoded (e.g., `./Databases/{model}`, `./sqliteDB/Database.db`)
- External LLM API endpoint is hardcoded in the query files


### Potential Improvements

1. **Environment Variables**: Move sensitive or environment-specific configurations to environment variables
2. **Configuration File**: Implement a `config.yaml` or `config.json` file for easier management of system-wide settings
3. **Dynamic Model Loading**: Allow for dynamic loading of embedding models based on configuration or runtime parameters
4. **API Key Management**: Implement secure storage and retrieval of API keys for the external LLM service


## Dependencies

The RAG system relies on the following main dependencies:

- Flask==3.0.3: Web framework for the API
- langchain_chroma==0.1.1: Integration with ChromaDB
- langchain_community==0.2.4: Community-driven language processing tools
- langchain_core==0.2.5: Core langchain functionalities
- langchain_text_splitters==0.2.1: Text splitting utilities
- Requests==2.32.3: HTTP library for API calls
- spacy==3.7.5: Natural Language Processing toolkit


Additional dependencies include:

- PyPDF2: For PDF processing
- sentence-transformers: For text embeddings
- chromadb: Vector database
- pydantic: Data validation and settings management


For a complete list of dependencies and their versions, refer to the `requirements.txt` file in the project root.

## File Structure

The RAG system is organized with the following file structure:

```
.
├── **pycache**/
├── Databases/
│   ├── roberta-base/
│   ├── all-MiniLM-L6-v2/
│   └── squeezebert-uncased/
├── sqliteDB/
│   └── Database.db
├── Uploaded_files/
├── .git/
├── .gitignore
├── app.py
├── Delete_all.py
├── Delete_one.py
├── json_injest.py
├── json_injest_mask.py
├── PDF_injest.py
├── PDF_injest_mask.py
├── Query.py
├── Query_unmask.py
├── requirements.txt
├── TXT_injest.py
└── TXT_injest_mask.py

```plaintext

## Contributing

Contributions to the RAG system are welcome. Please follow these steps to contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/AmazingFeature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
5. Push to the branch (`git push origin feature/AmazingFeature`)
6. Open a Pull Request

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

## License

This project is licensed under the MIT License. See the `LICENSE` file in the project root for the full license text.

## Contact

Your Name - your.email@example.com

Project Link: [https://github.com/Kelvin-1013/rag](https://github.com/Kelvin-1013/rag)

For any questions, feature requests, or issues, please use the GitHub Issues 
```