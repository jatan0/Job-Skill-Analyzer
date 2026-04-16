from typing import Optional
import json
import requests


def analyze_job_description(job_desc: str, company_name: Optional[str] = None) -> dict:
    """
    Analyzes a job description through Ollama.

    Args:
        job_desc: The full job posting text.
        company_name: Optional company name for context.

    Returns:
        dict with keys: required_skills, preferred_skills,
        technologies, experience_level, summary

    Raises:
        ConnectionError: If Ollama is not running.
        TimeoutError: If Ollama takes too long.
        ValueError: If response is invalid or missing fields.
    """
    company_context = f" from {company_name}" if company_name else ""
    prompt = f"""You are a job market analyst. Analyze the following job description{company_context}.
    Return ONLY a valid JSON object with these exact fields:
    - required_skills: array of must-have skills (5-8 items max)
    - preferred_skills: array of nice-to-have skills (3-5 items max)
    - technologies: array of specific tools/frameworks/languages mentioned
    - experience_level: exactly one of: "entry", "mid", or "senior"
    - summary: 2-3 sentence overview of the role
    Guidelines:
    - Be specific (e.g., "React" not "frontend framework")
    - For experience_level: 0-2 years = "entry", 2-5 years = "mid", 5+ years = "senior"
    - If experience not mentioned, infer from role complexity
    Job description{company_context}: {job_desc}
    Return ONLY the JSON object, no other text."""

    url = "http://localhost:11434/api/generate"
    payload = {"model": "llama3.1", "prompt": prompt, "stream": False}

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        response_text = data["response"].strip()
        if response_text.startswith("```"):
            response_text = response_text.split("\n", 1)[1]
            response_text = response_text.rsplit("```", 1)[0]

        parsed = json.loads(response_text)
        required_fields = [
            "required_skills",
            "preferred_skills",
            "technologies",
            "experience_level",
            "summary",
        ]
        missing_fields = [field for field in required_fields if field not in parsed]

        if missing_fields:
            raise ValueError(f"LLM response missing required fields: {missing_fields}")

        if company_name:
            parsed["company_name"] = company_name

        return parsed

    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Cannot connect to Ollama. Is it running on localhost:11434?"
        )
    except requests.exceptions.Timeout:
        raise TimeoutError("Ollama request timed out after 30 seconds")
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {str(e)}")
