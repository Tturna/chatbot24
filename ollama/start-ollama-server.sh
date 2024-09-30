#!/usr/bin/zsh

docker run -d --gpus=all -v ollama:/root/.ollama --network cb24 -p 11434:11434 --name ollama ollama/ollama
