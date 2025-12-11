#!/usr/bin/env python3
"""
Simple Python script to test FOCUS Corporation Ollama API
Use this on any device to quickly test the API
"""

import requests
import os

# Configuration (can be overridden by environment variables)
API_URL = os.getenv("API_URL", "http://192.168.10.2:9100")
TOKEN = os.getenv("API_TOKEN", "FOCUS_Corporation_a4e83f94514e155693c499c256e57a38")

# Headers
headers = {
    "Authorization": f"Bearer {TOKEN}"
}

print("Testing FOCUS Corporation Ollama API...")
print(f"Endpoint: {API_URL}\n")

# Simple test
response = requests.post(
    f"{API_URL}/api/generate",
    headers=headers,
    json={
        "model": "gemma3:1b",
        "prompt": "Say hello and introduce yourself in one sentence.",
        "stream": False
    }
)

if response.status_code == 200:
    print("✓ Success!")
    print(f"Response: {response.json()['response']}")
else:
    print(f"✗ Failed with status {response.status_code}")
    print(response.text)

