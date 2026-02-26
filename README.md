# 🛡️ Pi-Swarm Security Edition (Rust)

**Sovereign AI Security Agent - OpenClaw Architecture Rebuilt in Rust**

A security-focused, high-performance AI agent built with Rust that mirrors OpenClaw's architecture.

---

## ⚡ Why Rust?

| Metric | Node.js (OpenClaw) | Rust (Pi-Swarm) |
|--------|---------------------|-----------------|
| **Speed** | Interpreted | Native (10-100x faster) |
| **Memory** | GC pauses | Zero-cost safety |
| **Binary** | ~50MB + node_modules | Single ~5MB file |
| **Startup** | Seconds | Milliseconds |
| **Concurrency** | Event loop | Real threads |

---

## 📦 Installation

### Prerequisites

```bash
# 1. Install Rust (if not installed)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env

# 2. Install Ollama (required for AI)
curl -fsSL https://ollama.com/install.sh | sh
ollama pull qwen2.5:1.5b

# 3. Install nmap (for network scanning)
sudo apt install nmap   # Ubuntu/Debian
brew install nmap       # macOS
```

### Clone and Build

```bash
# Clone repository
git clone https://github.com/Pi-Swarm/pibot-swarm-v2.git
cd pibot-swarm-v2

# Build development version
cargo build

# Build optimized release
cargo build --release

# Result: target/release/pi (single binary)
```

### Install Globally (Optional)

```bash
# Copy to system PATH
sudo cp target/release/pi /usr/local/bin/

# Or create symlink
ln -sf $(pwd)/target/release/pi ~/.local/bin/pi

# Now you can run 'pi' from anywhere
pi status
```

---

## 🎮 How to Run

### 1. Quick Start

```bash
# Check system health
./target/release/pi status

# Expected output:
# 🛡️ Pi Swarm Security Edition
#    Version: 2026.2.26
#
# 🟢 AI Brain (Ollama): Connected
# 🛡️ Security Tools: Loaded
#    • audit_repo
#    • scan_target
#    • analyze_code
#    • write_patch
```

### 2. Main Commands

```bash
# System commands (same as 'openclaw')
./pi status                      # Check system health
./pi onboard                     # Setup wizard
./pi help                        # Show all commands

# Agent commands (same as 'openclaw agent --message')
./pi agent "How do I fix SQL injection?"
./pi agent "What are common Solana vulnerabilities?"

# Security audit
./pi security audit ./my_code.rs                   # Audit local file
./pi security audit https://github.com/user/repo   # Audit GitHub repo

# Network scanning
./pi security scan 192.168.1.1                     # Scan single IP
./pi security scan 192.168.1.0/24                  # Scan network range

# Autonomous tasks
./pi task "Find vulnerabilities in current directory"
./pi task "Audit all Rust files for UncheckedAccount issues"

# Gateway daemon (same as 'openclaw gateway')
./pi gateway                      # Start on default port
./pi gateway -p 9876              # Start on custom port
./pi gateway --verbose            # Show detailed logs
```

---

## 🛠️ Detailed Usage

### Security Audit Examples

```bash
# 1. Audit local Solana contract
./pi security audit ./programs/my_program/src/lib.rs

# Output: AI analyzes code, lists vulnerabilities, suggests fixes

# 2. Audit GitHub repository
./pi security audit https://github.com/KadeshX-Web3/KadeshX

# Output: Clones repo, finds code files, runs security analysis

# 3. Audit with custom task
./pi task "Read ./src/main.rs and check for all vulnerabilities"
```

### Network Scanning Examples

```bash
# 1. Quick scan on localhost
./pi security scan 127.0.0.1

# Output: Port scan + AI security analysis

# 2. Scan router
./pi security scan 192.168.1.1

# 3. Scan range (use carefully)
./pi security scan 192.168.1.0/24
```

### AI Agent Conversation

```bash
# Ask security questions
./pi agent "What is reentrancy attack and how to prevent it?"
./pi agent "Explain unchecked account vulnerability in Solana"
./pi agent "Compare Solidity vs Rust security patterns"

# Task planning
./pi task "Plan how to audit a DeFi protocol"
```

---

## 📱 Telegram Control

### Setup

```bash
# 1. Get bot token from @BotFather

# 2. Set environment variable
export PI_TELEGRAM_TOKEN="your_bot_token_here"

# 3. Start Telegram gateway
./pi telegram

# Output:
# 🛡️ Telegram Gateway starting...
#    Bot token: abc123...
#    Send /start to your bot on Telegram
```

### Telegram Commands

Once running, message your bot:

| Command | Example | Description |
|---------|---------|-------------|
| `/start` | | Welcome message |
| `/status` | | Check system |
| `/audit` | `/audit https://github.com/user/repo` | Security audit |
| `/scan` | `/scan 192.168.1.1` | Network scan |
| `/task` | `/task Find vulnerabilities` | Autonomous task |
| `/agent` | `/agent How to fix SQLi?` | AI chat |
| `/help` | | Show commands |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│         pi (Rust Binary)                │
│           5MB, Single File              │
├─────────────────────────────────────────┤
│                                         │
│  ┌─────────────┐  ┌─────────────────┐  │
│  │   Gateway   │  │     Session     │  │
│  │   (Axum)    │  │    Manager      │  │
│  └──────┬──────┘  └───────┬─────────┘  │
│         │                 │             │
│  ┌──────▼─────────────────▼─────────┐   │
│  │         Security Agent         │    │
│  │    Think → Act → Observe       │    │
│  └──────┬─────────────────┬───────┘    │
│         │                 │             │
│  ┌──────▼───┐  ┌──────────▼────────┐   │
│  │  Tools   │  │     Provider      │   │
│  │ • audit  │  │  (Ollama Client)   │   │
│  │ • scan   │  │  • qwen2.5:1.5b   │   │
│  │ • patch  │  └───────────────────┘   │
│  └──────────┘                           │
│                                         │
└─────────────────────────────────────────┘
```

---

## 🔄 Development Workflow

```bash
# 1. Edit source files in src/

# 2. Test changes
cargo run -- status
cargo run -- agent "Test message"

# 3. Build release
cargo build --release

# 4. Run binary directly
./target/release/pi status
```

---

## 📊 Comparison with OpenClaw

| Command | OpenClaw | Pi-Swarm |
|---------|----------|----------|
| Check status | `openclaw status` | `./pi status` |
| Agent chat | `openclaw agent -m "hello"` | `./pi agent "hello"` |
| Gateway | `openclaw gateway` | `./pi gateway` |
| Security audit | ❌ Not built-in | `./pi security audit` |
| Network scan | ❌ Not built-in | `./pi security scan` |
| Autonomous task | `openclaw agent --task` | `./pi task` |
| Telegram | Extension | Built-in |

---

## 🔧 Configuration

### Environment Variables

```bash
# AI Settings
export PI_MODEL="qwen2.5:1.5b"        # Default model
export PI_OLLAMA_URL="http://localhost:11434"

# Gateway Settings
export PI_PORT="18789"                 # Gateway port
export PI_VERBOSE="true"               # Enable debug logs

# Telegram
export PI_TELEGRAM_TOKEN="..."         # Bot token

# Workspace
export PI_WORKSPACE="$HOME/.openclaw/workspace/pibot"
```

---

## 🚀 Production Deployment

```bash
# 1. Build optimized binary
cargo build --release

# 2. Copy to server
scp target/release/pi server:~/

# 3. Set environment
export PI_TELEGRAM_TOKEN="..."

# 4. Run (or use systemd)
./pi gateway

# Or run as service
sudo systemctl enable pi-gateway
sudo systemctl start pi-gateway
```

---

## 📞 Support

- **Repository**: https://github.com/Pi-Swarm/pibot-swarm-v2
- **Issues**: Report bugs on GitHub Issues
- **Documentation**: See ARCHITECTURE.md for technical details

---

**🛡️ Sovereign AI Security. Built with Rust. Powered by Ollama.**
