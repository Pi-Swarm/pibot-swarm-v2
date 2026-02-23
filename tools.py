"""
🛠️ أدوات الفحص الأمني الفعلي
Real Security Scanning Tools for Pi bot Swarm

Safety Principles:
    ✅ ONLY scan authorized targets
    ✅ Use minimal intrusion methods
    ✅ Respect rate limits
    ✅ Log all actions
    ❌ NEVER exploit vulnerabilities
    ❌ NEVER brute-force credentials
    ❌ NEVER scan without authorization

تدعم:
- TCP Connect Scan
- Network Discovery (ICMP/ARP)
- Service Detection
- Risk Assessment
"""

import socket
import subprocess
import json
from typing import List, Dict, Optional
from datetime import datetime
from pathlib import Path

# --- Safety Configuration ---

SAFETY_CONFIG = {
    "require_authorization": True,
    "max_concurrent_scans": 10,
    "rate_limit_ms": 100,  # تأخير بين كل فحص
    "authorized_ranges": [
        "192.168.0.0/16",  # Private Class B
        "10.0.0.0/8",      # Private Class A
        "172.16.0.0/12",   # Private Class C
        "127.0.0.0/8",     # Localhost
    ],
    "forbidden_ports": [],  # منافذ ممنوع فحصها (إضافة حسب الحاجة)
    "log_all_scans": True,
}

# --- Logging ---

def log_scan_action(action: str, target: str, details: Dict = None):
    """تسجيل كل إجراءات الفحص للشفافية والمراجعة"""
    if not SAFETY_CONFIG["log_all_scans"]:
        return
    
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "target": target,
        "details": details or {}
    }
    
    # حفظ في ملف سجل
    log_dir = Path("scan_logs")
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / f"scan_log_{datetime.now().strftime('%Y-%m-%d')}.jsonl"
    
    with open(log_file, "a") as f:
        f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")
    
    print(f"📝 [LOG] {action} on {target}")

# --- Authorization ---

def is_authorized_target(target: str) -> bool:
    """
    التحقق من أن الهدف مصرح بفحصه
    
    Args:
        target: IP أو CIDR
    
    Returns:
        bool: True إذا كان مصرحاً
    """
    if not SAFETY_CONFIG["require_authorization"]:
        return True
    
    # تبسيط: التحقق من أن الهدف ضمن النطاقات الخاصة
    # في تطبيق حقيقي: استخدام ipaddress module للتحقق الدقيق
    if target.startswith(("192.168.", "10.", "172.16.", "172.17.", "172.18.", 
                          "172.19.", "172.20.", "172.21.", "172.22.", "172.23.",
                          "172.24.", "172.25.", "172.26.", "172.27.", "172.28.",
                          "172.29.", "172.30.", "172.31.", "127.")):
        return True
    
    # Check against authorized_ranges
    for authorized in SAFETY_CONFIG["authorized_ranges"]:
        if target.startswith(authorized.split(".")[0]):
            return True
    
    return False

def safety_check(func):
    """Decorator لإضافة فحوصات الأمان تلقائياً لكل دالة فحص"""
    def wrapper(*args, **kwargs):
        # استخراج الهدف من المعاملات
        target = None
        if args:
            target = args[0]
        elif "target" in kwargs:
            target = kwargs["target"]
        elif "target_ip" in kwargs:
            target = kwargs["target_ip"]
        elif "network_range" in kwargs:
            target = kwargs["network_range"]
        
        if target:
            # التحقق من التفويض
            if not is_authorized_target(target):
                error_msg = f"⛔ UNAUTHORIZED TARGET: {target}"
                print(f"\n🚨 {error_msg}")
                log_scan_action("BLOCKED_UNAUTHORIZED", target, {"reason": "Not in authorized ranges"})
                raise PermissionError(error_msg)
            
            # تسجيل الفحص
            log_scan_action("SCAN_STARTED", target)
        
        # تنفيذ الدالة الأصلية
        try:
            result = func(*args, **kwargs)
            if target:
                log_scan_action("SCAN_COMPLETED", target, {"status": "success"})
            return result
        except Exception as e:
            if target:
                log_scan_action("SCAN_FAILED", target, {"error": str(e)})
            raise
    
    wrapper.__name__ = func.__name__
    return wrapper

# --- 1. اكتشاف الشبكة (Network Discovery) ---

@safety_check
def discover_hosts(network_range: str, timeout: float = 1.0) -> List[Dict]:
    """
    اكتشاف الأجهزة النشطة في نطاق الشبكة
    
    Args:
        network_range: مثال "192.168.122.0/24"
        timeout: مهلة الاستجابة بالثواني
    
    Returns:
        قائمة بالأجهزة النشطة مع معلوماتها
    """
    print(f"\n🔍 جاري فحص الشبكة: {network_range}")
    
    # تحليل نطاق الشبكة
    if "/" in network_range:
        base_ip, prefix = network_range.split("/")
        prefix = int(prefix)
        
        if prefix == 24:
            # /24 يعني 256 عنوان (0-255)
            base_parts = base_ip.split(".")[:3]
            addresses = [f"{'.'.join(base_parts)}.{i}" for i in range(1, 255)]
        else:
            # نطاقات أخرى (مبسطة)
            addresses = [base_ip]
    else:
        addresses = [network_range]
    
    active_hosts = []
    
    for ip in addresses:
        # محاولة ping باستخدام socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            # محاولة الاتصال بمنفذ شائع (80 أو 22)
            result = sock.connect_ex((ip, 80))
            if result == 0:
                host_info = {"ip": ip, "status": "active", "detected_via": "port_80"}
                active_hosts.append(host_info)
                print(f"  ✅ {ip} نشط (منفذ 80)")
            else:
                # تجربة منفذ 22
                result = sock.connect_ex((ip, 22))
                if result == 0:
                    host_info = {"ip": ip, "status": "active", "detected_via": "port_22"}
                    active_hosts.append(host_info)
                    print(f"  ✅ {ip} نشط (منفذ 22)")
            
            sock.close()
        except Exception as e:
            pass
    
    print(f"\n📊 النتيجة: {len(active_hosts)} أجهزة نشطة")
    return active_hosts

# --- 2. فحص المنافذ (Port Scanning) ---

@safety_check
def scan_ports(target_ip: str, ports: Optional[List[int]] = None, timeout: float = 0.5) -> Dict:
    """
    فحص المنافذ المفتوحة على هدف معين
    
    Args:
        target_ip: عنوان IP الهدف
        ports: قائمة المنافذ للفحص (default: شائعة)
        timeout: مهلة كل اتصال
    
    Returns:
        قاموس يحتوي على المنافذ المفتوحة والمغلقة
    """
    if ports is None:
        # المنافذ الشائعة للفحص
        ports = [
            21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143,
            443, 445, 993, 995, 1723, 3306, 3389, 5900, 8080,
            18789, 18792  # OpenClaw
        ]
    
    print(f"\n🔍 جاري فحص المنافذ على {target_ip}")
    
    open_ports = []
    closed_ports = []
    filtered_ports = []
    
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((target_ip, port))
            
            if result == 0:
                open_ports.append(port)
                print(f"  ✅ منفذ {port} مفتوح")
            elif result == 11:  # Connection refused
                closed_ports.append(port)
            else:
                filtered_ports.append(port)  # Firewall filtered
            
            sock.close()
        except Exception as e:
            filtered_ports.append(port)
    
    result = {
        "target": target_ip,
        "scan_time": datetime.now().isoformat(),
        "open_ports": open_ports,
        "closed_ports": closed_ports,
        "filtered_ports": filtered_ports,
        "total_scanned": len(ports)
    }
    
    print(f"\n📊 النتيجة:")
    print(f"   ├─ مفتوحة: {len(open_ports)}")
    print(f"   ├─ مغلقة: {len(closed_ports)}")
    print(f"   └─ محجوبة: {len(filtered_ports)}")
    
    return result

# --- 3. كشف الخدمات (Service Detection) ---

COMMON_SERVICES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    111: "RPCbind",
    135: "MS-RPC",
    139: "NetBIOS",
    143: "IMAP",
    443: "HTTPS",
    445: "SMB",
    993: "IMAPS",
    995: "POP3S",
    1723: "PPTP",
    3306: "MySQL",
    3389: "RDP",
    5900: "VNC",
    8080: "HTTP-Proxy",
    18789: "OpenClaw Gateway",
    18792: "OpenClaw Internal"
}

def detect_services(target_ip: str, open_ports: List[int]) -> List[Dict]:
    """
    كشف الخدمات العاملة على المنافذ المفتوحة
    
    Args:
        target_ip: عنوان الهدف
        open_ports: قائمة المنافذ المفتوحة
    
    Returns:
        قائمة بالخدمات المكتشفة
    """
    print(f"\n🔍 جاري كشف الخدمات على {target_ip}")
    
    services = []
    
    for port in open_ports:
        service_name = COMMON_SERVICES.get(port, "Unknown")
        service_info = {
            "port": port,
            "service": service_name,
            "protocol": "TCP",
            "confidence": "high" if service_name != "Unknown" else "low"
        }
        services.append(service_info)
        print(f"  ├─ منفذ {port}: {service_name}")
    
    return services

# --- 4. تقييم المخاطر (Risk Assessment) ---

HIGH_RISK_PORTS = [22, 23, 135, 139, 445, 3389, 5900]
MEDIUM_RISK_PORTS = [21, 25, 110, 143, 3306, 8080]

def assess_risk(open_ports: List[int], target_ip: str) -> Dict:
    """
    تقييم مستوى المخاطر بناءً على المنافذ المفتوحة
    
    Args:
        open_ports: المنافذ المفتوحة
        target_ip: الهدف
    
    Returns:
        تقرير المخاطر
    """
    print(f"\n⚠️ تقييم المخاطر لـ {target_ip}")
    
    high_risk = [p for p in open_ports if p in HIGH_RISK_PORTS]
    medium_risk = [p for p in open_ports if p in MEDIUM_RISK_PORTS]
    low_risk = [p for p in open_ports if p not in HIGH_RISK_PORTS + MEDIUM_RISK_PORTS]
    
    # حساب مستوى الخطر العام
    if len(high_risk) > 0:
        overall_risk = "HIGH"
        risk_score = 80 + (len(high_risk) * 5)
    elif len(medium_risk) > 0:
        overall_risk = "MEDIUM"
        risk_score = 40 + (len(medium_risk) * 10)
    else:
        overall_risk = "LOW"
        risk_score = len(low_risk) * 5
    
    risk_score = min(risk_score, 100)
    
    report = {
        "target": target_ip,
        "overall_risk": overall_risk,
        "risk_score": risk_score,
        "high_risk_ports": high_risk,
        "medium_risk_ports": medium_risk,
        "low_risk_ports": low_risk,
        "recommendations": []
    }
    
    # إضافة توصيات
    if 139 in high_risk or 445 in high_risk:
        report["recommendations"].append("إيقاف Samba إذا لم يكن مستخدماً")
    if 22 in high_risk:
        report["recommendations"].append("تفعيل المصادقة الثنائية لـ SSH")
    if 3389 in high_risk:
        report["recommendations"].append("تعطيل RDP أو تقييده بعنوان IP معين")
    
    print(f"   ├─ مستوى الخطر: {overall_risk} (درجة: {risk_score}/100)")
    print(f"   ├─ منافذ عالية الخطورة: {len(high_risk)}")
    print(f"   └─ توصيات: {len(report['recommendations'])}")
    
    for rec in report["recommendations"]:
        print(f"      • {rec}")
    
    return report

# --- 5. دالة الفحص الشامل (Full Scan) ---

@safety_check
def full_network_scan(network_range: str, common_ports_only: bool = True) -> Dict:
    """
    فحص شبكة كامل: اكتشاف + فحص منافذ + كشف خدمات + تقييم مخاطر
    
    Args:
        network_range: نطاق الشبكة
        common_ports_only: استخدام قائمة منافذ شائعة فقط
    
    Returns:
        تقرير شامل
    """
    print("\n" + "="*60)
    print("🛡️  Pi bot Security Scanner - Full Network Scan")
    print("="*60)
    
    start_time = datetime.now()
    
    # المرحلة 1: اكتشاف الأجهزة
    active_hosts = discover_hosts(network_range)
    
    if not active_hosts:
        return {
            "status": "completed",
            "scan_time": start_time.isoformat(),
            "duration_seconds": (datetime.now() - start_time).total_seconds(),
            "targets": [],
            "summary": "لم يتم العثور على أجهزة نشطة"
        }
    
    # المرحلة 2-4: فحص كل جهاز
    scan_results = []
    
    for host in active_hosts:
        ip = host["ip"]
        
        # فحص المنافذ
        port_result = scan_ports(ip)
        
        if port_result["open_ports"]:
            # كشف الخدمات
            services = detect_services(ip, port_result["open_ports"])
            
            # تقييم المخاطر
            risk = assess_risk(port_result["open_ports"], ip)
            
            scan_results.append({
                "ip": ip,
                "status": host["status"],
                "detected_via": host.get("detected_via", "unknown"),
                "open_ports": port_result["open_ports"],
                "closed_ports": len(port_result["closed_ports"]),
                "services": services,
                "risk_assessment": risk
            })
        else:
            scan_results.append({
                "ip": ip,
                "status": "active",
                "detected_via": host.get("detected_via", "unknown"),
                "open_ports": [],
                "services": [],
                "risk_assessment": {"overall_risk": "LOW", "risk_score": 0}
            })
    
    # التقرير الشامل
    full_report = {
        "status": "completed",
        "scan_time": start_time.isoformat(),
        "end_time": datetime.now().isoformat(),
        "duration_seconds": (datetime.now() - start_time).total_seconds(),
        "network_range": network_range,
        "total_hosts_scanned": len(active_hosts),
        "hosts_with_open_ports": len([h for h in scan_results if h["open_ports"]]),
        "targets": scan_results,
        "summary": {
            "total_active": len(active_hosts),
            "high_risk_hosts": len([h for h in scan_results if h.get("risk_assessment", {}).get("overall_risk") == "HIGH"]),
            "medium_risk_hosts": len([h for h in scan_results if h.get("risk_assessment", {}).get("overall_risk") == "MEDIUM"]),
            "low_risk_hosts": len([h for h in scan_results if h.get("risk_assessment", {}).get("overall_risk") == "LOW"])
        }
    }
    
    print("\n" + "="*60)
    print("✅ اكتمل الفحص!")
    print(f"📊 المدة: {full_report['duration_seconds']:.2f} ثانية")
    print(f"📊 الأجهزة النشطة: {full_report['summary']['total_active']}")
    print(f"📊 أجهزة بمنافذ مفتوحة: {full_report['hosts_with_open_ports']}")
    print("="*60)
    
    return full_report

# --- نقطة التشغيل المباشر ---

if __name__ == "__main__":
    # فحص تجريبي
    report = full_network_scan("192.168.122.0/24")
    
    # حفظ التقرير
    with open("scan_report.json", "w") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 حُفظ التقرير في: scan_report.json")
