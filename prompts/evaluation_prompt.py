# prompts/evaluation_prompt.py
# This prompt instructs the LLM to evaluate a candidate's answer
# and return structured feedback in a consistent format.

from langchain_core.prompts import PromptTemplate

evaluation_prompt_template = PromptTemplate(
    input_variables=["question", "user_answer", "role", "difficulty"],
    template="""
You are an expert technical interviewer evaluating a candidate's answer.

Interview Details:
- Role: {role}
- Difficulty: {difficulty}

Question Asked:
{question}

Candidate's Answer:
{user_answer}

Evaluate the answer and respond in EXACTLY this format:

SCORE: [X/10]

STRENGTHS:
- [What the candidate got right]
- [Another strength if any]

WEAKNESSES:
- [What was missing or incorrect]
- [Another weakness if any]

MISSING CONCEPTS:
- [Important concept not mentioned]
- [Another missing concept if any]

IDEAL ANSWER:
[Write a complete, ideal answer for this question in 4-6 lines]

FOLLOW-UP QUESTION:
[Ask one follow-up question based on the candidate's answer]

Be honest, specific and constructive. Do not be vague.
"""
)