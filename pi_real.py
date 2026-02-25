#!/usr/bin/env python3
"""Pi Swarm - Real Implementation. Connects to Ollama and analyzes files."""

import sys
import os
import json
import urllib.request

def ask_ollama(prompt: str) -> str:
    """Send prompt to local Ollama and return real response."""
    url = "http://localhost:11434/api/generate"
    data = json.dumps({
        "model": "qwen2.5:1.5b",
        "prompt": prompt,
        "stream": False
    }).encode()
    
    req = urllib.request.Request(url, data=data, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            result = json.loads(resp.read().decode())
            return result.get("response", "No response")
    except Exception as e:
        return f"ERROR: {e}"

def analyze_file(filepath: str) -> str:
    """Read file and send to Qwen for analysis."""
    if not os.path.exists(filepath):
        return f"File not found: {filepath}"
    
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read()[:3000]  # First 3000 chars
    
    prompt = f"""You are a security auditor. Analyze this code for vulnerabilities.
Be concise. List any security issues found.

CODE:
{content}
"""
    return ask_ollama(prompt)

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pi_real.py <command>")
        print("  status   - Check if Ollama is running")
        print("  analyze <file> - Analyze a file with AI")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "status":
        print("Checking Ollama...")
        resp = ask_ollama("Say 'Pi Swarm is ready' if you can hear me.")
        print(f"Ollama response: {resp}")
    
    elif cmd == "analyze" and len(sys.argv) > 2:
        filepath = sys.argv[2]
        print(f"Analyzing: {filepath}")
        print("-" * 50)
        result = analyze_file(filepath)
        print(result)
    
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
