import json
from pathlib import Path

import pandas as pd
import streamlit as st

from chains.personalization_chain import generate_wellness_plan
from safety.safety_rules import run_safety_pipeline
from utils.analytics import generate_hr_analytics


EMPLOYEES_PATH = Path("data/employees.json")


def load_employees():
    with open(EMPLOYEES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


st.set_page_config(
    page_title="VitalCoach",
    page_icon="💚",
    layout="wide"
)


# ==================================================
# MAIN HEADER
# ==================================================

st.title("💚 VitalCoach")

st.subheader(
    "Corporate Wellness Program Personalization Agent"
)

st.write(
    "Create safe and personalized wellness guidance "
    "based on an employee's profile and wellness goal."
)

st.divider()


# ==================================================
# EMPLOYEE PROFILE
# ==================================================

st.header("Employee Profile")

employees = load_employees()

employee_ids = [
    employee["employee_id"]
    for employee in employees
]

selected_employee_id = st.selectbox(
    "Select Employee",
    employee_ids
)

selected_employee = next(
    employee
    for employee in employees
    if employee["employee_id"] == selected_employee_id
)

goal = selected_employee["goal"]
fitness_level = selected_employee["fitness_level"]
work_style = selected_employee["work_style"]
preferred_activity = selected_employee["preferred_activity"]

st.write(
    "**Wellness Goal:**",
    goal
)

st.write(
    "**Fitness Level:**",
    fitness_level
)

st.write(
    "**Work Style:**",
    work_style
)

st.write(
    "**Preferred Activity:**",
    preferred_activity
)


# ==================================================
# WELLNESS PLAN GENERATION + SAFETY REGENERATION
# ==================================================

if st.button("Generate Wellness Plan"):

    MAX_ATTEMPTS = 2

    plan = None
    safety_result = None

    previous_safety_feedback = (
        "No previous safety review. "
        "This is the first generation."
    )

    # --------------------------------------------------
    # Maximum 2 generation attempts
    # --------------------------------------------------

    for attempt in range(1, MAX_ATTEMPTS + 1):

        with st.spinner(
            f"Generating personalized wellness plan "
            f"(attempt {attempt}/{MAX_ATTEMPTS})..."
        ):

            plan = generate_wellness_plan(
                employee_profile=selected_employee,
                goal=goal,
                fitness_level=fitness_level,
                previous_safety_feedback=previous_safety_feedback
            )

        with st.spinner(
            f"Running safety review "
            f"(attempt {attempt}/{MAX_ATTEMPTS})..."
        ):

            safety_result = run_safety_pipeline(plan)

        # --------------------------------------------------
        # Stop if plan is safe
        # --------------------------------------------------

        if safety_result.status == "SAFE":
            break

        # --------------------------------------------------
        # Regenerate if unsafe and another attempt remains
        # --------------------------------------------------

        if attempt < MAX_ATTEMPTS:

            previous_safety_feedback = (
                "The previous wellness plan received a REVIEW status.\n\n"
                "Safety issues identified:\n"
                + "\n".join(
                    f"- {issue}"
                    for issue in safety_result.issues
                )
                + "\n\n"
                "Generate a new plan that corrects all of these issues."
            )


    # ==================================================
    # SAFETY REVIEW
    # ==================================================

    st.header("Safety Review")

    if safety_result.status == "SAFE":

        st.success(
            f"✅ Safety Status: SAFE "
            f"(Passed on attempt {attempt})"
        )

    else:

        st.warning(
            f"⚠️ Safety Status: REVIEW "
            f"(After {MAX_ATTEMPTS} attempts)"
        )

        st.write("**Issues detected:**")

        for issue in safety_result.issues:
            st.write(
                "•",
                issue
            )

    st.info(
        safety_result.explanation
    )

    st.divider()


    # ==================================================
    # PERSONALIZED WELLNESS PLAN
    # ==================================================

    st.header(
        "Your Personalized Wellness Plan"
    )

    st.write(
        "**Employee ID:**",
        plan.employee_id
    )

    st.write(
        "**Goal:**",
        plan.goal
    )

    st.write(
        "**Fitness Level:**",
        plan.fitness_level
    )


    # --------------------------------------------------
    # Weekly Activity
    # --------------------------------------------------

    st.subheader(
        "Weekly Activity Target"
    )

    st.write(
        plan.weekly_activity_target
    )


    # --------------------------------------------------
    # Exercise
    # --------------------------------------------------

    st.subheader(
        "Exercise Plan"
    )

    for item in plan.exercise_plan:

        st.write(
            "•",
            item
        )


    # --------------------------------------------------
    # Nutrition
    # --------------------------------------------------

    st.subheader(
        "Nutrition Guidelines"
    )

    for item in plan.nutrition_guidelines:

        st.write(
            "•",
            item
        )


    # --------------------------------------------------
    # Hydration
    # --------------------------------------------------

    st.subheader(
        "Hydration Target"
    )

    st.write(
        plan.hydration_target
    )


    # --------------------------------------------------
    # Sleep
    # --------------------------------------------------

    st.subheader(
        "Sleep Target"
    )

    st.write(
        plan.sleep_target
    )


    # --------------------------------------------------
    # Safety Notes
    # --------------------------------------------------

    st.subheader(
        "Safety Notes"
    )

    for item in plan.safety_notes:

        st.write(
            "•",
            item
        )


# ==================================================
# WELLNESS PROGRESS TRACKING
# ==================================================

st.divider()

st.header(
    "📊 Wellness Progress Tracking"
)

analytics = generate_hr_analytics()


# --------------------------------------------------
# Summary Metrics
# --------------------------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Average Activity",
        f"{analytics['average_activity_minutes']} min/week"
    )


with col2:

    st.metric(
        "Average Sleep",
        f"{analytics['average_sleep_hours']} hrs"
    )


with col3:

    st.metric(
        "Safe Plans",
        f"{analytics['safe_plan_percentage']}%"
    )


# ==================================================
# EMPLOYEE PROGRESS TABLE
# ==================================================

st.subheader(
    "Employee Progress"
)

progress_rows = analytics["employees"]

st.dataframe(
    progress_rows,
    use_container_width=True
)


# ==================================================
# HR ANALYTICS
# ==================================================

st.divider()

st.header(
    "🏢 HR Analytics"
)

st.write(
    "Aggregate wellness indicators and anonymous progress "
    "information for corporate wellness monitoring."
)


# Convert progress data to DataFrame

progress_df = pd.DataFrame(
    progress_rows
)


# --------------------------------------------------
# Weekly Activity Overview
# --------------------------------------------------

st.subheader(
    "Weekly Activity Overview"
)

activity_df = progress_df[
    [
        "anonymous_id",
        "activity_minutes"
    ]
].rename(
    columns={
        "anonymous_id": "Anonymous Employee",
        "activity_minutes": "Activity Minutes"
    }
)

st.bar_chart(
    activity_df,
    x="Anonymous Employee",
    y="Activity Minutes"
)


# --------------------------------------------------
# Sleep Overview
# --------------------------------------------------

st.subheader(
    "Sleep Overview"
)

sleep_df = progress_df[
    [
        "anonymous_id",
        "sleep_hours"
    ]
].rename(
    columns={
        "anonymous_id": "Anonymous Employee",
        "sleep_hours": "Sleep Hours"
    }
)

st.bar_chart(
    sleep_df,
    x="Anonymous Employee",
    y="Sleep Hours"
)


# --------------------------------------------------
# Safety Status Distribution
# --------------------------------------------------

st.subheader(
    "Plan Safety Status"
)

status_counts = (
    progress_df["plan_status"]
    .value_counts()
    .reset_index()
)

status_counts.columns = [
    "Safety Status",
    "Number of Plans"
]

st.bar_chart(
    status_counts,
    x="Safety Status",
    y="Number of Plans"
)