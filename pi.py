#!/usr/bin/env python3
"""
🛡️ Pi-Claw - Enhanced OpenClaw for Security Operations
Architecture: OpenClaw Gateway + Pi Swarm Security Tools
"""

import sys
import os
import json
import urllib.request
from pathlib import Path

# Configuration - Same as OpenClaw style
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:1.5b"
WORKSPACE = str(Path.home() / ".openclaw/workspace/pibot")

class PiSwarmTools:
    """Security tools that OpenClaw security agent can call"""
    
    def scan_target(self, target: str):
        """Network reconnaissance tool"""
        import subprocess
        result = subprocess.run(["nmap", "-sV", target], capture_output=True, text=True)
        return result.stdout[:2000] if result.returncode == 0 else f"Error: {result.stderr}"
    
    def audit_repo(self, repo_url: str):
        """Clone and audit a repository"""
        import subprocess
        import tempfile
        
        tmpdir = tempfile.mkdtemp()
        subprocess.run(["git", "clone", "--depth", "1", repo_url, tmpdir], capture_output=True)
        
        # Find code files
        files = []
        for ext in ["*.rs", "*.py", "*.js", "*.ts", "*.sol"]:
            files.extend(Path(tmpdir).rglob(ext))
        
        return {
            "repo": repo_url,
            "files_found": len(files),
            "sample_files": [str(f.relative_to(tmpdir)) for f in files[:5]]
        }
    
    def read_code(self, filepath: str, max_chars=4000):
        """Read code file for analysis"""
        try:
            with open(filepath, 'r', errors='ignore') as f:
                return f.read(max_chars)
        except Exception as e:
            return f"Error reading {filepath}: {e}"
    
    def write_patch(self, filepath: str, content: str):
        """Write security patch to file"""
        try:
            with open(filepath, 'w') as f:
                f.write(content)
            return f"Patch written to {filepath}"
        except Exception as e:
            return f"Error: {e}"

class OpenClawGateway:
    """
    OpenClaw-style Gateway with Pi Swarm security specialization
    Handles: status, audit, scan, task, agent commands
    """
    
    def __init__(self):
        self.tools = PiSwarmTools()
    
    def ask_ai(self, prompt: str, context="") -> str:
        """Connect to Ollama - the brain"""
        full_prompt = f"{context}\n\n{prompt}" if context else prompt
        
        try:
            data = json.dumps({
                "model": MODEL,
                "prompt": full_prompt,
                "stream": False
            }).encode()
            
            req = urllib.request.Request(
                OLLAMA_URL, data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode())
                return result.get("response", "")
        except Exception as e:
            return f"AI Error: {e}"
    
    def run(self, command: str, args: list = None):
        """Route commands like OpenClaw does"""
        args = args or []
        
        if command == "status":
            return self._cmd_status()
        elif command == "audit" and args:
            return self._cmd_audit(args[0])
        elif command == "scan" and args:
            return self._cmd_scan(args[0])
        elif command == "task" and args:
            return self._cmd_task(" ".join(args))
        elif command == "agent" and args:
            return self._cmd_agent(" ".join(args))
        elif command == "help":
            return self._show_help()
        else:
            return "Unknown command. Use: pi help"
    
    def _cmd_status(self):
        """Check system status like 'openclaw status'"""
        try:
            test = self.ask_ai("Say 'Pi Swarm online'")
            online = "online" in test.lower()
        except:
            online = False
        
        return f"""🛡️ Pi-Claw Gateway (Enhanced OpenClaw)
├─ AI Core: {'🟢 Qwen Connected' if online else '🔴 Disconnected'}
├─ Security Tools: 🟢 Loaded
│  ├─ scan_target
│  ├─ audit_repo
│  ├─ read_code
│  └─ write_patch
└─ Workspace: {WORKSPACE}
"""
    
    def _cmd_audit(self, target: str):
        """Security audit - Pi Swarm specialization"""
        print(f"🔍 Auditing: {target}")
        
        if target.startswith("http"):
            # Repo audit
            info = self.tools.audit_repo(target)
            context = f"Analyzing repo: {info['repo']}\nFiles: {info['files_found']}\nSample: {info['sample_files']}"
        else:
            # File/directory audit
            code = self.tools.read_code(target)
            context = f"Analyzing code:\n{code[:2000]}"
        
        prompt = f"Security audit report:\n{context}\n\nIdentify vulnerabilities and suggest fixes:"
        return self.ask_ai(prompt, "You are a security auditor.")
    
    def _cmd_scan(self, target: str):
        """Network scan with AI analysis"""
        print(f"📡 Scanning: {target}...")
        scan_result = self.tools.scan_target(target)
        
        prompt = f"Nmap scan results:\n{scan_result}\n\nAnalyze for security risks:"
        return self.ask_ai(prompt, "You are a network security analyst.")
    
    def _cmd_task(self, description: str):
        """Autonomous task like 'openclaw agent --task ...'"""
        print(f"🚀 Task: {description}")
        print("🧠 Planning...")
        
        plan = self.ask_ai(
            f"Task: {description}\nPlan step by step how to complete this using security tools.",
            "You are Pi Swarm, an autonomous security agent."
        )
        
        return f"Plan:\n{plan}\n\n[Use 'pi audit' or 'pi scan' to execute]"
    
    def _cmd_agent(self, message: str):
        """Direct AI conversation like 'openclaw agent --message ...'"""
        return self.ask_ai(
            message,
            "You are Pi Swarm, a sovereign AI security assistant. Built on OpenClaw architecture."
        )
    
    def _show_help(self):
        return """🛡️ Pi-Claw - Enhanced OpenClaw for Security

Usage: pi <command> [args]

Commands:
  status              Check AI connection and tools
  audit <target>      Audit file/repo (file path or GitHub URL)
  scan <target>       Network scan + AI analysis
  task <description>  Plan autonomous security task
  agent <message>     Direct chat with security AI
  help                Show this help

Examples:
  pi status
  pi audit ./smart_contract.sol
  pi audit https://github.com/user/repo
  pi scan 192.168.1.1
  pi task "Find reentrancy vulnerabilities in current directory"
"""

def main():
    if len(sys.argv) < 2:
        print("Pi-Claw Gateway")
        print("Run: pi help")
        return
    
    gateway = OpenClawGateway()
    result = gateway.run(sys.argv[1], sys.argv[2:])
    print(result)

if __name__ == "__main__":
    main()
