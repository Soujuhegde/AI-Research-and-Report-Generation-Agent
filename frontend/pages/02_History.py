"""History page - View past research reports."""
import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="Report History", page_icon="📚", layout="wide")

st.title("📚 Research Report History")

reports_dir = "data/reports"
os.makedirs(reports_dir, exist_ok=True)

files = [f for f in os.listdir(reports_dir) if f.endswith('.json')]

if not files:
    st.info("No reports yet. Go to the main page to create your first report!")
else:
    st.markdown(f"**{len(files)} reports found**")
    for file in sorted(files, reverse=True):
        path = os.path.join(reports_dir, file)
        with open(path) as f:
            data = json.load(f)
        
        with st.expander(f"📄 {data.get('topic', file)} - {file}"):
            st.markdown(data.get('report', 'No content'))