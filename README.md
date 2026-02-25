# 🛡️ Pi-Claw Security

**Pi Security Agent for OpenClaw** - A sovereign AI security agent that works exactly like OpenClaw, with specialized security tools.

## Quick Start

```bash
# Clone the repository
git clone https://github.com/Pi-Swarm/pibot-swarm-v2.git
cd pibot-swarm-v2

# Check status (like 'openclaw status')
./pi status

# Run security tasks (like 'openclaw agent --message ...')
./pi agent "audit https://github.com/user/repo"
./pi agent "scan 192.168.1.1"
./pi agent "analyze code for vulnerabilities"
```

## Architecture (Same as OpenClaw)

```
┌─────────────────────────────────────┐
│           Pi Security Agent         │
│     (OpenClaw-compatible skill)     │
├─────────────────────────────────────┤
│  Tools:                             │
│  • audit_repo - Clone & audit repos │
│  • scan_target - Network scanning   │
│  • read_code - Read source files    │
│  • write_patch - Apply fixes        │
│  • ask_ollama - AI reasoning        │
├─────────────────────────────────────┤
│  AI Brain: Qwen2.5 via Ollama      │
└─────────────────────────────────────┘
```

## Location

The skill is installed at:
```
~/.openclaw/skills/pi-security/
```

This allows it to work alongside other OpenClaw skills.

## Usage

### 1. Check Status
```bash
./pi status
```

### 2. Audit Repository
```bash
./pi agent "audit https://github.com/user/repo"
```

### 3. Scan Network
```bash
./pi agent "scan 192.168.1.0/24"
```

### 4. Analyze Code
```bash
./pi agent "analyze current directory for vulnerabilities"
```

## How It Works (OpenClaw-Style)

1. **Gateway** (`./pi`): Receives commands like `openclaw` CLI
2. **Agent** (`agent.py`): Plans and executes security tasks
3. **Tools**: Actual security tools (nmap, git, file analysis)
4. **AI**: Uses local Qwen model for reasoning

## Requirements

- Python 3.10+
- Ollama installed with `qwen2.5:1.5b` model
- nmap (for network scanning)
- git (for repo auditing)

## Integration with OpenClaw

This skill follows OpenClaw's architecture exactly:
- Uses skills directory (`~/.openclaw/skills/`)
- Tool-based execution
- Session-based task management
- Local AI reasoning via Ollama

---

🥧 **Sovereign Security. Open Architecture. Built on OpenClaw.**
