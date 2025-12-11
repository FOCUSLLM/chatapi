#!/bin/bash

echo "=========================================="
echo "  FOCUS Corporation - Ollama API Setup"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "Please run with sudo: sudo bash deploy.sh"
    exit 1
fi

# Install Nginx if not installed
if ! command -v nginx &> /dev/null; then
    echo "Installing Nginx..."
    apt update
    apt install nginx -y
else
    echo "✓ Nginx already installed"
fi

# Install Ollama if not installed
if ! command -v ollama &> /dev/null; then
    echo "Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "✓ Ollama already installed"
fi

# Copy Nginx configuration
echo "Configuring Nginx..."
cp nginx.conf /etc/nginx/sites-available/ollama

# Enable the site
ln -sf /etc/nginx/sites-available/ollama /etc/nginx/sites-enabled/ollama

# Remove default site if exists
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
echo "Testing Nginx configuration..."
nginx -t

if [ $? -ne 0 ]; then
    echo "✗ Nginx configuration error!"
    exit 1
fi

echo "✓ Nginx configuration valid"

# Restart Nginx
echo "Restarting Nginx..."
systemctl restart nginx
systemctl enable nginx

echo "✓ Nginx restarted and enabled"

# Configure Ollama to listen on all interfaces
echo ""
echo "Configuring Ollama..."
bash configure_ollama.sh

echo ""
echo "=========================================="
echo "  ✓ Installation Complete!"
echo "=========================================="
echo ""
echo "Your Ollama API is now running on:"
echo "  - Local (Port 80):   http://192.168.10.2"
echo "  - Local (Port 9100): http://192.168.10.2:9100"
echo "  - Public (Port 9100): http://197.13.2.177:9100"
echo ""
echo "Token: FOCUS_Corporation_a4e83f94514e155693c499c256e57a38"
echo ""
echo "Next steps:"
echo "1. Pull a model: ollama pull gemma3:1b"
echo "2. Test local: bash test.sh"
echo "3. Test public: bash test_public.sh"
echo ""

