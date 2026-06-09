import streamlit as st
from frontend.components.report_viewer import display_full_report
st.write("Starting test")
display_full_report("Test Topic", "## Test Report\n\nThis is a test report.", ["http://example.com"], {"quality_score": 9.5}, {"fact_check_result": {"overall_credibility": 0.9}})
st.write("Done test")
