"""
🧠 Qwen2.5:1.5B Integration Module
ربط نموذج Qwen2.5:1.5B مع سرب Pi bot 2.0

بدون مكتبات خارجية - يستخدم urllib القياسي

الاستخدام:
    from llm_connector import QwenConnector
    
    connector = QwenConnector()
    response = connector.generate("مرحباً، من أنت؟")
"""

import urllib.request
import urllib.error
import json
from typing import Dict, List, Optional
from datetime import datetime

# --- إعدادات Ollama ---

OLLAMA_API = "http://localhost:11434"
MODEL_NAME = "qwen2.5:1.5b"

# إعدادات التحسين للنموذج الصغير
GENERATION_CONFIG = {
    "temperature": 0.3,
    "top_p": 0.9,
    "num_predict": 512,
    "num_ctx": 4096,
    "stop": ["</s>", "User:", "\n\n"]
}

class QwenConnector:
    """
    🤖 موصل Qwen2.5:1.5B للسرب
    
    ملاحظات مهمة للنموذج الصغير:
    1. استخدم Prompts واضحة ومباشرة
    2. تجنب الأسئلة المفتوحة المعقدة
    3. قسّم المهام الكبيرة لمهام صغيرة
    """
    
    def __init__(self, model: str = MODEL_NAME, api_url: str = OLLAMA_API):
        self.model = model
        self.api_url = api_url
        self.base_url = f"{api_url}/api"
        self.conversation_history: List[Dict] = []
        self.system_prompt = self._default_system_prompt()
        
        # التحقق من اتصال Ollama
        if not self._check_connection():
            print(f"⚠️ تحذير: لا يمكن الاتصال بـ Ollama على {api_url}")
            print("  تأكد من تشغيل: ollama serve")
    
    def _check_connection(self) -> bool:
        """التحقق من أن Ollama يعمل"""
        try:
            req = urllib.request.Request(f"{self.api_url}/api/tags", method='GET')
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except:
            return False
    
    def _default_system_prompt(self) -> str:
        """System Prompt افتراضي لـ Pi bot"""
        return """أنت Pi bot 🥧، مساعد أمني ذكي متخصص في الفحص الدفاعي للشبكات.

المبادئ:
1. كن دقيقاً في التحليل
2. لا تستغل الثغرات، فقط اكتشفها
3. قدّم توصيات قابلة للتنفيذ
4. اعمل ضمن النطاق المصرح به فقط

التنسيق:
- إجابات واضحة ومباشرة
- استخدم الجداول عند الحاجة
- رقم التوصيات بالأولوية"""
    
    def set_system_prompt(self, prompt: str):
        """تغيير الـ System Prompt"""
        self.system_prompt = prompt
        print(f"✅ تم تحديث System Prompt")
    
    def generate(
        self, 
        prompt: str, 
        context: Optional[Dict] = None,
        use_history: bool = False,
        **kwargs
    ) -> str:
        """
        توليد رد من النموذج
        
        Args:
            prompt: سؤال المستخدم
            context: سياق إضافي
            use_history: استخدام سجل المحادثة
            **kwargs: إعدادات إضافية
        
        Returns:
            str: رد النموذج
        """
        # دمج السياق
        if context:
            full_prompt = self._format_with_context(prompt, context)
        else:
            full_prompt = prompt
        
        # بناء الرسائل
        messages = [{"role": "system", "content": self.system_prompt}]
        
        if use_history:
            messages.extend(self.conversation_history[-10:])
        
        messages.append({"role": "user", "content": full_prompt})
        
        # إعداد الطلب
        config = {**GENERATION_CONFIG, **kwargs}
        
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": config
        }
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(
                f"{self.base_url}/chat",
                data=data,
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            
            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode('utf-8'))
                assistant_message = result.get("message", {}).get("content", "لا يوجد رد")
                
                # حفظ في السجل
                if use_history:
                    self.conversation_history.append({"role": "user", "content": full_prompt})
                    self.conversation_history.append({"role": "assistant", "content": assistant_message})
                
                return assistant_message
                
        except urllib.error.URLError as e:
            if "refused" in str(e).lower():
                return "❌ لا يمكن الاتصال بـ Ollama - تأكد من تشغيل: ollama serve"
            return f"❌ خطأ في الاتصال: {str(e)}"
        except Exception as e:
            return f"❌ خطأ في النموذج: {str(e)}"
    
    def _format_with_context(self, prompt: str, context: Dict) -> str:
        """تنسيق السؤال مع السياق"""
        context_str = json.dumps(context, indent=2, ensure_ascii=False)
        return f"""السياق:
{context_str}

السؤال:
{prompt}
"""
    
    def analyze_ports(self, open_ports: List[int], target: str) -> str:
        """تحليل المنافذ المفتوحة"""
        prompt = f"""لدينا {len(open_ports)} منافذ مفتوحة على {target}:
{open_ports}

قم بـ:
1. تحديد الخطر لكل منفذ (HIGH/MEDIUM/LOW)
2. ذكر الخدمة المتوقعة
3. اقتراح إجراء لكل منفذ

الجدول:
| المنفذ | الخدمة | الخطر | الإجراء |
"""
        return self.generate(prompt)
    
    def generate_report_summary(self, scan_data: Dict) -> str:
        """توليد ملخص تنفيذي"""
        prompt = f"""بيانات الفحص:
{json.dumps(scan_data, indent=2, ensure_ascii=False)}

اكتب ملخصاً تنفيذياً (3-5 أسطر) يشمل:
1. مستوى الخطر العام
2. أهم 3 اكتشافات
3. الإجراء العاجل المطلوب
"""
        return self.generate(prompt)
    
    def clear_history(self):
        """مسح سجل المحادثة"""
        self.conversation_history = []
        print("✅ تم مسح سجل المحادثة")

# --- دوال مساعدة ---

def generate_response(prompt: str, **kwargs) -> str:
    """دالة سريعة"""
    return QwenConnector().generate(prompt, **kwargs)

# --- التشغيل المباشر ---

if __name__ == "__main__":
    print("🧠 اختبار Qwen2.5:1.5B مع Pi bot Swarm\n")
    
    connector = QwenConnector()
    
    # اختبار الاتصال
    print("=" * 50)
    if connector._check_connection():
        print("✅ Ollama متصل - النموذج:", connector.model)
    else:
        print("❌ Ollama غير متصل")
        print("\n💡 للتشغيل:")
        print("   1. تأكد من تثبيت Ollama")
        print("   2. شغّل: ollama serve")
        print("   3. تأكد من النموذج: ollama pull qwen2.5:1.5b")
        print("   4. أعد الاختبار")
        exit(1)
    
    # اختبار 1
    print("\n" + "=" * 50)
    print("📝 الاختبار 1: اتصال بسيط")
    print("=" * 50)
    response = connector.generate("مرحباً، من أنت؟")
    print(response)
    
    # اختبار 2
    print("\n" + "=" * 50)
    print("📝 الاختبار 2: تحليل منافذ")
    print("=" * 50)
    response = connector.analyze_ports([22, 445, 80], "192.168.122.1")
    print(response)
    
    # اختبار 3
    print("\n" + "=" * 50)
    print("✅ اكتمل الاختبار!")
    print("=" * 50)
