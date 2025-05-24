#!/bin/bash

# Start the Ollama server in background
echo "🔴 $ ollama serve "
/bin/ollama serve &
# record the PID of the server process
OLLAMA_SERVE_PID=$!

# Wait for the server to start
# echo "🔴 Ollama serve..."
# while ! curl -s http://localhost:11434/ > /dev/null; do
#     sleep 1
# done


echo "🔴 Retrieving models from Ollama server..."
ollama pull llama3.2:3b
ollama pull gemma3:1b
ollama pull nomic-embed-text:v1.5
# ollama pull deepseek-r1:1.5b-qwen-distill-q4_K_M
echo "🟢 Done!"

# Check if the server is running
# if ps -p $OLLAMA_SERVE_PID > /dev/null; then
#     echo "Ollama server is running with PID $OLLAMA_SERVE_PID"
# else
#     echo "Ollama server failed to start"
#     exit 1
# fi

# Wait for the Ollama server to be up and running
wait $OLLAMA_SERVE_PID
echo "🟢 Ollama server is up!"