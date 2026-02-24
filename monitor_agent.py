"""
📊 وكيل المراقبة (Monitor Agent) - مستوحى من Rowboat
وظيفة الوكيل: مراقبة أداء السرب، ضمان الأمان، وتقديم تقارير الحالة.
"""

import json
import os
from datetime import datetime

class MonitorAgent:
    def __init__(self, workspace_path="/home/faycel1/.openclaw/workspace/pibot/swarm_v2"):
        self.name = "Pi-Monitor"
        self.workspace = workspace_path
        self.stats_file = os.path.join(self.workspace, "swarm_stats.json")
        self.init_stats()

    def init_stats(self):
        if not os.path.exists(self.stats_file):
            initial_data = {
                "start_date": datetime.now().isoformat(),
                "total_tasks": 0,
                "security_alerts": 0,
                "skills_deployed": 0,
                "active_sessions": 0,
                "last_audit_status": "Clean"
            }
            self.save_stats(initial_data)

    def log_event(self, event_type, details):
        """تسجيل حدث جديد في السرب (Task, Alert, Skill)"""
        stats = self.load_stats()
        timestamp = datetime.now().isoformat()
        
        if event_type == "task":
            stats["total_tasks"] += 1
        elif event_type == "security_alert":
            stats["security_alerts"] += 1
            print(f"🚨 [SECURITY ALERT] {timestamp}: {details}")
        elif event_type == "skill_use":
            stats["skills_deployed"] += 1
            
        self.save_stats(stats)
        self.generate_sovereign_report(event_type, details)

    def generate_sovereign_report(self, event, details):
        """توليد تقرير "سيادي" حي يحتوي على بث للأحداث"""
        from event_bus import EventBus
        bus = EventBus()
        recent_events = bus.get_recent_events(5)
        
        report_path = os.path.join(self.workspace, "PI_STATUS_REPORT.md")
        stats = self.load_stats()
        
        live_stream = ""
        for ev in recent_events:
            live_stream += f"- `[{ev['timestamp'][11:19]}]` **{ev['agent']}**: {ev['message']}\n"

        report_content = f"""# 🥧 Sovereign Status Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}
## 📊 Swarm Metrics
- **Total Tasks Executed:** {stats['total_tasks']}
- **Security Health:** {"✅ Clean" if stats['security_alerts'] == 0 else "⚠️ Alerts Detected"}
- **Skills in Use:** {stats['skills_deployed']}

## 🔴 Live Event Stream (Redamon Style)
{live_stream}

---
*Pi Monitor: Observing the Swarm, Securing the Vision.*
"""
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)

    def load_stats(self):
        with open(self.stats_file, "r") as f:
            return json.load(f)

    def save_stats(self, data):
        with open(self.stats_file, "w") as f:
            json.dump(data, f, indent=2)

if __name__ == "__main__":
    monitor = MonitorAgent()
    monitor.log_event("task", "Initialized Monitor Agent (Rowboat Strategy)")
    print("✅ وكيل المراقبة قيد العمل الآن.")
