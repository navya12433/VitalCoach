from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from prompts.system_prompt import SYSTEM_PROMPT
from prompts.few_shot_examples import FEW_SHOT_EXAMPLES
from prompts.planning_prompt import PLANNING_PROMPT
from models.wellness_schema import WellnessPlan
from rag.retriever import create_retriever


load_dotenv()


def create_personalization_chain():

    model = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.2
    )

    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            SYSTEM_PROMPT
        ),
        (
            "system",
            "Here are examples of the expected personalization behavior:\n"
            "{few_shot_examples}"
        ),
        (
            "system",
            "Relevant wellness guidance retrieved from trusted sources:\n"
            "{retrieved_guidance}"
        ),
        (
            "human",
            PLANNING_PROMPT
        )
    ])

    structured_model = model.with_structured_output(
        WellnessPlan
    )

    chain = prompt | structured_model

    return chain


def generate_wellness_plan(
    employee_profile,
    goal,
    fitness_level,
    previous_safety_feedback=None
):

    if previous_safety_feedback is None:
        previous_safety_feedback = (
            "No previous safety review. "
            "This is the first generation."
        )

    retriever = create_retriever()

    query = (
        f"Physical activity and wellness recommendations for an employee "
        f"whose goal is {goal} and fitness level is {fitness_level}"
    )

    retrieved_docs = retriever.invoke(
        query
    )

    retrieved_guidance = "\n\n".join(
        doc.page_content
        for doc in retrieved_docs
    )

    chain = create_personalization_chain()

    result = chain.invoke({
        "few_shot_examples": str(
            FEW_SHOT_EXAMPLES
        ),
        "retrieved_guidance": retrieved_guidance,
        "employee_profile": str(
            employee_profile
        ),
        "goal": goal,
        "fitness_level": fitness_level,
        "previous_safety_feedback": previous_safety_feedback
    })

    return result