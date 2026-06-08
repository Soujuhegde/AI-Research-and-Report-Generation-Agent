"""
Report Assembler Agent - Concatenates section parts into the final draft_report.
Fourth node in the DAG.
"""
from src.graph.state import AgentState
from src.utils.logger import app_logger

def assembler_agent(state: AgentState) -> AgentState:
    """
    Assembler Agent Node.
    Joins the individual report_sections into a single draft_report.
    """
    app_logger.info(f"🧩 Assembler Agent activated")
    
    if not state.report_sections:
        state.error = "No report sections available to assemble."
        state.is_complete = True
        return state

    # Combine sections
    combined_content = []
    for section in state.report_sections:
        combined_content.append(section.content)
        combined_content.append("\n\n---\n\n")

    state.draft_report = "".join(combined_content)
    state.current_agent = "critic"
    
    app_logger.info(f"✅ Report assembled ({len(state.draft_report)} chars)")

    return state
