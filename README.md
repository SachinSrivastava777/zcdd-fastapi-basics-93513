# FastAPI-demo App

A minimal FastAPI example showing simple CRUD-like endpoints for a todo list.

## Overview

This repository contains a tiny FastAPI app in `main.py` and a `Dockerfile` that builds an image exposing the app on port 8003.

## Requirements

- Python 3.11+
- Docker (optional, for containerized runs)

Dependencies (as listed in `pyproject.toml`):

- `fastapi>=0.118.0`
- `uvicorn[standar]>=0.37.0` (note: the project lists this value in `pyproject.toml`; when installing locally use the corrected package name `uvicorn[standard]`)

## Install and run locally (Windows PowerShell)

1. Install uv using PowerShell as administrator:
If PowerShell blocks script execution, you may need to allow it for this session:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

2. Creates a project with uv:

```powershell
mkdir fastapi-demo # Make a project folder
cd fastapi-demo # Go to the project path

# Initialize with uv (creates virtual environment + project)
uv init --python 3.11 
# Add FastAPI + Uvicorn (server)
uv add fastapi "uvicorn[standard]" 
```

3. Update the main.py file with Todo CRUD operations.

4. Run the app with uvicorn:

```powershell
# Recommended: use python -m uvicorn to ensure the right Python is used or using uv manager.

uv run uvicorn main:app --reload
```

### The app will be available at: 
The App: http://127.0.0.1:8000

Swagger UI: http://127.0.0.1:8000/docs


## Run with Docker

Build the image from the project root (where `Dockerfile` is located):

```powershell
docker build -t fastapi-demo .
```

Run the container and map the container port 8003 to the host:

```powershell
# Run it normally
docker run -p 8003:8003 fastapi-demo

# Stop it, you can get Contianer-ID from "docker container ls" command.
docker container stop [Container-ID]

# Run in background (detached):
docker run -d -p 8003:8003 fastapi-demo

# Stop & remove (if running detached):
docker stop fastapi-demo; docker rm fastapi-demo


```

Notes:
- The `Dockerfile` in this repo exposes port `8003` and runs the app via a manager named `uv`. 

## API testing

Open the interactive API docs:

- Swagger UI: http://localhost:8003/docs

Expected responses

- `GET /` returns a JSON message like: `{ "message": "Hello, world! 🚀" }`
- `GET /todos` returns a JSON array of todos
- `GET /todos/{id}` returns a single todo object or a 404 JSON error


## Troubleshooting

- If the server does not start, check that dependencies are installed and that no other process is using port 8003.
- On Windows PowerShell you may need to adjust the execution policy to activate virtualenv scripts (see the venv steps above).


Enjoy tinkering with the demo!
