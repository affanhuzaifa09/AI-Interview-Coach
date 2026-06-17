# app.py
# Main entry point of AI Interview Coach application.
# Streamlit UI that connects all modules together.

import streamlit as st
from modules.question_generator import generate_questions

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("🎯 AI Interview Coach")
st.sidebar.markdown("---")

module = st.sidebar.radio(
    "Select Module",
    [
        "🧠 Question Generator",
        "🎤 Mock Interview",
        "📊 Answer Evaluator",
        "📄 Resume Analyzer",
        "📚 RAG Knowledge Base"
    ]
)

# --- MODULE 1: QUESTION GENERATOR ---
if module == "🧠 Question Generator":

    st.title("🧠 Interview Question Generator")
    st.markdown("Generate customized interview questions based on topic, role and difficulty.")
    st.markdown("---")

    # --- TOPIC SELECTION ---
    st.markdown("### 📌 Topic")

    common_topics = [
        "Select a common topic...",
        "Python", "SQL", "Machine Learning", "Deep Learning",
        "Generative AI", "LangChain", "Data Science", "Statistics",
        "Computer Vision", "NLP", "FastAPI", "System Design",
        "Docker", "Kubernetes", "REST APIs", "Data Structures",
        "Algorithms", "Cloud Computing", "Spark", "Kafka"
    ]

    col_drop, col_or, col_text = st.columns([3, 0.3, 3])

    with col_drop:
        selected_topic = st.selectbox(
            "Choose a common topic",
            common_topics
        )

    with col_or:
        st.markdown("<br><br>**OR**", unsafe_allow_html=True)

    with col_text:
        custom_topic = st.text_input(
            "Type your own topic",
            placeholder="e.g. Rust, GraphQL, Reinforcement Learning..."
        )

    # Custom topic overrides dropdown if user typed something
    if custom_topic.strip() != "":
        topic = custom_topic.strip()
    elif selected_topic != "Select a common topic...":
        topic = selected_topic
    else:
        topic = None

    st.markdown("---")

    # --- ROLE AND DIFFICULTY ---
    col1, col2 = st.columns(2)

    with col1:
        role = st.selectbox(
            "👔 Select Role",
            [
                "Data Scientist",
                "Machine Learning Engineer",
                "Data Analyst",
                "Backend Developer",
                "AI Engineer",
                "GenAI Developer",
                "Data Engineer",
                "Full Stack Developer",
                "DevOps Engineer",
                "Software Engineer"
            ]
        )

    with col2:
        difficulty = st.selectbox(
            "⚡ Select Difficulty",
            ["Easy", "Medium", "Hard"]
        )

    st.markdown("---")

    # --- GENERATE BUTTON ---
    if st.button("🚀 Generate Questions", use_container_width=True):

        # Validate that topic is selected or typed
        if topic is None:
            st.warning("⚠️ Please select a topic from the dropdown or type your own.")
        else:
            with st.spinner(f"Generating {difficulty} level {topic} questions..."):
                try:
                    questions = generate_questions(topic, role, difficulty)

                    st.success("✅ Questions Generated Successfully!")
                    st.markdown("---")
                    st.markdown(f"### 📋 {difficulty} Level — {topic} — {role}")
                    st.markdown(questions)

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("Please check your GROQ_API_KEY in the .env file")