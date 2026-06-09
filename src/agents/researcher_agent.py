"""
Researcher Agent - Executes web searches and compiles raw research.
Second node in the DAG (after Planner).
"""
from langchain_core.messages import HumanMessage, SystemMessage
from src.graph.state import AgentState
from src.tools.web_search import search_and_summarize
from src.llm.sarvam_client import get_llm
from src.utils.logger import app_logger


RESEARCHER_SYSTEM_PROMPT = """You are an expert Academic Research Analyst. 
You have been given raw search results from the web. Your job is to conduct DEEP, EXHAUSTIVE RESEARCH and:
1. Synthesize the information coherently, focusing on extreme academic rigor.
2. Identify and exhaustively list ALL key facts, statistical data points, and historical background information.
3. Extract and detail the research design, procedures, and methodologies used in the provided literature.
4. Note the sources for each claim clearly.
5. Highlight any conflicting information and structure findings by the provided subtopics.

Be extremely thorough, highly detailed, and extensive. Do not summarize briefly; provide an immense amount of detail suitable for a 20-page academic paper."""


def researcher_agent(state: AgentState) -> AgentState:
    """
    Researcher Agent Node.
    Performs web searches and synthesizes raw research.
    """
    app_logger.info(f"🔬 Researcher Agent activated")

    state.iteration_count += 1
    if state.iteration_count > state.max_iterations:
        state.error = "Max iterations exceeded in researcher"
        state.is_complete = True
        return state

    if not state.research_plan:
        state.error = "No research plan available"
        state.is_complete = True
        return state

    # Execute all search queries
    app_logger.info(
        f"📡 Running {len(state.research_plan.search_queries)} searches..."
    )
    
    search_results, compiled_text = search_and_summarize(
        state.research_plan.search_queries
    )

    state.search_results = search_results
    state.sources = [r.url for r in search_results if r.url]

    if not state.sources:
        state.error = "Web search failed to return any sources. Please check if your TAVILY_API_KEY is valid and has remaining quota in Render."
        state.is_complete = True
        return state

    # Use LLM to synthesize the research
    llm = get_llm(temperature=0.4, max_tokens=4000)

    messages = [
        SystemMessage(content=RESEARCHER_SYSTEM_PROMPT),
        HumanMessage(
            content=f"Topic: {state.topic}\n\n"
                    f"Subtopics to cover: {', '.join(state.research_plan.subtopics)}\n\n"
                    f"Web Search Results:\n{compiled_text}\n\n"
                    f"Please synthesize this research comprehensively."
        )
    ]

    try:
        response = llm.invoke(messages)
        state.raw_research = response.content

        state.current_agent = "writer"
        app_logger.info(
            f"✅ Research complete. Found {len(search_results)} sources."
        )

    except Exception as e:
        app_logger.error(f"❌ Researcher synthesis failed: {e}")
        state.raw_research = compiled_text  # Use raw results as fallback
        state.current_agent = "writer"

    return state