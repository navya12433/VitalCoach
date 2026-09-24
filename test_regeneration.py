from models.wellness_schema import WellnessPlan
from safety.safety_rules import check_safety


def create_test_plan(with_safety_issue=False):

    if with_safety_issue:

        return WellnessPlan(
            employee_id="E001",
            goal="Improve general fitness",
            fitness_level="Beginner",
            weekly_activity_target="Exercise all day",
            exercise_plan=[
                "Work out for several hours",
                "Train without rest"
            ],
            nutrition_guidelines=[
                "Eat balanced meals"
            ],
            hydration_target="Drink water regularly",
            sleep_target="7-9 hours per night",
            safety_notes=[
                "Continue activity even when tired"
            ]
        )

    return WellnessPlan(
        employee_id="E001",
        goal="Improve general fitness",
        fitness_level="Beginner",
        weekly_activity_target="Gradually work toward regular weekly activity",
        exercise_plan=[
            "Walk for 20-30 minutes on most days",
            "Include light strength exercises twice per week"
        ],
        nutrition_guidelines=[
            "Eat a balanced variety of foods"
        ],
        hydration_target="Drink water regularly throughout the day",
        sleep_target="Aim for 7-9 hours of sleep per night",
        safety_notes=[
            "Increase activity gradually",
            "Stop if you feel unwell"
        ]
    )


print("=" * 60)
print("VitalCoach Safety Regeneration Test")
print("=" * 60)


# --------------------------------------------------
# Attempt 1: Deliberately unsafe test plan
# --------------------------------------------------

print("\nAttempt 1: Testing an unsafe plan...")

plan_1 = create_test_plan(
    with_safety_issue=True
)

result_1 = check_safety(plan_1)

print(f"Safety Status: {result_1['status']}")
print("Issues:")

for issue in result_1["issues"]:
    print(f"- {issue}")


# --------------------------------------------------
# Simulate safety feedback
# --------------------------------------------------

if result_1["status"] == "REVIEW":

    previous_safety_feedback = (
        "The previous wellness plan received a REVIEW status.\n\n"
        "Safety issues identified:\n"
        + "\n".join(
            f"- {issue}"
            for issue in result_1["issues"]
        )
        + "\n\n"
        "Generate a new plan that corrects all of these issues."
    )

    print("\nSafety feedback generated successfully:")
    print(previous_safety_feedback)


# --------------------------------------------------
# Attempt 2: Safe replacement plan
# --------------------------------------------------

print("\nAttempt 2: Testing corrected plan...")

plan_2 = create_test_plan(
    with_safety_issue=False
)

result_2 = check_safety(plan_2)

print(f"Safety Status: {result_2['status']}")
print(f"Issues: {result_2['issues']}")


# --------------------------------------------------
# Final evaluation
# --------------------------------------------------

print("\n" + "=" * 60)

if (
    result_1["status"] == "REVIEW"
    and result_2["status"] == "SAFE"
):
    print("Safety Regeneration Logic: PASS")
    print(
        "The system correctly detects the unsafe first plan "
        "and accepts the corrected second plan."
    )
else:
    print("Safety Regeneration Logic: REVIEW")