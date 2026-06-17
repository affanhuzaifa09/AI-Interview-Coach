# modules/mock_interview.py
# This file handles the mock interview logic.
# It manages conversation memory and communicates with the Groq LLM.

import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage
from prompts.interview_prompt import interview_prompt_template

load_dotenv()

def get_llm():
    """Creates and returns the Groq LLM instance."""
    return ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.7,
        api_key=os.getenv("GROQ_API_KEY")
    )

def start_interview(role: str, topic: str, difficulty: str, chat_history: list) -> str:
    """
    Starts the interview by sending the first message.
    The AI will greet the candidate and ask the first question.

    Args:
        role: Job role for the interview
        topic: Technical topic to be interviewed on
        difficulty: Easy, Medium, or Hard
        chat_history: Empty list at the start

    Returns:
        AI's opening message with first question
    """

    llm = get_llm()

    # Build the chain
    chain = interview_prompt_template | llm | StrOutputParser()

    # First message - empty user input to trigger AI greeting
    response = chain.invoke({
        "role": role,
        "topic": topic,
        "difficulty": difficulty,
        "chat_history": chat_history,
        "user_input": "Hello, I am ready to start the interview."
    })

    return response


def chat(user_answer: str, role: str, topic: str, 
         difficulty: str, chat_history: list) -> str:
    """
    Continues the interview conversation.
    Takes the candidate's answer, adds to history, gets next response.

    Args:
        user_answer: What the candidate just typed
        role: Job role
        topic: Technical topic
        difficulty: Difficulty level
        chat_history: Full conversation so far as list of messages

    Returns:
        AI's feedback + next question
    """

    llm = get_llm()

    # Build the chain
    chain = interview_prompt_template | llm | StrOutputParser()

    # Send full conversation history + new answer to LLM
    response = chain.invoke({
        "role": role,
        "topic": topic,
        "difficulty": difficulty,
        "chat_history": chat_history,  # Full memory passed here
        "user_input": user_answer
    })

    return response


def build_chat_history(messages: list) -> list:
    """
    Converts our stored messages into LangChain message format.

    Streamlit stores messages as:
    {"role": "user", "content": "..."}
    {"role": "assistant", "content": "..."}

    LangChain needs them as:
    HumanMessage(content="...")
    AIMessage(content="...")

    This function does that conversion.
    """

    history = []

    for message in messages:
        if message["role"] == "user":
            history.append(HumanMessage(content=message["content"]))
        elif message["role"] == "assistant":
            history.append(AIMessage(content=message["content"]))

    return history