from models.wellness_schema import WellnessPlan
from safety.safety_rules import run_safety_pipeline
from utils.anonymization import anonymize_employee_id


def evaluate_structured_output(plan):
    """
    Check whether the generated plan follows the WellnessPlan schema.
    """

    if isinstance(plan, WellnessPlan):
        return {
            "criterion": "Structured JSON validity",
            "status": "PASS",
            "details": "Generated output successfully matches the WellnessPlan schema."
        }

    return {
        "criterion": "Structured JSON validity",
        "status": "FAIL",
        "details": "Generated output does not match the WellnessPlan schema."
    }


def evaluate_personalization(plan, employee_profile):
    """
    Check whether the plan reflects the employee's profile.
    """

    goal = employee_profile["goal"].lower()
    fitness_level = employee_profile["fitness_level"].lower()
    preferred_activity = employee_profile["preferred_activity"].lower()

    plan_text = " ".join([
        plan.goal,
        plan.fitness_level,
        plan.weekly_activity_target,
        *plan.exercise_plan,
        *plan.nutrition_guidelines
    ]).lower()

    goal_match = goal in plan_text
    fitness_match = fitness_level in plan_text
    activity_match = preferred_activity in plan_text

    passed = goal_match and fitness_match and activity_match

    return {
        "criterion": "Personalization",
        "status": "PASS" if passed else "REVIEW",
        "details": {
            "goal_match": goal_match,
            "fitness_level_match": fitness_match,
            "preferred_activity_match": activity_match
        }
    }


def evaluate_safety(plan):
    """
    Run the existing safety pipeline.
    """

    result = run_safety_pipeline(plan)

    return {
        "criterion": "Safety",
        "status": result.status,
        "details": result.explanation,
        "issues": result.issues
    }


def evaluate_anonymization():
    """
    Check whether employee IDs are transformed into pseudonymous identifiers.
    """

    original_id = "E001"

    anonymous_id = anonymize_employee_id(
        original_id
    )

    passed = (
        anonymous_id != original_id
        and anonymous_id.startswith("EMP-")
    )

    return {
        "criterion": "Anonymization",
        "status": "PASS" if passed else "FAIL",
        "details": {
            "original_id": original_id,
            "anonymous_id": anonymous_id
        }
    }


def run_evaluation(plan, employee_profile):

    results = []

    results.append(
        evaluate_structured_output(plan)
    )

    results.append(
        evaluate_personalization(
            plan,
            employee_profile
        )
    )

    results.append(
        evaluate_safety(plan)
    )

    results.append(
        evaluate_anonymization()
    )

    return results


if __name__ == "__main__":

    print("=" * 60)
    print("VitalCoach Evaluation")
    print("=" * 60)

    employee_profile = {
        "employee_id": "E001",
        "goal": "Improve general fitness",
        "fitness_level": "Beginner",
        "work_style": "Mostly desk-based",
        "preferred_activity": "Walking"
    }

    sample_plan = WellnessPlan(
        employee_id="E001",
        goal="Improve general fitness",
        fitness_level="Beginner",
        weekly_activity_target=(
            "Gradually work toward 150 minutes of moderate "
            "activity per week through walking"
        ),
        exercise_plan=[
            "Begin with 20-30 minute walking sessions on most days",
            "Add light strength exercises 2 days per week"
        ],
        nutrition_guidelines=[
            "Eat a balanced diet with vegetables, fruits, "
            "whole grains, and lean protein"
        ],
        hydration_target=(
            "Drink water regularly throughout the day"
        ),
        sleep_target=(
            "Aim for 7-9 hours of sleep per night"
        ),
        safety_notes=[
            "Start gradually and stop if you feel unusual "
            "pain, dizziness, or feel unwell"
        ]
    )

    results = run_evaluation(
        sample_plan,
        employee_profile
    )

    print("\nEvaluation Results:")
    print("-" * 60)

    for result in results:

        print(f"\nCriterion: {result['criterion']}")
        print(f"Status: {result['status']}")
        print(f"Details: {result['details']}")

        if "issues" in result:
            print(f"Issues: {result['issues']}")

    print("\n" + "=" * 60)
    print("Evaluation completed.")
    print("=" * 60)