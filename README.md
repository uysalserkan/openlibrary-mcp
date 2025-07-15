# Books MCP

A book search application that provides access to the OpenLibrary API through both FastAPI and MCP (Model Context Protocol) servers.

## 🚀 Features

- **Book Search**: Search for books using the OpenLibrary API
- **Dual Server Support**: Available as both FastAPI web server and MCP server
- **Data Validation**: Robust Pydantic models with proper validation
- **Error Handling**: Graceful handling of incomplete API responses
- **Comprehensive Logging**: Detailed logging for monitoring and debugging
- **Code Quality**: Pre-commit hooks for maintaining code standards

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

# Install pre-commit hooks
poetry run pre-commit install

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
- `GET /health` - Health check endpoint
- `GET /` - API information
- `GET /docs` - Interactive API documentation

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

## 🤖 Using with Claude Desktop

This MCP server can be easily integrated with Claude Desktop to provide book search capabilities directly in your conversations with Claude.

![example_usage](imgs/example1.png)

### 📋 **Prerequisites**

- Claude Desktop application installed
- This books_mcp project installed and working
- Poetry or Python environment set up

### ⚙️ **Setup Instructions**

#### 1. **Locate Claude Desktop Config**

Find your Claude Desktop configuration file:

**macOS:**
```bash
~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Windows:**
```bash
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

#### 2. **Add Books MCP Server**

Edit the `claude_desktop_config.json` file and add the books-mcp server:

```json
{
  "mcpServers": {
    "books-search": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/uysalserkan/books-mcp",
        "books-mcp"
      ]
    },
    ...
  }
}
```

#### 3. **Restart Claude Desktop**

Close and restart Claude Desktop for the changes to take effect.

### 🎯 **Using the Book Search Tool**

Once configured, you can use the book search functionality in Claude Desktop:

#### **Example Conversations:**

**You:** "Can you help me find books about Python programming?"

**Claude:** I'll search for Python programming books for you.

*[Claude uses the search_books tool]*

**Claude:** I found several Python programming books:

1. **"Learning Python"** by Mark Lutz (2013)
   - 5 editions available
   - Language: English

2. **"Python Crash Course"** by Eric Matthes (2019)
   - 3 editions available
   - Language: English

[...more results...]

#### **Other Example Queries:**

- "Find books by J.R.R. Tolkien"
- "Search for books about machine learning"
- "Look up George Orwell's 1984"
- "Find cookbooks published after 2020"

### 🔧 **Tool Details**

The MCP server provides one tool:

**`search_books(query: str)`**
- **Purpose**: Search for books using OpenLibrary API
- **Input**: Search query string
- **Output**: Structured book data including titles, authors, publication years, and more
- **Examples**:
  - `"python programming"`
  - `"tolkien lord of the rings"`
  - `"george orwell 1984"`

### ✅ **Verification**

After setup, you should see:

1. **In Claude Desktop**: The books-mcp server listed in available tools
2. **In Conversations**: Ability to ask Claude to search for books
3. **In Logs**: MCP server startup messages when Claude Desktop starts

The integration allows Claude to seamlessly search for books and provide detailed information about authors, publication years, editions, and more, making it a powerful research and discovery tool!

## 🔧 Development

### Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality and consistency. The following tools are configured:

#### 🛡️ **Code Quality Tools**

- **Black**: Code formatting (line length: 88)
- **isort**: Import sorting with black compatibility
- **Ruff**: Fast Python linter (replaces flake8)
- **mypy**: Static type checking
- **Bandit**: Security vulnerability scanner

#### 📝 **General Checks**

- **Trailing whitespace**: Automatically removes trailing spaces
- **End of file**: Ensures files end with newline
- **YAML/TOML validation**: Validates configuration files
- **Large files**: Prevents committing large files
- **Merge conflicts**: Detects merge conflict markers
- **Debug statements**: Finds debug statements in code

#### 🚀 **Running Pre-commit**

```bash
# Install hooks (run once)
poetry run pre-commit install

# Run on all files
poetry run pre-commit run --all-files

# Run on specific files
poetry run pre-commit run --files books_mcp/models.py

# Skip hooks for a commit (not recommended)
git commit -m "message" --no-verify
```

#### ⚙️ **Tool Configuration**

All tools are configured in `pyproject.toml`:

```toml
[tool.black]
line-length = 88
target-version = ['py311']

[tool.isort]
profile = "black"
line_length = 88

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP"]

[tool.mypy]
python_version = "3.11"
disallow_untyped_defs = true
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
├── .pre-commit-config.yaml # Pre-commit configuration
├── claude_desktop_config.json # Sample Claude Desktop configuration
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

### Development Dependencies

- **pre-commit**: Git hooks for code quality
- **black**: Code formatter
- **isort**: Import sorter
- **ruff**: Fast Python linter
- **mypy**: Static type checker
- **bandit**: Security linter

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

# Test pre-commit hooks
poetry run pre-commit run --all-files
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Ensure pre-commit hooks pass: `poetry run pre-commit run --all-files`
5. Add tests if applicable
6. Submit a pull request

### Code Quality Standards

- **Type hints**: All functions must have proper type annotations
- **Documentation**: Use docstrings for all public functions and classes
- **Error handling**: Use proper exception chaining with `raise ... from e`
- **Security**: Avoid binding to all interfaces (`0.0.0.0`) in production
- **Logging**: Include meaningful log messages with appropriate levels

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🔗 Related Links

- [OpenLibrary API Documentation](https://openlibrary.org/developers/api)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [MCP Documentation](https://modelcontextprotocol.io/docs/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Pre-commit Documentation](https://pre-commit.com/)

## 🐛 Issues

If you encounter any issues, please create an issue on the GitHub repository with:

- Description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment details
