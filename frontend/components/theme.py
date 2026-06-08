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
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&display=swap');

        /* Hide Streamlit default clutter */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden !important;}
        footer {visibility: hidden !important;}

        /* Base Typography & Structure */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif !important;
            color: #1F2937;
            background-color: #F8FAFC;
        }

        /* Enforce high contrast headers for UI */
        h1, h2, h3, h4, h5, h6 {
            color: #111827 !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em !important;
        }

        /* Hero Banner */
        .hero-banner {
            text-align: center;
            padding: 4rem 1rem 3rem 1rem;
            animation: fadeIn 0.8s ease-out;
            background: linear-gradient(180deg, #FFFFFF 0%, #F8FAFC 100%);
            border-bottom: 1px solid #E2E8F0;
            margin-top: -3rem; /* pull up */
            padding-bottom: 5rem;
            margin-bottom: 2rem;
        }
        
        .hero-banner h1 {
            color: #111827 !important;
            font-size: 3.5rem !important;
            margin-bottom: 1rem;
            font-weight: 800 !important;
            letter-spacing: -0.04em !important;
            background: linear-gradient(90deg, #111827 0%, #374151 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero-banner p {
            color: #4B5563 !important;
            font-size: 1.2rem;
            max-width: 650px;
            margin: 0 auto;
            font-weight: 400;
            line-height: 1.6;
        }
        
        /* Clean Cards & Forms */
        [data-testid="stForm"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 16px !important;
            padding: 2.5rem !important;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01) !important;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            position: relative;
            top: -4.5rem; /* Pull up into the hero section slightly */
            z-index: 10;
            margin-bottom: -2rem !important;
        }

        [data-testid="stForm"]:hover {
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01) !important;
        }

        /* Input fields styling */
        .stTextInput input, .stTextArea textarea {
            background-color: #F8FAFC !important;
            border: 1px solid #E2E8F0 !important;
            color: #111827 !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            font-size: 1.1rem !important;
            transition: all 0.2s ease;
            box-shadow: inset 0 1px 2px rgba(0,0,0,0.02) !important;
        }
        
        .stTextInput input:focus, .stTextArea textarea:focus {
            border-color: #3B82F6 !important;
            background-color: #FFFFFF !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
        }

        /* Submit Button Micro-interactions */
        [data-testid="baseButton-primary"] {
            background: linear-gradient(135deg, #2563EB 0%, #1D4ED8 100%) !important;
            border: none !important;
            color: white !important;
            border-radius: 10px !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            transition: all 0.2s ease !important;
            padding: 0.75rem 1.5rem !important;
            box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2), 0 2px 4px -1px rgba(37, 99, 235, 0.1) !important;
        }
        
        [data-testid="baseButton-primary"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 15px -3px rgba(37, 99, 235, 0.3), 0 4px 6px -2px rgba(37, 99, 235, 0.15) !important;
        }

        [data-testid="baseButton-primary"]:active {
            transform: translateY(0px) !important;
        }
        
        /* Outline buttons (Secondary) */
        [data-testid="baseButton-secondary"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            color: #374151 !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.2s ease !important;
            box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.05) !important;
        }
        
        [data-testid="baseButton-secondary"]:hover {
            background: #F8FAFC !important;
            border-color: #CBD5E1 !important;
            color: #111827 !important;
        }

        /* Expander */
        [data-testid="stExpander"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px !important;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.03) !important;
            margin-bottom: 1rem !important;
        }
        [data-testid="stExpander"] > summary {
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            color: #111827 !important;
            padding: 1.2rem 1.5rem !important;
            transition: background 0.2s;
            background: #FFFFFF !important;
            border-bottom: 1px solid #F1F5F9 !important;
        }
        [data-testid="stExpander"] > summary:hover {
            background: #F8FAFC !important;
        }
        
        /* The Report Reading Container */
        .academic-report-container {
            background-color: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-radius: 16px;
            padding: 4rem 5rem;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.02), 0 10px 15px -3px rgba(0,0,0,0.03);
            margin-bottom: 3rem;
            margin-top: 1rem;
        }
        
        /* Academic Typography within the report */
        .academic-report-container p, .academic-report-container li {
            font-family: 'Lora', serif !important;
            font-size: 1.15rem !important;
            line-height: 1.8 !important;
            color: #374151 !important;
            margin-bottom: 1.5rem !important;
        }
        
        .academic-report-container h1 {
            font-family: 'Inter', sans-serif !important;
            font-size: 2.5rem !important;
            font-weight: 800 !important;
            color: #111827 !important;
            margin-bottom: 2rem !important;
            line-height: 1.2 !important;
            border-bottom: 2px solid #F1F5F9;
            padding-bottom: 1rem;
        }
        
        .academic-report-container h2 {
            font-family: 'Inter', sans-serif !important;
            font-size: 1.75rem !important;
            font-weight: 700 !important;
            color: #111827 !important;
            margin-top: 3rem !important;
            margin-bottom: 1.5rem !important;
            border-bottom: 1px solid #F1F5F9;
            padding-bottom: 0.5rem;
        }
        
        .academic-report-container h3 {
            font-family: 'Inter', sans-serif !important;
            font-size: 1.35rem !important;
            font-weight: 600 !important;
            color: #1F2937 !important;
            margin-top: 2rem !important;
            margin-bottom: 1rem !important;
        }
        
        .academic-report-container blockquote {
            font-family: 'Lora', serif !important;
            font-size: 1.15rem !important;
            font-style: italic;
            border-left: 4px solid #3B82F6;
            padding-left: 1.5rem;
            margin-left: 0;
            margin-right: 0;
            color: #4B5563;
            background: #F8FAFC;
            padding: 1.5rem;
            border-radius: 0 8px 8px 0;
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
            border-radius: 12px !important;
            font-weight: 500;
        }
        
        /* Metric Styling */
        [data-testid="stMetric"] {
            background: #FFFFFF !important;
            border: 1px solid #E2E8F0 !important;
            border-radius: 12px;
            padding: 1rem 1.5rem;
            box-shadow: 0 1px 2px rgba(0,0,0,0.02);
            margin-bottom: 0.5rem;
        }
        [data-testid="stMetricValue"] {
            color: #111827 !important;
            font-weight: 700 !important;
            font-size: 1.75rem !important;
        }
        [data-testid="stMetricLabel"] {
            color: #64748B !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-size: 0.75rem;
            margin-bottom: 0.25rem;
        }
        
        /* Sidebar container */
        .sidebar-panel {
            position: sticky;
            top: 2rem;
            background-color: transparent;
        }

        /* Custom UI badges */
        .badge {
            display: inline-block;
            font-size: 0.75rem;
            font-weight: 600;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            margin-bottom: 0.5rem;
        }
        .badge-verified { background: #DEF7EC; color: #03543F; }
        .badge-disputed { background: #FDE8E8; color: #9B1C1C; }
        .badge-neutral { background: #E5E7EB; color: #374151; }

    </style>
    """
    st.markdown(css, unsafe_allow_html=True)
