# modules/resume_analyzer.py
# This file analyzes a resume PDF and generates personalized interview questions.
# It uses the extracted text from pdf_loader and sends it to the LLM.

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# We define the prompt directly here since it's specific to resume analysis
resume_analysis_prompt = PromptTemplate(
    input_variables=["resume_text", "job_role"],
    template="""
You are an expert technical interviewer and resume analyst.

A candidate has applied for the role of: {job_role}

Here is their resume:
--------------------------
{resume_text}
--------------------------

Analyze the resume carefully and respond in EXACTLY this format:

EXTRACTED SKILLS:
- [List all technical skills found]

PROJECTS:
- [Project name]: [One line description]

TECHNOLOGIES USED:
- [All technologies, frameworks, libraries mentioned]

PERSONALIZED INTERVIEW QUESTIONS:
1. [Question directly referencing a specific project from resume]
2. [Question about a specific technology they used]
3. [Question about their most recent experience]
4. [Question challenging a technical choice they made]
5. [Question about how their experience relates to {job_role}]
6. [Question about a gap or weakness you noticed in their resume]
7. [Question about scaling or improving one of their projects]
8. [General role-specific question based on their background]

RESUME STRENGTHS:
- [What stands out positively]

RESUME IMPROVEMENTS:
- [What could be added or improved]

Be specific. Reference actual project names, technologies and experiences from the resume.
"""
)


def analyze_resume(resume_text: str, job_role: str) -> dict:
    """
    Analyzes resume text and generates personalized interview questions.

    Args:
        resume_text: Extracted text from the resume PDF
        job_role: The role the candidate is applying for

    Returns:
        Dictionary with parsed resume analysis sections
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.5,
        api_key=os.getenv("GROQ_API_KEY")
    )

    chain = resume_analysis_prompt | llm | StrOutputParser()

    raw_response = chain.invoke({
        "resume_text": resume_text,
        "job_role": job_role
    })

    # Parse the response into sections
    result = parse_resume_analysis(raw_response)
    return result


def parse_resume_analysis(raw_text: str) -> dict:
    """
    Parses the structured LLM response into a clean dictionary.
    """

    result = {
        "skills": "Not found",
        "projects": "Not found",
        "technologies": "Not found",
        "questions": "Not found",
        "strengths": "Not found",
        "improvements": "Not found",
        "raw": raw_text
    }

    try:
        sections = {
            "skills": extract_section(
                raw_text, "EXTRACTED SKILLS:", "PROJECTS:"),
            "projects": extract_section(
                raw_text, "PROJECTS:", "TECHNOLOGIES USED:"),
            "technologies": extract_section(
                raw_text, "TECHNOLOGIES USED:", "PERSONALIZED INTERVIEW QUESTIONS:"),
            "questions": extract_section(
                raw_text, "PERSONALIZED INTERVIEW QUESTIONS:", "RESUME STRENGTHS:"),
            "strengths": extract_section(
                raw_text, "RESUME STRENGTHS:", "RESUME IMPROVEMENTS:"),
            "improvements": extract_section(
                raw_text, "RESUME IMPROVEMENTS:", None)
        }

        for key, value in sections.items():
            if value:
                result[key] = value.strip()

    except Exception:
        pass

    return result


def extract_section(text: str, start_label: str, end_label: str) -> str:
    """Extracts text between two labels."""
    try:
        start_idx = text.find(start_label)
        if start_idx == -1:
            return ""
        start_idx += len(start_label)
        if end_label:
            end_idx = text.find(end_label, start_idx)
            if end_idx == -1:
                return text[start_idx:].strip()
            return text[start_idx:end_idx].strip()
        else:
            return text[start_idx:].strip()
    except Exception:
        return ""