import json
from pathlib import Path

from utils.anonymization import anonymize_employee_id


PROGRESS_PATH = Path("data/progress.json")


def load_progress():
    with open(PROGRESS_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_hr_analytics():
    progress_data = load_progress()

    if not progress_data:
        return {
            "total_records": 0,
            "average_activity_minutes": 0,
            "average_sleep_hours": 0,
            "safe_plan_percentage": 0,
            "employees": []
        }

    total_records = len(progress_data)

    average_activity = (
        sum(item["activity_minutes"] for item in progress_data)
        / total_records
    )

    average_sleep = (
        sum(item["sleep_hours"] for item in progress_data)
        / total_records
    )

    safe_count = sum(
        1
        for item in progress_data
        if item["plan_status"] == "SAFE"
    )

    safe_percentage = (safe_count / total_records) * 100

    anonymous_employees = [
        {
            "anonymous_id": anonymize_employee_id(item["employee_id"]),
            "week": item["week"],
            "activity_minutes": item["activity_minutes"],
            "sleep_hours": item["sleep_hours"],
            "plan_status": item["plan_status"]
        }
        for item in progress_data
    ]

    return {
        "total_records": total_records,
        "average_activity_minutes": round(average_activity, 2),
        "average_sleep_hours": round(average_sleep, 2),
        "safe_plan_percentage": round(safe_percentage, 2),
        "employees": anonymous_employees
    }