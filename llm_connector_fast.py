"""
🧠 Qwen2.5:0.5B - النسخة السريعة جداً
نموذج خفيف للمهام البسيطة والسريعة

الاستخدام:
    from llm_connector_fast import QwenConnector
    connector = QwenConnector()  # يستخدم 0.5B تلقائياً
"""

import urllib.request
import urllib.error
import json
from typing import Dict, List, Optional

# --- إعدادات Ollama - نموذج أسرع ---

OLLAMA_API = "http://localhost:11434"
MODEL_NAME = "qwen2.5:0.5b"  # 🚀 أسرع 3x من 1.5B

# إعدادات مُحسّنة للسرعة
GENERATION_CONFIG = {
    "temperature": 0.5,      # أعلى قليلاً للإبداع
    "top_p": 0.95,
    "num_predict": 256,      # ردود أقصر = أسرع
    "num_ctx": 2048,         # سياق أقصر = أسرع
    "num_thread": 4,         # عدد الأنوية (عدّل حسب CPU)
    "stop": ["</s>", "\n\n"]
}

class QwenConnector:
    """موصل سريع للنموذج الصغير"""
    
    def __init__(self, model: str = MODEL_NAME, api_url: str = OLLAMA_API):
        self.model = model
        self.api_url = api_url
        self.base_url = f"{api_url}/api"
        print(f"🚀 QwenFast: {model} ({MODEL_NAME})")
    
    def _check_connection(self) -> bool:
        try:
            req = urllib.request.Request(f"{self.api_url}/api/tags")
            with urllib.request.urlopen(req, timeout=3) as response:
                return response.status == 200
        except:
            return False
    
    def generate(self, prompt: str, context: Optional[Dict] = None, timeout_sec: int = 30) -> str:
        """
        توليد رد سريع
        
        Args:
            prompt: السؤال
            context: سياق إضافي
            timeout_sec: مهلة بالثواني (أقصر = أسرع فشلاً)
        """
        if context:
            full_prompt = f"السياق:\n{json.dumps(context, ensure_ascii=False)}\n\nالسؤال: {prompt}"
        else:
            full_prompt = prompt
        
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "أنت Pi bot 🥧، مساعد أمني للشبكات."},
                {"role": "user", "content": full_prompt}
            ],
            "stream": False,
            "options": GENERATION_CONFIG
        }
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                f"{self.base_url}/chat",
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=timeout_sec) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get("message", {}).get("content", "لا يوجد رد")
                
        except urllib.error.URLError as e:
            if "timed out" in str(e).lower():
                return f"⏱️ مهلة قصيرة ({timeout_sec}ث) - جرّب نموذجاً أصغر أو زد المهلة"
            return f"❌ خطأ: {str(e)}"
        except Exception as e:
            return f"❌ خطأ: {str(e)}"
    
    def analyze_ports_fast(self, ports: List[int]) -> str:
        """تحليل سريع للمنافذ - رد خلال 10-15 ثانية"""
        prompt = f"منافذ: {ports}. لكل منفذ: الخطر (HIGH/MED/LOW) + خدمة + توصية. جدول مختصر."
        return self.generate(prompt, timeout_sec=20)
    
    def quick_decision(self, scenario: str) -> str:
        """قرار سريع - 5-10 ثواني"""
        prompt = f"سيناريو: {scenario}. القرار: (توصية واحدة محددة)"
        return self.generate(prompt, timeout_sec=15)

# --- اختبار ---

if __name__ == "__main__":
    print("🚀 اختبار Qwen2.5:0.5B السريع\n")
    connector = QwenConnector()
    
    if not connector._check_connection():
        print("❌ Ollama غير متصل")
        exit(1)
    
    print("✅ متصل - اختبار التحليل السريع:")
    print("-" * 50)
    
    import time
    start = time.time()
    response = connector.analyze_ports_fast([22, 445, 80])
    elapsed = time.time() - start
    
    print(response)
    print(f"\n⏱️ الوقت: {elapsed:.1f} ثانية")
    print("✅ إذا كان < 20ث ← ممتاز!")
    print("⚠️ إذا كان > 30ث ← استخدم القوالب الجاهزة بدلاً من LLM")
