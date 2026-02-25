"""Security Agent Runner"""
import os
import subprocess
from pathlib import Path
from .provider import PiClawProvider

class AgentRunner:
    def __init__(self, task):
        self.task = task
        self.ai = PiClawProvider()
    
    def run(self):
        if "audit" in self.task.lower():
            return self._run_audit()
        elif "scan" in self.task.lower():
            return self._run_scan()
        else:
            return self.ai.ask_ai(self.task, "Security task:")
    
    def _run_audit(self):
        # Extract target from task
        words = self.task.split()
        target = None
        for w in words:
            if "." in w or "/" in w:
                target = w
                break
        
        if not target:
            return "No target specified"
        
        if target.startswith("http"):
            return self._audit_repo(target)
        else:
            return self._audit_file(target)
    
    def _audit_file(self, filepath):
        try:
            with open(filepath, 'r', errors='ignore') as f:
                content = f.read(4000)
        except Exception as e:
            return f"Error: {e}"
        
        prompt = f"Analyze this code for security vulnerabilities:\n{content}"
        return self.ai.ask_ai(prompt, "You are a security auditor.")
    
    def _audit_repo(self, url):
        import tempfile
        tmpdir = tempfile.mkdtemp()
        subprocess.run(["git", "clone", "--depth", "1", url, tmpdir], capture_output=True)
        
        files = list(Path(tmpdir).rglob("*.py")) + list(Path(tmpdir).rglob("*.rs"))
        if not files:
            return "No code files found"
        
        with open(files[0], 'r', errors='ignore') as f:
            content = f.read(3000)
        
        prompt = f"Repo: {url}\nFile: {files[0].name}\n\n{content}\n\nSecurity issues:"
        return self.ai.ask_ai(prompt, "Security auditor")
    
    def _run_scan(self):
        import re
        ip_match = re.search(r'(\d+\.\d+\.\d+\.\d+)', self.task)
        if not ip_match:
            return "No IP found"
        
        ip = ip_match.group(1)
        result = subprocess.run(["nmap", "-sV", ip], capture_output=True, text=True)
        
        output = result.stdout if result.returncode == 0 else result.stderr
        prompt = f"Nmap scan:\n{output[:2000]}\n\nAnalyze security risks:"
        return self.ai.ask_ai(prompt, "Network security analyst")
