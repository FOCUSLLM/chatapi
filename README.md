# 🚀 FOCUS Corporation - Ollama API with Token Authentication

Secure Ollama API deployment with Nginx reverse proxy and token authentication.

## ✨ Features

- 🔐 Token-based authentication
- 🚀 Nginx reverse proxy on ports 80 and 9100
- 🐍 Python test scripts included
- 🔄 Streaming support
- 🌐 OpenAI-compatible API

---

## 📋 Quick Start

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd <repo-name>
```

### 2. Configure Your Server IP
Edit `config.env` and set your server IP:
```bash
SERVER_IP=192.168.10.2  # Change this to your server's IP
```

### 3. Deploy on Server
```bash
chmod +x deploy.sh
sudo bash deploy.sh
```

### 4. Start Ollama and Pull a Model
```bash
# Start Ollama service
ollama serve

# In another terminal, pull a model
ollama pull gemma3:1b
```

### 5. Test the API
```bash
bash test.sh
```

---

## 🔑 Configuration

**Default Settings** (edit `config.env` to change):
- **Local IP:** `192.168.10.2`
- **Public IP:** `197.13.2.177`
- **API Port:** `9100`
- **Token:** `FOCUS_Corporation_a4e83f94514e155693c499c256e57a38`
- **Test Model:** `gemma3:1b`

---

## 🧪 Testing

### Bash Test Scripts
```bash
# Test local network
bash test.sh

# Test public IP
bash test_public.sh
```

### Python Test Scripts

**Install dependencies:**
```bash
pip install -r requirements.txt
```

**Run tests:**
```bash
# Test local network
python3 test_remote.py    # Full test suite (6 tests)
python3 simple_test.py    # Quick test

# Test public IP
python3 test_public.py    # Public IP test (5 tests)

# OpenAI library example
python3 openai_example.py
```

---

## 📡 API Endpoints

Your API will be accessible on:
- **Local Network (Port 80):** `http://192.168.10.2`
- **Local Network (Port 9100):** `http://192.168.10.2:9100`
- **Public IP (Port 9100):** `http://197.13.2.177:9100`

---

## 🔥 Usage Examples

### Using curl (Local Network)
```bash
curl -H "Authorization: Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38" \
     -d '{"model": "gemma3:1b", "prompt": "Hello!", "stream": false}' \
     http://192.168.10.2:9100/api/generate
```

### Using curl (Public IP)
```bash
curl -H "Authorization: Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38" \
     -d '{"model": "gemma3:1b", "prompt": "Hello!", "stream": false}' \
     http://197.13.2.177:9100/api/generate
```

### Using Python (Local Network)
```python
import requests

response = requests.post(
    "http://192.168.10.2:9100/api/generate",
    headers={"Authorization": "Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38"},
    json={"model": "gemma3:1b", "prompt": "Hello!", "stream": False}
)

print(response.json()['response'])
```

### Using Python (Public IP)
```python
import requests

response = requests.post(
    "http://197.13.2.177:9100/api/generate",
    headers={"Authorization": "Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38"},
    json={"model": "gemma3:1b", "prompt": "Hello!", "stream": False}
)

print(response.json()['response'])
```

### Using OpenAI Library
```python
from openai import OpenAI

# Use local IP or public IP
client = OpenAI(
    base_url="http://197.13.2.177:9100/v1",  # or http://192.168.10.2:9100/v1
    api_key="FOCUS_Corporation_a4e83f94514e155693c499c256e57a38"
)

response = client.chat.completions.create(
    model="gemma3:1b",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

---

## 📁 Project Structure

```
.
├── config.env              # Configuration file (edit this!)
├── deploy.sh              # Deployment script
├── test.sh                # Bash test script
├── nginx.conf             # Nginx configuration
├── requirements.txt       # Python dependencies
├── test_remote.py         # Full Python test suite
├── simple_test.py         # Quick Python test
├── openai_example.py      # OpenAI library examples
├── .gitignore            # Git ignore file
└── README.md             # This file
```

---

## 🔧 Advanced Configuration

### Change the API Token

1. Edit `nginx.conf` and replace the token in the `map` directive
2. Edit `config.env` and update `API_TOKEN`
3. Restart nginx: `sudo systemctl restart nginx`

### Use Environment Variables

All Python scripts support environment variables:
```bash
export API_URL="http://192.168.10.2:9100"
export API_TOKEN="your_custom_token"
export TEST_MODEL="gemma3:1b"

python3 test_remote.py
```

### Add More Ports

Edit `nginx.conf` and add another `server` block with a different port.

---

## 🐛 Troubleshooting

### Port 9100 not accessible?
```bash
# Check if nginx is listening
sudo netstat -tlnp | grep :9100

# Check nginx logs
sudo tail -f /var/log/nginx/error.log

# Restart nginx
sudo systemctl restart nginx
```

### Ollama not responding?
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama
ollama serve

# Check Ollama logs
tail -f ollama.log
```

### 401 Unauthorized?
- Verify the token in your request matches the one in `nginx.conf`
- Check the Authorization header format: `Bearer YOUR_TOKEN`

### Model not found?
```bash
# List available models
ollama list

# Pull a model
ollama pull gemma3:1b
```

---

## 🔒 Security Notes

- ⚠️ **Change the default token** before deploying to production
- 🔥 Use HTTPS in production (add SSL certificates to nginx)
- 🛡️ Consider using a firewall to restrict access
- 🔐 Keep your token secret and rotate it periodically

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 📧 Support

For issues and questions, please open an issue on GitHub.

---

**Made with ❤️ by FOCUS Corporation**

## Setup

1. **Install Ollama:**
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. **Install Nginx:**
```bash
# Ubuntu/Debian
sudo apt update && sudo apt install nginx -y

# CentOS/RHEL
sudo yum install nginx -y
```

3. **Generate a secure token:**
```bash
openssl rand -hex 32
```

4. **Update the token in `nginx.conf`:**
   - Open `nginx.conf`
   - Replace `YOUR_SECRET_TOKEN_HERE` with your generated token

5. **Copy nginx config:**
```bash
sudo cp nginx.conf /etc/nginx/sites-available/ollama
sudo ln -s /etc/nginx/sites-available/ollama /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default  # Remove default site
```

6. **Test and restart nginx:**
```bash
sudo nginx -t
sudo systemctl restart nginx
```

7. **Start Ollama:**
```bash
ollama serve
```

8. **Pull a model:**
```bash
ollama pull llama2
```

## Usage

### With curl:
```bash
curl -H "Authorization: Bearer YOUR_SECRET_TOKEN_HERE" \
     -d '{"model": "llama2", "prompt": "Hello!"}' \
     http://YOUR_PUBLIC_IP/api/generate
```

### With Python:
```python
import requests

headers = {
    "Authorization": "Bearer YOUR_SECRET_TOKEN_HERE"
}

response = requests.post(
    "http://YOUR_PUBLIC_IP/api/generate",
    headers=headers,
    json={
        "model": "llama2",
        "prompt": "Hello!",
        "stream": False
    }
)

print(response.json())
```

### With OpenAI-compatible API:
```python
from openai import OpenAI

client = OpenAI(
    base_url="http://YOUR_PUBLIC_IP/v1",
    api_key="YOUR_SECRET_TOKEN_HERE"
)

response = client.chat.completions.create(
    model="llama2",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## Check Status

```bash
# Check nginx status
sudo systemctl status nginx

# Check Ollama
ps aux | grep ollama

# Test without token (should fail)
curl http://YOUR_PUBLIC_IP/

# Test with token (should work)
curl -H "Authorization: Bearer YOUR_SECRET_TOKEN_HERE" http://YOUR_PUBLIC_IP/
```

## Run Ollama as Service (Optional)

Create `/etc/systemd/system/ollama.service`:
```ini
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
ExecStart=/usr/local/bin/ollama serve
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
```

## Security Notes

- Keep your token secret
- Consider using HTTPS in production (add SSL certificate to nginx)
- Restrict access by IP if needed

