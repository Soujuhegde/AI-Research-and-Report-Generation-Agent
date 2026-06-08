"""
Streamlit Frontend - Main Application Entry Point
Multi-Agent Research & Report Generation System
"""
import streamlit as st
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(
    page_title="Multi-Agent Research System",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get Help": "https://github.com/yourusername/multi-agent-research",
        "About": "Multi-Agent Research & Report Generation System",
    }
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        margin-bottom: 2rem;
        text-align: center;
    }
    .agent-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin: 2px;
    }
    .stProgress .st-bo { background-color: #4CAF50; }
    .metric-card {
        background: #f8f9fa;
        border-left: 4px solid #4CAF50;
        padding: 1rem;
        border-radius: 4px;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)


def main():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Multi-Agent Research System</h1>
        <p>Orchestrate AI agents to research any topic and generate structured reports</p>
        <p>
            <span style="background:#4CAF50;padding:4px 10px;border-radius:20px;font-size:12px">Planner</span>
            <span style="color:white">→</span>
            <span style="background:#2196F3;padding:4px 10px;border-radius:20px;font-size:12px">Researcher</span>
            <span style="color:white">→</span>
            <span style="background:#FF9800;padding:4px 10px;border-radius:20px;font-size:12px">Writer</span>
            <span style="color:white">→</span>
            <span style="background:#9C27B0;padding:4px 10px;border-radius:20px;font-size:12px">Critic</span>
            <span style="color:white">→</span>
            <span style="background:#F44336;padding:4px 10px;border-radius:20px;font-size:12px">Fact-Checker</span>
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.markdown("## ⚙️ Configuration")
        max_iterations = st.slider("Max Iterations", 5, 20, 10)
        max_revisions = st.slider("Max Revisions", 0, 3, 2)
        search_results = st.slider("Search Results per Query", 3, 10, 5)

        st.markdown("---")
        st.markdown("## 📊 Agent Pipeline")
        st.markdown("""
        1. 🗺️ **Planner** - Creates research plan
        2. 🔬 **Researcher** - Web search & synthesis  
        3. ✍️ **Writer** - Drafts the report
        4. 🎭 **Critic** - Reviews & scores
        5. 🔍 **Fact-Checker** - Verifies claims
        """)

        st.markdown("---")
        st.markdown("## 🔗 Quick Links")
        st.markdown("- [View History](History)")
        st.markdown("- [Settings](Settings)")

    # Main research interface
    col1, col2 = st.columns([3, 1])

    with col1:
        topic = st.text_input(
            "🎯 Research Topic",
            placeholder="e.g., Impact of AI on healthcare in 2024",
            help="Enter any topic you want to research"
        )

    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        run_button = st.button(
            "🚀 Start Research",
            type="primary",
            use_container_width=True,
            disabled=not topic
        )

    instructions = st.text_area(
        "📝 Additional Instructions (Optional)",
        placeholder="e.g., Focus on recent developments, include statistics, target audience: non-technical",
        height=80,
    )

    # Example topics
    st.markdown("### 💡 Example Topics")
    example_cols = st.columns(4)
    examples = [
        "AI in Healthcare 2024",
        "Quantum Computing Progress",
        "Climate Change Solutions",
        "Web3 & DeFi Trends",
    ]
    for i, (col, example) in enumerate(zip(example_cols, examples)):
        with col:
            if st.button(f"🔍 {example}", key=f"ex_{i}", use_container_width=True):
                st.session_state.example_topic = example
                st.rerun()

    # Handle example topic selection
    if "example_topic" in st.session_state:
        topic = st.session_state.example_topic
        del st.session_state.example_topic

    # Run research pipeline
    if run_button and topic:
        _run_research(topic, instructions, max_iterations, max_revisions)


def _run_research(topic: str, instructions: str, max_iterations: int, max_revisions: int):
    """Execute the research pipeline with live progress updates."""
    from src.graph.workflow import run_research_pipeline

    st.markdown("---")
    st.markdown(f"## 🔄 Researching: *{topic}*")

    # Progress tracking
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    agent_stages = {
        "planner": ("🗺️ Planning research strategy...", 15),
        "researcher": ("🔬 Searching the web & synthesizing...", 45),
        "writer": ("✍️ Writing the report...", 65),
        "critic": ("🎭 Reviewing quality...", 80),
        "fact_checker": ("🔍 Fact-checking claims...", 95),
    }

    # Live status containers
    col1, col2, col3 = st.columns(3)
    with col1:
        sources_metric = st.empty()
    with col2:
        score_metric = st.empty()
    with col3:
        credibility_metric = st.empty()

    log_container = st.expander("📋 Agent Logs", expanded=True)

    try:
        # Update UI to show pipeline started
        status_text.info("🚀 Initializing multi-agent pipeline...")
        progress_bar.progress(5)

        with log_container:
            st.write("🚀 Pipeline started...")

        # Run the pipeline
        final_state = run_research_pipeline(
            topic=topic,
            user_instructions=instructions if instructions else None,
            max_iterations=max_iterations,
        )

        # Update metrics
        progress_bar.progress(100)
        status_text.success("✅ Research complete!")

        with col1:
            sources_metric.metric("Sources Found", len(final_state.sources))
        with col2:
            score = final_state.critic_feedback.score if final_state.critic_feedback else 0
            score_metric.metric("Quality Score", f"{score:.1f}/10")
        with col3:
            cred = final_state.fact_check_result.overall_credibility if final_state.fact_check_result else 0
            credibility_metric.metric("Credibility", f"{cred:.1%}")

        # Display report
        _display_report(final_state, topic)

    except Exception as e:
        st.error(f"❌ Pipeline failed: {str(e)}")
        st.exception(e)


def _display_report(state, topic: str):
    """Display the final report with tabs."""
    from src.utils.pdf_exporter import export_to_pdf
    import json

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "📄 Final Report",
        "🔍 Research Data", 
        "📊 Analysis",
        "⬇️ Export"
    ])

    with tab1:
        if state.final_report:
            st.markdown(state.final_report)
        else:
            st.warning("No report generated")

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🗺️ Research Plan")
            if state.research_plan:
                st.json(state.research_plan.dict())
        with col2:
            st.markdown("### 🔗 Sources")
            for i, url in enumerate(state.sources, 1):
                st.markdown(f"{i}. [{url}]({url})")

    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("### 🎭 Critic Feedback")
            if state.critic_feedback:
                fc = state.critic_feedback
                st.metric("Score", f"{fc.score}/10")
                st.markdown("**Strengths:**")
                for s in fc.strengths:
                    st.markdown(f"✅ {s}")
                st.markdown("**Areas for Improvement:**")
                for w in fc.weaknesses:
                    st.markdown(f"⚠️ {w}")
        with col2:
            st.markdown("### ✅ Fact-Check Results")
            if state.fact_check_result:
                fct = state.fact_check_result
                st.metric("Credibility", f"{fct.overall_credibility:.1%}")
                st.markdown(f"✅ Verified: {len(fct.verified_claims)} claims")
                st.markdown(f"⚠️ Disputed: {len(fct.disputed_claims)} claims")
                st.markdown(f"❓ Unverifiable: {len(fct.unverifiable_claims)} claims")

    with tab4:
        st.markdown("### ⬇️ Export Report")
        col1, col2 = st.columns(2)

        with col1:
            if state.final_report:
                st.download_button(
                    label="📄 Download Markdown",
                    data=state.final_report,
                    file_name=f"report_{topic[:30]}.md",
                    mime="text/markdown",
                    use_container_width=True,
                )

        with col2:
            if st.button("📑 Generate PDF", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    try:
                        pdf_path = export_to_pdf(state.final_report, topic)
                        with open(pdf_path, "rb") as f:
                            st.download_button(
                                label="⬇️ Download PDF",
                                data=f.read(),
                                file_name=f"report_{topic[:30]}.pdf",
                                mime="application/pdf",
                                use_container_width=True,
                            )
                    except Exception as e:
                        st.error(f"PDF generation failed: {e}")

        with col1:
            report_json = json.dumps({
                "topic": state.topic,
                "report": state.final_report,
                "sources": state.sources,
                "metadata": {
                    "quality_score": state.critic_feedback.score if state.critic_feedback else None,
                    "credibility": state.fact_check_result.overall_credibility if state.fact_check_result else None,
                }
            }, indent=2)
            st.download_button(
                label="📊 Download JSON",
                data=report_json,
                file_name=f"report_{topic[:30]}.json",
                mime="application/json",
                use_container_width=True,
            )


if __name__ == "__main__":
    main()