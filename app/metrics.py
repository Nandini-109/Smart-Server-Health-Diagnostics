"""Collect CPU, memory, and disk usage from the local computer."""

import os
import psutil


def collect_metrics():
    """Return current CPU, memory, and disk usage percentages."""
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_percent = psutil.virtual_memory().percent

    # On Windows, check the current system drive; on other systems, check root.
    if os.name == "nt":
        disk_path = os.environ.get("SystemDrive", "C:") + "\\"
    else:
        disk_path = "/"

    disk_percent = psutil.disk_usage(disk_path).percent

    return {
        "cpu_percent": round(cpu_percent, 1),
        "memory_percent": round(memory_percent, 1),
        "disk_percent": round(disk_percent, 1),
    }


def classify_status(metrics):
    """Classify overall health using the highest resource utilization."""
    highest_usage = max(metrics.values())

    if highest_usage > 85:
        return "CRITICAL"
    if highest_usage > 70:
        return "WARNING"
    return "HEALTHY"
