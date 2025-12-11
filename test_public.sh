#!/bin/bash

# Load configuration
source config.env 2>/dev/null || true

# Use public IP
SERVER_IP=${PUBLIC_IP:-197.13.2.177}
API_PORT=${API_PORT:-9100}
API_TOKEN=${API_TOKEN:-FOCUS_Corporation_a4e83f94514e155693c499c256e57a38}
TEST_MODEL=${TEST_MODEL:-gemma3:1b}

API_URL="http://${SERVER_IP}:${API_PORT}"

echo "=========================================="
echo "  FOCUS Corporation - Public IP Test"
echo "=========================================="
echo "Public Endpoint: $API_URL"
echo "Token: $API_TOKEN"
echo ""

# Test 1: Without token (should fail)
echo "1. Testing WITHOUT token (should return 401)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 $API_URL/api/tags)
if [ "$HTTP_CODE" = "401" ]; then
    echo "   ✓ PASS - Correctly blocked (401)"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "   ✗ FAIL - Cannot connect to server (check if server is running)"
else
    echo "   ✗ FAIL - Expected 401, got $HTTP_CODE"
fi
echo ""

# Test 2: With token (should work)
echo "2. Testing WITH token (should return 200)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 10 -H "Authorization: Bearer $API_TOKEN" $API_URL/api/tags)
if [ "$HTTP_CODE" = "200" ]; then
    echo "   ✓ PASS - Authentication successful (200)"
elif [ "$HTTP_CODE" = "000" ]; then
    echo "   ✗ FAIL - Cannot connect to server"
else
    echo "   ✗ FAIL - Expected 200, got $HTTP_CODE"
fi
echo ""

# Test 3: List models
echo "3. Listing available models..."
MODELS=$(curl -s --connect-timeout 10 -H "Authorization: Bearer $API_TOKEN" $API_URL/api/tags | jq -r '.models[].name' 2>/dev/null)
if [ -n "$MODELS" ]; then
    echo "   ✓ PASS - Models found:"
    echo "$MODELS" | while read model; do
        echo "      - $model"
    done
else
    echo "   ✗ FAIL - No models found or jq not installed"
fi
echo ""

# Test 4: Generate text
echo "4. Testing text generation with $TEST_MODEL..."
echo "   Prompt: 'Say hello in one sentence.'"
RESPONSE=$(curl -s --connect-timeout 30 -H "Authorization: Bearer $API_TOKEN" \
    -d "{\"model\": \"$TEST_MODEL\", \"prompt\": \"Say hello in one sentence.\", \"stream\": false}" \
    $API_URL/api/generate | jq -r '.response' 2>/dev/null)

if [ -n "$RESPONSE" ] && [ "$RESPONSE" != "null" ]; then
    echo "   ✓ PASS - Response received:"
    echo "      $RESPONSE"
else
    echo "   ✗ FAIL - No response or model not available"
    echo "      Make sure to pull the model: ollama pull $TEST_MODEL"
fi
echo ""

echo "=========================================="
echo "  Test Complete"
echo "=========================================="
echo ""
echo "Your API is accessible at:"
echo "  - Local:  http://192.168.10.2:9100"
echo "  - Public: http://197.13.2.177:9100"
echo ""

