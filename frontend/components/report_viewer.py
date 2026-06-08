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
        color = "#10B981" if done else "#CBD5E1"
        html += f'''
<div style="position: relative; margin-bottom: 1.25rem;">
    <div style="position: absolute; left: -27px; top: 12px; width: 12px; height: 12px; border-radius: 50%; background: {color}; border: 2px solid white;"></div>
    <div style="background: #FFFFFF; border: 1px solid #F1F5F9; border-radius: 8px; padding: 0.75rem 1rem; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
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
    """Render download buttons for various export formats."""
    st.markdown("<div style='margin-top: 0.5rem;'>", unsafe_allow_html=True)
    if report_markdown:
        try:
            from src.utils.pdf_exporter import export_to_pdf
            pdf_path = export_to_pdf(report_markdown, topic)

            with open(pdf_path, "rb") as f:
                pdf_bytes = f.read()

            st.download_button(
                label="📄 Export PDF (Academic)",
                data=pdf_bytes,
                file_name=f"report_{topic[:30].replace(' ', '_')}.pdf",
                mime="application/pdf",
                use_container_width=True,
                key=f"dl_pdf_{hash(topic)}",
            )
        except Exception as e:
            st.error(f"PDF generation failed: {e}")

    if report_markdown:
        st.download_button(
            label="⬇️ Download Markdown",
            data=report_markdown.encode("utf-8"),
            file_name=f"report_{topic[:30].replace(' ', '_')}.md",
            mime="text/markdown",
            use_container_width=True,
            key=f"dl_md_{hash(topic)}",
        )

    if report_json:
        st.download_button(
            label="⬇️ Download JSON Data",
            data=json.dumps(report_json, indent=2, default=str).encode("utf-8"),
            file_name=f"report_{topic[:30].replace(' ', '_')}.json",
            mime="application/json",
            use_container_width=True,
            key=f"dl_json_{hash(topic)}",
        )
    st.markdown("</div>", unsafe_allow_html=True)


def display_full_report(
    report_markdown: str,
    topic: str,
    sources: list = None,
    metadata: dict = None,
    state_dict: dict = None,
):
    """
    Master function: Render a complete report with all sections.
    Call this from any page that needs to show a report.
    """
    st.markdown("<br>", unsafe_allow_html=True)
    
    col_main, col_sidebar = st.columns([7, 3])
    
    with col_main:
        # Overview Section at top of main column
        st.markdown(f"<h1 style='font-size:2.5rem; letter-spacing:-0.03em; margin-bottom:0.5rem;'>{topic}</h1>", unsafe_allow_html=True)
        st.markdown(f"<p style='color:#64748B; font-size:1.1rem; margin-top:0; margin-bottom:2rem;'>Research complete. Report generated on {datetime.utcnow().strftime('%B %d, %Y')}</p>", unsafe_allow_html=True)
        
        # Executive Summary Extractor (Grab first ~400 chars before first ##)
        summary = ""
        lines = report_markdown.split('\\n')
        for line in lines:
            if line.startswith('##'):
                break
            if line.strip() and not line.startswith('#'):
                summary += line + " "
                if len(summary) > 400:
                    summary += "..."
                    break
        
        if summary:
            st.markdown(f"""
            <div style='background: linear-gradient(to right, #F8FAFC, #FFFFFF); border-left: 4px solid #4F46E5; padding: 1.5rem; border-radius: 0 12px 12px 0; margin-bottom: 2rem;'>
                <h4 style='margin-top:0; color:#0F172A; font-weight:700;'>Executive Summary</h4>
                <p style='color:#475569; font-size:1.05rem; line-height:1.6; margin-bottom:0;'>{summary}</p>
            </div>
            """, unsafe_allow_html=True)

        # The Report Reading Interface
        st.markdown("<div class='academic-report-container'>", unsafe_allow_html=True)
        st.markdown(report_markdown, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
    with col_sidebar:
        st.markdown("<div class='sidebar-panel'>", unsafe_allow_html=True)
        
        # Verification Summary First (Trust & Credibility)
        if state_dict and state_dict.get('fact_check_result'):
            fc = state_dict['fact_check_result']
            credibility = fc.get('overall_credibility', 0)
            
            with st.expander("🛡️ Verification & Trust", expanded=True):
                st.markdown(f"<h1 style='text-align:center; font-size:3rem; margin:1rem 0; color:{'#059669' if credibility > 0.8 else '#D97706'}'>{credibility:.0%}</h1>", unsafe_allow_html=True)
                st.markdown("<p style='text-align:center; color:#64748B; margin-top:-1rem; font-weight:600; text-transform:uppercase; font-size:0.75rem; letter-spacing:0.05em;'>Credibility Score</p>", unsafe_allow_html=True)
                
                v_claims = len(fc.get('verified_claims', []))
                d_claims = len(fc.get('disputed_claims', []))
                u_claims = len(fc.get('unverifiable_claims', []))
                
                st.markdown(f"""
                <div style='display:flex; justify-content:space-between; margin-bottom:0.5rem;'>
                    <span class='badge badge-verified'>✓ {v_claims} Verified</span>
                    <span class='badge badge-disputed'>✗ {d_claims} Disputed</span>
                </div>
                <div style='display:flex; justify-content:center; margin-bottom:0.5rem;'>
                    <span class='badge badge-neutral'>? {u_claims} Unverifiable</span>
                </div>
                """, unsafe_allow_html=True)
                
        # Metadata / Metrics
        if metadata:
            with st.expander("📊 Report Metrics", expanded=True):
                m_col1, m_col2 = st.columns(2)
                m_col1.metric("Sources", metadata.get("total_sources", "0"))
                m_col2.metric("Quality", f"{metadata.get('quality_score', 0):.1f}/10")
                m_col3, m_col4 = st.columns(2)
                
                words = len(report_markdown.split())
                read_time = max(1, words // 200)
                m_col3.metric("Words", f"{words:,}")
                m_col4.metric("Read Time", f"{read_time} min")
                
        # Sources
        if sources:
            with st.expander(f"📚 References ({len(sources)})", expanded=False):
                html = "<div style='max-height: 350px; overflow-y: auto; padding-right: 5px;'>"
                for i, url in enumerate(sources, 1):
                    html += f"""
                    <div style="background:#F8FAFC; border:1px solid #E2E8F0; border-radius:8px; padding:0.75rem; margin-bottom:0.5rem; display:flex; align-items:flex-start;">
                        <div style="color:#64748B; font-size:0.75rem; font-weight:700; margin-right:0.75rem; margin-top:0.2rem;">[{i}]</div>
                        <a href="{url}" target="_blank" style="color:#2563EB; text-decoration:none; word-break:break-all; font-size:0.85rem; line-height:1.4;">{url}</a>
                    </div>
                    """
                html += "</div>"
                st.markdown(html, unsafe_allow_html=True)
                
        # Behind the scenes timeline
        if state_dict:
            with st.expander("⚙️ Generation Trace", expanded=False):
                render_agent_timeline(state_dict)
                
        # Export Actions
        with st.expander("💾 Export Options", expanded=True):
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