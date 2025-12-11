# 🚀 Deployment Guide

## Server Deployment (192.168.10.2)

### Step 1: Clone Repository on Server
```bash
git clone <your-repo-url>
cd <repo-name>
```

### Step 2: Configure Server IP
Edit `config.env`:
```bash
nano config.env
```

Make sure `SERVER_IP=192.168.10.2` (or your actual server IP)

### Step 3: Run Deployment Script
```bash
chmod +x deploy.sh
sudo bash deploy.sh
```

This will:
- Install Nginx
- Install Ollama
- Configure Nginx with token authentication
- Enable services

### Step 4: Start Ollama
```bash
# Option 1: Run in foreground
ollama serve

# Option 2: Run in background
nohup ollama serve > ollama.log 2>&1 &
```

### Step 5: Pull Models
```bash
# Pull recommended model for testing
ollama pull gemma3:1b

# Pull other models (optional)
ollama pull llama3
ollama pull qwen3:8b
```

### Step 6: Test the API
```bash
bash test.sh
```

Expected output:
```
1. Testing WITHOUT token (should return 401)...
   ✓ PASS - Correctly blocked (401)

2. Testing WITH token (should return 200)...
   ✓ PASS - Authentication successful (200)

3. Listing available models...
   ✓ PASS - Models found:
      - gemma3:1b

4. Testing text generation with gemma3:1b...
   ✓ PASS - Response received:
      Hello! ...
```

---

## Remote Testing (From Another Device)

### Step 1: Copy Test Scripts
Copy these files to your remote device:
- `test_remote.py`
- `simple_test.py`
- `openai_example.py`
- `requirements.txt`
- `config.env`

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API URL
Edit `config.env` or set environment variable:
```bash
export API_URL="http://192.168.10.2:9100"
```

### Step 4: Run Tests
```bash
# Full test suite
python3 test_remote.py

# Quick test
python3 simple_test.py

# OpenAI example
python3 openai_example.py
```

---

## Public IP Forwarding

If your server IP (192.168.10.2) is forwarded to a public IP:

### Update Configuration
```bash
# Set the public IP in config.env
SERVER_IP=YOUR_PUBLIC_IP

# Or use environment variable
export API_URL="http://YOUR_PUBLIC_IP:9100"
```

### Firewall Configuration
Make sure ports are open:
```bash
# Ubuntu/Debian (ufw)
sudo ufw allow 80/tcp
sudo ufw allow 9100/tcp

# CentOS/RHEL (firewalld)
sudo firewall-cmd --permanent --add-port=80/tcp
sudo firewall-cmd --permanent --add-port=9100/tcp
sudo firewall-cmd --reload
```

---

## Production Deployment

### 1. Change the Default Token
Edit `nginx.conf`:
```nginx
map $http_authorization $auth_valid {
    default 0;
    "Bearer YOUR_NEW_SECURE_TOKEN" 1;
}
```

Update `config.env`:
```bash
API_TOKEN=YOUR_NEW_SECURE_TOKEN
```

Restart nginx:
```bash
sudo systemctl restart nginx
```

### 2. Enable HTTPS (Recommended)
Install certbot:
```bash
sudo apt install certbot python3-certbot-nginx
```

Get SSL certificate:
```bash
sudo certbot --nginx -d your-domain.com
```

### 3. Set Up Ollama as a Service
Create `/etc/systemd/system/ollama.service`:
```ini
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=ollama
ExecStart=/usr/local/bin/ollama serve
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
```

### 4. Monitor Services
```bash
# Check nginx status
sudo systemctl status nginx

# Check ollama status
sudo systemctl status ollama

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# View ollama logs
sudo journalctl -u ollama -f
```

---

## Troubleshooting

### Cannot connect to server
1. Check if nginx is running: `sudo systemctl status nginx`
2. Check if port is open: `sudo netstat -tlnp | grep :9100`
3. Check firewall rules
4. Verify server IP is correct

### 401 Unauthorized
1. Verify token matches in `nginx.conf` and your request
2. Check header format: `Authorization: Bearer TOKEN`
3. Restart nginx after config changes

### Model not found
1. Check available models: `ollama list`
2. Pull the model: `ollama pull gemma3:1b`
3. Wait for model to download completely

### Slow responses
1. Use smaller models for testing (gemma3:1b)
2. Check server resources (CPU, RAM, GPU)
3. Increase nginx timeouts in `nginx.conf`

---

## Quick Commands Reference

```bash
# Server setup
sudo bash deploy.sh
ollama serve
ollama pull gemma3:1b
bash test.sh

# Service management
sudo systemctl restart nginx
sudo systemctl restart ollama
sudo systemctl status nginx
sudo systemctl status ollama

# Testing
bash test.sh                    # Bash test
python3 test_remote.py          # Python full test
python3 simple_test.py          # Python quick test

# Logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u ollama -f
```

---

**Your Ollama API is ready! 🚀**

