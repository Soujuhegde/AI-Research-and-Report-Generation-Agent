# 🤖 Multi-Agent Research & Report Generation System

An advanced agentic AI system that orchestrates 5 specialized agents to autonomously research any topic and generate highly structured, fact-checked, and comprehensive reports.

## ✨ Features

- **Agentic AI Orchestration**: Seamlessly coordinates 5 specialized AI agents (e.g., Planner, Researcher, Writer, Critic, Fact-Checker).
- **Structured Report Generation**: Produces well-organized, comprehensive reports with automatically generated Table of Contents and subheadings.
- **Fact-Checking Built-In**: Automatically cross-references claims with reliable sources to ensure high trust and accuracy.
- **Modern User Interface**: Beautiful, responsive UI featuring dynamic sidebars, active TOC tracking, and markdown rendering.
- **Source Citation**: Transparently cites sources and provides a trust score for the generated content.

## 🏗️ Architecture

The system utilizes a multi-agent framework where each agent has a distinct role:
1. **Planner Agent**: Breaks down the research topic into logical sections and subheadings.
2. **Researcher Agent**: Gathers raw data and context from reliable web sources.
3. **Writer Agent**: Drafts the content section by section based on the research.
4. **Critic Agent**: Reviews the drafts for flow, tone, and adherence to requirements.
5. **Fact-Checker Agent**: Validates the drafted facts against the raw research and flags inconsistencies.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- API Keys for the required LLM providers (e.g., OpenAI/Anthropic/Gemini)

### Installation

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

### Running the Application

**Using Makefile:**
```bash
make run
```

**Using Docker:**
```bash
docker-compose up --build
```

## 🛠️ Technologies Used

- **Backend**: Python, FastAPI / LangGraph (Multi-Agent Framework)
- **Frontend**: Streamlit / HTML, CSS, JavaScript
- **Deployment**: Docker, Render
