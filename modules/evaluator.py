# modules/evaluator.py
# This file handles the answer evaluation logic.
# It takes a question + candidate answer and returns structured feedback.

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from prompts.evaluation_prompt import evaluation_prompt_template

load_dotenv()

def evaluate_answer(question: str, user_answer: str, 
                    role: str, difficulty: str) -> dict:
    """
    Evaluates a candidate's answer to an interview question.

    Args:
        question: The interview question that was asked
        user_answer: The candidate's answer
        role: Job role context
        difficulty: Difficulty level context

    Returns:
        Dictionary with parsed evaluation sections
    """

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,  # Lower temperature for consistent evaluation
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Build the chain
    chain = evaluation_prompt_template | llm | StrOutputParser()

    # Get raw evaluation from LLM
    raw_response = chain.invoke({
        "question": question,
        "user_answer": user_answer,
        "role": role,
        "difficulty": difficulty
    })

    # Parse the structured response into a dictionary
    result = parse_evaluation(raw_response)

    return result


def parse_evaluation(raw_text: str) -> dict:
    """
    Parses the structured LLM response into a clean dictionary.

    The LLM returns text like:
    SCORE: 7/10
    STRENGTHS:
    - Good point
    WEAKNESSES:
    - Missing something

    We convert this into:
    {
        "score": "7/10",
        "strengths": "- Good point",
        ...
    }
    """

    # Default values in case parsing fails
    result = {
        "score": "N/A",
        "strengths": "Not available",
        "weaknesses": "Not available",
        "missing_concepts": "Not available",
        "ideal_answer": "Not available",
        "follow_up": "Not available",
        "raw": raw_text
    }

    try:
        # Split response into sections by looking for our labels
        sections = {
            "score": extract_section(raw_text, "SCORE:", "STRENGTHS:"),
            "strengths": extract_section(raw_text, "STRENGTHS:", "WEAKNESSES:"),
            "weaknesses": extract_section(raw_text, "WEAKNESSES:", "MISSING CONCEPTS:"),
            "missing_concepts": extract_section(raw_text, "MISSING CONCEPTS:", "IDEAL ANSWER:"),
            "ideal_answer": extract_section(raw_text, "IDEAL ANSWER:", "FOLLOW-UP QUESTION:"),
            "follow_up": extract_section(raw_text, "FOLLOW-UP QUESTION:", None)
        }

        # Update result with parsed sections
        for key, value in sections.items():
            if value:
                result[key] = value.strip()

    except Exception:
        # If parsing fails, return raw response
        pass

    return result


def extract_section(text: str, start_label: str, end_label: str) -> str:
    """
    Extracts text between two labels.

    Example:
    extract_section(text, "SCORE:", "STRENGTHS:")
    Returns everything between SCORE: and STRENGTHS:
    """

    try:
        start_idx = text.find(start_label)
        if start_idx == -1:
            return ""

        # Move past the start label
        start_idx += len(start_label)

        if end_label:
            end_idx = text.find(end_label, start_idx)
            if end_idx == -1:
                return text[start_idx:].strip()
            return text[start_idx:end_idx].strip()
        else:
            # No end label - take everything till end
            return text[start_idx:].strip()

    except Exception:
        return ""