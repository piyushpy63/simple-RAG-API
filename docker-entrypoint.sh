#!/bin/bash
set -e

echo "Starting Ollama..."
ollama serve &
OLLAMA_PID=$!

# Wait for Ollama to be ready
echo "Waiting for Ollama to start..."
while ! curl -s http://localhost:11434/api/tags > /dev/null; do
    sleep 1
done
echo "Ollama started!"

echo "Pulling tinyllama model..."
ollama pull tinyllama

echo "Running embedding script..."
python embed.py

echo "Starting server..."
exec "$@"
