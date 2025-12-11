#!/usr/bin/env python3
"""
FOCUS Corporation - Public IP Test
Test Ollama API on public IP address
"""

import requests
import json
import sys
import os
from typing import Dict, Any

# Configuration - Public IP
API_URL = os.getenv("API_URL", "http://197.13.2.177:9100")
TOKEN = os.getenv("API_TOKEN", "FOCUS_Corporation_a4e83f94514e155693c499c256e57a38")
MODEL = os.getenv("TEST_MODEL", "gemma3:1b")

# Headers with authentication
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

def print_header():
    print("=" * 50)
    print("  FOCUS Corporation - Public IP Test")
    print("=" * 50)
    print(f"Endpoint: {API_URL}")
    print(f"Token: {TOKEN}")
    print()

def test_auth_block() -> bool:
    """Test that requests without token are blocked"""
    print("1. Testing authentication blocking...")
    try:
        response = requests.get(f"{API_URL}/api/tags", timeout=10)
        if response.status_code == 401:
            print("   ✓ PASS - Correctly blocked (401)")
            return True
        else:
            print(f"   ✗ FAIL - Expected 401, got {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ FAIL - Connection error: {e}")
        return False

def test_auth_success() -> bool:
    """Test that requests with valid token work"""
    print("2. Testing authentication success...")
    try:
        response = requests.get(f"{API_URL}/api/tags", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print("   ✓ PASS - Authentication successful (200)")
            return True
        else:
            print(f"   ✗ FAIL - Expected 200, got {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ✗ FAIL - Connection error: {e}")
        return False

def test_list_models() -> bool:
    """Test listing available models"""
    print("3. Testing list models...")
    try:
        response = requests.get(f"{API_URL}/api/tags", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = data.get("models", [])
            if models:
                print(f"   ✓ PASS - Found {len(models)} models:")
                for model in models[:5]:  # Show first 5
                    print(f"      - {model['name']}")
                if len(models) > 5:
                    print(f"      ... and {len(models) - 5} more")
                return True
            else:
                print("   ✗ FAIL - No models found")
                return False
        else:
            print(f"   ✗ FAIL - Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ FAIL - Error: {e}")
        return False

def test_generate() -> bool:
    """Test text generation"""
    print(f"4. Testing text generation with {MODEL}...")
    try:
        payload = {
            "model": MODEL,
            "prompt": "Say hello in one sentence.",
            "stream": False
        }
        response = requests.post(
            f"{API_URL}/api/generate",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            text = data.get("response", "")
            if text:
                print("   ✓ PASS - Response received:")
                print(f"      {text[:100]}...")
                return True
            else:
                print("   ✗ FAIL - Empty response")
                return False
        else:
            print(f"   ✗ FAIL - Status code: {response.status_code}")
            print(f"      Make sure to pull the model: ollama pull {MODEL}")
            return False
    except Exception as e:
        print(f"   ✗ FAIL - Error: {e}")
        return False

def test_chat() -> bool:
    """Test chat completion"""
    print(f"5. Testing chat completion with {MODEL}...")
    try:
        payload = {
            "model": MODEL,
            "messages": [
                {"role": "user", "content": "Say hi!"}
            ],
            "stream": False
        }
        response = requests.post(
            f"{API_URL}/v1/chat/completions",
            headers=HEADERS,
            json=payload,
            timeout=30
        )
        if response.status_code == 200:
            data = response.json()
            message = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            if message:
                print("   ✓ PASS - Chat response received:")
                print(f"      {message[:100]}...")
                return True
            else:
                print("   ✗ FAIL - Empty response")
                return False
        else:
            print(f"   ✗ FAIL - Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ FAIL - Error: {e}")
        return False

def main():
    print_header()
    
    tests = [
        test_auth_block,
        test_auth_success,
        test_list_models,
        test_generate,
        test_chat
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    # Summary
    passed = sum(results)
    total = len(results)
    
    print("=" * 50)
    print(f"  Results: {passed}/{total} tests passed")
    print("=" * 50)
    print()
    print("Your API is accessible at:")
    print("  - Local:  http://192.168.10.2:9100")
    print("  - Public: http://197.13.2.177:9100")
    print()
    
    sys.exit(0 if passed == total else 1)

if __name__ == "__main__":
    main()

