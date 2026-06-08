"""
LangGraph State Schema - The shared memory across all agents.
Uses Pydantic for validation and type safety.
"""
from typing import List, Optional, Dict, Any, Annotated
from pydantic import BaseModel, Field
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
import operator
from datetime import datetime


class SearchResult(BaseModel):
    """A single web search result."""
    url: str
    title: str
    content: str
    score: float = 0.0
    published_date: Optional[str] = None


class ReportSection(BaseModel):
    """A section in the final report."""
    title: str
    content: str
    sources: List[str] = Field(default_factory=list)
    confidence: float = Field(default=0.8, ge=0.0, le=1.0)


class ResearchPlan(BaseModel):
    """The planner's output - structured research plan."""
    topic: str
    subtopics: List[str] = Field(default_factory=list)
    search_queries: List[str] = Field(default_factory=list)
    estimated_sections: List[str] = Field(default_factory=list)


class CriticFeedback(BaseModel):
    """Critic agent's review of the draft."""
    score: float = Field(ge=0.0, le=10.0)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    suggestions: List[str] = Field(default_factory=list)
    needs_revision: bool = True


class FactCheckResult(BaseModel):
    """Fact-checker's verification results."""
    verified_claims: List[str] = Field(default_factory=list)
    disputed_claims: List[str] = Field(default_factory=list)
    unverifiable_claims: List[str] = Field(default_factory=list)
    overall_credibility: float = Field(default=0.8, ge=0.0, le=1.0)


class AgentState(BaseModel):
    """
    Complete shared state for the multi-agent graph.
    This is passed between all agents in the DAG.
    """
    # Input
    topic: str = ""
    user_instructions: Optional[str] = None

    # Messages history (LangGraph native)
    messages: Annotated[List[BaseMessage], add_messages] = Field(default_factory=list)

    # Agent outputs
    research_plan: Optional[ResearchPlan] = None
    search_results: List[SearchResult] = Field(default_factory=list)
    raw_research: str = ""
    draft_report: str = ""
    final_report: str = ""
    report_sections: List[ReportSection] = Field(default_factory=list)
    critic_feedback: Optional[CriticFeedback] = None
    fact_check_result: Optional[FactCheckResult] = None

    # Control flow
    current_agent: str = "planner"
    iteration_count: int = 0
    max_iterations: int = 10
    revision_count: int = 0
    max_revisions: int = 2
    is_complete: bool = False
    error: Optional[str] = None

    # Metadata
    run_id: str = Field(default_factory=lambda: datetime.now().strftime("%Y%m%d_%H%M%S"))
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    total_tokens_used: int = 0
    sources: List[str] = Field(default_factory=list)

    class Config:
        arbitrary_types_allowed = True