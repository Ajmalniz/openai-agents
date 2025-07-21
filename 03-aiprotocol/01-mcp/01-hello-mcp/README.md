# hello-mcp

A minimal MCP (Multi-Channel Protocol) server example using the `mcp` Python package.

## Description
This project demonstrates a simple, stateless MCP server using the `mcp` library. It is intended as a starting point for building streamable HTTP applications with MCP.

## Requirements
- Python 3.13+
- [mcp](https://pypi.org/project/mcp/)
- [uvicorn](https://www.uvicorn.org/)

## Installation
Install dependencies using your preferred package manager. For example, with [uv](https://github.com/astral-sh/uv):

```sh
uv pip install -r pyproject.toml
```

Or with pip:

```sh
pip install -r requirements.txt
```

## Usage
Run the MCP server with Uvicorn:

```sh
uvicorn main:mcp_app --reload
```

This will start the server on [http://localhost:8000](http://localhost:8000).

## Project Structure
- `main.py`: Main entry point, defines the MCP app.
- `pyproject.toml`: Project metadata and dependencies.
- `README.md`: This file.

## License
MIT (add your license here)
