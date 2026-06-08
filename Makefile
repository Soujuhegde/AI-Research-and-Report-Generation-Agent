.PHONY: setup run-api run-frontend run-all test docker-build docker-up docker-down clean

# Setup virtual environment
setup:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip
	.venv/bin/pip install -r requirements.txt
	cp .env.example .env
	mkdir -p data/reports data/checkpoints logs
	@echo "✅ Setup complete! Edit .env with your API keys"

# Activate venv helper
venv:
	@echo "Run: source .venv/bin/activate  (Linux/Mac)"
	@echo "Run: .venv\Scripts\activate     (Windows)"

# Run FastAPI backend
run-api:
	.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload

# Run Streamlit frontend
run-frontend:
	.venv/bin/streamlit run frontend/app.py --server.port 8501

# Run both (requires tmux or two terminals)
run-all:
	@echo "Starting API in background..."
	.venv/bin/uvicorn api.main:app --host 0.0.0.0 --port 8000 --reload &
	@echo "Starting Streamlit frontend..."
	.venv/bin/streamlit run frontend/app.py

# Run tests
test:
	.venv/bin/pytest tests/ -v --cov=src --cov-report=term-missing

# Docker commands
docker-build:
	docker-compose build

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

docker-prod-up:
	docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Clean up
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".pytest_cache" -exec rm -rf {} +

# Format code
format:
	.venv/bin/black src/ api/ frontend/
	.venv/bin/isort src/ api/ frontend/

# Lint
lint:
	.venv/bin/ruff check src/ api/ frontend/