"""FastAPI application for the Smart Server Health Diagnostics API."""

from datetime import datetime, timezone

from fastapi import FastAPI

from app.metrics import collect_metrics, classify_status
from app.ai_diagnostics import get_ai_analysis

app = FastAPI(
    title="Smart Server Health Diagnostics API",
    description="Checks local system health and provides an AI diagnostic report.",
    version="1.0.0",
)


@app.get("/api/health-report")
def health_report():
    """Collect system metrics and return a health report."""
    metrics = collect_metrics()
    status = classify_status(metrics)
    ai_analysis = get_ai_analysis(metrics, status)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "status": status,
        "metrics": metrics,
        "ai_analysis": ai_analysis,
    }


@app.get("/")
def home():
    return {
        "message": "Smart Server Health Diagnostics API is running.",
        "docs": "/docs",
        "health_report": "/api/health-report",
    }
