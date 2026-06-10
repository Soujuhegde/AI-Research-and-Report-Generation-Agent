<div align="center">
  <h1>🧠 AI Autonomous Research Workspace</h1>
  <p>An advanced, fully autonomous multi-agent AI system that researches any topic and generates highly structured, fact-checked, and comprehensive academic-style reports.</p>

  [![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://www.python.org/downloads/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=FastAPI&logoColor=white)](https://fastapi.tiangolo.com/)
  [![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=Streamlit&logoColor=white)](https://streamlit.io/)
</div>

## ✨ Features

- **Autonomous Agentic Orchestration**: Seamlessly coordinates **6 specialized AI agents** using LangGraph.
- **Strict Academic Structure**: Enforces a professional, rigid 6-point report structure (Preliminary, Literature Review, Methodology, Analysis, Conclusions, Sources).
- **Fact-Checking & Credibility Built-In**: Automatically cross-references claims with raw search data to calculate and assign a trust score.
- **Modern Document Workspace UI**: Beautiful, responsive Streamlit dashboard featuring:
  - Sticky, collapsible accordion Table of Contents.
  - Distinct right-sidebar for metadata, citations, and trust scores.
  - Real-time agent generation trace logs.
- **One-Click Deploy**: Production-ready deployment to Render via the included Blueprint.

## 🏗️ Architecture

The system utilizes a central **LangGraph State Machine** to orchestrate the workflow of 6 specialized agents. They do not talk over a network; instead, they sequentially mutate and pass a strict Pydantic shared state.

1. **Planner Agent**: Breaks down the research topic into logical sections and devises targeted search queries.
2. **Researcher Agent**: Uses Tavily Search to gather raw, factual data and citations from the web.
3. **Writer Agent**: Iteratively drafts the content, exactly one section at a time, adhering strictly to the required academic format.
4. **Assembler Agent**: Stitches the individually drafted sections into a cohesive markdown document.
5. **Critic Agent**: Reviews the full draft for flow, tone, and requirements. If it scores poorly, it sends it back for revision.
6. **Fact-Checker Agent**: Validates the finalized facts against the original raw research to calculate an overall credibility score.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- [Sarvam AI](https://sarvam.ai) API Key (or OpenAI/Anthropic depending on your configuration)
- [Tavily](https://tavily.com/) Search API Key

### Local Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Soujuhegde/AI-Research-and-Report-Generation-Agent.git
   cd AI-Research-and-Report-Generation-Agent
   ```

2. **Set up a virtual environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Copy the `.env.example` file to `.env` and fill in your API keys.
   ```bash
   cp .env.example .env
   ```

### Running the Application Locally

The application consists of a FastAPI backend (optional for UI) and a Streamlit frontend. For local development, running the frontend is sufficient:

```bash
streamlit run frontend/app.py
```

*Alternatively, run the API for headless integration:*
```bash
uvicorn api.main:app --reload --port 8000
```

## ☁️ Deployment (Render)

This project is completely ready to be deployed to Render for free using the included `render.yaml` Blueprint.

1. Push your repository to GitHub.
2. Log into [Render.com](https://render.com).
3. Click **New +** -> **Blueprint**.
4. Connect this repository and click **Apply Blueprint**.
5. Go to the newly created `research-frontend` service dashboard on Render.
6. Under **Environment**, securely paste your `SARVAM_API_KEY` and `TAVILY_API_KEY`.
7. Once the build finishes, access your live workspace URL!

## 🛠️ Technologies Used

- **AI/LLM Framework**: LangGraph, LangChain, Sarvam AI
- **Web Search**: Tavily Search API
- **Backend API**: FastAPI, Uvicorn, Python 3.9+
- **Frontend Dashboard**: Streamlit, Custom HTML/CSS
- **Cloud Infrastructure**: Docker, Render (Web Services Blueprint)

## Author 
Soujanya S P 
