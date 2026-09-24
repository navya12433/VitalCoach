# 💚 VitalCoach

## Corporate Wellness Program Personalization Agent

VitalCoach is an AI-powered corporate wellness personalization system that generates safe and personalized wellness plans based on an employee's profile, wellness goal, fitness level, work style, and preferred activity.

The system combines prompt engineering, structured LLM output, Retrieval-Augmented Generation (RAG), safety validation, progress tracking, and pseudonymous HR analytics.

---

## 🎯 Project Objective

The objective of VitalCoach is to provide personalized and practical wellness guidance for employees while maintaining safety constraints.

The system can generate recommendations related to:

- Physical activity
- Exercise
- Healthy eating
- Hydration
- Sleep
- Workplace activity habits

The system is designed for general wellness guidance and does not provide medical diagnosis or treatment.

---

## 🏗️ System Architecture

```text
Employee Profile
       ↓
Goal Personalization
       ↓
Prompt Engineering
       ↓
RAG / WHO Physical Activity Guidance
       ↓
Structured Wellness Plan
       ↓
Safety Rules + LLM Safety Judge
       ↓
SAFE / REVIEW
       ↓
Safety-based Regeneration
       ↓
Progress Tracking
       ↓
Pseudonymous HR Analytics
```

---

## 🧠 Prompt Engineering Techniques

VitalCoach uses multiple prompt-engineering techniques to improve personalization, structure, and safety.

### 1. Role-based prompting

The system defines the LLM as an AI corporate wellness personalization assistant that provides practical and safe wellness guidance.

### 2. Few-shot prompting

Example employee profiles and expected recommendation behavior are provided to guide the model toward consistent personalized outputs.

### 3. Constraint prompting

The system prompt explicitly restricts:

- Medical diagnosis
- Medication recommendations
- Medical treatment
- Extreme diets
- Unsafe exercise
- Unsupported medical claims

### 4. Structured output

The generated wellness plan is returned using a Pydantic `WellnessPlan` schema.

The safety evaluation is returned using a structured `SafetyAssessment` schema.

### 5. Safety feedback prompting

If a generated plan receives a `REVIEW` status, the identified safety issues are passed back to the generation prompt so that the next generation can correct those issues.

---

## 📚 Retrieval-Augmented Generation (RAG)

VitalCoach uses Retrieval-Augmented Generation to provide wellness recommendations using trusted reference material.

The current knowledge base uses:

- WHO Physical Activity and Sedentary Behaviour Guidelines

### RAG Pipeline

```text
WHO Guideline PDF
       ↓
Document Loading
       ↓
Text Chunking
       ↓
HuggingFace Embeddings
       ↓
FAISS Vector Store
       ↓
Similarity Retrieval
       ↓
Relevant Guidance
       ↓
Wellness Plan Generation
```

The RAG pipeline retrieves relevant guidance before generating the personalized wellness plan.

---

## 🛡️ Safety and Validation

VitalCoach uses multiple safety mechanisms to reduce unsafe wellness recommendations.

### Deterministic Safety Rules

The system checks generated plans for:

- Medication or supplement recommendations
- Medical diagnosis
- Medical treatment recommendations
- Extreme dietary restrictions
- Excessive exercise
- Missing safety guidance

If a safety rule is triggered, the plan receives a `REVIEW` status.

### LLM Safety Judge

Plans that pass the deterministic checks are additionally reviewed by an LLM-based safety judge.

The safety judge checks whether the plan:

- Follows general wellness guidelines
- Avoids medical claims
- Avoids unsafe recommendations
- Contains appropriate safety guidance
- Uses realistic activity, hydration, and sleep targets

The result is returned as a structured `SafetyAssessment`.

### Safety Regeneration

If a generated plan receives a `REVIEW` status, the identified issues are passed back to the generation chain.

The system can make up to two generation attempts:

```text
Generate Plan
     ↓
Safety Check
     ↓
SAFE → Continue
     ↓
REVIEW
     ↓
Safety Feedback
     ↓
Regenerate Plan
     ↓
Safety Check
```

---

## 🧪 Evaluation

VitalCoach includes evaluation checks to verify the quality, safety, and reliability of generated wellness plans.

The evaluation covers:

- **Structured JSON Validity** – verifies that the generated plan follows the `WellnessPlan` schema.
- **Personalization** – checks whether recommendations match the employee's goal, fitness level, and preferred activity.
- **RAG Grounding** – verifies that relevant guidance can be retrieved from the WHO guideline knowledge base.
- **Safety Validation** – checks generated plans using deterministic safety rules and the LLM safety judge.
- **Constraint Adherence** – verifies that the system avoids medical diagnosis, medication recommendations, treatment claims, extreme diets, and unsafe exercise.
- **Anonymization** – verifies that employee identifiers used for analytics are transformed into pseudonymous identifiers.

### Safety Regeneration Test

The regeneration mechanism was tested using an intentionally unsafe wellness plan.

```text
Unsafe Plan
    ↓
Safety Check → REVIEW
    ↓
Safety Feedback
    ↓
Regenerate
    ↓
Corrected Plan
    ↓
Safety Check → SAFE
```

---

## ✨ Key Features

- Personalized wellness plan generation
- Role-based and few-shot prompt engineering
- Structured Pydantic output validation
- RAG using WHO physical-activity guidance
- FAISS-based semantic retrieval
- Deterministic safety rule checking
- LLM-based safety evaluation
- Safety-feedback-based plan regeneration
- Employee progress tracking
- Pseudonymous employee identifiers for analytics
- HR wellness analytics dashboard
- Streamlit-based interactive interface

---

## 🛠️ Technologies Used

### Programming Language

- Python

### LLM and Prompt Engineering

- Groq LLM
- LangChain
- LangChain Expression Language (LCEL)
- Few-shot prompting
- Structured output prompting

### RAG

- PyPDFLoader
- RecursiveCharacterTextSplitter
- HuggingFace Embeddings
- FAISS

### Validation and Safety

- Pydantic
- Deterministic safety rules
- LLM-based safety judge

### Frontend

- Streamlit

### Data and Analytics

- JSON
- Pandas

### Development Tools

- VS Code
- Python Virtual Environment
- Git / GitHub

---

## 📁 Project Structure

```text
VitalCoach/
│
├── app.py
├── evaluation.py
├── requirements.txt
├── .env
├── README.md
│
├── prompts/
│   ├── system_prompt.py
│   ├── few_shot_examples.py
│   ├── planning_prompt.py
│   └── safety_prompt.py
│
├── chains/
│   ├── personalization_chain.py
│   ├── planning_chain.py
│   ├── rag_chain.py
│   └── safety_chain.py
│
├── models/
│   └── wellness_schema.py
│
├── rag/
│   ├── documents/
│   │   └── WHO_Physical_Activity_Guidelines.pdf
│   ├── vectorstore/
│   │   ├── index.faiss
│   │   └── index.pkl
│   ├── ingest.py
│   └── retriever.py
│
├── safety/
│   └── safety_rules.py
│
├── data/
│   ├── employees.json
│   └── progress.json
│
└── utils/
    ├── anonymization.py
    └── analytics.py
```

---

## ⚠️ Limitations

- VitalCoach provides general wellness guidance and is not a medical diagnostic system.
- The current RAG knowledge base focuses on physical-activity guidance from the WHO guideline.
- The generated recommendations depend on the quality and completeness of the employee profile.
- LLM-generated recommendations may require human review in real-world corporate wellness deployments.
- Pseudonymous employee IDs are used for analytics; they should not be treated as complete anonymization by themselves.
- The current prototype uses sample employee and progress data.

---

## 📌 Project Status

VitalCoach is an academic prototype demonstrating prompt engineering, LLM-based personalization, RAG, safety validation, and wellness analytics.

The system is intended for educational and demonstration purposes and should be further validated before use in a real corporate wellness environment.