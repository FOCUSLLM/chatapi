#!/usr/bin/env python3
"""
Use FOCUS Corporation Ollama API with OpenAI Python library
This allows you to use Ollama as a drop-in replacement for OpenAI
"""

from openai import OpenAI
import os

# Configuration (can be overridden by environment variables)
API_URL = os.getenv("API_URL", "http://192.168.10.2:9100")
TOKEN = os.getenv("API_TOKEN", "FOCUS_Corporation_a4e83f94514e155693c499c256e57a38")

# Initialize client with FOCUS Corporation API
client = OpenAI(
    base_url=f"{API_URL}/v1",
    api_key=TOKEN
)

print("FOCUS Corporation Ollama API - OpenAI Compatible\n")

# Example 1: Simple chat
print("Example 1: Simple Chat")
print("-" * 50)
response = client.chat.completions.create(
    model="gemma3:1b",
    messages=[
        {"role": "user", "content": "What is artificial intelligence? Answer briefly."}
    ]
)
print(response.choices[0].message.content)
print()

# Example 2: Chat with system message
print("Example 2: Chat with System Message")
print("-" * 50)
response = client.chat.completions.create(
    model="gemma3:1b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant that speaks like a pirate."},
        {"role": "user", "content": "Tell me about machine learning."}
    ]
)
print(response.choices[0].message.content)
print()

# Example 3: Streaming response
print("Example 3: Streaming Response")
print("-" * 50)
stream = client.chat.completions.create(
    model="gemma3:1b",
    messages=[
        {"role": "user", "content": "Count from 1 to 5 slowly."}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
print("\n")

print("✓ All examples completed successfully!")

