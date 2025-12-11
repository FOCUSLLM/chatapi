#!/usr/bin/env python3
"""
FOCUS Corporation - Ollama API Remote Test
Test Ollama API with token authentication from any device
"""

import requests
import json
import sys
import os
from typing import Dict, Any

# Configuration (can be overridden by environment variables)
API_URL = os.getenv("API_URL", "http://192.168.10.2:9100")
TOKEN = os.getenv("API_TOKEN", "FOCUS_Corporation_a4e83f94514e155693c499c256e57a38")
MODEL = os.getenv("TEST_MODEL", "gemma3:1b")

# Headers with authentication
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}


def print_section(title: str):
    """Print a formatted section header"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def test_without_token():
    """Test 1: API should block requests without token"""
    print("1. Testing WITHOUT token (should fail with 401)...")
    try:
        response = requests.get(f"{API_URL}/api/tags", timeout=10)
        if response.status_code == 401:
            print(f"   ✓ Correctly blocked! Status: {response.status_code}")
            return True
        else:
            print(f"   ✗ Should be blocked! Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_with_token():
    """Test 2: API should accept requests with valid token"""
    print("2. Testing WITH token (should work)...")
    try:
        response = requests.get(f"{API_URL}/api/tags", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            print(f"   ✓ Authentication successful! Status: {response.status_code}")
            return True
        else:
            print(f"   ✗ Authentication failed! Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def list_models():
    """Test 3: List available models"""
    print("3. Listing available models...")
    try:
        response = requests.get(f"{API_URL}/api/tags", headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            models = [model['name'] for model in data.get('models', [])]
            print(f"   ✓ Found {len(models)} models:")
            for model in models:
                print(f"      - {model}")
            return True
        else:
            print(f"   ✗ Failed to list models. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_generate():
    """Test 4: Simple text generation"""
    print(f"4. Testing text generation with {MODEL}...")
    print("   Prompt: 'What is FOCUS Corporation?'")
    
    payload = {
        "model": MODEL,
        "prompt": "What is FOCUS Corporation? Answer in one sentence.",
        "stream": False
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/generate",
            headers=HEADERS,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✓ Response:")
            print(f"      {data.get('response', 'No response')}")
            return True
        else:
            print(f"   ✗ Failed. Status: {response.status_code}")
            print(f"      {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_chat():
    """Test 5: Chat completion (OpenAI-compatible)"""
    print(f"5. Testing chat completion with {MODEL}...")
    print("   Prompt: 'Tell me a fun fact about AI'")
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": "Tell me a fun fact about AI in one sentence."}
        ],
        "stream": False
    }
    
    try:
        response = requests.post(
            f"{API_URL}/v1/chat/completions",
            headers=HEADERS,
            json=payload,
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            message = data.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
            print(f"   ✓ Response:")
            print(f"      {message}")
            return True
        else:
            print(f"   ✗ Failed. Status: {response.status_code}")
            print(f"      {response.text}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def test_streaming():
    """Test 6: Streaming response"""
    print(f"6. Testing streaming with {MODEL}...")
    print("   Prompt: 'Count from 1 to 5'")
    
    payload = {
        "model": MODEL,
        "prompt": "Count from 1 to 5",
        "stream": True
    }
    
    try:
        response = requests.post(
            f"{API_URL}/api/generate",
            headers=HEADERS,
            json=payload,
            stream=True,
            timeout=60
        )
        
        if response.status_code == 200:
            print(f"   ✓ Streaming response:")
            print("      ", end="", flush=True)
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if 'response' in data:
                        print(data['response'], end="", flush=True)
            print()  # New line
            return True
        else:
            print(f"   ✗ Failed. Status: {response.status_code}")
            return False
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False


def main():
    """Run all tests"""
    print_section("FOCUS Corporation - Ollama API Remote Test")
    print(f"API Endpoint: {API_URL}")
    print(f"Model: {MODEL}")
    
    results = []
    
    # Run all tests
    results.append(("Authentication Block", test_without_token()))
    results.append(("Authentication Success", test_with_token()))
    results.append(("List Models", list_models()))
    results.append(("Text Generation", test_generate()))
    results.append(("Chat Completion", test_chat()))
    results.append(("Streaming", test_streaming()))
    
    # Summary
    print_section("Test Summary")
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! API is working perfectly!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed!")
        return 1


if __name__ == "__main__":
    sys.exit(main())

