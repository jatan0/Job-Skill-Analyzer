# import httpx
import requests
import json as json_lib

# api endpoint and get request
url = "http://localhost:11434/api/generate"

prompt = """
You must respond with ONLY valid JSON. No other text before or after.

Analyze this job description and return a JSON object with these exact fields:
- required_skills: array of strings (3-5 items)
- experience_level: string (must be exactly "entry", "mid", or "senior")

Job description:
"We need a Python developer with 3+ years experience in FastAPI and PostgreSQL."

Remember: ONLY JSON, nothing else.
"""

payload = {"model": "llama3.1", "prompt": prompt, "stream": False}
response = requests.post(url, json=payload)
data = response.json()
print("Raw response:", data["response"])
print("\n" + "=" * 50 + "\n")

# Try to parse it as JSON
try:
    parsed = json_lib.loads(data["response"])
    print("Successfully parsed as JSON!")
    print(f"Required skills: {parsed['required_skills']}")
    print(f"Experience level: {parsed['experience_level']}")
except json_lib.JSONDecodeError as e:
    print(f"Failed to parse as JSON: {e}")
    print("The LLM didn't follow instructions perfectly")
