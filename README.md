# 🥧 Pi-Swarm v8.0

**AI Security Swarm via Telegram**

Control your AI security agent from Telegram. Simple commands, powerful results.

---

## ⚡ Quick Install

```bash
# One line - that's it!
curl -fsSL https://raw.githubusercontent.com/Pi-Swarm/pibot-swarm-v2/main/install.sh | bash
```

### What it does:
1. Downloads Pi binary (~4MB)
2. Installs to `/usr/local/bin`
3. Optionally installs Ollama for local AI
4. Configures Telegram token

---

## 🤖 Telegram Commands

Message your bot:

| Command | Description | Example |
|---------|-------------|---------|
| `/status` | System status | `/status` |
| `/scan` | Scan IP/domain | `/scan 192.168.1.1` |
| `/audit` | Audit code | `/audit https://github.com/user/repo` |
| `/ask` | Ask AI | `/ask explain blockchain` |
| `/search` | Web search | `/search latest CVE` |
| `/help` | Show commands | `/help` |

---

## 🔑 Telegram Token Setup

1. Message [@BotFather](https://t.me/BotFather)
2. Send `/newbot`
3. Choose name: `MyPiSwarm`
4. Choose username: `mypiswarm_bot`
5. **Copy token** shown (e.g., `123456789:ABCdef...`)

---

## 🚀 Manual Install

If you prefer manual:

```bash
# Download
wget https://github.com/Pi-Swarm/pibot-swarm-v2/releases/download/v8.0/pi-linux-amd64
chmod +x pi-linux-amd64
sudo mv pi-linux-amd64 /usr/local/bin/pi

# Configure token
pi config telegram.token "YOUR_TOKEN"

# Start
pi telegram
```

---

## 📱 Example Chat

```
You: /status
Bot: 🥧 Pi-Swarm v8.0
     Status: Online ✅
     AI: Connected

You: /scan 192.168.1.1
Bot: 🔍 Scanning...
     Port 80: HTTP
     Port 443: HTTPS
     ✅ Done!

You: /ask what is DeFi?
Bot: DeFi is decentralized finance...
```

---

## 🛠️ Requirements

- Linux/macOS
- Telegram Bot Token
- Optional: Ollama for local AI

---

## 📦 Binary Downloads

Download directly for your platform:

| Platform | Download |
|----------|----------|
| Linux AMD64 | [pi-linux-amd64](https://github.com/Pi-Swarm/pibot-swarm-v2/releases/download/v8.0/pi-linux-amd64) |
| Linux ARM64 | [pi-linux-arm64](https://github.com/Pi-Swarm/pibot-swarm-v2/releases/download/v8.0/pi-linux-arm64) |
| macOS AMD64 | [pi-macos-amd64](https://github.com/Pi-Swarm/pibot-swarm-v2/releases/download/v8.0/pi-macos-amd64) |
| Windows | [pi-windows-amd64.exe](https://github.com/Pi-Swarm/pibot-swarm-v2/releases/download/v8.0/pi-windows-amd64.exe) |

---

## ♻️ Update

```bash
pi update
```

---

## 🆘 Troubleshoot

```bash
# Check version
pi --version

# Check config
pi config show

# Test AI
pi agent "hello" --dry-run

# View logs
pi logs
```

---

**Simple. Fast. Powerful.** 🥧
