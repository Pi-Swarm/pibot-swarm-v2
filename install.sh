#!/bin/bash
#
# Pi-Swarm One-Line Installer
#

set -e

echo "🥧 Installing Pi-Swarm..."

# Detect OS and architecture
OS="linux"
ARCH="amd64"

if [[ "$OSTYPE" == "darwin"* ]]; then
    OS="macos"
fi

if [[ $(uname -m) == "aarch64" ]] || [[ $(uname -m) == "arm64" ]]; then
    ARCH="arm64"
fi

echo "📱 Platform: $OS-$ARCH"

# Download URL
URL="https://github.com/Pi-Swarm/pibot-swarm-v2/releases/download/v8.0/pi-$OS-$ARCH"
INSTALL_DIR="/usr/local/bin"

# Check if can write to /usr/local/bin
if [ -w "$INSTALL_DIR" ]; then
    INSTALL_PATH="$INSTALL_DIR/pi"
else
    INSTALL_DIR="$HOME/.local/bin"
    INSTALL_PATH="$INSTALL_DIR/pi"
    mkdir -p "$INSTALL_DIR"
fi

# Download
echo "⬇️  Downloading..."
if command -v curl >/dev/null; then
    curl -fsSL "$URL" -o "$INSTALL_PATH"
elif command -v wget >/dev/null; then
    wget -q "$URL" -O "$INSTALL_PATH"
else
    echo "❌ Need curl or wget"
    exit 1
fi

# Make executable
chmod +x "$INSTALL_PATH"

# Add to PATH if needed
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo 'export PATH="$PATH:'$INSTALL_DIR'"' >> ~/.bashrc
    echo '📌 Added to PATH. Run: source ~/.bashrc'
fi

echo "✅ Pi-Swarm installed!"

# Ask about Ollama
read -p "Install Ollama for local AI? (y/n) " reply
if [ "$reply" = "y" ]; then
    echo "🤖 Installing Ollama..."
    curl -fsSL https://ollama.com/install.sh | sh
    ollama pull qwen2.5:1.5b
    echo "✅ Ollama ready!"
fi

# Telegram token
echo ""
echo "🤖 Get Telegram token:"
echo "   1. Message @BotFather on Telegram"
echo "   2. Send /newbot"
echo "   3. Copy token shown"
echo ""
read -p "Paste Telegram token: " token

if [ -n "$token" ]; then
    mkdir -p ~/.pi-swarm
    echo "{\"telegram\":{\"token\":\"$token\",\"enabled\":true}}" > ~/.pi-swarm/config.json
    echo "✅ Config saved"
fi

echo ""
echo "🎮 Start: pi telegram"
echo "📚 Help: pi --help"
