# Job Skill Analyzer API

A REST API that analyzes job descriptions using AI to extract required skills, technologies, and experience levels.

## Why I Built This

I built this project to practice designing and deploying a production-style REST API that integrates a local LLM, persists structured results, and handles errors gracefully. The goal was to simulate a real backend service that processes unstructured text, applies AI-driven analysis, and exposes clean, documented endpoints.

I chose to work with Ollama and Llama 3.1 specifically because I wanted to explore local LLM integration and understand how to leverage my GPU for practical AI applications beyond cloud APIs. While the initial use case focuses on job description analysis, the core architecture—accepting unstructured input, processing it through an AI model, and returning structured JSON—translates to many document analysis scenarios.

This project pushed me into unfamiliar territory with FastAPI, async Python, and prompt engineering for structured outputs, which was exactly what I was looking for: a chance to build something modern, functional, and applicable to real-world backend development.

## Tech Stack

- **Python 3.x** - Core language
- **FastAPI** - Web framework (chosen for automatic API docs and async support)
- **Ollama + Llama 3.1 8B** - Local LLM for AI analysis
- **SQLite** - Database for caching results
- **Uvicorn** - ASGI server

## Features

- Analyzes job descriptions and extracts structured data
- Identifies required vs. preferred skills
- Detects technologies and experience level
- Caches results for future reference
- RESTful API with automatic documentation
- Graceful error handling for AI service failures

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) installed and running
- Llama 3.1 model pulled: `ollama pull llama3.1`

## Installation

1. Clone the repository

```bash
git clone https://github.com/yourusername/job-skill-analyzer
cd job-skill-analyzer
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Start Ollama (if not already running)

```bash
ollama serve
```

4. Run the API

```bash
uvicorn app.main:app --reload
```

5. Open the interactive docs at `http://localhost:8000/docs`

## API Endpoints

### 1. Analyze Job Description

**POST** `/api/analyze`

Analyzes a job posting and returns structured data.

**Request:**

```json
{
	"job_description": "We're hiring a Python developer with 3+ years experience in backend development. Must know FastAPI, PostgreSQL, and Docker. React experience is a plus.",
	"company_name": "TechCo"
}
```

**Response:**

```json
{
	"id": 1,
	"company_name": "TechCo",
	"required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
	"preferred_skills": ["React"],
	"technologies": ["Python", "FastAPI", "PostgreSQL", "Docker"],
	"experience_level": "mid",
	"summary": "Mid-level backend role focused on API development with database and containerization experience.",
	"created_at": "2026-02-04 04:09:59"
}
```

### 2. Get Analysis History

**GET** `/api/history`

Returns all past analyses, most recent first.

### 3. Get Single Analysis

**GET** `/api/analysis/{id}`

Returns a specific analysis by ID. Returns 404 if not found.

## Key Technical Learnings

- Building async REST APIs with FastAPI and proper error handling
- Integrating local LLMs (Ollama) with prompt engineering for structured outputs
- Database design for caching AI results
- GPU-accelerated inference on consumer hardware

## Project Structure

```
job-skill-analyzer/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI endpoints
│   ├── database.py       # Database operations
│   └── ai_service.py     # Ollama integration
├── requirements.txt
└── README.md
```

## License

MIT

```
