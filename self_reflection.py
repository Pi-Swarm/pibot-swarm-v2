"""
🧠 محرك التصحيح الذاتي (Self-Reflection Engine)
مستوحى من Reflexion Architecture لضمان عدم تكرار الأخطاء التقنية
"""

import json
from datetime import datetime
from typing import Dict, List, Any

class SelfReflection:
    def __init__(self, log_path: str = "error_reflection.json"):
        self.log_path = log_path
        self.lessons_learned = self.load_lessons()

    def reflect_on_failure(self, task_name: str, error_msg: str, attempt: int):
        """تحليل الفشل واستخراج الدروس"""
        reflection = {
            "timestamp": datetime.now().isoformat(),
            "task": task_name,
            "error": error_msg,
            "attempt": attempt,
            "root_cause": self._analyze_root_cause(error_msg),
            "prevention_plan": self._generate_prevention(task_name)
        }
        self.lessons_learned.append(reflection)
        self.save_lessons()
        print(f"🧠 [Reflection] Lesson learned for task: {task_name}")

    def _analyze_root_cause(self, error: str) -> str:
        if "404" in error: return "Premature confirmation before data sync"
        if "Permission denied" in error: return "Token scope insufficient"
        if "SyntaxError" in error: return "Non-ASCII character in code (Arabic comma?)"
        return "Unknown technical friction"

    def _generate_prevention(self, task: str) -> str:
        return f"Verify success via API/curl before reporting success for {task}."

    def save_lessons(self):
        with open(self.log_path, "w", encoding="utf-8") as f:
            json.dump(self.lessons_learned, f, indent=2, ensure_ascii=False)

    def load_lessons(self) -> List:
        try:
            with open(self.log_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return []

if __name__ == "__main__":
    engine = SelfReflection()
    # تجربة محاكاة فشل قديم
    engine.reflect_on_failure("GitHub Push", "404 Not Found", 1)
    print("✅ تم تسجيل الدرس في الذاكرة الدائمة.")
