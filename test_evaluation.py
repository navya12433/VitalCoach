from chains.personalization_chain import generate_wellness_plan
from evaluation import run_evaluation


employee_profile = {
    "employee_id": "E001",
    "goal": "Improve general fitness",
    "fitness_level": "Beginner",
    "work_style": "Mostly desk-based",
    "preferred_activity": "Walking"
}


print("=" * 60)
print("VitalCoach Evaluation Test")
print("=" * 60)


print("\nGenerating wellness plan...")

plan = generate_wellness_plan(
    employee_profile=employee_profile,
    goal=employee_profile["goal"],
    fitness_level=employee_profile["fitness_level"]
)


print("\nGenerated plan successfully.")


print("\nRunning evaluation...")

results = run_evaluation(
    plan,
    employee_profile
)


print("\n" + "=" * 60)
print("EVALUATION RESULTS")
print("=" * 60)


for result in results:

    print(f"\nCriterion: {result['criterion']}")
    print(f"Status: {result['status']}")
    print(f"Details: {result['details']}")

    if "issues" in result:
        print(f"Issues: {result['issues']}")