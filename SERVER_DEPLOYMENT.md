# 🚀 Server Deployment Instructions

## ✅ GitHub Repository
**URL:** https://github.com/FOCUSLLM/chatapi

---

## 📦 Deploy on Server (192.168.10.2)

### Step 1: SSH to Your Server
```bash
ssh user@192.168.10.2
```

### Step 2: Clone the Repository
```bash
git clone https://github.com/FOCUSLLM/chatapi.git
cd chatapi
```

### Step 3: Run Deployment Script
```bash
chmod +x deploy.sh
sudo bash deploy.sh
```

**This will:**
- ✅ Install Nginx
- ✅ Install Ollama
- ✅ Configure Nginx with token authentication
- ✅ Enable services on ports 80 and 9100

### Step 4: Start Ollama
```bash
# Option 1: Run in foreground (for testing)
ollama serve

# Option 2: Run in background (for production)
nohup ollama serve > ollama.log 2>&1 &
```

### Step 5: Pull Models
```bash
# Pull recommended model for testing
ollama pull gemma3:1b

# Pull other models (optional)
ollama pull llama3
ollama pull qwen3:8b
ollama pull gemma3:4b
```

### Step 6: Test the API
```bash
bash test.sh
```

**Expected output:**
```
==========================================
  FOCUS Corporation - API Test
==========================================
Endpoint: http://192.168.10.2:9100
Token: FOCUS_Corporation_a4e83f94514e155693c499c256e57a38

1. Testing WITHOUT token (should return 401)...
   ✓ PASS - Correctly blocked (401)

2. Testing WITH token (should return 200)...
   ✓ PASS - Authentication successful (200)

3. Listing available models...
   ✓ PASS - Models found:
      - gemma3:1b

4. Testing text generation with gemma3:1b...
   ✓ PASS - Response received:
      Hello! I'm Gemma...
```

---

## 🧪 Test from Remote Device

### On Any Device on the Network:

```bash
# Clone the repository
git clone https://github.com/FOCUSLLM/chatapi.git
cd chatapi

# Install Python dependencies
pip install -r requirements.txt

# Run full test suite
python3 test_remote.py

# Or quick test
python3 simple_test.py
```

---

## 🌐 If Using Public IP

If 192.168.10.2 is forwarded to a public IP:

### Option 1: Edit config.env
```bash
nano config.env
# Change: SERVER_IP=YOUR_PUBLIC_IP
```

### Option 2: Use environment variable
```bash
export API_URL="http://YOUR_PUBLIC_IP:9100"
python3 test_remote.py
```

---

## 🔑 API Credentials

- **Endpoint (Port 80):** `http://192.168.10.2`
- **Endpoint (Port 9100):** `http://192.168.10.2:9100`
- **Token:** `FOCUS_Corporation_a4e83f94514e155693c499c256e57a38`
- **Test Model:** `gemma3:1b`

---

## 🔥 Quick Usage Examples

### Using curl
```bash
curl -H "Authorization: Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38" \
     -d '{"model": "gemma3:1b", "prompt": "Hello!", "stream": false}' \
     http://192.168.10.2:9100/api/generate
```

### Using Python
```python
import requests

response = requests.post(
    "http://192.168.10.2:9100/api/generate",
    headers={"Authorization": "Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38"},
    json={"model": "gemma3:1b", "prompt": "Hello!", "stream": False}
)

print(response.json()['response'])
```

---

## 🔧 Service Management

```bash
# Check nginx status
sudo systemctl status nginx

# Restart nginx
sudo systemctl restart nginx

# Check if Ollama is running
ps aux | grep ollama

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# View Ollama logs (if running in background)
tail -f ollama.log
```

---

## 🛡️ Firewall Configuration

Make sure ports are open:

```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 80/tcp
sudo ufw allow 9100/tcp
sudo ufw status

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=9100/tcp
sudo firewall-cmd --reload
```

---

## ✨ All Set!

Your Ollama API is now running on:
- ✅ `http://192.168.10.2:80`
- ✅ `http://192.168.10.2:9100`

With token authentication: `FOCUS_Corporation_a4e83f94514e155693c499c256e57a38`

**Ready to use! 🚀**

