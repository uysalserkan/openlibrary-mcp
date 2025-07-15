# Books MCP

A book search application that provides access to the OpenLibrary API through both FastAPI and MCP (Model Context Protocol) servers.

## 🚀 Features

- **Book Search**: Search for books using the OpenLibrary API
- **Dual Server Support**: Available as both FastAPI web server and MCP server
- **Data Validation**: Robust Pydantic models with proper validation
- **Error Handling**: Graceful handling of incomplete API responses

## 📦 Installation

### Prerequisites

- Python 3.11+
- Poetry (recommended) or pip

### Using Poetry (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd books_mcp

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Using pip

```bash
# Clone the repository
git clone <repository-url>
cd books_mcp

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## 🛠️ Usage

### FastAPI Server

Start the FastAPI web server:

```bash
python -m books_mcp.fastapi_server
```

The server will be available at `http://localhost:8000`

#### API Endpoints

- `GET /search?query=<search_term>` - Search for books

Example:
```bash
curl "http://localhost:8000/search?query=python+programming"
```

### MCP Server

The MCP server provides tool-based access for AI assistants:

```bash
python -m books_mcp.mcp_server
```

Or use the installed command:

```bash
books-mcp
```

## 📊 API Response Format

```json
{
  "num_found": 1234,
  "q": "python programming",
  "docs": [
    {
      "author_name": "John Doe",
      "edition_count": 5,
      "first_publish_year": 2020,
      "language": "en",
      "title": "Python Programming Guide"
    }
  ]
}
```

## 🏗️ Project Structure

```
books_mcp/
├── books_mcp/           # Main package directory
│   ├── __init__.py      # Package initialization
│   ├── fastapi_server.py # FastAPI web server
│   ├── mcp_server.py    # MCP server implementation
│   ├── models.py        # Pydantic data models
│   └── providers.py     # OpenLibrary API provider
├── pyproject.toml       # Project configuration
├── poetry.lock          # Dependency lock file
├── README.md           # This file
└── dist/               # Built packages
```

## 🔧 Dependencies

- **FastAPI**: Web framework for building APIs
- **FastMCP**: MCP server implementation
- **Pydantic**: Data validation and settings management
- **Uvicorn**: ASGI server for FastAPI
- **HTTPX**: Async HTTP client for API calls
- **Requests**: HTTP library for synchronous requests

## 🔍 Data Models

### BookDetails

Represents individual book information with optional fields to handle incomplete API responses:

- `author_name`: Author's name
- `edition_count`: Number of available editions
- `first_publish_year`: Year of first publication
- `language`: Book language(s)
- `title`: Book title

### OpenLibrary

Represents the complete API response:

- `num_found`: Total number of books found
- `q`: Search query
- `docs`: List of book details

## 📋 Logging

The application includes comprehensive logging to help with monitoring and debugging:

### 🎯 **Key Logging Features:**

- **API Calls**: Track OpenLibrary API requests, responses, and timing
- **Data Validation**: Monitor model validation, data cleaning, and incomplete records
- **Server Activity**: Log server startup, endpoint access, and request processing
- **Error Handling**: Detailed error logging with context

### 📊 **Log Levels:**

- **INFO**: General application flow and important events
- **DEBUG**: Detailed validation steps and data processing
- **WARNING**: Non-critical issues (empty queries, missing fields)
- **ERROR**: Failures and exceptions with full context

### 🔧 **Log Format:**

```
2025-07-15 16:57:40,733 - books_mcp.providers - INFO - 📚 Starting book search for query: 'python'
2025-07-15 16:57:40,734 - books_mcp.models - INFO - ⚠️  1/3 books have missing critical fields
```

### 📝 **Example Log Messages:**

```
🔧 OpenLibraryProvider initialized with base_url: https://openlibrary.org
📚 Starting book search for query: 'python programming'
📡 API Response: 200 | Content-Length: 12345
✅ Search completed: 1234 total books found, 20 returned in response
🎯 Successfully processed 20 book records
🔍 MCP tool called: search_books with query='python'
🌐 GET /search - Query: {'query': 'python'}
📊 Response: 200 | Time: 0.523s
```

## 🧪 Testing

Run a quick test to verify the installation:

```bash
# Test FastAPI server
python -c "from books_mcp.providers import OpenLibraryProvider; print('✅ OpenLibrary provider works!')"

# Test models
python -c "from books_mcp.models import BookDetails, OpenLibrary; print('✅ Models imported successfully!')"
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Related Links

- [OpenLibrary API Documentation](https://openlibrary.org/developers/api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MCP Documentation](https://modelcontextprotocol.io/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)

## 🐛 Issues

If you encounter any issues, please create an issue on the GitHub repository with:

- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment details 