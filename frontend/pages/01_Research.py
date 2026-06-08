"""
Research Page - Dedicated full-screen research interface.
This is Page 1 in the Streamlit multipage app.
"""
import streamlit as st
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

st.set_page_config(
    page_title="Research | Multi-Agent System",
    page_icon="🔬",
    layout="wide",
)

from frontend.components.sidebar import render_sidebar
from frontend.components.report_viewer import display_full_report


def main():
    # Render sidebar and get config
    config = render_sidebar()

    st.title("🔬 Start New Research")
    st.markdown(
        "Enter any topic below. The AI agent crew will plan, search, "
        "write, review, and fact-check a comprehensive report."
    )

    # Research form
    with st.form("research_form", clear_on_submit=False):
        topic = st.text_input(
            "📌 Research Topic *",
            placeholder="e.g., Generative AI impact on education in 2024",
            help="Be specific for better results"
        )

        instructions = st.text_area(
            "📝 Additional Instructions",
            placeholder=(
                "Optional: e.g., 'Focus on emerging markets', "
                "'Include statistics', 'Target: non-technical audience'"
            ),
            height=80,
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            submitted = st.form_submit_button(
                "🚀 Start Research",
                type="primary",
                use_container_width=True,
            )
        with col2:
            st.form_submit_button(
                "🔄 Clear",
                use_container_width=True,
            )

    # Quick topic suggestions
    st.markdown("### 💡 Try These Topics")
    suggestion_cols = st.columns(4)
    suggestions = [
        ("🏥", "AI in Healthcare"),
        ("⚡", "Renewable Energy 2024"),
        ("🚀", "Space Exploration Trends"),
        ("💰", "DeFi & Web3 Finance"),
        ("🌍", "Climate Change Solutions"),
        ("🤖", "LLM Capabilities 2024"),
        ("🧬", "CRISPR Gene Editing"),
        ("📱", "5G & 6G Networks"),
    ]

    for i, col in enumerate(st.columns(4)):
        with col:
            emoji, text = suggestions[i]
            if st.button(f"{emoji} {text}", key=f"sug_{i}", use_container_width=True):
                st.session_state["prefill_topic"] = text
                st.rerun()

    for i, col in enumerate(st.columns(4)):
        with col:
            emoji, text = suggestions[i + 4]
            if st.button(f"{emoji} {text}", key=f"sug_{i+4}", use_container_width=True):
                st.session_state["prefill_topic"] = text
                st.rerun()

    # Handle prefilled topic
    if "prefill_topic" in st.session_state:
        st.info(f"💡 Topic selected: **{st.session_state['prefill_topic']}** — Click 'Start Research'")

    # Execute research
    actual_topic = (
        st.session_state.get("prefill_topic", "")
        if not topic
        else topic
    )

    if submitted and actual_topic:
        if "prefill_topic" in st.session_state:
            del st.session_state["prefill_topic"]

        _execute_research(
            topic=actual_topic,
            instructions=instructions,
            config=config,
        )


def _execute_research(topic: str, instructions: str, config: dict):
    """Run the research pipeline with a progress UI."""
    from src.graph.workflow import run_research_pipeline

    st.markdown("---")
    st.markdown(f"## 🔄 Researching: *{topic}*")

    # Agent progress tracking
    agent_steps = [
        ("🗺️ Planner", "Creating research strategy..."),
        ("🔬 Researcher", "Searching the web..."),
        ("✍️ Writer", "Writing the report..."),
        ("🎭 Critic", "Reviewing quality..."),
        ("🔍 Fact-Checker", "Verifying claims..."),
    ]

    progress_bar = st.progress(0, text="Initializing...")
    status_placeholder = st.empty()

    # Metrics placeholders
    m1, m2, m3, m4 = st.columns(4)
    sources_ph = m1.empty()
    score_ph = m2.empty()
    cred_ph = m3.empty()
    iter_ph = m4.empty()

    log_area = st.expander("📋 Live Agent Logs", expanded=True)

    with log_area:
        log_placeholder = st.empty()
        logs = []

        def add_log(msg: str):
            logs.append(f"[{time.strftime('%H:%M:%S')}] {msg}")
            log_placeholder.code("\n".join(logs[-20:]))  # Show last 20 lines

    add_log(f"🚀 Starting pipeline for: '{topic}'")
    add_log(f"⚙️ Config: iterations={config.get('max_iterations', 10)}, revisions={config.get('max_revisions', 2)}")

    try:
        progress_bar.progress(10, text="🗺️ Planner working...")
        add_log("🗺️ Planner agent activated...")

        final_state = run_research_pipeline(
            topic=topic,
            user_instructions=instructions or None,
            max_iterations=config.get("max_iterations", 10),
        )

        progress_bar.progress(100, text="✅ Complete!")
        status_placeholder.success(f"🎉 Research complete for: **{topic}**")

        add_log(f"✅ Pipeline complete!")
        add_log(f"📊 Sources: {len(final_state.sources)}")
        add_log(f"⭐ Quality score: {final_state.critic_feedback.score if final_state.critic_feedback else 'N/A'}/10")
        add_log(f"✅ Credibility: {final_state.fact_check_result.overall_credibility if final_state.fact_check_result else 'N/A':.1%}")

        # Update metrics
        sources_ph.metric("🔗 Sources", len(final_state.sources))
        score_ph.metric("⭐ Quality", f"{final_state.critic_feedback.score if final_state.critic_feedback else 0:.1f}/10")
        cred_ph.metric("✅ Credibility", f"{final_state.fact_check_result.overall_credibility if final_state.fact_check_result else 0:.1%}")
        iter_ph.metric("🔄 Iterations", final_state.iteration_count)

        # Display full report
        st.markdown("---")
        display_full_report(
            report_markdown=final_state.final_report,
            topic=topic,
            sources=final_state.sources,
            metadata={
                "total_sources": len(final_state.sources),
                "quality_score": final_state.critic_feedback.score if final_state.critic_feedback else 0,
                "credibility": final_state.fact_check_result.overall_credibility if final_state.fact_check_result else 0,
                "revision_count": final_state.revision_count,
            },
            state_dict=final_state.dict(),
        )

    except Exception as e:
        progress_bar.progress(0)
        status_placeholder.error(f"❌ Research failed: {str(e)}")
        add_log(f"❌ ERROR: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()