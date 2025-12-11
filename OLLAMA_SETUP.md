# 🔧 Ollama Network Configuration

## ⚠️ Important: Ollama Must Listen on Network Interface

By default, Ollama only listens on `localhost (127.0.0.1)`, which means it's only accessible from the same machine. To make it work with Nginx forwarding from public IP, **Ollama must listen on all network interfaces (0.0.0.0)**.

---

## 🚀 Quick Setup (Automated)

Run the configuration script:

```bash
chmod +x configure_ollama.sh
sudo bash configure_ollama.sh
```

This will:
- ✅ Configure Ollama to listen on `0.0.0.0:11434`
- ✅ Create systemd service
- ✅ Start Ollama automatically
- ✅ Enable Ollama on boot

---

## 🔧 Manual Setup

### Option 1: Using Systemd Service (Recommended)

#### 1. Create Systemd Service
```bash
sudo tee /etc/systemd/system/ollama.service > /dev/null <<EOF
[Unit]
Description=Ollama Service
After=network-online.target

[Service]
Type=simple
User=$USER
ExecStart=/usr/local/bin/ollama serve
Environment="OLLAMA_HOST=0.0.0.0:11434"
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
EOF
```

#### 2. Reload and Start
```bash
sudo systemctl daemon-reload
sudo systemctl enable ollama
sudo systemctl start ollama
```

#### 3. Check Status
```bash
sudo systemctl status ollama
```

---

### Option 2: Using Environment Variable

#### Start Ollama with OLLAMA_HOST
```bash
OLLAMA_HOST=0.0.0.0:11434 ollama serve
```

#### Or export it first
```bash
export OLLAMA_HOST=0.0.0.0:11434
ollama serve
```

#### Run in background
```bash
OLLAMA_HOST=0.0.0.0:11434 nohup ollama serve > ollama.log 2>&1 &
```

---

## ✅ Verify Ollama is Listening

### Check if Ollama is listening on all interfaces
```bash
# Should show 0.0.0.0:11434
sudo netstat -tlnp | grep :11434

# Or using ss
sudo ss -tlnp | grep :11434
```

**Expected output:**
```
tcp   0   0 0.0.0.0:11434   0.0.0.0:*   LISTEN   12345/ollama
```

**NOT this (wrong):**
```
tcp   0   0 127.0.0.1:11434   0.0.0.0:*   LISTEN   12345/ollama
```

---

## 🧪 Test Ollama Access

### Test from localhost
```bash
curl http://localhost:11434/api/tags
```

### Test from local IP
```bash
curl http://192.168.10.2:11434/api/tags
```

### Test from another machine on the network
```bash
curl http://192.168.10.2:11434/api/tags
```

**All should return the same response!**

---

## 🔄 How It Works

```
Internet Request (197.13.2.177:9100)
    ↓
Nginx (checks token)
    ↓
Forwards to Ollama (0.0.0.0:11434)
    ↓
Ollama processes request
    ↓
Response back through Nginx
    ↓
Back to client
```

**Key Point:** Nginx runs on the server and forwards to Ollama. Ollama must be accessible on the network interface (not just localhost) for this to work.

---

## 🛡️ Security Note

**Ollama on 0.0.0.0:11434 is NOT directly exposed to the internet!**

- ✅ Nginx (ports 80, 9100) is exposed with token authentication
- ✅ Ollama (port 11434) is only accessible on local network
- ✅ Firewall should block port 11434 from internet
- ✅ Only Nginx can access Ollama

**Firewall configuration:**
```bash
# Allow Nginx ports
sudo ufw allow 80/tcp
sudo ufw allow 9100/tcp

# Block Ollama port from internet (only allow local)
sudo ufw deny 11434/tcp
```

---

## 🐛 Troubleshooting

### Problem: "Connection refused" when testing API

**Check if Ollama is running:**
```bash
ps aux | grep ollama
sudo systemctl status ollama
```

**Check if Ollama is listening:**
```bash
sudo netstat -tlnp | grep :11434
```

**If showing 127.0.0.1:11434 instead of 0.0.0.0:11434:**
```bash
# Stop Ollama
sudo systemctl stop ollama
pkill -f "ollama serve"

# Reconfigure
sudo bash configure_ollama.sh
```

---

### Problem: Ollama not starting

**Check logs:**
```bash
sudo journalctl -u ollama -f
```

**Check if port is already in use:**
```bash
sudo lsof -i :11434
```

**Restart service:**
```bash
sudo systemctl restart ollama
```

---

### Problem: Works locally but not from public IP

**Check Nginx is forwarding correctly:**
```bash
# Test Nginx locally
curl -H "Authorization: Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38" \
     http://localhost:9100/api/tags

# Check Nginx logs
sudo tail -f /var/log/nginx/error.log
```

**Check firewall:**
```bash
sudo ufw status
```

**Make sure port 9100 is open:**
```bash
sudo ufw allow 9100/tcp
```

---

## 📋 Service Management Commands

```bash
# Start Ollama
sudo systemctl start ollama

# Stop Ollama
sudo systemctl stop ollama

# Restart Ollama
sudo systemctl restart ollama

# Check status
sudo systemctl status ollama

# View logs
sudo journalctl -u ollama -f

# Enable on boot
sudo systemctl enable ollama

# Disable on boot
sudo systemctl disable ollama
```

---

## ✨ Summary

**For Ollama to work with public IP access:**

1. ✅ Ollama must listen on `0.0.0.0:11434` (not `127.0.0.1`)
2. ✅ Use `OLLAMA_HOST=0.0.0.0:11434` environment variable
3. ✅ Or use the automated script: `sudo bash configure_ollama.sh`
4. ✅ Verify with: `sudo netstat -tlnp | grep :11434`
5. ✅ Should show `0.0.0.0:11434`, not `127.0.0.1:11434`

**Then Nginx can forward requests from public IP to Ollama!** 🚀

