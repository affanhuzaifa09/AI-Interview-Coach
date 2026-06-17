# modules/question_generator.py
# Uses modern LangChain syntax (pipe operator instead of LLMChain)

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from prompts.question_prompt import question_prompt_template

# Load environment variables from .env file
load_dotenv()

def generate_questions(topic: str, role: str, difficulty: str) -> str:
    """
    Generates 10 interview questions based on topic, role and difficulty.
    """

    # Initialize the Groq LLM
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Modern LangChain syntax using pipe operator
    # prompt | llm | parser forms a chain pipeline
    # StrOutputParser converts the LLM response object to a plain string
    chain = question_prompt_template | llm | StrOutputParser()

    # Run the chain with our inputs
    response = chain.invoke({
        "topic": topic,
        "role": role,
        "difficulty": difficulty
    })

    return response