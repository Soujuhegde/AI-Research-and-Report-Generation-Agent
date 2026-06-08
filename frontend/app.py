"""
Streamlit Frontend - Main Application Entry Point
Single-page minimal architecture.
"""
import streamlit as st
import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from frontend.components.theme import apply_theme
from frontend.components.report_viewer import display_full_report

st.set_page_config(
    page_title="Research AI",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Apply global premium SaaS theme
apply_theme()


def main():
    # Hide sidebar toggle button completely to ensure a pure single page feel
    st.markdown(
        """
        <style>
            [data-testid="collapsedControl"] { display: none; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Hero Section
    st.markdown("""
    <div class="hero-banner">
        <h1>Research Intelligence</h1>
        <p>A minimal, clean AI assistant to research any topic and write comprehensive reports.</p>
    </div>
    """, unsafe_allow_html=True)

    # Main Input Area (Centered Search Engine Style)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        with st.form("research_form", clear_on_submit=False):
            topic = st.text_input(
                "Topic",
                placeholder="e.g. How will Generative AI impact healthcare by 2030?",
                label_visibility="collapsed"
            )
            
            instructions = st.text_area(
                "Instructions (Optional)",
                placeholder="e.g., 'Focus on emerging markets', 'Target: non-technical audience'",
                height=80,
                label_visibility="collapsed"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            # Center the submit button
            c1, c2, c3 = st.columns([1, 1, 1])
            with c2:
                submitted = st.form_submit_button("Start Research", type="primary", use_container_width=True)

    if submitted and topic:
        _execute_research(topic, instructions)


def _execute_research(topic: str, instructions: str):
    """Run the research pipeline with a progress UI."""
    from src.graph.workflow import run_research_pipeline

    st.divider()
    st.markdown(f"<h2>Researching: {topic}</h2>", unsafe_allow_html=True)

    progress_bar = st.progress(0)
    status_placeholder = st.empty()
    status_placeholder.info("Initializing...", icon="🔄")

    # Metrics placeholders
    m1, m2, m3, m4 = st.columns(4)
    sources_ph = m1.empty()
    score_ph = m2.empty()
    cred_ph = m3.empty()
    iter_ph = m4.empty()

    def add_log(msg: str):
        pass # UI logging removed as per user request

    add_log(f"Starting pipeline for: '{topic}'")

    try:
        progress_bar.progress(10)
        status_placeholder.info("Planner working...", icon="🗺️")
        add_log("Planner agent activated...")

        # We don't have config sliders anymore, use sensible defaults
        final_state = run_research_pipeline(
            topic=topic,
            user_instructions=instructions or None,
            max_iterations=30,
        )

        progress_bar.progress(100)
        status_placeholder.success(f"Research complete for: {topic}", icon="✅")

        score_str = f"{final_state.critic_feedback.score:.1f}/10" if final_state.critic_feedback else "N/A"
        cred_str = f"{final_state.fact_check_result.overall_credibility:.1%}" if final_state.fact_check_result else "N/A"

        add_log("Pipeline complete.")
        add_log(f"Sources: {len(final_state.sources)}")
        add_log(f"Quality score: {score_str}")
        add_log(f"Credibility: {cred_str}")

        sources_ph.metric("Sources", len(final_state.sources))
        score_ph.metric("Quality", score_str)
        cred_ph.metric("Credibility", cred_str)
        iter_ph.metric("Steps Taken", final_state.iteration_count)

        st.markdown("<br>", unsafe_allow_html=True)
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
            state_dict=final_state.model_dump(),
        )

    except Exception as e:
        progress_bar.progress(0)
        status_placeholder.error(f"Research failed: {str(e)}", icon="❌")
        add_log(f"ERROR: {str(e)}")
        st.exception(e)


if __name__ == "__main__":
    main()