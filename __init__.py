"""
🥧 Pi bot Swarm 2.0
Autonomous Blue Team Security Operations

Usage:
    from swarm_v2 import SwarmOrchestrator
    from swarm_v2.agents import ReconnaissanceAgent, AnalysisAgent
    from swarm_v2.core import AgentMessage, SwarmReplay
"""

from .core import (
    BaseAgent,
    AgentMessage,
    AgentState,
    SwarmReplay
)

from .agents import (
    ReconnaissanceAgent,
    AnalysisAgent,
    PlannerAgent,
    ReporterAgent
)
from .osint_agent import OSINTScraperAgent

from .orchestrator import SwarmOrchestrator

__version__ = "2.0.0"
__author__ = "Pi bot"
__all__ = [
    # Core
    "BaseAgent",
    "AgentMessage",
    "AgentState",
    "SwarmReplay",
    
    # Agents
    "ReconnaissanceAgent",
    "AnalysisAgent",
    "PlannerAgent",
    "ReporterAgent",
    "OSINTScraperAgent",  # 🕷️ الوكيل الجديد
    
    # Orchestrator
    "SwarmOrchestrator"
]
