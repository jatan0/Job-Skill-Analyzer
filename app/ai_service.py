import requests
import json


def analyze_job_description(jobDesc: str, companyName: str = None) -> dict:
    """
    Analyzes a job description though Ollama

    Args:
        jobDesc: The full job posting text
        companyName: Optional company name for context

    Returns:
        dict with keys: required_skills, preferred_skills,
                       technologies, experience_level, summary

    Raises:
        ConnectionError: If Ollama is not running
        TimeoutError: If Ollama takes too long
        ValueError: If Response is invalid or missing fields
    """
    # Build the Prompt
    company_context = f" from {companyName}" if companyName else ""
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
    Job description{company_context}: {jobDesc}
    Return ONLY the JSON object, no other text."""

    # Call Ollama
    url = "http://localhost:11434/api/generate"
    payload = {"model": "llama3.1", "prompt": prompt, "stream": False}

    try:
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()

        # Parsing and Validating Response
        # print("Raw LLM Response:")
        # print(data["response"])
        # print("\n" + "="*100 + "\n")
        responseText = data["response"].strip()
        if responseText.startswith("```"):
            # removes formatting backtics at start and end of output
            responseText = responseText.split("\n", 1)[1]
            responseText = responseText.rsplit("```", 1)[0]

        parsed = json.loads(responseText)
        requiredFields = [
            "required_skills",
            "preferred_skills",
            "technologies",
            "experience_level",
            "summary",
        ]
        missingFields = [field for field in requiredFields if field not in parsed]

        if missingFields:
            raise ValueError(f"LLM response missing following fields: {missingFields}")

        if companyName:
            parsed["company_name"] = companyName

        return parsed
    except requests.exceptions.ConnectionError:
        raise ConnectionError(
            "Cannot connect to Ollama. Is it running on localhost:11434?"
        )
    except requests.exceptions.Timeout:
        raise TimeoutError("Ollama request timed out after 30 seconds")
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {str(e)}")


# Testing Function Block
# if __name__ == "__main__":
#     jobDesc = input("Enter the job description: ")
#     companyName = input(
#         "Enter the company name (optional, press Enter to skip): "
#     ).strip()

#     # Convert empty string to None for optional parameter
#     companyName = companyName if companyName else None

#     result = analyze_job_description(jobDesc, companyName)
#     print(result)
