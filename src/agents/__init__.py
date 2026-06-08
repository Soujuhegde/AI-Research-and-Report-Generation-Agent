#created this just for an initializing the file

"""
Agents package - All specialized AI agents for the research pipeline.

Agents:
    - PlannerAgent: Creates structured research plans
    - ResearcherAgent: Performs web search and synthesis
    - WriterAgent: Drafts the research report
    - CriticAgent: Reviews and scores the draft
    - FactCheckerAgent: Verifies claims and sources
"""

from src.agents.planner_agent import planner_agent
from src.agents.researcher_agent import researcher_agent
from src.agents.writer_agent import writer_agent
from src.agents.critic_agent import critic_agent
from src.agents.fact_checker_agent import fact_checker_agent

__all__ = [
    "planner_agent",
    "researcher_agent",
    "writer_agent",
    "critic_agent",
    "fact_checker_agent",
]