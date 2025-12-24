#!/bin/bash
# Start the FastAPI server

cd "$(dirname "$0")/.." || exit 1

echo "Starting Warhammer 40K Probability Calculator API..."
echo "Server will be available at http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
echo ""

pipenv run uvicorn war_application.api:app --host 0.0.0.0 --port 8000 --reload
