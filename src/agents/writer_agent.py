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
- Write ONLY the section requested.
- The target length is massive and highly detailed (thousands of words).
- Provide exhaustive content, case studies, and statistical breakdowns where relevant.
- Format using clear Markdown.
- Cite sources inline based on the raw research.
- **CRITICAL FORMATTING:** Use exactly the requested section name as your main `##` heading, with no extra words.
- **CRITICAL STRUCTURE:** You must use the exact `###` sub-headings requested.
- **ABSTRACT CONTENT:** If writing an Abstract or Preliminary Section, ensure you explain: why the topic was chosen, the exact problem being faced, and what research is being done.
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

    # Define strict structure
    strict_structure = {
        "Preliminary Section": "### 1. Title Page\n### 2. Acknowledgments (if any)\n### 3. Abstract\n### 4. Table of Contents\n### 5. List of Tables (if any)\n### 6. List of Figures (if any)",
        "Introduction": "### a. Statement of the Problem\n### b. Significance of the Problem (and historical background)\n### c. Purpose\n### d. Statement of Hypothesis\n### e. Assumptions\n### f. Limitations\n### g. Definition of Terms",
        "Review of Related Literature": "### (and analysis of previous research)",
        "Design of the Study": "### a. Description of Research Design and Procedures Used\n### b. Sources of Data\n### c. Sampling Procedures\n### d. Methods and Instruments of Data Gathering\n### e. Statistical Treatment",
        "Analysis of Data": "### a. text with appropriate\n### b. tables and\n### c. figures",
        "Summary and Conclusions": "### a. Restatement of the Problem\n### b. Description of Procedures\n### c. Major Findings (reject or fail to reject H₂)\n### d. Conclusions",
        "Reference Section": "### 1. End Notes (if in that format of citation)\n### 2. Bibliography or Literature Cited\n### 3. Appendix"
    }
    
    subheadings_prompt = strict_structure.get(current_section, "")

    messages = [
        SystemMessage(content=WRITER_SYSTEM_PROMPT),
        HumanMessage(
            content=f"Topic: {state.topic}\n\n"
                    f"SECTION TO WRITE RIGHT NOW: **{current_section}**\n\n"
                    f"CRITICAL RULES:\n"
                    f"1. Your VERY FIRST line must be exactly: `## {current_section}` (This is used for the UI Table of Contents)\n"
                    f"2. You MUST include these exact sub-headings:\n{subheadings_prompt}\n"
                    f"3. You MUST write comprehensive and detailed paragraphs under EVERY SINGLE sub-heading. DO NOT leave any sub-heading empty (especially the Abstract).\n"
                    f"4. For non-scientific topics, deduce logical equivalents for 'Hypothesis' or 'Sampling'.\n\n"
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