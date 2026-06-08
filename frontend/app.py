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
        <p>A premium AI platform for deep academic research, synthesis, and automated report generation.</p>
    </div>
    """, unsafe_allow_html=True)

    # Main Input Area (Centered Search Engine Style)
    col1, col2, col3 = st.columns([1, 6, 1])
    with col2:
        with st.form("research_form", clear_on_submit=False):
            topic = st.text_input(
                "Topic",
                placeholder="Enter your research topic... (e.g., 'Impact of Generative AI on Global Markets')",
                label_visibility="collapsed"
            )
            
            instructions = st.text_area(
                "Instructions (Optional)",
                placeholder="Specific instructions or focus areas (e.g., 'Focus heavily on emerging markets', 'Ensure academic tone')...",
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
    st.divider()

    # Create UI placeholders immediately for instant feedback
    progress_bar = st.progress(5)
    status_placeholder = st.empty()
    
    # Instant funny feedback before the heavy imports block the thread
    status_placeholder.info("Waking up the AI hamsters... 🐹 Please hold!", icon="☕")

    # Now do the heavy backend imports
    from src.graph.workflow import run_research_pipeline

    try:
        progress_bar.progress(15)
        status_placeholder.info("Brewing coffee for the research agents... ☕ Deploying Planner!", icon="🚀")

        final_state = run_research_pipeline(
            topic=topic,
            user_instructions=instructions or None,
            max_iterations=30,
        )

        # Clear loading UI for a clean transition
        progress_bar.empty()
        status_placeholder.empty()

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
        st.exception(e)


if __name__ == "__main__":
    main()