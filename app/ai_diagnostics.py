"""Generate AI diagnostics using Groq API with safe fallback."""

import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GROQ_MODEL = "openai/gpt-oss-20b"


def get_ai_analysis(metrics, status):
    """Generate a short AI summary and recommendation."""

    api_key = os.getenv("LLM_API_KEY", "").strip()

    fallback = {
        "summary": (
            f"AI analysis is temporarily unavailable. "
            f"Current system status is {status}."
        ),
        "recommendation": (
            "Check the system metrics and try again when the AI service is available."
        )
    }

    if not api_key:
        return fallback

    prompt = f"""
You are a server health monitoring assistant.

Analyze these server metrics:
{json.dumps(metrics, indent=2)}

Current server status: {status}

Return ONLY valid JSON in this exact format:
{{
    "summary": "Write a short 1-2 sentence summary.",
    "recommendation": "Give one practical recommendation."
}}
"""

    try:
        response = requests.post(
            GROQ_URL,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": GROQ_MODEL,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "temperature": 0.3,
                "max_tokens": 300
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()
        ai_text = result["choices"][0]["message"]["content"].strip()

        # Remove Markdown code fences if the AI returns them.
        if ai_text.startswith("```"):
            ai_text = ai_text.replace("```json", "", 1)
            ai_text = ai_text.replace("```", "").strip()

        analysis = json.loads(ai_text)

        summary = analysis.get("summary")
        recommendation = analysis.get("recommendation")

        if not isinstance(summary, str) or not isinstance(recommendation, str):
            return fallback

        if not summary.strip() or not recommendation.strip():
            return fallback

        return {
            "summary": summary.strip(),
            "recommendation": recommendation.strip()
        }

    except Exception as e:
     print("AI DIAGNOSTIC ERROR:", repr(e))
     return fallback