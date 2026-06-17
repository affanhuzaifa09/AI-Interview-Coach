# prompts/question_prompt.py
# This file contains the prompt template for interview question generation.
# We keep prompts separate from logic - this is clean, industry-standard practice.

from langchain_core.prompts import PromptTemplate

# PromptTemplate is a LangChain class that creates reusable prompt structures.
# The variables inside {} will be filled dynamically based on user input.

question_prompt_template = PromptTemplate(
    input_variables=["topic", "role", "difficulty"],
    template="""
You are an expert technical interviewer with 10+ years of experience.

Your task is to generate exactly 10 interview questions.

Details:
- Topic: {topic}
- Role: {role}  
- Difficulty Level: {difficulty}

Instructions:
- Questions must be relevant to the topic and role
- Match the difficulty level strictly
- Include a mix of conceptual and practical questions
- Number each question from 1 to 10
- Do not include answers, only questions
- Be specific, not generic

Generate the 10 interview questions now:
"""
)