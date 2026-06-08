"""
Critic Agent - Reviews the draft report and provides structured feedback.
Fourth node with conditional loop back to Writer.
"""
from langchain_core.messages import HumanMessage, SystemMessage
from src.graph.state import AgentState, CriticFeedback
from src.llm.sarvam_client import get_llm
from src.utils.logger import app_logger
import json
import re


CRITIC_SYSTEM_PROMPT = """You are a Critical Academic Editor with extremely high standards.
Review the given research report and provide structured feedback.

Output ONLY valid JSON with this exact structure:
{
  "score": <float 0-10>,
  "strengths": ["strength 1", "strength 2"],
  "weaknesses": ["weakness 1", "weakness 2"],  
  "suggestions": ["suggestion 1", "suggestion 2"],
  "needs_revision": <true/false>
}

Score rubric:
- 9-10: Publication-ready, excellent depth and citations
- 7-8: Good quality, minor improvements needed
- 5-6: Acceptable but needs significant improvement
- Below 5: Major revision required

Set needs_revision=false only if score >= 8.0"""


def critic_agent(state: AgentState) -> AgentState:
    """
    Critic Agent Node.
    Reviews draft and decides if revision is needed.
    """
    app_logger.info(f"🎭 Critic Agent reviewing draft (revision #{state.revision_count})")

    state.iteration_count += 1
    if state.iteration_count > state.max_iterations:
        app_logger.warning("Max iterations reached, skipping to fact-checker")
        state.current_agent = "fact_checker"
        return state

    if not state.draft_report:
        state.current_agent = "fact_checker"
        return state

    llm = get_llm(temperature=0.2, max_tokens=800)  # Low temp, low tokens for evaluation

    messages = [
        SystemMessage(content=CRITIC_SYSTEM_PROMPT),
        HumanMessage(
            content=f"Research Report to Review (First 4000 chars):\n\n{state.draft_report[:4000]}\n\n"
                    f"Original Topic: {state.topic}\n"
                    f"This is revision #{state.revision_count}"
        )
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        # Clean markdown codeblocks
        content = re.sub(r'^```[a-zA-Z]*\s*', '', content)
        content = re.sub(r'\s*```$', '', content)
        
        # Extract JSON
        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            feedback_data = json.loads(json_match.group())
        else:
            feedback_data = json.loads(content)

        state.critic_feedback = CriticFeedback(
            score=float(feedback_data.get("score", 7.0)),
            strengths=feedback_data.get("strengths", []),
            weaknesses=feedback_data.get("weaknesses", []),
            suggestions=feedback_data.get("suggestions", []),
            needs_revision=feedback_data.get("needs_revision", False),
        )

        app_logger.info(
            f"📊 Critic score: {state.critic_feedback.score}/10 | "
            f"Needs revision: {state.critic_feedback.needs_revision}"
        )

        # Decide next step
        if (state.critic_feedback.needs_revision 
                and state.revision_count < state.max_revisions):
            state.revision_count += 1
            state.current_section_index = 0
            state.report_sections = []
            state.current_agent = "writer"  # Loop back
            app_logger.info(f"🔄 Sending back for revision #{state.revision_count}")
        else:
            state.current_agent = "fact_checker"
            app_logger.info("➡️ Moving to fact-checker")

    except Exception as e:
        app_logger.error(f"❌ Critic failed: {e}")
        # Fallback feedback
        state.critic_feedback = CriticFeedback(
            score=7.0,
            strengths=["Comprehensive overview"],
            weaknesses=["Formatting issues"],
            suggestions=["Improve structure"],
            needs_revision=False,
        )
        state.current_agent = "fact_checker"

    return state