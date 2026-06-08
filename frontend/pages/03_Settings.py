"""Settings page."""
import streamlit as st

st.set_page_config(page_title="Settings", page_icon="⚙️", layout="wide")
st.title("⚙️ Settings")

st.markdown("### API Configuration")
st.info("Set your API keys in the `.env` file for security. Never hardcode secrets!")

with st.expander("Environment Variables Guide"):
    st.code("""
SARVAM_API_KEY=your_key_here
TAVILY_API_KEY=your_key_here
MAX_ITERATIONS=10
MAX_SEARCH_RESULTS=5
    """)

st.markdown("### About")
st.markdown("""
**Multi-Agent Research System**  
- 🤖 5 specialized AI agents  
- 🔍 Real-time web search via Tavily  
- 🗺️ DAG orchestration via LangGraph  
- 📊 Structured output with Pydantic  
- 📄 PDF export via WeasyPrint  
""")