#!/bin/bash

# Start the Dance Pose Analyzer API server using the project's venv python
set -euo pipefail

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"

echo "Using project directory: $PROJECT_DIR"

# Create virtualenv if it doesn't exist
if [ ! -x "$VENV_PYTHON" ]; then
    echo "Virtual environment not found. Creating venv..."
    python3 -m venv "$PROJECT_DIR/venv"
    "$VENV_PYTHON" -m pip install --upgrade pip setuptools
    echo "Installing Python dependencies into venv..."
    "$VENV_PYTHON" -m pip install -r "$PROJECT_DIR/requirements.txt"
fi

echo ""
echo "Starting server on http://localhost:8000"
echo "API Documentation: http://localhost:8000/docs"
echo "Press Ctrl+C to stop"
echo ""

# Run uvicorn with the venv python to ensure the correct interpreter and packages are used
exec "$VENV_PYTHON" -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
