"""
📡 ناقل الأحداث (Event Bus) - مستوحى من فلسفة Redamon
وظيفة الملف: نقل الرسائل والنبضات الأمنية بين الوكلاء في وقت حقيقي.
"""

import json
import os
from datetime import datetime

class EventBus:
    def __init__(self, bus_path="/home/faycel1/.openclaw/workspace/pibot/swarm_v2/swarm_pulse.jsonl"):
        self.bus_path = bus_path

    def publish(self, agent_name, event_type, message):
        """نشر حدث جديد في الناقل"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "agent": agent_name,
            "type": event_type,
            "message": message
        }
        with open(self.bus_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def get_recent_events(self, limit=5):
        """جلب آخر الأحداث للمراقبة اللحظية"""
        if not os.path.exists(self.bus_path):
            return []
        
        with open(self.bus_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            recent = [json.loads(line) for line in lines[-limit:]]
            return recent[::-1] # ترتيب من الأحدث للأقدم

if __name__ == "__main__":
    bus = EventBus()
    bus.publish("Pi-Core", "PULSE", "Event Bus Initialized Successfully.")
    print("📡 Event Bus is live and pulsing.")
