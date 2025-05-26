#!/bin/bash

# Start the Ollama server in background
echo "⏳ Starting Ollama server..."
/bin/ollama serve &
# record the PID of the server process
OLLAMA_SERVE_PID=$!

# Sync server PID and keep it running
while ! /bin/ollama ls; do
    echo "Waiting for Ollama server to start..."
    sleep 2
done
echo "🟢 Ollama is up!"

echo "⏳⏳ Pulling models ..."
ollama pull nomic-embed-text:v1.5 &
OLLAMA_EMBEDDING_PULL_PID=$!
ollama pull llama3.2:3b &
OLLAMA_CHAT_MODEL_PULL_PID=$!
# not supported yet
# ollama pull gemma3:1b
# ollama pull deepseek-r1:1.5b-qwen-distill-q4_K_M

# Check if last model pulled successfully
wait $OLLAMA_EMBEDDING_PULL_PID
PULL_EMBEDDING_MODEL_STATUS=$?
wait $OLLAMA_CHAT_MODEL_PULL_PID
PULL_CHAT_MODEL_STATUS=$?

# Check if the models were pulled successfully
if [ $PULL_CHAT_MODEL_STATUS -ne 0 ] || [ $PULL_EMBEDDING_MODEL_STATUS -ne 0 ]; then
    echo "❌ Failed to pull models."
    exit 1
fi
echo "🟢 Done Pulling Models!"

# Sync server PID and keep it running
wait $OLLAMA_SERVE_PID
echo "🟢 Ollama is up!"