"""
🥧 Pi bot Swarm 2.0 - Main Entry Point
نقطة الدخول الرئيسية لتشغيل السرب

استخدام:
    python -m swarm_v2.main          (مفضل)
    أو
    cd swarm_v2 && python main.py    (بديل)

أو:
    from swarm_v2 import SwarmOrchestrator
    orch = SwarmOrchestrator()
    orch.start_mission("Network Scan", "192.168.122.0/24")
"""

import sys
import os

# إضافة المسار الحالي للـ sys.path لدعم الاستيراد
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    # محاولة الاستيراد النسبي (عند التشغيل كـ module)
    from .orchestrator import SwarmOrchestrator
except ImportError:
    # فallback للاستيراد المطلق (عند التشغيل المباشر)
    from orchestrator import SwarmOrchestrator

import json

def print_banner():
    """عرض الشعار الترحيبي"""
    banner = """
    ╔═══════════════════════════════════════════════════════╗
    ║                                                       ║
    ║           🥧 Pi bot Swarm 2.0 🥧                      ║
    ║                                                       ║
    ║    Autonomous Blue Team Security Operations          ║
    ║    Inspired by Decepticon Architecture               ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """
    print(banner)

def run_demo_mission():
    """تشغيل مهمة تجريبية"""
    print_banner()
    
    # إنشاء المنسق
    print("\n🔧 تهيئة السرب...\n")
    orchestrator = SwarmOrchestrator()
    
    # عرض حالة الوكلاء المسجلين
    print("\n📋 حالة السرب الأولية:")
    status = orchestrator.get_status()
    for agent_name, agent_info in status["agents"].items():
        print(f"   ├─ {agent_name}: {agent_info['role']} [{agent_info['status']}]")
    
    # بدء المهمة التجريبية
    print("\n")
    log_file = orchestrator.start_mission(
        mission_name="فحص الشبكة المحلية",
        target="192.168.122.0/24"
    )
    
    # عرض الحالة النهائية
    print("\n📊 الحالة النهائية:")
    final_status = orchestrator.get_status()
    print(f"   ├─ الرسائل المعالجة: {final_status['stats']['messages_processed']}")
    print(f"   ├─ التنبيهات: {final_status['stats']['alerts_triggered']}")
    print(f"   └ـ الجلسات المكتملة: {final_status['stats']['sessions_completed']}")
    
    print(f"\n💾 سجل الجلسة: {log_file}")
    
    return orchestrator

def run_interactive():
    """وضع تفاعلي مع المستخدم"""
    print_banner()
    
    orchestrator = SwarmOrchestrator()
    
    while True:
        print("\n" + "="*50)
        print("🎯 القائمة الرئيسية:")
        print("  1. بدء مهمة فحص شبكة جديدة")
        print("  2. عرض حالة السرب")
        print("  3. عرض سجلات الجلسات السابقة")
        print("  4. تصدير جلسة للمشاركة")
        print("  5. خروج")
        print("="*50)
        
        choice = input("\nاختر خياراً (1-5): ").strip()
        
        if choice == "1":
            target = input("أدخل هدف الشبكة (مثال: 192.168.122.0/24): ").strip()
            mission_name = input("أدخل اسم المهمة: ").strip() or "مهمة مخصصة"
            orchestrator.start_mission(mission_name, target)
        
        elif choice == "2":
            status = orchestrator.get_status()
            print("\n📊 حالة السرب:")
            for agent_name, agent_info in status["agents"].items():
                print(f"   ├─ {agent_name}: {agent_info['status']} - مهام مكتملة: {agent_info['completed_tasks']}")
            print(f"   └إجمالي الرسائل: {status['stats']['messages_processed']}")
        
        elif choice == "3":
            print("\n⚠️ وظيفة عرض السجلات قيد التطوير")
        
        elif choice == "4":
            session_id = input("أدخل معرف الجلسة: ").strip()
            if session_id:
                exported = orchestrator.export_session(session_id)
                print(json.dumps(exported, indent=2))
        
        elif choice == "5":
            print("\n👋 وداعاً! في أمان الله")
            break
        
        else:
            print("\n❌ خيار غير صحيح، حاول مرة أخرى")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive()
    else:
        run_demo_mission()
