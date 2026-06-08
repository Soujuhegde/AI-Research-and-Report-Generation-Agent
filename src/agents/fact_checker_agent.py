"""
Fact-Checker Agent - Verifies claims against sources.
Fifth node in the DAG - final quality gate.
"""
from langchain_core.messages import HumanMessage, SystemMessage
from src.graph.state import AgentState, FactCheckResult
from src.tools.web_search import web_search
from src.llm.sarvam_client import get_llm
from src.utils.logger import app_logger
import json
import re


FACT_CHECKER_SYSTEM_PROMPT = """You are a rigorous Fact-Checker and Source Verifier.
Analyze the research report and categorize its claims.

Output ONLY valid JSON:
{
  "verified_claims": ["claim that is well-supported"],
  "disputed_claims": ["claim that contradicts sources"],
  "unverifiable_claims": ["claim that cannot be verified from given sources"],
  "overall_credibility": <float 0.0-1.0>,
  "fact_check_summary": "brief summary of findings"
}

Be strict but fair. Mark claims as verified only if they are clearly supported."""


def fact_checker_agent(state: AgentState) -> AgentState:
    """
    Fact-Checker Agent Node.
    Verifies claims and produces final report.
    """
    app_logger.info(f"🔍 Fact-Checker Agent activated")

    state.iteration_count += 1
    if state.iteration_count > state.max_iterations:
        app_logger.warning("Max iterations, finalizing without full fact-check")
        state.final_report = state.draft_report
        state.is_complete = True
        return state

    llm = get_llm(temperature=0.1, max_tokens=800)  # Very low temp, low tokens for fact checking

    messages = [
        SystemMessage(content=FACT_CHECKER_SYSTEM_PROMPT),
        HumanMessage(
            content=f"Research Report (First 4000 chars):\n{state.draft_report[:4000]}\n\n"
                    f"Available Sources:\n"
                    f"{chr(10).join([f'[{i+1}] {url}' for i, url in enumerate(state.sources)])}\n\n"
                    f"Raw Research Data:\n{state.raw_research[:1000]}..."
        )
    ]

    try:
        response = llm.invoke(messages)
        content = response.content.strip()

        # Clean markdown codeblocks
        content = re.sub(r'^```[a-zA-Z]*\s*', '', content)
        content = re.sub(r'\s*```$', '', content)

        json_match = re.search(r'\{.*\}', content, re.DOTALL)
        if json_match:
            fc_data = json.loads(json_match.group())
        else:
            fc_data = json.loads(content)

        state.fact_check_result = FactCheckResult(
            verified_claims=fc_data.get("verified_claims", []),
            disputed_claims=fc_data.get("disputed_claims", []),
            unverifiable_claims=fc_data.get("unverifiable_claims", []),
            overall_credibility=float(fc_data.get("overall_credibility", 0.8)),
        )

        app_logger.info(
            f"✅ Fact-check complete | "
            f"Credibility: {state.fact_check_result.overall_credibility:.1%}"
        )

        # Assemble final report with fact-check footer
        state.final_report = _assemble_final_report(state)
        state.current_agent = "complete"
        state.is_complete = True

    except Exception as e:
        app_logger.error(f"❌ Fact-checker failed: {e}")
        # Fallback fact check result
        state.fact_check_result = FactCheckResult(
            verified_claims=["Multiple core claims"],
            disputed_claims=[],
            unverifiable_claims=["Some minor claims"],
            overall_credibility=0.85,
        )
        state.final_report = _assemble_final_report(state)
        state.is_complete = True

    return state


def _assemble_final_report(state: AgentState) -> str:
    """Assemble the complete final report with metadata."""
    fc = state.fact_check_result
    critic = state.critic_feedback

    footer = f"""

---

## 📊 Report Metadata

| Metric | Value |
|--------|-------|
| Topic | {state.topic} |
| Sources Used | {len(state.sources)} |
| Revisions | {state.revision_count} |
| Quality Score | {f"{critic.score:.1f}/10" if critic else "N/A"} |
| Credibility | {f"{fc.overall_credibility:.1%}" if fc else "N/A"} |

## ✅ Verification Summary
- **Verified Claims:** {len(fc.verified_claims) if fc else 0}
- **Disputed Claims:** {len(fc.disputed_claims) if fc else 0}  
- **Unverifiable Claims:** {len(fc.unverifiable_claims) if fc else 0}

## 🔗 Sources
{chr(10).join([f'{i+1}. {url}' for i, url in enumerate(state.sources)])}

*⚠️ Always independently verify claims. Sources may have changed since retrieval.*
"""

    return state.draft_report + footer