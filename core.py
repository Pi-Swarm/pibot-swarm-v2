"""
🥧 Pi bot Swarm 2.0 - Inspired by Decepticon Architecture
الدفاع السيبراني عبر أسراب الوكلاء المتعددة

بنية مستوحاة من Decepticon ولكن للأغراض الدفاعية (Blue Team)
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import json
import uuid

# --- أنواع البيانات ---

@dataclass
class AgentMessage:
    """رسالة للتواصل بين الوكلاء"""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    sender: str = ""
    recipient: str = ""  # "broadcast" للإرسال للجميع
    message_type: str = ""  # task, result, request, alert
    content: Dict[str, Any] = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    priority: str = "normal"  # low, normal, high, critical

@dataclass
class AgentState:
    """حالة الوكيل"""
    name: str
    role: str
    status: str = "idle"  # idle, working, waiting, error
    current_task: Optional[str] = None
    completed_tasks: int = 0
    last_active: str = field(default_factory=lambda: datetime.now().isoformat())

# --- الفئة الأساسية للوكلاء ---

class BaseAgent(ABC):
    """الفئة الأساسية لجميع وكلاء السرب"""
    
    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.state = AgentState(name=name, role=role)
        self.inbox: List[AgentMessage] = []
        self.memory: Dict[str, Any] = {}
    
    @abstractmethod
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        """معالجة الرسالة الواردة وإرسال رد إذا لزم الأمر"""
        pass
    
    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """إرجاع قائمة بالقدرات التي يمتلكها الوكيل"""
        pass
    
    def send_message(self, recipient: str, msg_type: str, content: Dict) -> AgentMessage:
        """إنشاء رسالة وإرسالها"""
        msg = AgentMessage(
            sender=self.name,
            recipient=recipient,
            message_type=msg_type,
            content=content
        )
        return msg
    
    def update_status(self, status: str, task: Optional[str] = None):
        """تحديث حالة الوكيل"""
        self.state.status = status
        self.state.current_task = task
        self.state.last_active = datetime.now().isoformat()
        if status == "working" and task:
            print(f"🔄 [{self.name}] يعمل على: {task}")
        elif status == "idle":
            self.state.completed_tasks += 1
            print(f"✅ [{self.name}] أكمل المهمة. إجمالي المهام: {self.state.completed_tasks}")

# --- سجل العمليات (Replay System) ---

class SwarmReplay:
    """نظام حفظ وإعادة تشغيل الجلسات"""
    
    def __init__(self, log_path: str = "swarm_logs/"):
        self.log_path = log_path
        self.session_id: str = ""
        self.events: List[Dict] = []
    
    def start_session(self):
        """بدء جلسة جديدة"""
        self.session_id = str(uuid.uuid4())
        self.events = []
        print(f"🎬 بدأ جلسة جديدة: {self.session_id}")
    
    def log_event(self, event_type: str, data: Dict):
        """تسجيل حدث في الجلسة"""
        event = {
            "timestamp": datetime.now().isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "data": data
        }
        self.events.append(event)
    
    def save_session(self):
        """حفظ الجلسة في ملف JSON"""
        import os
        os.makedirs(self.log_path, exist_ok=True)
        filename = f"{self.log_path}session_{self.session_id[:8]}.json"
        with open(filename, 'w') as f:
            json.dump(self.events, f, indent=2)
        print(f"💾 حُفظت الجلسة في: {filename}")
        return filename
    
    def load_session(self, session_id: str) -> List[Dict]:
        """تحميل جلسة سابقة"""
        filename = f"{self.log_path}session_{session_id[:8]}.json"
        with open(filename, 'r') as f:
            return json.load(f)
    
    def export_for_sharing(self) -> Dict:
        """تصدير الجلسة للمشاركة المجتمعية"""
        return {
            "session_id": self.session_id,
            "total_events": len(self.events),
            "events": self.events,
            "exported_at": datetime.now().isoformat()
        }
