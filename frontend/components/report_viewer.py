"""
Report Viewer Component - Reusable Streamlit component for displaying reports.
Used across multiple pages to render research reports consistently.
"""
import streamlit as st
import json
import os
from typing import Optional
from datetime import datetime


def render_agent_timeline(state_dict: dict):
    """Render a visual timeline of agent execution."""
    agents = [
        ("Planner", "Created research plan", True),
        ("Researcher", f"Found {len(state_dict.get('sources', []))} sources", True),
        ("Section Writer", f"Wrote {state_dict.get('current_section_index', 0)} sections", True),
        ("Assembler", "Combined report", True),
        ("Critic", f"Score: {state_dict.get('critic_feedback', {}).get('score', 'N/A') if state_dict.get('critic_feedback') else 'N/A'}/10", True),
        ("Fact-Checker", "Verified claims", True),
    ]

    html = "<div style='position: relative; padding-left: 20px; border-left: 2px solid #E2E8F0; margin-left: 10px; margin-top: 10px;'>"
    
    for i, (agent, action, done) in enumerate(agents):
        color = "#2563EB" if done else "#CBD5E1"
        html += f'''
<div style="position: relative; margin-bottom: 1.25rem;">
    <div style="position: absolute; left: -27px; top: 12px; width: 12px; height: 12px; border-radius: 50%; background: {color}; border: 2px solid white;"></div>
    <div style="background: transparent; padding: 0.5rem 1rem;">
        <strong style="color:#0F172A; display:block; margin-bottom: 0.15rem; font-size: 0.9rem;">{agent}</strong>
        <span style="color:#64748B; font-size: 0.8rem;">{action}</span>
    </div>
</div>
'''
        
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)


def render_export_buttons(
    report_markdown: str,
    topic: str,
    report_json: dict = None,
):
    """Render download buttons for various export formats as a grid."""
    
    # We use Streamlit columns to layout the buttons as a grid (3 buttons)
    html = '<div class="quick-actions-grid">'
    st.markdown(html, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    
    with c1:
        if report_markdown:
            try:
                from src.utils.pdf_exporter import export_to_pdf
                pdf_path = export_to_pdf(report_markdown, topic)

                with open(pdf_path, "rb") as f:
                    pdf_bytes = f.read()

                st.download_button(
                    label="📄\nPDF",
                    data=pdf_bytes,
                    file_name=f"report_{topic[:30].replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key=f"dl_pdf_{hash(topic)}",
                )
            except Exception as e:
                st.error("PDF failed")
                
    with c2:
        if report_markdown:
            st.download_button(
                label="⬇️\nMD",
                data=report_markdown.encode("utf-8"),
                file_name=f"report_{topic[:30].replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True,
                key=f"dl_md_{hash(topic)}",
            )
            
    with c3:
        if report_json:
            st.download_button(
                label="📊\nData",
                data=json.dumps(report_json, indent=2, default=str).encode("utf-8"),
                file_name=f"report_{topic[:30].replace(' ', '_')}.json",
                mime="application/json",
                use_container_width=True,
                key=f"dl_json_{hash(topic)}",
            )
            
    st.markdown('</div>', unsafe_allow_html=True)


def extract_toc(markdown_text):
    """Extract headers for the Table of Contents."""
    headers = []
    lines = markdown_text.split('\\n')
    for line in lines:
        if line.startswith('## '):
            headers.append((2, line.replace('## ', '').strip()))
        elif line.startswith('### '):
            headers.append((3, line.replace('### ', '').strip()))
    return headers


def display_full_report(
    report_markdown: str,
    topic: str,
    sources: list = None,
    metadata: dict = None,
    state_dict: dict = None,
):
    """
    Master function: Render a complete report with all sections.
    Uses a 3-column Layout dashboard.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Dashboard 3-column layout (optimised for sidebar readability)
    col_left, col_main, col_right = st.columns([2.8, 4.2, 2.8])
    
    # LEFT COLUMN: Table of Contents
    with col_left:
        st.markdown("<div class='sidebar-panel'>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-panel-title toc-title'><span>Table of Contents</span><svg width='16' height='16' viewBox='0 0 24 24' fill='none' stroke='#64748B' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'><polyline points='18 15 12 9 6 15'></polyline></svg></div>", unsafe_allow_html=True)
        
        html = """
        <div class='toc-scroll-container'>
            
            <details class="toc-accordion" open>
                <summary class="toc-item active">Preliminary Section</summary>
                <ul class="toc-sublist">
                    <li class="toc-subitem">Title Page</li>
                    <li class="toc-subitem">Acknowledgments</li>
                    <li class="toc-subitem">Abstract</li>
                    <li class="toc-subitem">Table of Contents</li>
                    <li class="toc-subitem">List of Tables</li>
                    <li class="toc-subitem">List of Figures</li>
                </ul>
            </details>

            <details class="toc-accordion">
                <summary class="toc-item">1. Introduction</summary>
                <ul class="toc-sublist">
                    <li class="toc-subitem">Statement of the Problem</li>
                    <li class="toc-subitem">Significance of the Problem</li>
                    <li class="toc-subitem">Purpose</li>
                    <li class="toc-subitem">Statement of Hypothesis</li>
                    <li class="toc-subitem">Assumptions</li>
                    <li class="toc-subitem">Limitations</li>
                    <li class="toc-subitem">Definition of Terms</li>
                </ul>
            </details>

            <details class="toc-accordion">
                <summary class="toc-item">2. Review of Related Literature</summary>
            </details>

            <details class="toc-accordion">
                <summary class="toc-item">3. Design of the Study</summary>
                <ul class="toc-sublist">
                    <li class="toc-subitem">Description of Research Design and Procedures Used</li>
                    <li class="toc-subitem">Sources of Data</li>
                    <li class="toc-subitem">Sampling Procedures</li>
                    <li class="toc-subitem">Methods and Instruments of Data Gathering</li>
                    <li class="toc-subitem">Statistical Treatment</li>
                </ul>
            </details>

            <details class="toc-accordion">
                <summary class="toc-item">4. Analysis of Data</summary>
                <ul class="toc-sublist">
                    <li class="toc-subitem">Text</li>
                    <li class="toc-subitem">Tables</li>
                    <li class="toc-subitem">Figures</li>
                </ul>
            </details>

            <details class="toc-accordion">
                <summary class="toc-item">5. Summary and Conclusions</summary>
                <ul class="toc-sublist">
                    <li class="toc-subitem">Restatement of the Problem</li>
                    <li class="toc-subitem">Description of Procedures</li>
                    <li class="toc-subitem">Major Findings</li>
                    <li class="toc-subitem">Conclusions</li>
                </ul>
            </details>

            <details class="toc-accordion">
                <summary class="toc-item">6. Sources</summary>
                <ul class="toc-sublist">
                    <li class="toc-subitem">End Notes</li>
                    <li class="toc-subitem">Bibliography / Literature Cited</li>
                    <li class="toc-subitem">Appendix</li>
                </ul>
            </details>

        </div>
        """
        st.markdown(html, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
        

    # CENTER COLUMN: Main Report Content
    with col_main:
        st.markdown(f"<h1 style='font-size:2.2rem; margin-top:0;'>{topic}</h1>", unsafe_allow_html=True)
        
        # Executive Summary / Quick Insights
        summary = ""
        lines = report_markdown.split('\\n')
        for line in lines:
            if line.startswith('##'):
                break
            if line.strip() and not line.startswith('#'):
                summary += line + " "
                if len(summary) > 300:
                    summary += "..."
                    break
        
        if summary:
            st.markdown(f"""
            <div class='tech-summary-box'>
                <div class='tech-summary-box-icon'>💡</div>
                <div class='tech-summary-content'>
                    <h4>Quick Insights</h4>
                    <p><b>Key Takeaway:</b> {summary}</p>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # The Report Reading Interface
        st.markdown("<div class='academic-report-container'>", unsafe_allow_html=True)
        st.markdown(report_markdown, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    # RIGHT COLUMN: Verification & Quick Actions
    with col_right:
        # Trust Score (Mocking the UI progress bar)
        credibility = 0
        if state_dict and state_dict.get('fact_check_result'):
            credibility = state_dict['fact_check_result'].get('overall_credibility', 0)
        elif metadata and metadata.get("quality_score"):
            credibility = metadata.get("quality_score", 0) / 10.0
            
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="trust-score-container">
            <div class="trust-score-header">
                <span class="trust-score-title">Trust Score</span>
                <span class="trust-score-value">{int(credibility * 100)}% Credibility</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {int(credibility * 100)}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Quick Actions
        st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
        st.markdown("<div class='sidebar-card-title'>Quick Action</div>", unsafe_allow_html=True)
        render_export_buttons(
            report_markdown=report_markdown,
            topic=topic,
            report_json={
                "topic": topic,
                "report": report_markdown,
                "sources": sources or [],
                "metadata": metadata or {},
                "generated_at": datetime.utcnow().isoformat(),
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Report Metrics
        if metadata:
            st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
            st.markdown("<div class='sidebar-card-title'>Analysis Metrics</div>", unsafe_allow_html=True)
            m_col1, m_col2 = st.columns(2)
            m_col1.metric("Sources Analysed", metadata.get("total_sources", "0"))
            words = len(report_markdown.split())
            m_col2.metric("Total Words", f"{words:,}")
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Agent Timeline
        if state_dict:
            st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
            st.markdown("<div class='sidebar-card-title'>Generation Trace</div>", unsafe_allow_html=True)
            render_agent_timeline(state_dict)
            st.markdown("</div>", unsafe_allow_html=True)
            
        # Citations Panel in Right Column
        if sources:
            st.markdown("<div class='sidebar-card'>", unsafe_allow_html=True)
            st.markdown("<div class='sidebar-card-title'>Related Citations</div>", unsafe_allow_html=True)
            html = "<div style='max-height: 400px; overflow-y: auto; padding-right: 5px;'>"
            for i, url in enumerate(sources, 1):
                html += f"""
                <div style="margin-bottom:1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #F1F5F9;">
                    <div style="color:#0F172A; font-size:15px; font-weight:700; margin-bottom: 0.2rem;">Citation {i}</div>
                    <a href="{url}" target="_blank" style="color:#2563EB; text-decoration:none; word-break:break-all; font-size:14px; line-height:1.4;">{url}</a>
                </div>
                """
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)