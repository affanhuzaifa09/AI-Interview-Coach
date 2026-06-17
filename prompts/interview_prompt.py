# prompts/interview_prompt.py
# This file contains the prompt template for the mock interview module.
# Unlike Module 1, this prompt handles a full conversation with memory.

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# ChatPromptTemplate is used for conversational AI - it understands roles
# (system, human, assistant) unlike the simple PromptTemplate we used before.

interview_prompt_template = ChatPromptTemplate.from_messages([

    # SYSTEM MESSAGE - Sets the AI's personality and behavior rules
    # This message is sent once and defines how the AI behaves throughout
    ("system", """
You are a strict but fair technical interviewer with 10+ years of experience.

You are conducting a mock interview for the role of {role} on the topic of {topic}.
Difficulty level: {difficulty}

Your behavior rules:
- Ask ONE question at a time
- After the candidate answers, give brief feedback (2-3 lines)
- Mention what was good and what was missing
- Then ask the next relevant question
- Keep track of what was already asked - do not repeat questions
- After 5 questions, end the interview with a final performance summary
- Be professional, encouraging but honest

Start by greeting the candidate and asking the first question.
"""),

    # MESSAGES PLACEHOLDER - This is where the entire conversation history goes
    # Every message the user and AI have exchanged will be inserted here
    # This is what gives the AI its memory of the conversation
    MessagesPlaceholder(variable_name="chat_history"),

    # HUMAN MESSAGE - The candidate's current message/answer
    ("human", "{user_input}")
])