"""
🎯 منسق السرب (Swarm Orchestrator)
إدارة التواصل والتنسيق بين الوكلاء

مستوحى من Multi-Agent System Architecture في Decepticon
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .core import BaseAgent, AgentMessage, SwarmReplay, AgentState
    from .agents import ReconnaissanceAgent, AnalysisAgent, PlannerAgent, ReporterAgent
    from .osint_agent import OSINTScraperAgent
except ImportError:
    from core import BaseAgent, AgentMessage, SwarmReplay, AgentState
    from agents import ReconnaissanceAgent, AnalysisAgent, PlannerAgent, ReporterAgent
    from osint_agent import OSINTScraperAgent

from typing import Dict, List, Optional
from datetime import datetime
import json

class SwarmOrchestrator:
    """
    المنسق المركزي للسرب
    - إدارة سجل رسائل الوكلاء (Message Bus)
    - توجيه الرسائل بين الوكلاء
    - مراقبة حالة السرب
    - حفظ الجلسات (Replay)
    """
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: List[AgentMessage] = []
        self.replay = SwarmReplay()
        self.running = False
        self.stats = {
            "messages_processed": 0,
            "sessions_completed": 0,
            "alerts_triggered": 0
        }
        
        # تسجيل الوكلاء المتاحين
        self.register_default_agents()
    
    def register_default_agents(self):
        """تسجيل الوكلاء الافتراضيين"""
        self.register_agent(ReconnaissanceAgent())
        self.register_agent(AnalysisAgent())
        self.register_agent(PlannerAgent())
        self.register_agent(ReporterAgent())
        self.register_agent(OSINTScraperAgent())  # 🕷️ الوكيل الجديد
        print(f"✅ تم تسجيل {len(self.agents)} وكلاء في السرب")
    
    def register_agent(self, agent: BaseAgent):
        """تسجيل وكيل جديد في السرب"""
        self.agents[agent.name] = agent
        print(f"  └─ 🤖 {agent.name} ({agent.role})")
    
    def broadcast(self, message: AgentMessage, exclude: Optional[str] = None):
        """إرسال رسالة لجميع الوكلاء"""
        for name, agent in self.agents.items():
            if name != exclude:
                agent.inbox.append(message)
                self.replay.log_event("message_sent", {
                    "from": message.sender,
                    "to": name,
                    "type": message.message_type,
                    "content": message.content
                })
    
    def process_messages(self):
        """معالجة جميع الرسائل في صناديق ورود الوكلاء"""
        processed = 0
        
        for agent_name, agent in self.agents.items():
            while agent.inbox:
                message = agent.inbox.pop(0)
                response = agent.process_message(message)
                processed += 1
                self.stats["messages_processed"] += 1
                
                # معالجة الردود
                if response:
                    if response.recipient == "broadcast":
                        self.broadcast(response, exclude=agent_name)
                    else:
                        # إرسال لوكيل محدد
                        if response.recipient in self.agents:
                            self.agents[response.recipient].inbox.append(response)
                    
                    # تسجيل التنبيهات
                    if response.message_type == "alert":
                        self.stats["alerts_triggered"] += 1
                        print(f"\n🚨 تنبيه أمني من {response.sender}:")
                        print(f"   المستوى: {response.content.get('level', 'UNKNOWN')}")
                        print(f"   الرسالة: {response.content.get('message', 'N/A')}")
                        print(f"   التوصية: {response.content.get('recommendation', 'N/A')}\n")
        
        return processed
    
    def start_mission(self, mission_name: str, target: str):
        """بدء مهمة جديدة"""
        print(f"\n{'='*60}")
        print(f"🚀 بدء المهمة: {mission_name}")
        print(f"🎯 الهدف: {target}")
        print(f"⏰ الوقت: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # بدء جلسة Replay
        self.replay.start_session()
        self.replay.log_event("mission_started", {
            "name": mission_name,
            "target": target
        })
        
        # إنشاء مهمة التخطيط
        planner = self.agents.get("Planner")
        if planner:
            start_mission_msg = AgentMessage(
                sender="Orchestrator",
                recipient="Planner",
                message_type="task",
                content={
                    "task_type": "start_mission",
                    "name": mission_name,
                    "target": target,
                    "timestamp": datetime.now().isoformat()
                }
            )
            planner.inbox.append(start_mission_msg)
        
        # معالجة الرسائل حتى تنتهي المهمة
        self.running = True
        iterations = 0
        max_iterations = 50  # منع الحلقة اللانهائية
        
        while self.running and iterations < max_iterations:
            processed = self.process_messages()
            iterations += 1
            
            # التحقق من انتهاء المهمة
            if processed == 0 and iterations > 5:
                self.running = False
            
            # عرض حالة بسيطة
            if iterations % 5 == 0:
                print(f"  ⏳ المعالجة... (iteration {iterations})")
        
        # إنهاء الجلسة
        self.stats["sessions_completed"] += 1
        print(f"\n✅ اكتملت المهمة في {iterations} تكرارات")
        print(f"📊 رسائل تمت معالجتها: {self.stats['messages_processed']}")
        print(f"🚨 تنبيهات: {self.stats['alerts_triggered']}")
        
        # حفظ الجلسة
        log_file = self.replay.save_session()
        
        # إنشاء تقرير
        self.generate_mission_report(mission_name, log_file)
        
        return log_file
    
    def generate_mission_report(self, mission_name: str, log_file: str):
        """إنشاء تقرير المهمة"""
        reporter = self.agents.get("Reporter")
        if reporter:
            report_msg = AgentMessage(
                sender="Orchestrator",
                recipient="Reporter",
                message_type="task",
                content={
                    "task_type": "generate_report",
                    "report_id": f"RPT-{self.stats['sessions_completed']:03d}",
                    "mission_name": mission_name,
                    "timestamp": datetime.now().isoformat()
                }
            )
            reporter.inbox.append(report_msg)
            # معالجة رسالة التقرير
            self.process_messages()
    
    def get_status(self) -> Dict:
        """الحالة الحالية للسرب"""
        return {
            "agents": {
                name: {
                    "role": agent.role,
                    "status": agent.state.status,
                    "completed_tasks": agent.state.completed_tasks
                }
                for name, agent in self.agents.items()
            },
            "stats": self.stats,
            "running": self.running
        }
    
    def export_session(self, session_id: str) -> Dict:
        """تصدير الجلسة للمشاركة المجتمعية"""
        return self.replay.export_for_sharing()
