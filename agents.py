"""
🛡️ الوكلاء الدفاعيون (Blue Team Agents)
مستوحى من بنية Decepticon Red Team
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from .core import BaseAgent, AgentMessage
    from .tools import discover_hosts, scan_ports, detect_services, assess_risk, full_network_scan
except ImportError:
    from core import BaseAgent, AgentMessage
    from tools import discover_hosts, scan_ports, detect_services, assess_risk, full_network_scan

from typing import List, Dict, Optional
import json

# --- 1. وكيل الاستطلاع (Reconnaissance Agent) ---

class ReconnaissanceAgent(BaseAgent):
    """
    🕵️ Network Reconnaissance Specialist
    
    Identity:
        وكيل استطلاع أمني للشبكات. هدفك هو اكتشاف وتوثيق البنية التحتية
        للشبكة بدقة واحترافية وأمان.
    
    Core Principles:
        1. Be Thorough: لا تترك حجراً دون حجر، لكن احترم الموارد
        2. Be Accurate: الإيجابيات الكاذبة تضيع الوقت؛ تحقّق قبل الإبلاغ
        3. Be Safe: لا تستغل أبداً، فقط اكتشف ووثّق
        4. Be Efficient: جمّع العمليات، احترم المهل، تجنّب الإغراق
    
    Safety Boundaries:
        ❌ NEVER attempt exploitation
        ❌ NEVER brute-force credentials
        ❌ NEVER exfiltrate data beyond scan results
        ✅ ONLY discover and document
        ✅ ONLY operate within authorized scope
    
    Output Format:
        {
            "target": "IP or CIDR",
            "hosts_found": [...],
            "open_ports": {...},
            "services": [...],
            "confidence": "high|medium|low",
            "notes": "Any anomalies or observations"
        }
    """
    
    def __init__(self):
        super().__init__("Recon", "Network Reconnaissance Specialist")
        self.discovered_hosts: List[str] = []
        self.open_ports: Dict[str, List[int]] = {}
        self.scan_history: List[Dict] = []  # سجل الفحوصات
        self.authorized_scope: Optional[str] = None  # النطاق المصرح به
    
    def get_capabilities(self) -> List[str]:
        return [
            "network_discovery",
            "port_scanning",
            "service_enumeration",
            "topology_mapping"
        ]
    
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.message_type == "task":
            task = message.content.get("task_type")
            
            if task == "scan_network":
                return self.scan_network(message.content.get("target"))
            elif task == "scan_ports":
                return self.scan_ports(message.content.get("target"))
        
        elif message.message_type == "request":
            req = message.content.get("request_type")
            if req == "discovered_hosts":
                return self.send_message(
                    message.sender,
                    "result",
                    {"hosts": self.discovered_hosts}
                )
        
        return None
    
    def scan_network(self, target: str) -> AgentMessage:
        """فحص الشبكة الفعلي"""
        self.update_status("working", f"فحص الشبكة: {target}")
        
        try:
            # تنفيذ الفحص الحقيقي
            hosts = discover_hosts(target)
            
            self.discovered_hosts = [h["ip"] for h in hosts]
            
            result = {
                "target": target,
                "hosts_found": self.discovered_hosts,
                "total_active": len(hosts),
                "status": "completed",
                "raw_data": hosts
            }
            
            print(f"\n📊 [{self.name}] اكتشف {len(hosts)} أجهزة نشطة")
            
        except Exception as e:
            result = {
                "target": target,
                "error": str(e),
                "status": "failed"
            }
        
        self.update_status("idle")
        return self.send_message("broadcast", "result", result)
    
    def scan_ports(self, target: str) -> AgentMessage:
        """فحص المنافذ الفعلي"""
        self.update_status("working", f"فحص المنافذ: {target}")
        
        try:
            # تنفيذ الفحص الحقيقي
            port_result = scan_ports(target)
            
            self.open_ports[target] = port_result["open_ports"]
            
            # كشف الخدمات
            services = []
            if port_result["open_ports"]:
                services = detect_services(target, port_result["open_ports"])
            
            result = {
                "target": target,
                "open_ports": port_result["open_ports"],
                "closed_ports": port_result["closed_ports"],
                "services": services,
                "status": "completed",
                "raw_data": port_result
            }
            
            print(f"\n📊 [{self.name}] اكتشف {len(port_result['open_ports'])} منافذ مفتوحة على {target}")
            
        except Exception as e:
            result = {
                "target": target,
                "error": str(e),
                "status": "failed"
            }
        
        self.update_status("idle")
        return self.send_message("broadcast", "result", result)

# --- 2. وكيل التحليل (Analysis Agent) ---

class AnalysisAgent(BaseAgent):
    """
    🧠 Threat Analysis & Risk Assessment Specialist
    
    Identity:
        أنت محلل أمن سيبراني. هدفك هو تفسير بيانات الفحوصات، تقييم المخاطر،
        وتقديم توصيات قابلة للتنفيذ.
    
    Analytical Framework:
        Step 1: Data Correlation
            - Cross-reference open ports with known CVEs
            - Map services to potential attack vectors
            - Identify misconfigurations
        
        Step 2: Risk Scoring (CVSS-like)
            - Impact: What could happen if exploited?
            - Likelihood: How easy is exploitation?
            - Exposure: Is it internet-facing?
        
        Step 3: Prioritization
            1. Critical: Immediate action required
            2. High: Address within 24-48 hours
            3. Medium: Schedule for next maintenance
            4. Low: Document and monitor
    
    Cognitive Biases to Avoid:
        ⚠️ Confirmation Bias: Don't only look for expected patterns
        ⚠️ Anchoring: Don't fixate on first finding
        ⚠️ Availability Heuristic: Recent ≠ more important
        ✅ Always consider alternative explanations
    
    Output Format:
        {
            "finding": "Description",
            "affected_assets": [...],
            "cve_references": [...],
            "risk_score": 0-100,
            "risk_level": "CRITICAL|HIGH|MEDIUM|LOW",
            "impact": "What could happen",
            "likelihood": "How probable",
            "recommendation": "Specific remediation steps",
            "references": ["Link to CVE", "Best practice doc"]
        }
    """
    
    def __init__(self):
        super().__init__("Analyst", "Threat Analysis & Risk Assessment Specialist")
        self.risk_assessments: Dict[str, Dict] = {}
        self.findings_history: List[Dict] = []
        self.cve_database: Dict[int, List[str]] = {}  # Port → CVEs
        self._init_cve_database()
    
    def _init_cve_database(self):
        """تهيئة قاعدة بيانات مبسطة للثغرات المعروفة"""
        self.cve_database = {
            21: ["CVE-2015-3306", "CVE-2011-2523"],  # FTP
            22: ["CVE-2021-28041", "CVE-2020-15778"],  # SSH
            23: ["CVE-2022-0512", "CVE-2020-10188"],  # Telnet (insecure)
            139: ["CVE-2020-1472", "CVE-2017-0144"],  # NetBIOS (SMBv1)
            445: ["CVE-2020-1472", "CVE-2017-0144", "CVE-2021-34527"],  # SMB
            3389: ["CVE-2019-0708", "CVE-2019-1181"],  # RDP
            3306: ["CVE-2023-22084", "CVE-2022-37000"],  # MySQL
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "risk_assessment",
            "pattern_detection",
            "anomaly_detection",
            "threat_correlation"
        ]
    
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.message_type == "result":
            # تحليل النتائج الواردة من وكلاء آخرين
            return self.analyze_data(message.sender, message.content)
        
        elif message.message_type == "task":
            task = message.content.get("task_type")
            if task == "assess_risk":
                return self.assess_risk(message.content.get("target"))
        
        return None
    
    def analyze_data(self, source: str, data: Dict) -> AgentMessage:
        """
        تحليل البيانات الواردة مع منهجية CVSS
        
        Returns:
            AgentMessage: تنبيه أو إقرار بالتحليل
        """
        self.update_status("working", f"تحليل بيانات من {source}")
        
        alerts = []
        findings = []
        
        # تحليل المنافذ المفتوحة
        if "open_ports" in data:
            target = data.get("target", "unknown")
            open_ports = data["open_ports"]
            
            # Step 1: Data Correlation - ربط المنافذ بالثغرات
            port_cves = []
            for port in open_ports:
                if port in self.cve_database:
                    port_cves.extend([
                        {"port": port, "cve": cve} 
                        for cve in self.cve_database[port]
                    ])
            
            # Step 2: Risk Scoring
            risk_report = assess_risk(open_ports, target)
            
            # Step 3: Prioritization
            risk_level = risk_report["overall_risk"]
            risk_score = risk_report["risk_score"]
            
            # حساب التأثير والاحتمالية
            impact = "HIGH" if risk_score > 70 else "MEDIUM" if risk_score > 40 else "LOW"
            likelihood = "HIGH" if len(port_cves) > 3 else "MEDIUM" if len(port_cves) > 0 else "LOW"
            
            # إنشاء نتيجة تحليلية شاملة
            finding = {
                "finding": f"منافذ محفوفة بالمخاطر مكتشفة على {target}",
                "affected_assets": [target],
                "cve_references": [cve["cve"] for cve in port_cves],
                "risk_score": risk_score,
                "risk_level": risk_level,
                "impact": impact,
                "likelihood": likelihood,
                "recommendation": "راجع التوصيات المحددة في risk_report",
                "references": [
                    f"https://nvd.nist.gov/vuln/detail/{cve}" 
                    for cve in list(set([cve["cve"] for cve in port_cves]))[:3]
                ],
                "ports_details": [
                    {
                        "port": p,
                        "risk": "HIGH" if p in [139, 445, 23, 3389] else "MEDIUM",
                        "known_cves": self.cve_database.get(p, [])
                    }
                    for p in open_ports
                ]
            }
            
            self.findings_history.append(finding)
            self.risk_assessments[target] = finding
            
            # إنشاء تنبيه إذا كان الخطر متوسط أو أعلى
            if risk_level in ["HIGH", "MEDIUM", "CRITICAL"]:
                alert_msg = self.send_message(
                    "broadcast",
                    "alert",
                    {
                        "level": risk_level,
                        "target": target,
                        "message": f"منافذ محفوفة بالمخاطر: {risk_report['high_risk_ports'] + risk_report['medium_risk_ports']}",
                        "risk_score": risk_score,
                        "impact": impact,
                        "likelihood": likelihood,
                        "known_cves": len(port_cves),
                        "recommendations": risk_report["recommendations"],
                        "analysis": "تحليل CVSS كامل متاح في findings_history"
                    }
                )
                alerts.append(alert_msg)
                print(f"\n🧠 [{self.name}] تم التحليل: {target} - الخطر: {risk_level} (درجة: {risk_score})")
        
        self.update_status("idle")
        
        # إرجاع آخر تنبيه أو إقرار عادي
        if alerts:
            return alerts[-1]
        return self.send_message(source, "ack", {
            "analyzed": True, 
            "risk_level": risk_level if 'risk_level' in dir() else "LOW",
            "findings_count": len(self.findings_history)
        })
    
    def assess_risk(self, target: str) -> AgentMessage:
        """تقييم المخاطر لهدف معين"""
        self.update_status("working", f"تقييم المخاطر: {target}")
        risk_level = "LOW"  # حساب فعلي هنا
        self.risk_assessments[target] = risk_level
        self.update_status("idle")
        return self.send_message(
            "broadcast",
            "result",
            {"target": target, "risk_level": risk_level}
        )

# --- 3. وكيل التخطيط (Planner Agent) - العقل المدبر ---

class PlannerAgent(BaseAgent):
    """
    🎯 Mission Planning & Orchestration Coordinator
    
    Identity:
        أنت العقل الاستراتيجي لسرب الأمان. هدفك هو تخطيط وتنسيق وتحسين
        عمليات الأمان متعددة الوكلاء.
    
    Planning Methodology:
        Phase 1: Mission Definition
            - Clarify objectives with stakeholder
            - Define scope and boundaries
            - Identify constraints (time, resources, risk tolerance)
        
        Phase 2: Resource Allocation
            - Assign agents to tasks based on capabilities
            - Sequence operations logically
            - Build in redundancy for critical steps
        
        Phase 3: Execution Monitoring
            - Track progress in real-time
            - Adapt to changing conditions
            - Escalate blockers immediately
        
        Phase 4: Review & Learn
            - Conduct post-mission retrospective
            - Document lessons learned
            - Update playbooks for future missions
    
    Decision Framework:
        IF target_risk == "HIGH" AND confidence == "LOW":
            → Assign multiple agents for verification
        
        IF time_constraint == "TIGHT":
            → Prioritize critical assets only
        
        IF network_size > 1000_hosts:
            → Use sampling + targeted deep-dive
    
    Communication Patterns:
        To Agents:
            Task: {specific_action}
            Target: {scope}
            Deadline: {timebox}
            Priority: {level}
            Dependencies: {other_agents}
            Success Criteria: {measurable_outcome}
        
        To Stakeholders:
            Status: {progress_percentage}
            Findings So Far: {summary}
            Blockers: {issues}
            ETA: {completion_estimate}
            Recommendations: {next_steps}
    
    Stress Management:
        🧘 Stay calm under pressure
        🎯 Focus on priorities, not perfection
        🤝 Escalate when stuck
        📚 Learn from every mission
    """
    
    def __init__(self):
        super().__init__("Planner", "Mission Planning & Orchestration Coordinator")
        self.active_operations: Dict[str, Dict] = {}
        self.agent_tasks: Dict[str, List[str]] = {}
        self.mission_history: List[Dict] = []
        self.playbooks: Dict[str, List[Dict]] = self._init_playbooks()
        self.resource_load: Dict[str, int] = {"Recon": 0, "Analyst": 0, "Reporter": 0}
    
    def _init_playbooks(self) -> Dict[str, List[Dict]]:
        """تهيئة كتب التشغيل (Playbooks) للسيناريوهات الشائعة"""
        return {
            "network_scan": [
                {"agent": "Recon", "task": "scan_network", "phase": 1},
                {"agent": "Recon", "task": "scan_ports", "phase": 2},
                {"agent": "Analyst", "task": "assess_risk", "phase": 3},
                {"agent": "Reporter", "task": "generate_report", "phase": 4}
            ],
            "quick_audit": [
                {"agent": "Recon", "task": "scan_network", "phase": 1},
                {"agent": "Analyst", "task": "assess_risk", "phase": 2}
            ],
            "deep_inspection": [
                {"agent": "Recon", "task": "scan_network", "phase": 1},
                {"agent": "Recon", "task": "scan_ports", "phase": 2},
                {"agent": "Analyst", "task": "assess_risk", "phase": 3},
                {"agent": "Analyst", "task": "correlate_threats", "phase": 4},
                {"agent": "Reporter", "task": "generate_report", "phase": 5}
            ]
        }
    
    def get_capabilities(self) -> List[str]:
        return [
            "mission_planning",
            "task_orchestration",
            "priority_management",
            "resource_allocation"
        ]
    
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.message_type == "task":
            if message.content.get("task_type") == "start_mission":
                return self.start_mission(message.content)
        
        elif message.message_type == "result":
            # تحديث حالة المهمة بناءً على النتائج
            return self.update_mission_status(message.sender, message.content)
        
        return None
    
    def start_mission(self, mission_params: Dict) -> AgentMessage:
        """بدء مهمة جديدة وتنسيق الوكلاء"""
        self.update_status("working", f"تخطيط المهمة: {mission_params.get('name')}")
        
        mission_id = str(len(self.active_operations) + 1)
        self.active_operations[mission_id] = {
            "name": mission_params.get("name"),
            "status": "in_progress",
            "agents_involved": [],
            "tasks_completed": [],
            "started_at": mission_params.get("timestamp")
        }
        
        # إنشاء مهام للوكلاء
        tasks = [
            {"agent": "Recon", "task": "scan_network", "target": mission_params.get("target")},
            {"agent": "Analyst", "task": "assess_risk", "target": mission_params.get("target")}
        ]
        
        self.update_status("idle")
        
        return self.send_message(
            "broadcast",
            "task",
            {
                "mission_id": mission_id,
                "tasks": tasks,
                "coordinator": self.name
            }
        )
    
    def update_mission_status(self, agent: str, result: Dict) -> AgentMessage:
        """تحديث حالة المهمة بناءً على نتائج الوكيل"""
        return self.send_message(
            "Planner",
            "ack",
            {"received_from": agent, "status": "logged"}
        )

# --- 4. وكيل التقارير (Reporter Agent) ---

class ReporterAgent(BaseAgent):
    """
    📝 Documentation & Reporting Specialist
    
    Identity:
        أنت متواصل تقني. هدفك هو تحويل بيانات الأمان الخام إلى تقارير
        واضحة وقابلة للتنفيذ لجمهور متنوع.
    
    Audience Adaptation:
        Executive Summary (C-Level):
            • Length: 1 page max
            • Focus: Business impact, risk exposure, budget needs
            • Tone: Strategic, non-technical
            • Metrics: Risk score, compliance status, trend arrows
        
        Technical Report (Security Team):
            • Length: As needed (comprehensive)
            • Focus: Technical details, exploitation paths, remediation
            • Tone: Precise, evidence-based
            • Metrics: CVSS scores, affected systems, patches needed
        
        Developer Brief (Engineering):
            • Length: Per-issue (concise)
            • Focus: Code-level fixes, before/after examples
            • Tone: Collaborative, solution-oriented
            • Metrics: Lines affected, effort estimate, priority
    
    Report Structure:
        # Security Assessment Report
        ## Executive Summary
        - Overall posture
        - Key findings
        - Immediate actions
        
        ## Methodology
        - Scope
        - Tools used
        - Limitations
        
        ## Findings
        ### Finding 1: [Name]
        - Severity: 🔴 Critical
        - Description: What is it?
        - Impact: What could happen?
        - Evidence: Proof (screenshots, logs)
        - Recommendation: How to fix?
        - Timeline: When to address?
        
        ## Appendix
        - Full scan results
        - Tool configurations
        - Raw data exports
    
    Writing Principles:
        ✍️ Clarity over cleverness: Simple > fancy
        📊 Visuals where possible: Diagrams, charts, tables
        🔢 Quantify everything: Numbers > adjectives
        ✅ Actionable language: "Do X" not "Consider X"
    
    Version Control:
        Always include:
        - Report version
        - Date/time
        - Author (agent ID)
        - Change log (for updates)
    """
    
    def __init__(self):
        super().__init__("Reporter", "Documentation & Reporting Specialist")
        self.reports: Dict[str, Dict] = {}
        self.collected_data: List[Dict] = []  # بيانات مجمعة من الوكلاء
        self.templates = self._init_templates()
        self.report_versions: Dict[str, int] = {}  # تتبع الإصدارات
    
    def _init_templates(self) -> Dict[str, str]:
        """تهيئة قوالب التقارير للجمهور المختلف"""
        return {
            "executive": self._executive_template(),
            "technical": self._technical_template(),
            "developer": self._developer_template()
        }
    
    def _executive_template(self) -> str:
        """قمل تقرير المدراء التنفيذيين"""
        return """
# 📊 Security Assessment - Executive Summary

## Overall Posture
- **Risk Level**: {risk_level}
- **Risk Score**: {risk_score}/100
- **Trend**: {trend}

## Key Findings (Top 3)
{key_findings}

## Immediate Actions Required
{immediate_actions}

## Budget Implications
{budget_notes}

---
*Report v{version} | Generated: {timestamp} | Pi bot Swarm 2.0*
"""
    
    def _technical_template(self) -> str:
        """قالب التقرير الفني"""
        return """
# 🛡️ Security Assessment - Technical Report

## Executive Summary
{executive_summary}

## Methodology
- **Scope**: {scope}
- **Tools Used**: Pi bot Swarm 2.0 (Recon, Analyst, Planner)
- **Scan Duration**: {duration}
- **Limitations**: {limitations}

## Detailed Findings

{findings_detail}

## Appendix
### A. Full Scan Results
{raw_results}

### B. CVE References
{cve_refs}

### C. Tool Configuration
{config}

---
*Report v{version} | Generated: {timestamp} | Pi bot Swarm 2.0*
"""
    
    def _developer_template(self) -> str:
        """قالب تقرير المطورين"""
        return """
# 🔧 Developer Security Brief

## Issue: {issue_name}

### What's Wrong?
{description}

### Impact
{impact}

### How to Fix
```diff
{code_fix}
```

### Effort Estimate
- **Time**: {time_estimate}
- **Complexity**: {complexity}
- **Priority**: {priority}

### References
- {references}

---
*Brief v{version} | Generated: {timestamp} | Pi bot Swarm 2.0*
"""
    
    def get_capabilities(self) -> List[str]:
        return [
            "report_generation",
            "data_aggregation",
            "executive_summary",
            "export_formats",
            "audience_adaptation",
            "version_control"
        ]
    
    def process_message(self, message: AgentMessage) -> Optional[AgentMessage]:
        if message.message_type == "task":
            if message.content.get("task_type") == "generate_report":
                return self.generate_report(message.content)
        
        elif message.message_type == "result":
            # حفظ النتائج للتقرير
            return self.accumulate_data(message.sender, message.content)
        
        elif message.message_type == "request":
            if message.content.get("request_type") == "get_report":
                return self.get_report(message.content.get("report_id"))
        
        return None
    
    def accumulate_data(self, source: str, data: Dict) -> AgentMessage:
        """تجميع البيانات للتقرير"""
        self.collected_data.append({
            "source": source,
            "timestamp": data.get("timestamp", "unknown"),
            "data": data
        })
        return self.send_message(
            source,
            "ack",
            {"data_logged": True, "from": source, "total_collected": len(self.collected_data)}
        )
    
    def generate_report(self, params: Dict) -> AgentMessage:
        """
        إنشاء تقرير شامل متعدد الجماهير
        
        Params:
            report_id: معرف التقرير
            audience: executive|technical|developer
            mission_data: بيانات المهمة من Planner
        """
        self.update_status("working", "إنشاء التقرير الأمني")
        
        report_id = params.get("report_id", f"RPT-{len(self.reports) + 1:03d}")
        
        # تتبع الإصدار
        if report_id in self.report_versions:
            self.report_versions[report_id] += 1
        else:
            self.report_versions[report_id] = 1
        
        version = self.report_versions[report_id]
        timestamp = params.get("timestamp", "unknown")
        
        # تحليل البيانات المجمعة
        risk_level = "LOW"
        risk_score = 0
        findings = []
        recommendations = []
        
        for item in self.collected_data:
            if "risk_level" in item["data"]:
                risk_level = item["data"]["risk_level"]
                risk_score = item["data"].get("risk_score", 0)
            if "finding" in item["data"]:
                findings.append(item["data"])
            if "recommendations" in item["data"]:
                recommendations.extend(item["data"]["recommendations"])
        
        # إنشاء التقرير الأساسي
        base_report = {
            "report_id": report_id,
            "version": version,
            "generated_by": "Pi bot Swarm 2.0",
            "generated_at": timestamp,
            "risk_level": risk_level,
            "risk_score": risk_score,
            "findings_count": len(findings),
            "findings": findings,
            "recommendations": list(set(recommendations)),  # إزالة التكرار
            "raw_data": self.collected_data.copy()
        }
        
        # إنشاء نسخ للجمهور المختلف
        audiences = {}
        
        # 1. تقرير تنفيذي
        audiences["executive"] = self._executive_template().format(
            risk_level=risk_level,
            risk_score=risk_score,
            trend="⬆️ Increasing" if risk_score > 50 else "➡️ Stable" if risk_score > 20 else "⬇️ Improving",
            key_findings="\n".join([f"• {f.get('finding', 'N/A')}" for f in findings[:3]]),
            immediate_actions="\n".join([f"• {r}" for r in recommendations[:3]]),
            budget_notes="No immediate budget impact" if risk_score < 30 else "Budget review recommended",
            version=version,
            timestamp=timestamp
        )
        
        # 2. تقرير فني
        audiences["technical"] = self._technical_template().format(
            executive_summary=f"Overall risk level: {risk_level} (Score: {risk_score}/100)",
            scope=params.get("scope", "Network scan"),
            duration=params.get("duration", "N/A"),
            limitations="Standard TCP connect scan only",
            findings_detail="\n\n".join([
                f"### {f.get('finding', 'Unknown')}\n"
                f"- **Risk**: {f.get('risk_level', 'N/A')}\n"
                f"- **Score**: {f.get('risk_score', 'N/A')}\n"
                f"- **CVEs**: {', '.join(f.get('cve_references', [])) or 'None'}\n"
                f"- **Recommendation**: {f.get('recommendation', 'N/A')}"
                for f in findings
            ]),
            raw_results=json.dumps(self.collected_data, indent=2),
            cve_refs="\n".join(set([
                cve for f in findings 
                for cve in f.get('cve_references', [])
            ])),
            config="Default Pi bot Swarm 2.0 configuration",
            version=version,
            timestamp=timestamp
        )
        
        # 3. تقرير مطورين (نموذج لأولFinding)
        if findings:
            first_finding = findings[0]
            audiences["developer"] = self._developer_template().format(
                issue_name=first_finding.get('finding', 'Security Issue'),
                description=first_finding.get('impact', 'N/A'),
                impact=first_finding.get('impact', 'N/A'),
                code_fix="# Review firewall rules\n# Close unnecessary ports\n# Update service configurations",
                time_estimate="1-2 hours",
                complexity="Low" if risk_score < 40 else "Medium" if risk_score < 70 else "High",
                priority=["CRITICAL", "HIGH", "MEDIUM", "LOW"][
                    min(3, int(risk_score / 25))
                ],
                references="\n- ".join(first_finding.get('references', ['N/A'])),
                version=version,
                timestamp=timestamp
            )
        else:
            audiences["developer"] = "No findings to report."
        
        # حفظ التقرير
        full_report = {
            **base_report,
            "audiences": audiences,
            "export_formats": ["json", "markdown", "pdf"]
        }
        
        self.reports[report_id] = full_report
        
        self.update_status("idle")
        
        print(f"\n📝 [{self.name}] تم إنشاء التقرير {report_id} (v{version})")
        print(f"   ├─ مستوى الخطر: {risk_level}")
        print(f"   ├─ النتائج: {len(findings)}")
        print(f"   └إجمالي التوصيات: {len(recommendations)}")
        
        return self.send_message(
            "broadcast",
            "result",
            {
                "report_ready": True,
                "report_id": report_id,
                "version": version,
                "risk_level": risk_level,
                "audiences_available": list(audiences.keys()),
                "export_formats": full_report["export_formats"]
            }
        )
    
    def get_report(self, report_id: str) -> Optional[AgentMessage]:
        """استرجاع تقرير محدد"""
        if report_id in self.reports:
            return self.send_message(
                "Orchestrator",
                "result",
                {"report": self.reports[report_id], "found": True}
            )
        return self.send_message(
            "Orchestrator",
            "result",
            {"error": "Report not found", "report_id": report_id, "found": False}
        )
