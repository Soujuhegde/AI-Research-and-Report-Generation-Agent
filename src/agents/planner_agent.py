"""
Planner Agent - Analyzes the research topic and creates a structured plan.
First node in the DAG.
"""
from langchain_core.messages import HumanMessage, SystemMessage
from src.graph.state import AgentState, ResearchPlan
from src.llm.sarvam_client import get_llm
from src.utils.logger import app_logger
import json
import re


PLANNER_SYSTEM_PROMPT = """You are an expert Research Planner. Your job is to analyze 
a research topic and create a comprehensive, structured research plan.

Given a topic, you must output a JSON research plan with:
1. subtopics: List of 6-10 key subtopics to investigate.
2. search_queries: List of 15-20 specific web search queries for deep research.
3. estimated_sections: List of exact report sections to be used. MUST exactly be: ["Preliminary Section", "Introduction", "Review of Related Literature", "Design of the Study", "Analysis of Data", "Summary and Conclusions", "Reference Section"]

Always respond with valid JSON only. No markdown, no explanation outside JSON.

Example output:
{
  "subtopics": ["historical background", "statistical data", "analysis", "future outlook"],
  "search_queries": ["query 1", "query 2", "query 3", "query 4"],
  "estimated_sections": ["Preliminary Section", "Introduction", "Review of Related Literature", "Design of the Study", "Analysis of Data", "Summary and Conclusions", "Reference Section"]
}"""


def planner_agent(state: AgentState) -> AgentState:
    """
    Planner Agent Node.
    Creates a structured research plan from the topic.
    """
    app_logger.info(f"🗺️ Planner Agent activated for topic: '{state.topic}'")

    # Guard: check iteration limit
    state.iteration_count += 1
    if state.iteration_count > state.max_iterations:
        state.error = "Max iterations exceeded in planner"
        state.is_complete = True
        return state

    llm = get_llm(temperature=0.3)  # Low temp for structured output

    messages = [
        SystemMessage(content=PLANNER_SYSTEM_PROMPT),
        HumanMessage(
            content=f"Create a research plan for this topic: {state.topic}\n"
                    f"Additional instructions: {state.user_instructions or 'None'}"
        )
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        # Extract JSON from response
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            plan_data = json.loads(json_match.group())
        else:
            plan_data = json.loads(content)

        state.research_plan = ResearchPlan(
            topic=state.topic,
            subtopics=plan_data.get("subtopics", []),
            search_queries=plan_data.get("search_queries", []),
            estimated_sections=plan_data.get("estimated_sections", []),
        )

        state.current_agent = "researcher"
        app_logger.info(
            f"✅ Research plan created with "
            f"{len(state.research_plan.search_queries)} queries"
        )

    except Exception as e:
        app_logger.error(f"❌ Planner failed: {e}")
        # Fallback plan
        state.research_plan = ResearchPlan(
            topic=state.topic,
            subtopics=[f"{state.topic} historical background", f"{state.topic} statistics", f"{state.topic} methodology"],
            search_queries=[
                f"{state.topic} comprehensive overview",
                f"{state.topic} latest academic developments",
                f"{state.topic} key statistics and data",
                f"{state.topic} research methodology",
                f"{state.topic} historical background",
                f"{state.topic} future outlook",
            ],
            estimated_sections=["Preliminary Section", "Introduction", "Review of Related Literature", "Design of the Study", "Analysis of Data", "Summary and Conclusions", "Reference Section"],
        )
        state.current_agent = "researcher"

    return state