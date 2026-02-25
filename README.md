<p align="center">
  <img src="https://github.com/Pi-Swarm/Pi-Swarm/raw/main/logo.png" width="120" alt="Pi Swarm Logo">
</p>

<h1 align="center">🛡️ PI SOVEREIGN CORE (v3.1)</h1>

<p align="center">
  <strong>Autonomous AI Security Engine built on OpenClaw Philosophy.</strong>
</p>

---

## 🚀 The Pi-Claw Interface
Pi Swarm now operates via a unified Command Line Interface (CLI), mirroring the robustness of **OpenClaw**. Every security task is driven by an autonomous reasoning loop.

### 1. Prerequisites
- **Python 3.10+**
- **[Ollama](https://ollama.com)** with the `qwen2.5:1.5b` model installed.
- **OpenClaw** environment configured.

### 2. Quick Setup
```bash
git clone https://github.com/Pi-Swarm/pibot-swarm-v2.git
cd pibot-swarm-v2
# Ensure Ollama is running:
ollama run qwen2.5:1.5b
```

---

## 🛠️ Usage (CLI Commands)

### Check Fortress Status:
Display the health, version, and workspace of the swarm.
```bash
python3 pi.py status
```

### Autonomous Security Audit:
Instruct the swarm to clone, analyze, and generate AI-driven patches for a target repository.
```bash
python3 pi.py audit <github_url>
```

---

## 🧠 Intelligence Architecture
- **Reasoning Engine:** Qwen2.5:1.5B (via local Ollama API).
- **Core Logic:** Multi-agent handoff inspired by **Cline** and **Decepticon**.
- **Audit Standard:** [Sovereign Security Standard v1.1](docs/intelligence/AUDIT_METHODOLOGY.md)

---
## 📡 Connectivity
- **Official Hub:** [Pi-Swarm.github.io](https://Pi-Swarm.github.io)
- **Status Reports:** Generated locally by the Monitor Agent.

<p align="center">
  <em>Securing the Frontier of Sovereign AI. Built on OpenClaw.</em>
</p>
