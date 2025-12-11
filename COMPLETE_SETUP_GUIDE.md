# 🚀 Complete Setup Guide - FOCUS Corporation Ollama API

## ⚠️ IMPORTANT: Understanding the Setup

### The Problem You Had:
- Nginx was configured to forward requests from public IP (197.13.2.177)
- But Ollama was only listening on localhost (127.0.0.1)
- So public IP requests couldn't reach Ollama

### The Solution:
- Configure Ollama to listen on **0.0.0.0:11434** (all interfaces)
- This allows Nginx to forward requests from any IP to Ollama
- Now both local and public IP work!

---

## 📋 Complete Deployment Steps

### On Your Server (192.168.10.2):

```bash
# 1. Clone the repository
git clone https://github.com/FOCUSLLM/chatapi.git
cd chatapi

# 2. Run deployment (installs Nginx + Ollama + configures everything)
chmod +x deploy.sh configure_ollama.sh
sudo bash deploy.sh

# 3. Pull a model
ollama pull gemma3:1b

# 4. Open firewall
sudo ufw allow 80/tcp
sudo ufw allow 9100/tcp

# 5. Test local network
bash test.sh

# 6. Test public IP
bash test_public.sh
```

**That's it! Your API is ready!** 🎉

---

## 🔧 What deploy.sh Does:

1. ✅ Installs Nginx
2. ✅ Installs Ollama
3. ✅ Configures Nginx to listen on ports 80 and 9100
4. ✅ Configures Nginx to forward to Ollama
5. ✅ **Configures Ollama to listen on 0.0.0.0:11434** ⭐
6. ✅ Creates systemd service for Ollama
7. ✅ Starts all services

---

## 🌐 How It Works:

```
┌─────────────────────────────────────────────────────────┐
│  Client Request                                         │
│  http://197.13.2.177:9100/api/generate                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Nginx (Port 9100)                                      │
│  - Checks token authentication                          │
│  - If valid, forwards to Ollama                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Ollama (0.0.0.0:11434)                                │
│  - Listens on ALL interfaces                            │
│  - Processes AI request                                 │
│  - Returns response                                     │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  Response back to client                                │
└─────────────────────────────────────────────────────────┘
```

**Key Point:** Ollama must listen on `0.0.0.0` (not `127.0.0.1`) to accept forwarded requests!

---

## ✅ Verify Everything is Working:

### 1. Check Nginx is running
```bash
sudo systemctl status nginx
sudo netstat -tlnp | grep :9100
# Should show nginx listening on port 9100
```

### 2. Check Ollama is running
```bash
sudo systemctl status ollama
```

### 3. Check Ollama is listening on ALL interfaces ⚠️ IMPORTANT!
```bash
sudo netstat -tlnp | grep :11434
```

**Expected (CORRECT):**
```
tcp   0   0 0.0.0.0:11434   0.0.0.0:*   LISTEN   12345/ollama
```

**NOT this (WRONG):**
```
tcp   0   0 127.0.0.1:11434   0.0.0.0:*   LISTEN   12345/ollama
```

If you see `127.0.0.1`, run:
```bash
sudo bash configure_ollama.sh
```

---

## 🧪 Testing:

### Test 1: Local Network
```bash
bash test.sh
```

### Test 2: Public IP
```bash
bash test_public.sh
```

### Test 3: Manual curl (Public IP)
```bash
curl -H "Authorization: Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38" \
     -d '{"model": "gemma3:1b", "prompt": "Hello!", "stream": false}' \
     http://197.13.2.177:9100/api/generate
```

---

## 📡 Your API Endpoints:

| Endpoint | Access From | Status |
|----------|-------------|--------|
| `http://192.168.10.2:80` | Local network | ✅ |
| `http://192.168.10.2:9100` | Local network | ✅ |
| `http://197.13.2.177:9100` | Internet | ✅ |

**Token:** `FOCUS_Corporation_a4e83f94514e155693c499c256e57a38`

---

## 🔒 Security:

### What's Protected:
- ✅ Nginx ports (80, 9100) require token authentication
- ✅ Ollama port (11434) is NOT exposed to internet
- ✅ Only Nginx can access Ollama

### Firewall Configuration:
```bash
# Allow Nginx ports (public access with token)
sudo ufw allow 80/tcp
sudo ufw allow 9100/tcp

# Block Ollama port from internet (local only)
sudo ufw deny 11434/tcp
```

---

## 🐛 Troubleshooting:

### Problem: "Connection refused" from public IP

**Solution:**
```bash
# 1. Check Ollama is listening on 0.0.0.0
sudo netstat -tlnp | grep :11434

# 2. If showing 127.0.0.1, reconfigure:
sudo bash configure_ollama.sh

# 3. Verify again
sudo netstat -tlnp | grep :11434
```

### Problem: Works locally but not from public IP

**Solution:**
```bash
# 1. Check firewall
sudo ufw status
sudo ufw allow 9100/tcp

# 2. Check nginx is listening on public IP
sudo netstat -tlnp | grep :9100

# 3. Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Problem: 401 Unauthorized

**Solution:**
- Verify token is correct
- Check header format: `Authorization: Bearer TOKEN`
- No extra spaces or quotes

---

## 📚 Documentation Files:

- **README.md** - Main documentation
- **DEPLOYMENT.md** - Deployment guide
- **SERVER_DEPLOYMENT.md** - Server deployment steps
- **OLLAMA_SETUP.md** - Ollama configuration guide ⭐
- **PUBLIC_IP_SETUP.md** - Public IP configuration
- **COMPLETE_SETUP_GUIDE.md** - This file

---

## 🎯 Quick Reference:

### Service Management:
```bash
# Nginx
sudo systemctl status nginx
sudo systemctl restart nginx

# Ollama
sudo systemctl status ollama
sudo systemctl restart ollama
sudo journalctl -u ollama -f
```

### Testing:
```bash
bash test.sh           # Local network
bash test_public.sh    # Public IP
python3 test_remote.py # Python test (local)
python3 test_public.py # Python test (public)
```

### Logs:
```bash
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u ollama -f
```

---

## ✨ Summary:

**The key to making public IP work:**
1. ✅ Ollama must listen on `0.0.0.0:11434` (not `127.0.0.1`)
2. ✅ Use `configure_ollama.sh` to set this up
3. ✅ Verify with `sudo netstat -tlnp | grep :11434`
4. ✅ Should show `0.0.0.0:11434`

**Then everything works!** 🚀

**Repository:** https://github.com/FOCUSLLM/chatapi

