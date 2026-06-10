<div align="center">

# 🚀 AI Research & Report Generation Agent

**A multi-agent AI system that automates deep research and generates comprehensive editorial reports.**

[![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.x-teal?logo=fastapi)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.x-red?logo=streamlit)](https://streamlit.io)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker)](https://docker.com)
[![Stars](https://img.shields.io/github/stars/Soujuhegde/AI-Research-and-Report-Generation-Agent?style=social)](https://github.com/Soujuhegde/AI-Research-and-Report-Generation-Agent)

[Features](#-features) · [Architecture](#-architecture) · [Getting Started](#-getting-started) · [Usage](#-usage) · [Roadmap](#-roadmap)

</div>

---

## 📌 Overview

> The **AI Research & Report Generation Agent** is a multi-agent system that automates the process of researching topics and writing structured, well-cited reports. Built with FastAPI and Streamlit, it leverages advanced LLMs via Sarvam AI and web search capabilities via Tavily. Designed for researchers, writers, and analysts who need high-quality, synthesized information quickly.

---

## ✨ Features

- ⚡ **Multi-Agent Orchestration** — Utilizes specialized AI agents (Researcher, Fact-Checker, Writer) to ensure high-quality output.
- 🧠 **Deep Web Research** — Integrated with Tavily API to fetch the most relevant and up-to-date sources from the web.
- 🔗 **Dual Frontends** — Choose between a sleek Streamlit dashboard or a custom HTML/JS interface (complete with a loading mini-game!).
- 📊 **Automated Citations & Trust Scores** — Generates credible reports with source citations and calculated trust scores.
- 🛡️ **Rate Limiting & Production Ready** — Includes built-in API rate limiting and full Docker support for easy deployment.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                      User Interface                      │
│            (Streamlit Dashboard / Custom Web UI)         │
└────────────────────────┬────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────┐
│                     FastAPI Backend                      │
│             (REST Endpoints / Job Polling)               │
└──────┬──────────────────────────────────────┬───────────┘
       │                                      │
┌──────▼───────┐                    ┌─────────▼──────────┐
│ AI Graph     │                    │ External APIs      │
│ (Agents)     │                    │ (Sarvam AI /       │
│              │                    │  Tavily Search)    │
└───────────────┘                    └────────────────────┘
```

**Component Breakdown:**

| Layer | Technology | Role |
|-------|-----------|------|
| Frontend | Streamlit / HTML+JS | User interaction & report viewing |
| Backend | FastAPI | API routing, job management, rate limiting |
| Orchestration | Python Graph Logic | Agent state management |
| LLM | Sarvam AI | Reasoning, synthesis & generation |
| Web Search | Tavily API | Fetching real-time information |

---

## 🛠️ Tech Stack

- **Language:** Python 3.11
- **Backend:** FastAPI
- **Frontend:** Streamlit, Vanilla JS/HTML/CSS
- **LLM:** Sarvam AI
- **Search Provider:** Tavily
- **Infrastructure:** Docker, Docker Compose, GitHub Actions (CI/CD)

---

## 🚀 Getting Started

### Prerequisites

- Docker and Docker Compose (Recommended)
- OR Python 3.11+
- API keys (see [Environment Setup](#environment-setup))

### Installation (Using Docker - Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/Soujuhegde/AI-Research-and-Report-Generation-Agent.git
cd AI-Research-and-Report-Generation-Agent

# 2. Setup your environment variables (see below)

# 3. Build and run with Docker Compose
docker compose up --build
```

### Manual Installation

```bash
# 1. Create a virtual environment
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
.venv\Scripts\activate           # Windows

# 2. Install dependencies
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file in the root directory by copying the example file:

```bash
cp .env.example .env
```

Fill in your `.env` file:
```env
# Sarvam AI API
SARVAM_API_KEY=your_sarvam_api_key_here
SARVAM_API_BASE_URL=https://api.sarvam.ai

# Tavily Web Search
TAVILY_API_KEY=your_tavily_api_key_here

APP_ENV=development
APP_NAME=MultiAgentResearch
```

> ⚠️ Never commit your `.env` file. It's already in `.gitignore`.

---

## 💻 Usage

### Accessing the Applications (Docker)

Once `docker compose up` is running:
- **Streamlit Frontend:** `http://localhost:8501`
- **FastAPI Backend / Swagger UI:** `http://localhost:8000/docs`
- **Vanilla HTML Frontend:** Serve the `static` folder or access it via the configured static route on the FastAPI server.

### Example API Call

```python
import requests

response = requests.post("http://localhost:8000/api/research", json={
    "topic": "Impact of Quantum Computing on Cryptography",
    "instructions": "Focus on RSA encryption",
    "max_iterations": 15
})

print(response.json())
```

---

## 📂 Project Structure

```
AI-Research-and-Report-Generation-Agent/
│
├── api/                    # FastAPI Backend
│   ├── main.py             # FastAPI entry point
│   ├── routes/             # API Endpoints
│   └── middleware/         # Rate limiting & security
│
├── src/                    # Core AI Engine
│   ├── agents/             # Agent definitions (Researcher, Writer, etc.)
│   ├── tools/              # Custom tools (Web search)
│   ├── graph/              # Multi-agent orchestration
│   └── llm/                # LLM provider connections
│
├── frontend/               # Streamlit UI
│   ├── app.py              
│   └── components/         
│
├── static/                 # Custom HTML/JS UI (with mini-game)
├── docker/                 # Dockerfiles
├── .github/workflows/      # CI/CD pipelines
├── .env.example            # Environment variable template
├── requirements.txt
└── docker-compose.yml
```

---

## 📈 Roadmap

- [x] Multi-agent orchestration setup
- [x] Integration with Sarvam AI and Tavily
- [x] FastAPI backend with rate limiting
- [x] Streamlit and custom web frontends
- [x] Docker containerization
- [x] CI/CD pipeline with GitHub Actions
- [ ] Add more LLM provider options

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 👩‍💻 Author

**Soujanya** — AI/ML Engineer

[![GitHub](https://img.shields.io/badge/GitHub-Soujuhegde-black?logo=github)](https://github.com/Soujuhegde)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?logo=linkedin)](https://linkedin.com/in/your-profile)

---

<div align="center">
  <sub>Built with ❤️ using FastAPI, Streamlit, and Multi-Agent AI</sub>
</div>
