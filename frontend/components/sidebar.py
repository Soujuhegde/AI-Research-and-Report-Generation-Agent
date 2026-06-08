"""
Sidebar Component - Reusable sidebar for all Streamlit pages.
Contains navigation, configuration, and system status.
"""
import streamlit as st
import os
from datetime import datetime
from typing import Optional


def render_sidebar(
    show_config: bool = True,
    show_history: bool = True,
    show_status: bool = True,
) -> dict:
    """
    Render the main application sidebar.
    
    Returns:
        dict: Configuration values selected by user
    """
    config = {}

    with st.sidebar:
        # Logo / Branding
        st.markdown("""
        <div style="text-align:center; padding:1rem 0; border-bottom:1px solid #333">
            <h2 style="color:#4CAF50; margin:0">🤖 Research AI</h2>
            <small style="color:#aaa">Multi-Agent System v1.0</small>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")  # spacer

        # Navigation
        st.markdown("### 📍 Navigation")
        st.page_link("app.py", label="🏠 Home", icon="🏠")
        st.page_link("pages/01_Research.py", label="🔬 Research", icon="🔬")
        st.page_link("pages/02_History.py", label="📚 History", icon="📚")
        st.page_link("pages/03_Settings.py", label="⚙️ Settings", icon="⚙️")

        st.markdown("---")

        # Configuration panel
        if show_config:
            st.markdown("### ⚙️ Agent Config")

            config["max_iterations"] = st.slider(
                "Max Iterations",
                min_value=5,
                max_value=20,
                value=10,
                help="Guards against infinite agent loops"
            )

            config["max_revisions"] = st.slider(
                "Max Revisions",
                min_value=0,
                max_value=3,
                value=2,
                help="How many times Critic can send back to Writer"
            )

            config["search_results"] = st.slider(
                "Search Results per Query",
                min_value=3,
                max_value=10,
                value=5,
                help="More results = better research, more API calls"
            )

            config["search_depth"] = st.selectbox(
                "Search Depth",
                options=["basic", "advanced"],
                index=1,
                help="Advanced search is more thorough but slower"
            )

            st.markdown("---")

        # Recent history preview
        if show_history:
            st.markdown("### 🕐 Recent Reports")
            _render_recent_reports()
            st.markdown("---")

        # System status
        if show_status:
            _render_system_status()

        # Footer
        st.markdown("""
        <div style="position:fixed; bottom:0; left:0; right:0; 
                    padding:10px; text-align:center; 
                    background:#0e1117; border-top:1px solid #333;
                    font-size:11px; color:#666">
            Built with 🤖 LangGraph + Sarvam AI + Streamlit
        </div>
        """, unsafe_allow_html=True)

    return config


def _render_recent_reports():
    """Show last 3 reports from disk."""
    reports_dir = "data/reports"
    os.makedirs(reports_dir, exist_ok=True)

    try:
        import json
        files = sorted(
            [f for f in os.listdir(reports_dir) if f.endswith(".json")],
            reverse=True
        )[:3]

        if not files:
            st.caption("No reports yet")
        else:
            for file in files:
                try:
                    with open(os.path.join(reports_dir, file)) as f:
                        data = json.load(f)
                    topic = data.get("topic", "Unknown")[:25]
                    st.markdown(f"📄 {topic}...")
                except Exception:
                    pass

    except Exception:
        st.caption("Could not load history")


def _render_system_status():
    """Show API connectivity status."""
    st.markdown("### 🔌 System Status")

    # Check env vars
    sarvam_ok = bool(os.getenv("SARVAM_API_KEY"))
    tavily_ok = bool(os.getenv("TAVILY_API_KEY"))

    def status_dot(ok: bool) -> str:
        return "🟢" if ok else "🔴"

    st.markdown(
        f"{status_dot(sarvam_ok)} **Sarvam AI** "
        f"({'Connected' if sarvam_ok else 'No API Key'})"
    )
    st.markdown(
        f"{status_dot(tavily_ok)} **Tavily Search** "
        f"({'Connected' if tavily_ok else 'No API Key'})"
    )

    if not sarvam_ok or not tavily_ok:
        st.warning(
            "⚠️ Missing API keys! "
            "Check your `.env` file or Settings page."
        )