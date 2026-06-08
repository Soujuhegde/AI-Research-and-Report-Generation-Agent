"""
Writer Agent - Transforms research into a structured, polished report.
Third node in the DAG.
"""
from langchain_core.messages import HumanMessage, SystemMessage
from src.graph.state import AgentState, ReportSection
from src.llm.sarvam_client import get_llm
from src.utils.logger import app_logger
import json
import re


WRITER_SYSTEM_PROMPT = """You are an expert Technical Writer specializing in research reports.
Your job is to transform raw research into a beautifully structured, professional report.

The report MUST include:
1. **Executive Summary** - 2-3 sentence overview
2. **Introduction** - Context and why this topic matters  
3. **Key Findings** - Bullet-pointed main discoveries
4. **Detailed Analysis** - In-depth exploration of subtopics
5. **Data & Statistics** - Quantitative evidence (if available)
6. **Conclusion** - Summary and future outlook
7. **Sources** - All referenced URLs

Format using clear Markdown. Be professional, clear, and insightful.
Cite sources inline using [Source N] notation."""


def writer_agent(state: AgentState) -> AgentState:
    """
    Writer Agent Node.
    Produces the initial draft report from research.
    """
    app_logger.info(f"✍️ Writer Agent activated")

    state.iteration_count += 1
    if state.iteration_count > state.max_iterations:
        state.error = "Max iterations exceeded in writer"
        state.is_complete = True
        return state

    if not state.raw_research:
        state.error = "No research available for writing"
        state.is_complete = True
        return state

    llm = get_llm(temperature=0.6)  # Slightly creative for writing

    # Include critic feedback if this is a revision
    revision_context = ""
    if state.critic_feedback and state.revision_count > 0:
        revision_context = f"""
        
PREVIOUS CRITIC FEEDBACK (incorporate these improvements):
Score: {state.critic_feedback.score}/10
Weaknesses to fix: {', '.join(state.critic_feedback.weaknesses)}
Suggestions: {', '.join(state.critic_feedback.suggestions)}
"""

    messages = [
        SystemMessage(content=WRITER_SYSTEM_PROMPT),
        HumanMessage(
            content=f"Topic: {state.topic}\n\n"
                    f"Research Sections to Include: "
                    f"{', '.join(state.research_plan.estimated_sections if state.research_plan else [])}\n\n"
                    f"Raw Research:\n{state.raw_research}\n\n"
                    f"Sources Available:\n"
                    f"{chr(10).join([f'[{i+1}] {url}' for i, url in enumerate(state.sources)])}\n"
                    f"{revision_context}"
                    f"\nWrite a comprehensive, professional research report."
        )
    ]

    try:
        response = llm.invoke(messages)
        state.draft_report = response.content
        state.current_agent = "critic"
        
        app_logger.info(
            f"✅ Draft report written ({len(state.draft_report)} chars)"
        )

    except Exception as e:
        app_logger.error(f"❌ Writer failed: {e}")
        state.error = str(e)
        state.is_complete = True

    return state