# Smart Server Health Diagnostics API

A small Python REST API that checks the local computer's CPU, memory, and disk usage, classifies system health, and optionally asks Groq for a short diagnostic summary and recommendation.

## Requirements

* Python 3.9 or newer
* Internet connection for Groq AI analysis
* A Groq API key (optional; the API still works without it using a fallback message)

## 1\. Open the project

Open this folder in VS Code:
`Smart-Server-Health-Diagnostics`

## 2\. Install dependencies

Open the VS Code terminal in this folder and run:

```bash
python -m pip install -r requirements.txt
```

## 3\. Configure the Groq API key (optional)

1. Make a copy of `.env.example`.
2. Rename the copy to `.env`.
3. Replace `your\\\_groq\\\_api\\\_key\\\_here` with your Groq API key.

The real `.env` file is ignored by Git. Never publish your API key.

If you do not add a key, the endpoint still works and returns a clear fallback AI message.

## 4\. Start the API

In the VS Code terminal, run:

```bash
python -m uvicorn app.main:app --reload
```

Or on Windows, double-click `run.bat`.

## 5\. Test the endpoint

Open this URL in your browser:

`http://127.0.0.1:8000/api/health-report`

Interactive API documentation is available at:

`http://127.0.0.1:8000/docs`

## Example JSON response

The percentages and timestamp below are examples. Your actual values will depend on your computer.

```json
{
  "timestamp": "2026-11-21T16:30:00Z",
  "status": "WARNING",
  "metrics": {
    "cpu\\\_percent": 76.5,
    "memory\\\_percent": 68.2,
    "disk\\\_percent": 54.0
  },
  "ai\\\_analysis": {
    "summary": "CPU usage is elevated, while memory and disk usage are within normal limits.",
    "recommendation": "Check for background applications that may be using significant CPU resources."
  }
}
```

## Project structure

```text
Smart-Server-Health-Diagnostics/
│
├── app/
│   ├── \\\_\\\_init\\\_\\\_.py
│   ├── metrics.py
│   ├── ai\\\_diagnostics.py
│   └── main.py
│
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
└── run.bat
```

## How the project works

1. `metrics.py` reads CPU, memory, and disk usage using `psutil`.
2. `metrics.py` classifies the overall status:

   * Above 85%: `CRITICAL`
   * Above 70%: `WARNING`
   * Otherwise: `HEALTHY`
3. `ai\\\_diagnostics.py` sends the metrics and status to Groq and requests a JSON summary and recommendation.
4. If the API key is missing or the AI request fails, a fallback message is returned instead of crashing.
5. `main.py` exposes the `GET /api/health-report` endpoint using FastAPI.





### **Automated Testing**



Automated unit tests are included to verify AI fallback handling.



Test Scenarios



\- Missing API key

\- Invalid API key

\- API request timeout

\- Invalid AI response



Run Tests



Run this command from the project root directory:



python -m unittest discover -s tests -v



Test Results



All 4 automated fallback tests passed successfully.

## 

## 

## 

## Notes

* No database, Docker, Redis, or frontend is required.
* The disk usage is checked for the current system drive on Windows and the root filesystem on other operating systems.
* The AI integration requires a valid Groq API key and internet access.

