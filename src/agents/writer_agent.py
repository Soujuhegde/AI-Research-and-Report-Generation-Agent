"""
Writer Agent - Transforms research into a structured, polished report section by section.
Third node in the DAG. Loops back to itself until all sections are written.
"""
from langchain_core.messages import HumanMessage, SystemMessage
from src.graph.state import AgentState, ReportSection
from src.llm.sarvam_client import get_llm
from src.utils.logger import app_logger

WRITER_SYSTEM_PROMPT = """You are an expert Technical Writer specializing in massive, highly detailed academic research reports.
Your job is to take raw research and write ONE specific section of a larger 20-page report.

CRITICAL INSTRUCTIONS FOR THIS SECTION:
- Write ONLY the section requested. Do not write the introduction unless it is the requested section. Do not write the conclusion unless requested.
- The target length for this single section is massive and highly detailed (thousands of words).
- DO NOT summarize briefly. You MUST expand exhaustively.
- Provide multiple extensive case studies, statistical breakdowns, methodological deep-dives, and detailed historical context where relevant.
- Format using clear Markdown. Use `#` for the main section title and `##` or `###` for sub-sections.
- Cite sources inline based on the raw research.
- Be extremely verbose, highly analytical, and extensive.
"""

def writer_agent(state: AgentState) -> AgentState:
    """
    Section Writer Agent Node.
    Writes the report one section at a time.
    """
    
    if not state.research_plan or not state.research_plan.estimated_sections:
        state.error = "No estimated sections found to write."
        state.is_complete = True
        return state

    current_section = state.research_plan.estimated_sections[state.current_section_index]
    app_logger.info(f"✍️ Section Writer Agent writing: '{current_section}'")

    state.iteration_count += 1
    if state.iteration_count > state.max_iterations:
        state.error = "Max iterations exceeded in writer"
        state.is_complete = True
        return state

    if not state.raw_research:
        state.error = "No research available for writing"
        state.is_complete = True
        return state

    llm = get_llm(temperature=0.6, max_tokens=4000)

    # Include critic feedback if this is a revision.
    revision_context = ""
    if state.critic_feedback and state.revision_count > 0:
        revision_context = f"""
        
PREVIOUS CRITIC FEEDBACK (incorporate these improvements across all sections):
Score: {state.critic_feedback.score}/10
Weaknesses to fix: {', '.join(state.critic_feedback.weaknesses)}
Suggestions: {', '.join(state.critic_feedback.suggestions)}
"""

    messages = [
        SystemMessage(content=WRITER_SYSTEM_PROMPT),
        HumanMessage(
            content=f"Topic: {state.topic}\n\n"
                    f"Report Sections Plan: {', '.join(state.research_plan.estimated_sections)}\n"
                    f"SECTION TO WRITE RIGHT NOW: **{current_section}**\n\n"
                    f"Raw Research:\n{state.raw_research}\n\n"
                    f"Sources Available:\n"
                    f"{chr(10).join([f'[{i+1}] {url}' for i, url in enumerate(state.sources)])}\n"
                    f"{revision_context}"
                    f"\nWrite an extremely exhaustive and massive deep dive ONLY for the section: {current_section}."
        )
    ]

    try:
        response = llm.invoke(messages)
        content = response.content

        # Append to report_sections
        section = ReportSection(
            title=current_section,
            content=content,
            sources=state.sources
        )
        state.report_sections.append(section)
        
        state.current_section_index += 1
        
        if state.current_section_index < len(state.research_plan.estimated_sections):
            state.current_agent = "writer" # Loop
        else:
            state.current_agent = "assembler" # Next step
            
        app_logger.info(f"✅ Section '{current_section}' written ({len(content)} chars)")

    except Exception as e:
        app_logger.error(f"❌ Writer failed on section '{current_section}': {e}")
        state.error = str(e)
        state.is_complete = True

    return state