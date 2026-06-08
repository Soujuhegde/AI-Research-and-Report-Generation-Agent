import streamlit as st

def apply_theme():
    """Apply the clean, structured, white and blue neumorphic dashboard theme."""
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;600;700;800&display=swap');

        /* Dashboard Background */
        .stApp {
            background-color: #F0F4F8; /* Light grayish-blue for neumorphism */
            font-family: 'Inter', sans-serif;
            color: #1E293B;
        }

        /* Hide default Streamlit header & sidebar button */
        header {visibility: hidden;}
        [data-testid="collapsedControl"] { display: none; }
        
        /* Modern Typography */
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Outfit', sans-serif !important;
            font-weight: 700 !important;
            letter-spacing: -0.02em;
            color: #0F172A;
        }

        /* Neumorphic Report Container */
        .academic-report-container {
            background-color: #F0F4F8;
            border-radius: 20px;
            padding: 2.5rem 3.5rem;
            box-shadow: 
                8px 8px 16px rgba(163, 177, 198, 0.6), 
                -8px -8px 16px rgba(255, 255, 255, 0.8);
            margin-bottom: 2rem;
            color: #334155;
        }
        
        .academic-report-container h1, 
        .academic-report-container h2 {
            color: #0F172A;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 0.5rem;
            margin-top: 2rem;
        }

        .academic-report-container p, .academic-report-container li {
            font-family: 'Inter', sans-serif !important;
            font-size: 1.05rem;
            line-height: 1.7;
            color: #334155 !important;
            margin-bottom: 1.25rem;
        }

        /* Quick Insights / Tech Summary Box */
        .tech-summary-box {
            background-color: #E6F0FE; /* Light blue */
            border: 1px solid #BFDBFE;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            box-shadow: 
                5px 5px 10px rgba(163, 177, 198, 0.4), 
                -5px -5px 10px rgba(255, 255, 255, 0.6);
            display: flex;
            align-items: flex-start;
            gap: 1rem;
        }
        
        .tech-summary-box-icon {
            font-size: 1.5rem;
            color: #2563EB;
            margin-top: 0.2rem;
        }

        .tech-summary-content h4 {
            color: #1E40AF;
            margin-top: 0;
            margin-bottom: 0.5rem;
        }
        .tech-summary-content p {
            color: #1E3A8A;
            margin: 0;
            font-size: 0.95rem;
            line-height: 1.5;
        }

        /* Sidebar Panels (Neumorphic) */
        .sidebar-panel {
            background-color: #F0F4F8;
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 
                6px 6px 12px rgba(163, 177, 198, 0.6), 
                -6px -6px 12px rgba(255, 255, 255, 0.8);
            margin-bottom: 1.5rem;
        }

        .sidebar-panel-title {
            font-family: 'Outfit', sans-serif;
            font-weight: 700;
            font-size: 1.1rem;
            color: #0F172A;
            margin-bottom: 1rem;
            border-bottom: 1px solid #E2E8F0;
            padding-bottom: 0.5rem;
        }

        /* Quick Actions Grid */
        .quick-actions-grid {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.75rem;
            margin-bottom: 1rem;
        }

        .action-button {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background-color: #F0F4F8;
            border-radius: 10px;
            padding: 0.75rem 0.5rem;
            text-align: center;
            text-decoration: none;
            color: #475569;
            font-size: 0.75rem;
            font-weight: 600;
            box-shadow: 
                4px 4px 8px rgba(163, 177, 198, 0.5), 
                -4px -4px 8px rgba(255, 255, 255, 0.7);
            transition: all 0.2s ease;
            cursor: pointer;
            border: none;
        }
        
        .action-button:hover {
            box-shadow: 
                inset 2px 2px 5px rgba(163, 177, 198, 0.5), 
                inset -2px -2px 5px rgba(255, 255, 255, 0.7);
            color: #2563EB;
        }

        .action-button span {
            font-size: 1.25rem;
            margin-bottom: 0.25rem;
            color: #64748B;
        }
        
        .action-button:hover span {
            color: #2563EB;
        }

        /* Streamlit Primary Buttons */
        .stButton button[kind="primary"] {
            background-color: #2563EB !important;
            color: white !important;
            font-family: 'Inter', sans-serif !important;
            font-weight: 600 !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.6rem 1.2rem !important;
            box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2) !important;
            transition: all 0.2s ease !important;
        }
        .stButton button[kind="primary"]:hover {
            background-color: #1D4ED8 !important;
            box-shadow: 0 6px 8px rgba(37, 99, 235, 0.3) !important;
        }

        /* Custom Input fields */
        div[data-baseweb="input"], div[data-baseweb="textarea"] {
            background-color: #F0F4F8 !important;
            border-radius: 10px !important;
            border: none !important;
            box-shadow: 
                inset 4px 4px 8px rgba(163, 177, 198, 0.5), 
                inset -4px -4px 8px rgba(255, 255, 255, 0.7) !important;
        }

        /* Progress Bar for Trust Score */
        .trust-score-container {
            margin-bottom: 1rem;
        }
        .trust-score-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 0.5rem;
        }
        .trust-score-title {
            font-size: 0.95rem;
            font-weight: 600;
            color: #0F172A;
        }
        .trust-score-value {
            font-size: 0.95rem;
            font-weight: 700;
            color: #2563EB;
        }
        .progress-bar-bg {
            background-color: #E2E8F0;
            border-radius: 999px;
            height: 8px;
            width: 100%;
            overflow: hidden;
            box-shadow: inset 1px 1px 3px rgba(0,0,0,0.1);
        }
        .progress-bar-fill {
            background-color: #2563EB;
            height: 100%;
            border-radius: 999px;
        }

        /* Streamlit expanders */
        .streamlit-expanderHeader {
            background-color: #F0F4F8 !important;
            border-radius: 10px !important;
            border: none !important;
            box-shadow: 
                3px 3px 6px rgba(163, 177, 198, 0.4), 
                -3px -3px 6px rgba(255, 255, 255, 0.6) !important;
            margin-bottom: 0.5rem !important;
        }

        /* Table of Contents List */
        .toc-list {
            list-style: none;
            padding: 0;
            margin: 0;
        }
        .toc-item {
            padding: 0.6rem 1rem;
            margin-bottom: 0.5rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.9rem;
            color: #475569;
            transition: all 0.2s ease;
        }
        .toc-item:hover {
            background-color: #E2E8F0;
            color: #0F172A;
        }
        .toc-item.active {
            background-color: #E6F0FE;
            color: #2563EB;
            font-weight: 600;
            box-shadow: inset 2px 2px 4px rgba(0,0,0,0.05);
        }

        /* Hero Header */
        .hero-banner {
            padding: 2rem 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .hero-title {
            font-size: 1.5rem;
            font-weight: 800;
            color: #0F172A;
            margin: 0;
        }

        /* Hide Streamlit components that break layout */
        [data-testid="stSidebar"] { display: none; }
        
        /* Metric overriding */
        [data-testid="stMetricValue"] {
            color: #2563EB !important;
            font-weight: 700 !important;
        }
        </style>
    """, unsafe_allow_html=True)
