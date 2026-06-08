"""
LangGraph DAG Workflow - Orchestrates all agents.
Implements: Planner → Researcher → Writer → Critic → (loop) → Fact-Checker
"""
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from typing import Literal

from src.graph.state import AgentState
from src.agents.planner_agent import planner_agent
from src.agents.researcher_agent import researcher_agent
from src.agents.writer_agent import writer_agent
from src.agents.critic_agent import critic_agent
from src.agents.fact_checker_agent import fact_checker_agent
from src.utils.logger import app_logger


def route_after_critic(state: AgentState) -> Literal["writer", "fact_checker"]:
    """
    Conditional routing after critic review.
    Implements the reflection/self-critique loop.
    """
    if (state.critic_feedback 
            and state.critic_feedback.needs_revision 
            and state.revision_count <= state.max_revisions
            and state.iteration_count < state.max_iterations):
        app_logger.info("🔄 Routing back to writer for revision")
        return "writer"
    else:
        app_logger.info("➡️ Routing to fact_checker")
        return "fact_checker"


def route_after_planner(state: AgentState) -> Literal["researcher", "end"]:
    """Handle planner errors."""
    if state.error or state.is_complete:
        return "end"
    return "researcher"


def should_end(state: AgentState) -> bool:
    """Check if we should terminate."""
    return state.is_complete or bool(state.error)


def build_graph() -> StateGraph:
    """
    Build the complete multi-agent DAG.
    
    Graph structure:
    START → planner → researcher → writer → critic → [loop|fact_checker] → END
    """
    # Use dict for LangGraph compatibility
    workflow = StateGraph(dict)

    # Add all agent nodes
    workflow.add_node("planner", lambda state: planner_agent(AgentState(**state)).dict())
    workflow.add_node("researcher", lambda state: researcher_agent(AgentState(**state)).dict())
    workflow.add_node("writer", lambda state: writer_agent(AgentState(**state)).dict())
    workflow.add_node("critic", lambda state: critic_agent(AgentState(**state)).dict())
    workflow.add_node("fact_checker", lambda state: fact_checker_agent(AgentState(**state)).dict())

    # Set entry point
    workflow.set_entry_point("planner")

    # Add edges (linear flow)
    workflow.add_edge("planner", "researcher")
    workflow.add_edge("researcher", "writer")
    workflow.add_edge("writer", "critic")

    # Conditional edge from critic (self-critique loop)
    workflow.add_conditional_edges(
        "critic",
        lambda state: route_after_critic(AgentState(**state)),
        {
            "writer": "writer",
            "fact_checker": "fact_checker",
        }
    )

    # Final edge
    workflow.add_edge("fact_checker", END)

    return workflow


def create_compiled_graph():
    """
    Create and compile the workflow with memory checkpointing.
    """
    workflow = build_graph()
    memory = MemorySaver()
    graph = workflow.compile(checkpointer=memory)
    app_logger.info("✅ Multi-agent graph compiled successfully")
    return graph


# Singleton compiled graph
compiled_graph = create_compiled_graph()


def run_research_pipeline(
    topic: str,
    user_instructions: str = None,
    max_iterations: int = 10,
    thread_id: str = None,
) -> AgentState:
    """
    Main entry point to run the complete research pipeline.
    
    Args:
        topic: Research topic
        user_instructions: Optional additional instructions
        max_iterations: Guard against infinite loops
        thread_id: For LangGraph checkpointing (resume capability)
    
    Returns:
        Final AgentState with complete report
    """
    import uuid
    thread_id = thread_id or str(uuid.uuid4())

    initial_state = {
        "topic": topic,
        "user_instructions": user_instructions,
        "max_iterations": max_iterations,
        "current_agent": "planner",
        "iteration_count": 0,
        "revision_count": 0,
        "is_complete": False,
        "sources": [],
        "search_results": [],
        "messages": [],
    }

    config = {"configurable": {"thread_id": thread_id}}

    app_logger.info(f"🚀 Starting research pipeline for: '{topic}'")
    app_logger.info(f"📋 Thread ID: {thread_id}")

    try:
        final_state = compiled_graph.invoke(initial_state, config=config)
        app_logger.info(f"🎉 Pipeline complete for: '{topic}'")
        return AgentState(**final_state)

    except Exception as e:
        app_logger.error(f"💥 Pipeline failed: {e}")
        raise