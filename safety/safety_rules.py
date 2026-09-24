from typing import List

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate

from prompts.safety_prompt import SAFETY_PROMPT
from models.wellness_schema import SafetyAssessment


def check_safety(plan) -> dict:
    """
    Perform deterministic safety checks on a generated wellness plan.
    """

    issues: List[str] = []

    text_fields = [
        plan.weekly_activity_target,
        plan.hydration_target,
        plan.sleep_target,
        *plan.exercise_plan,
        *plan.nutrition_guidelines,
        *plan.safety_notes,
    ]

    full_text = " ".join(text_fields).lower()

    # Check for medication or treatment recommendations
    medical_terms = [
        "prescribe",
        "prescription",
        "medication",
        "medicine",
        "drug",
        "treat",
        "treatment",
        "cure",
        "diagnose",
        "diagnosis",
    ]

    for term in medical_terms:
        if term in full_text:
            issues.append(
                f"Potential medical recommendation detected: '{term}'"
            )

    # Check for extreme dietary recommendations
    extreme_diet_terms = [
        "starve",
        "fast for",
        "no food",
        "zero calories",
        "extreme calorie restriction",
    ]

    for term in extreme_diet_terms:
        if term in full_text:
            issues.append(
                f"Potentially unsafe dietary recommendation detected: '{term}'"
            )

    # Check for potentially excessive exercise language
    excessive_exercise_terms = [
        "exercise all day",
        "work out for several hours",
        "no rest",
        "train without rest",
    ]

    for term in excessive_exercise_terms:
        if term in full_text:
            issues.append(
                f"Potentially excessive exercise recommendation detected: '{term}'"
            )

    # Ensure safety notes are present
    if not plan.safety_notes:
        issues.append("Safety notes are missing.")

    if issues:
        return {
            "status": "REVIEW",
            "issues": issues,
            "explanation": (
                "The wellness plan requires safety review because "
                "one or more deterministic safety checks were triggered."
            ),
        }

    return {
        "status": "SAFE",
        "issues": [],
        "explanation": (
            "The wellness plan passed the deterministic safety checks."
        ),
    }


def llm_safety_check(plan) -> SafetyAssessment:
    """
    Use an LLM to perform a structured safety assessment.
    """

    model = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0
    )

    prompt = ChatPromptTemplate.from_messages([
        ("system", SAFETY_PROMPT),
        (
            "human",
            "Review the following wellness plan:\n\n{wellness_plan}"
        )
    ])

    structured_model = model.with_structured_output(SafetyAssessment)

    chain = prompt | structured_model

    result = chain.invoke({
        "wellness_plan": plan.model_dump_json(indent=2)
    })

    return result


def run_safety_pipeline(plan) -> SafetyAssessment:
    """
    Run both deterministic and LLM-based safety checks
    and return one final safety assessment.
    """

    rule_result = check_safety(plan)

    # If deterministic rules detect a problem,
    # immediately require human/professional review.
    if rule_result["status"] == "REVIEW":
        return SafetyAssessment(
            status="REVIEW",
            issues=rule_result["issues"],
            explanation=rule_result["explanation"]
        )

    # Run the LLM safety judge when deterministic checks pass.
    llm_result = llm_safety_check(plan)

    if llm_result.status == "REVIEW":
        return llm_result

    return SafetyAssessment(
        status="SAFE",
        issues=[],
        explanation=(
            "The wellness plan passed both deterministic safety checks "
            "and the LLM safety review."
        )
    )