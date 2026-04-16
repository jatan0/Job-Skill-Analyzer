# Job Skill Analyzer API

A REST API that analyzes job descriptions using AI to extract required skills, technologies, and experience levels.

## Why I Built This

I built this project to get hands-on experience building a REST API end to end instead of just writing scripts. I wanted to understand what it takes to run an LLM-backed service locally, handle requests properly, and return structured data that other systems could actually use.

Rather than using a hosted API, I integrated Llama 3.1 through Ollama so I could experiment with running inference on my own GPU. That forced me to think about response times, model behavior, and how to deal with outputs that are not always perfectly formatted.

The current use case focuses on analyzing job descriptions, but the broader goal was to design a backend pattern that accepts unstructured text, processes it through a model, validates the output, and stores the results for later retrieval.

This was also my first serious project using FastAPI. I ran into issues around request validation and inconsistent model responses, which led me to tighten up schema checks and add more defensive error handling.

## Tech Stack

- **Python 3.x** - Core language
- **FastAPI** - Web framework chosen for API development and automatic documentation
- **Ollama + Llama 3.1 8B** - Local LLM for AI analysis
- **SQLite** - Stores past analyses
- **Uvicorn** - ASGI server

## Features

- Analyzes job descriptions and extracts structured data
- Identifies required vs. preferred skills
- Detects technologies and experience level
- Stores analysis history in SQLite
- RESTful API with automatic documentation
- Graceful error handling for AI service failures
- Handles malformed LLM output with basic validation

## How It Works

1. The API receives a job description through a POST request
2. The backend sends the text to a local Ollama model with a prompt requesting structured JSON output
3. The response is parsed, validated, stored in SQLite, and returned to the client

## Prerequisites

- Python 3.8+
- [Ollama](https://ollama.ai) installed and running
- Llama 3.1 model pulled: `ollama pull llama3.1`

## Installation

1. Clone the repository

```bash
git clone https://github.com/jatan0/Job-Skill-Analyzer
cd Job-Skill-Analyzer
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

## Current Limitations

- Requires a locally running Ollama instance
- Uses synchronous request handling
- LLM responses can still be inconsistent or malformed
- SQLite is used for simple local storage, not production-scale deployment
- No authentication or authorization
- Stores analysis history, but does not currently implement deduplicated caching

## Key Technical Learnings

- Designing REST endpoints with FastAPI
- Integrating a local LLM through Ollama and prompting for structured JSON output
- Separating application responsibilities into API, AI service, and database layers
- Validating and handling unreliable model output before returning results
- Persisting analysis results for later retrieval with SQLite

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
