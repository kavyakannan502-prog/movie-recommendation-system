
import csv
from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).with_name("api_logs.csv")

HEADERS = [
    "timestamp",
    "user_id",
    "latency_ms",
    "status",
    "recommendations_count",
]


def write_log(user_id, latency_ms, status, recommendations_count):
    file_exists = LOG_FILE.exists()
    needs_header = (
        not file_exists or LOG_FILE.stat().st_size == 0
    )

    with LOG_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if needs_header:
            writer.writerow(HEADERS)

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            user_id,
            round(float(latency_ms), 2),
            status,
            recommendations_count,
        ])


def log_request(
    user_id, latency_ms, status_code, recommendations_count
):
    """Record an API request in the monitoring log."""
    write_log(
        user_id,
        latency_ms,
        status_code,
        recommendations_count,
    )
