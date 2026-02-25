"""AI Provider Module"""
import json
import urllib.request

class PiClawProvider:
    def __init__(self, model="qwen2.5:1.5b"):
        self.model = model
        self.url = "http://localhost:11434/api/generate"
    
    def ask_ai(self, prompt, context=""):
        full = f"{context}\n{prompt}" if context else prompt
        try:
            data = json.dumps({
                "model": self.model,
                "prompt": full,
                "stream": False
            }).encode()
            req = urllib.request.Request(
                self.url, data=data,
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=120) as resp:
                result = json.loads(resp.read().decode())
                return result.get("response", "No response")
        except Exception as e:
            return f"Error: {e}"
