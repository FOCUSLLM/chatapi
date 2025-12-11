# 🌐 Public IP Configuration

## ✅ Public IP Support Added!

Your Ollama API is now configured to be accessible on both:
- **Local Network:** `192.168.10.2:9100`
- **Public IP:** `197.13.2.177:9100`

---

## 🔧 What's Been Configured

### Nginx Configuration
The nginx server now listens on:
```nginx
server {
    listen 9100;                    # All interfaces
    listen 197.13.2.177:9100;      # Specific public IP
    ...
}
```

This means your API is accessible from:
- ✅ Local network devices (192.168.10.2)
- ✅ Internet (197.13.2.177)

---

## 📡 API Endpoints

### Local Network Access
```
http://192.168.10.2:9100
```

### Public IP Access
```
http://197.13.2.177:9100
```

**Both use the same token:** `FOCUS_Corporation_a4e83f94514e155693c499c256e57a38`

---

## 🧪 Testing

### Test Local Network
```bash
bash test.sh
# or
python3 test_remote.py
```

### Test Public IP
```bash
bash test_public.sh
# or
python3 test_public.py
```

---

## 🔥 Usage Examples

### From Local Network
```bash
curl -H "Authorization: Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38" \
     -d '{"model": "gemma3:1b", "prompt": "Hello!", "stream": false}' \
     http://192.168.10.2:9100/api/generate
```

### From Internet (Public IP)
```bash
curl -H "Authorization: Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38" \
     -d '{"model": "gemma3:1b", "prompt": "Hello!", "stream": false}' \
     http://197.13.2.177:9100/api/generate
```

### Python Example (Public IP)
```python
import requests

response = requests.post(
    "http://197.13.2.177:9100/api/generate",
    headers={"Authorization": "Bearer FOCUS_Corporation_a4e83f94514e155693c499c256e57a38"},
    json={"model": "gemma3:1b", "prompt": "Hello!", "stream": False}
)

print(response.json()['response'])
```

---

## 🚀 Deployment Steps

### On Your Server (192.168.10.2):

```bash
# 1. Clone/pull latest changes
cd chatapi
git pull

# 2. Update nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/ollama
sudo nginx -t
sudo systemctl restart nginx

# 3. Verify nginx is listening on public IP
sudo netstat -tlnp | grep :9100
```

Expected output:
```
tcp        0      0 0.0.0.0:9100            0.0.0.0:*               LISTEN      12345/nginx
tcp        0      0 197.13.2.177:9100       0.0.0.0:*               LISTEN      12345/nginx
```

### 4. Test from Server
```bash
# Test local
bash test.sh

# Test public IP
bash test_public.sh
```

---

## 🛡️ Firewall Configuration

Make sure port 9100 is open on your firewall:

### Ubuntu/Debian (ufw)
```bash
sudo ufw allow 9100/tcp
sudo ufw status
```

### CentOS/RHEL (firewalld)
```bash
sudo firewall-cmd --permanent --add-port=9100/tcp
sudo firewall-cmd --reload
sudo firewall-cmd --list-ports
```

### Cloud Provider Firewall
If your server is on a cloud provider (AWS, GCP, Azure, etc.), make sure to:
1. Add inbound rule for port 9100
2. Allow TCP traffic from 0.0.0.0/0 (or specific IPs)

---

## 🔒 Security Considerations

### ✅ Already Implemented
- Token-based authentication
- Same token for both local and public access
- Nginx rate limiting (can be added)

### 🔐 Recommended for Production
1. **Change the default token** in `nginx.conf`
2. **Enable HTTPS** with SSL certificates
3. **Add rate limiting** to prevent abuse
4. **Whitelist specific IPs** if possible
5. **Monitor access logs** regularly

### Enable HTTPS (Recommended)
```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get SSL certificate (requires domain name)
sudo certbot --nginx -d your-domain.com

# Or use self-signed certificate for testing
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /etc/ssl/private/nginx-selfsigned.key \
    -out /etc/ssl/certs/nginx-selfsigned.crt
```

---

## 📊 Monitoring

### Check Nginx Access Logs
```bash
sudo tail -f /var/log/nginx/access.log
```

### Check Nginx Error Logs
```bash
sudo tail -f /var/log/nginx/error.log
```

### Check Active Connections
```bash
sudo netstat -an | grep :9100
```

---

## 🐛 Troubleshooting

### Cannot connect from public IP
1. **Check firewall:**
   ```bash
   sudo ufw status
   sudo netstat -tlnp | grep :9100
   ```

2. **Check nginx is listening on public IP:**
   ```bash
   sudo nginx -T | grep "listen.*9100"
   ```

3. **Test from server itself:**
   ```bash
   curl http://197.13.2.177:9100/api/tags
   ```

4. **Check cloud provider security groups/firewall rules**

### Getting 401 errors
- Verify token is correct
- Check header format: `Authorization: Bearer TOKEN`

### Slow responses
- Check server resources (CPU, RAM)
- Use smaller models for testing
- Increase nginx timeouts if needed

---

## ✨ Summary

Your Ollama API is now accessible from:
- ✅ **Local Network:** `http://192.168.10.2:9100`
- ✅ **Public IP:** `http://197.13.2.177:9100`

**Same token works for both!**

**Next steps:**
1. Deploy updated nginx config on server
2. Open firewall port 9100
3. Test with `bash test_public.sh`
4. Use from anywhere with public IP!

🚀 **Ready to use!**

