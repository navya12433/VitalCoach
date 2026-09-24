PLANNING_PROMPT = """
Create a personalized corporate wellness plan using the employee profile below.

Employee Profile:
{employee_profile}

Wellness Goal:
{goal}

Fitness Level:
{fitness_level}

Previous Safety Review:
{previous_safety_feedback}

Follow these requirements:

- Personalize the recommendations to the employee's goal and fitness level.
- Consider the employee's work style and preferred activity when appropriate.
- Provide practical exercise recommendations.
- Provide general healthy-eating guidelines.
- Include a reasonable hydration target.
- Include a reasonable sleep target.
- Include clear safety notes.
- Avoid medical diagnosis or treatment.
- Avoid medication or supplement prescriptions.
- Avoid extreme diets and unsafe exercise recommendations.
- Do not make unsupported medical claims.
- Keep the recommendations realistic for a working employee.
- Follow the retrieved wellness guidance when relevant.
- If a previous safety review identified issues, correct those issues
  in the new plan.
- Do not repeat recommendations that were identified as unsafe.
- Return the result according to the WellnessPlan structured schema.

Generate only the wellness plan information.
"""