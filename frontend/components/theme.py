"""
Global UI Theme Module
Injects premium custom CSS for a clean, minimal, modern SaaS light theme.
"""
import streamlit as st

def apply_theme():
    """Apply premium global custom CSS for structured, minimal aesthetics."""
    
    css = """
    <style>
        /* Import premium typography */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

        /* Hide Streamlit default clutter */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}

        /* Typography & Structure */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: #0F172A;
            background-color: #FAFAFA;
        }

        /* Enforce high contrast headers */
        h1, h2, h3, h4, h5, h6 {
            color: #0F172A !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        /* Hero Banner */
        .hero-banner {
            text-align: center;
            padding: 3rem 1rem 2rem 1rem;
            margin-bottom: 2rem;
            animation: fadeIn 0.8s ease-out;
        }
        
        .hero-banner h1 {
            color: #0F172A !important;
            font-size: 3.5rem !important;
            margin-bottom: 0.5rem;
            font-weight: 800 !important;
            letter-spacing: -0.04em !important;
        }
        
        .hero-banner p {
            color: #64748B !important;
            font-size: 1.25rem;
            max-width: 650px;
            margin: 0 auto;
            font-weight: 400;
        }
        
        /* Clean Cards & Forms */
        [data-testid="stForm"], .highlight-card {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            padding: 2rem !important;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05) !important;
            transition: box-shadow 0.2s ease, border-color 0.2s ease;
        }

        [data-testid="stForm"]:hover {
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.03) !important;
            border-color: #CBD5E1 !important;
        }

        /* Input fields styling */
        .stTextInput input, .stTextArea textarea {
            background-color: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #0F172A !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            font-size: 1rem !important;
            transition: all 0.2s ease;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #4F46E5 !important;
            box-shadow: 0 0 0 3px rgba(79, 70, 229, 0.1) !important;
        }

        /* Submit Button Micro-interactions */
        [data-testid="baseButton-primary"] {
            background: #4F46E5 !important;
            border: 1px solid #4338CA !important;
            color: white !important;
            border-radius: 8px !important;
            font-weight: 600 !important;
            transition: all 0.2s ease !important;
            padding: 0.6rem 1.2rem !important;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
        }
        
        [data-testid="baseButton-primary"]:hover {
            background: #4338CA !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 4px 6px -1px rgba(79, 70, 229, 0.2) !important;
        }

        [data-testid="baseButton-primary"]:active {
            transform: translateY(0px) !important;
            background: #3730A3 !important;
        }

        /* Metric Cards */
        [data-testid="stMetric"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px;
            padding: 1.2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.02);
            transition: transform 0.2s ease;
        }
        
        [data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            border-color: #CBD5E1 !important;
        }

        [data-testid="stMetricValue"] {
            color: #0F172A !important;
            font-weight: 700 !important;
            font-size: 2rem !important;
        }

        [data-testid="stMetricLabel"] {
            color: #64748B !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
        }

        /* Expander */
        [data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            overflow: hidden;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02) !important;
        }
        [data-testid="stExpander"] > summary {
            font-weight: 600 !important;
            color: #0F172A !important;
            padding: 1rem 1.2rem !important;
            transition: background 0.2s;
            background: #F8FAFC !important;
            border-bottom: 1px solid #E2E8F0 !important;
        }
        [data-testid="stExpander"] > summary:hover {
            background: #F1F5F9 !important;
        }
        
        /* Keyframe Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        /* Status Info Messages */
        .stAlert {
            background: #EFF6FF !important;
            border: 1px solid #BFDBFE !important;
            color: #1E3A8A !important;
            border-radius: 8px !important;
        }
        
        /* Center form container */
        .centered-container {
            max-width: 800px;
            margin: 0 auto;
        }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
