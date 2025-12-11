#!/bin/bash

echo "=========================================="
echo "  Configure Ollama for Network Access"
echo "=========================================="
echo ""

# Create systemd service directory if it doesn't exist
sudo mkdir -p /etc/systemd/system/ollama.service.d

# Create environment override file
echo "Creating Ollama environment configuration..."
sudo tee /etc/systemd/system/ollama.service.d/environment.conf > /dev/null <<EOF
[Service]
Environment="OLLAMA_HOST=0.0.0.0:11434"
EOF

echo "✓ Environment configuration created"
echo ""

# Create or update the main systemd service file
echo "Creating Ollama systemd service..."
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

echo "✓ Systemd service created"
echo ""

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Stop any running Ollama processes
echo "Stopping any running Ollama processes..."
pkill -f "ollama serve" 2>/dev/null || true
sleep 2

# Enable and start the service
echo "Enabling and starting Ollama service..."
sudo systemctl enable ollama
sudo systemctl start ollama

# Wait a moment for the service to start
sleep 3

# Check status
echo ""
echo "Checking Ollama status..."
sudo systemctl status ollama --no-pager | head -15

echo ""
echo "Checking if Ollama is listening on all interfaces..."
sudo netstat -tlnp | grep :11434 || sudo ss -tlnp | grep :11434

echo ""
echo "=========================================="
echo "  ✓ Ollama Configuration Complete!"
echo "=========================================="
echo ""
echo "Ollama is now configured to listen on:"
echo "  - 0.0.0.0:11434 (all interfaces)"
echo ""
echo "This allows Nginx to forward requests from:"
echo "  - Local network (192.168.10.2)"
echo "  - Public IP (197.13.2.177)"
echo ""
echo "Test Ollama directly:"
echo "  curl http://localhost:11434/api/tags"
echo "  curl http://192.168.10.2:11434/api/tags"
echo ""
echo "Manage Ollama service:"
echo "  sudo systemctl status ollama"
echo "  sudo systemctl restart ollama"
echo "  sudo systemctl stop ollama"
echo "  sudo journalctl -u ollama -f"
echo ""

