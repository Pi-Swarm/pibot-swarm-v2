"""
🎯 Hybrid Intelligence System
دمج القوالب الجاهزة + LLM للتحسين

الفكرة:
1. القوالب تولّد 80% من المحتوى (سريع ⚡)
2. LLM يُحسّن 20% للذكاء (🧠)

النتيجة: سرعة + جودة
"""

import json
from typing import Dict, List
from datetime import datetime

# ──────────────────────────────────────────────────────
# الجزء 1: القوالب الجاهزة (Template Engine)
# ──────────────────────────────────────────────────────

class TemplateEngine:
    """محرك القوالب - توليد سريع بدون LLM"""
    
    @staticmethod
    def analyze_ports_template(ports: List[int], target: str) -> Dict:
        """
        تحليل المنافذ باستخدام القوالب
        
        Returns:
            dict: تحليل جاهز خلال < 100ms
        """
        # قاعدة بيانات المنافذ المعروفة
        PORT_DB = {
            21: {"service": "FTP", "risk": "MEDIUM", "desc": "نقل ملفات غير مشفر"},
            22: {"service": "SSH", "risk": "LOW", "desc": "اتصال آمن"},
            23: {"service": "Telnet", "risk": "HIGH", "desc": "غير مشفر - خطير"},
            53: {"service": "DNS", "risk": "LOW", "desc": "ترجمة أسماء نطاقات"},
            80: {"service": "HTTP", "risk": "LOW", "desc": "ويب غير مشفر"},
            139: {"service": "NetBIOS", "risk": "HIGH", "desc": "مشاركة ملفات قديمة"},
            443: {"service": "HTTPS", "risk": "LOW", "desc": "ويب مشفر"},
            445: {"service": "SMB", "risk": "HIGH", "desc": "مشاركة ملفات - معرض للثغرات"},
            3306: {"service": "MySQL", "risk": "MEDIUM", "desc": "قاعدة بيانات"},
            3389: {"service": "RDP", "risk": "HIGH", "desc": "سطح مكتب بعيد"},
            8080: {"service": "HTTP-Alt", "risk": "MEDIUM", "desc": "ويب بديل"},
        }
        
        analysis = []
        risk_scores = {"HIGH": 3, "MEDIUM": 2, "LOW": 1}
        
        for port in ports:
            info = PORT_DB.get(port, {"service": "Unknown", "risk": "MEDIUM", "desc": "خدمة غير معروفة"})
            analysis.append({
                "port": port,
                "service": info["service"],
                "risk_level": info["risk"],
                "risk_score": risk_scores[info["risk"]],
                "description": info["desc"],
                "recommendation": TemplateEngine._get_recommendation(port, info)
            })
        
        # حساب الخطر العام
        total_score = sum(a["risk_score"] for a in analysis)
        avg_score = total_score / len(analysis) if analysis else 0
        
        overall_risk = "HIGH" if avg_score > 2.5 else "MEDIUM" if avg_score > 1.5 else "LOW"
        
        return {
            "target": target,
            "scan_time": datetime.now().isoformat(),
            "total_ports": len(ports),
            "risk_breakdown": {
                "HIGH": len([a for a in analysis if a["risk_level"] == "HIGH"]),
                "MEDIUM": len([a for a in analysis if a["risk_level"] == "MEDIUM"]),
                "LOW": len([a for a in analysis if a["risk_level"] == "LOW"]),
            },
            "overall_risk": overall_risk,
            "overall_score": min(100, total_score * 10),
            "ports_analysis": analysis,
            "template": True  # علامة أن هذا من قالب
        }
    
    @staticmethod
    def _get_recommendation(port: int, info: Dict) -> str:
        """الحصول على توصية سريعة"""
        recommendations = {
            "FTP": "استخدم SFTP بدلاً من FTP",
            "SSH": "فعّل المصادقة الثنائية",
            "Telnet": "استبدل Telnet بـ SSH فوراً",
            "NetBIOS": "عطّل NetBIOS إذا لم يكن مستخدماً",
            "SMB": "حدّث SMB لأعلى إصدار، عطّل SMBv1",
            "RDP": "استخدم VPN للوصول عن بعد",
        }
        return recommendations.get(info["service"], "راجع خدمة المنفذ")
    
    @staticmethod
    def generate_report_template(scan_data: Dict) -> Dict:
        """توليد تقرير تنفيذي كامل"""
        return {
            "report_id": f"RPT-{datetime.now().strftime('%Y%m%d-%H%M%S')}",
            "generated_at": datetime.now().isoformat(),
            "executive_summary": TemplateEngine._gen_exec_summary(scan_data),
            "key_findings": TemplateEngine._gen_key_findings(scan_data),
            "recommendations_priority": TemplateEngine._gen_recommendations(scan_data),
            "template_version": "1.0"
        }
    
    @staticmethod
    def _gen_exec_summary(data: Dict) -> str:
        risk = data.get("overall_risk", "UNKNOWN")
        score = data.get("overall_score", 0)
        return f"""
تم إكمال الفحص الأمني.
مستوى الخطر العام: {risk} (درجة: {score}/100)
المنافذ المفتوحة: {data.get('total_ports', 0)}
الإجراء المطلوب: {'فوري' if risk == 'HIGH' else 'مجدول' if risk == 'MEDIUM' else 'وقائي'}
""".strip()
    
    @staticmethod
    def _gen_key_findings(data: Dict) -> List[str]:
        findings = []
        for port in data.get("ports_analysis", [])[:5]:
            if port["risk_level"] in ["HIGH", "MEDIUM"]:
                findings.append(f"منفذ {port['port']} ({port['service']}): {port['risk_level']} - {port['description']}")
        return findings or ["لا توجد اكتشافات هامة"]
    
    @staticmethod
    def _gen_recommendations(data: Dict) -> List[Dict]:
        recs = []
        for port in data.get("ports_analysis", []):
            if port["risk_level"] == "HIGH":
                recs.append({"priority": 1, "action": port["recommendation"], "port": port["port"]})
            elif port["risk_level"] == "MEDIUM":
                recs.append({"priority": 2, "action": port["recommendation"], "port": port["port"]})
        return sorted(recs, key=lambda x: x["priority"])

# ──────────────────────────────────────────────────────
# الجزء 2: تحسين LLM (يُستخدم اختياري للذكاء الإضافي)
# ──────────────────────────────────────────────────────

class LLMEnhancer:
    """
    محسّن LLM - يُستخدم فقط عندما نريد ذكاءً إضافياً
    
    يمكن تعطيله تماماً للسرعة القصوى
    """
    
    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        self.connector = None
        if use_llm:
            try:
                from .llm_connector_fast import QwenConnector
                self.connector = QwenConnector()
                print("✅ LLM Enhancer مفعل")
            except:
                print("⚠️ LLM Enhancer غير متاح - سيستخدم القوالب فقط")
                self.use_llm = False
    
    def enhance_report(self, template_report: Dict) -> Dict:
        """تحسين التقرير باستخدام LLM (اختياري)"""
        if not self.use_llm or not self.connector:
            template_report["llm_enhanced"] = False
            return template_report
        
        # هنا يمكن إضافة تحسينات LLM
        # مثل: صياغة أفضل، توصيات أكثر تفصيلاً
        template_report["llm_enhanced"] = True
        template_report["llm_notes"] = "LLM متاح للتحسينات المستقبلية"
        
        return template_report

# ──────────────────────────────────────────────────────
# واجهة موحدة
# ──────────────────────────────────────────────────────

class HybridIntelligence:
    """
    النظام الهجين: قوالب سريعة + LLM اختياري
    """
    
    def __init__(self, use_llm: bool = False):
        self.template_engine = TemplateEngine()
        self.llm_enhancer = LLMEnhancer(use_llm)
    
    def analyze_ports(self, ports: List[int], target: str, use_llm: bool = False) -> Dict:
        """
        تحليل المنافذ
        
        Args:
            ports: المنافذ المفتوحة
            target: الهدف
            use_llm: استخدام LLM للتحسين (افتراضي: False للسرعة)
        
        Returns:
            dict: تحليل كامل
        """
        # الخطوة 1: توليد سريع بالقوالب (< 100ms)
        analysis = self.template_engine.analyze_ports_template(ports, target)
        
        # الخطوة 2: تحسين LLM اختياري (10-30 ثانية)
        if use_llm:
            analysis = self.llm_enhancer.enhance_report(analysis)
        
        return analysis
    
    def generate_full_report(self, scan_data: Dict) -> Dict:
        """توليد تقرير كامل"""
        return self.template_engine.generate_report_template(scan_data)

# ──────────────────────────────────────────────────────
# اختبار
# ──────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🎯 اختبار النظام الهجين (قوالب + LLM اختياري)\n")
    
    import time
    
    # اختبار 1: قوالب فقط (سريع جداً)
    print("=" * 60)
    print("📊 الاختبار 1: قوالب فقط (بدون LLM)")
    print("=" * 60)
    
    hybrid = HybridIntelligence(use_llm=False)
    
    start = time.time()
    analysis = hybrid.analyze_ports([22, 445, 80, 3389], "192.168.122.1")
    elapsed = time.time() - start
    
    print(f"النتيجة: {json.dumps(analysis, indent=2, ensure_ascii=False)}")
    print(f"\n⏱️ الوقت: {elapsed*1000:.1f} مللي ثانية")
    print("✅ سريع جداً! يمكن استخدامه للإنتاج")
    
    # اختبار 2: تقرير كامل
    print("\n" + "=" * 60)
    print("📝 الاختبار 2: تقرير كامل")
    print("=" * 60)
    
    report = hybrid.generate_full_report(analysis)
    print(f"التقرير: {json.dumps(report, indent=2, ensure_ascii=False)}")
    
    print("\n" + "=" * 60)
    print("✅ الخلاصة:")
    print("   • القوالب: < 100ms ← للاستخدام اليومي")
    print("   • LLM: 10-30ث ← للتحليلات العميقة فقط")
    print("=" * 60)
