from pydantic import BaseModel
from typing import List


class WellnessPlan(BaseModel):
    employee_id: str
    goal: str
    fitness_level: str
    weekly_activity_target: str
    exercise_plan: List[str]
    nutrition_guidelines: List[str]
    hydration_target: str
    sleep_target: str
    safety_notes: List[str]


class SafetyAssessment(BaseModel):
    status: str
    issues: List[str]
    explanation: str