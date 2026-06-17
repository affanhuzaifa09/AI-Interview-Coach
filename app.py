# app.py
# Main entry point of AI Interview Coach application.

import streamlit as st
from modules.question_generator import generate_questions
from modules.mock_interview import start_interview, chat, build_chat_history
from modules.evaluator import evaluate_answer

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AI Interview Coach",
    page_icon="🎯",
    layout="wide"
)

# --- SIDEBAR ---
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

# ============================================================
# MODULE 1: QUESTION GENERATOR
# ============================================================
if module == "🧠 Question Generator":

    st.title("🧠 Interview Question Generator")
    st.markdown("Generate customized interview questions based on topic, role and difficulty.")
    st.markdown("---")

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
        selected_topic = st.selectbox("Choose a common topic", common_topics)

    with col_or:
        st.markdown("<br><br>**OR**", unsafe_allow_html=True)

    with col_text:
        custom_topic = st.text_input(
            "Type your own topic",
            placeholder="e.g. Rust, GraphQL, Reinforcement Learning..."
        )

    if custom_topic.strip() != "":
        topic = custom_topic.strip()
    elif selected_topic != "Select a common topic...":
        topic = selected_topic
    else:
        topic = None

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        role = st.selectbox(
            "👔 Select Role",
            ["Data Scientist", "Machine Learning Engineer", "Data Analyst",
             "Backend Developer", "AI Engineer", "GenAI Developer",
             "Data Engineer", "Full Stack Developer", "DevOps Engineer",
             "Software Engineer"]
        )

    with col2:
        difficulty = st.selectbox(
            "⚡ Select Difficulty",
            ["Easy", "Medium", "Hard"]
        )

    st.markdown("---")

    if st.button("🚀 Generate Questions", use_container_width=True):
        if topic is None:
            st.warning("⚠️ Please select a topic or type your own.")
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

# ============================================================
# MODULE 2: MOCK INTERVIEW
# ============================================================
elif module == "🎤 Mock Interview":

    st.title("🎤 Mock Interview")
    st.markdown("Practice a real conversational interview with AI feedback after every answer.")
    st.markdown("---")

    if "interview_active" not in st.session_state:
        st.session_state.interview_active = False
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "interview_config" not in st.session_state:
        st.session_state.interview_config = {}

    if not st.session_state.interview_active:

        st.markdown("### ⚙️ Interview Setup")
        col1, col2, col3 = st.columns(3)

        with col1:
            mock_topic = st.selectbox(
                "📌 Topic",
                ["Python", "SQL", "Machine Learning", "Deep Learning",
                 "Generative AI", "LangChain", "Data Science", "Statistics",
                 "Computer Vision", "NLP", "FastAPI", "System Design"]
            )
        with col2:
            mock_role = st.selectbox(
                "👔 Role",
                ["Data Scientist", "Machine Learning Engineer", "Data Analyst",
                 "Backend Developer", "AI Engineer", "GenAI Developer",
                 "Data Engineer", "Software Engineer"]
            )
        with col3:
            mock_difficulty = st.selectbox(
                "⚡ Difficulty",
                ["Easy", "Medium", "Hard"]
            )

        st.markdown("---")

        if st.button("🚀 Start Interview", use_container_width=True):
            st.session_state.interview_config = {
                "topic": mock_topic,
                "role": mock_role,
                "difficulty": mock_difficulty
            }
            with st.spinner("Starting your interview..."):
                try:
                    opening = start_interview(
                        role=mock_role,
                        topic=mock_topic,
                        difficulty=mock_difficulty,
                        chat_history=[]
                    )
                    st.session_state.messages = [
                        {"role": "assistant", "content": opening}
                    ]
                    st.session_state.interview_active = True
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    else:
        config = st.session_state.interview_config
        st.markdown(f"**Topic:** {config['topic']} | **Role:** {config['role']} | **Difficulty:** {config['difficulty']}")
        st.markdown("---")

        for message in st.session_state.messages:
            if message["role"] == "assistant":
                with st.chat_message("assistant", avatar="🤖"):
                    st.markdown(message["content"])
            else:
                with st.chat_message("user", avatar="🧑‍💻"):
                    st.markdown(message["content"])

        user_input = st.chat_input("Type your answer here...")

        if user_input:
            st.session_state.messages.append(
                {"role": "user", "content": user_input}
            )
            chat_history = build_chat_history(st.session_state.messages[:-1])
            with st.spinner("Thinking..."):
                try:
                    response = chat(
                        user_answer=user_input,
                        role=config["role"],
                        topic=config["topic"],
                        difficulty=config["difficulty"],
                        chat_history=chat_history
                    )
                    st.session_state.messages.append(
                        {"role": "assistant", "content": response}
                    )
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

        st.markdown("---")
        if st.button("🔴 End Interview", use_container_width=True):
            st.session_state.interview_active = False
            st.session_state.messages = []
            st.session_state.interview_config = {}
            st.rerun()

# ============================================================
# MODULE 3: ANSWER EVALUATOR
# ============================================================
elif module == "📊 Answer Evaluator":

    st.title("📊 Answer Evaluator")
    st.markdown("Get detailed AI feedback on your interview answers.")
    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        eval_role = st.selectbox(
            "👔 Role",
            ["Data Scientist", "Machine Learning Engineer", "Data Analyst",
             "Backend Developer", "AI Engineer", "GenAI Developer",
             "Data Engineer", "Software Engineer"]
        )

    with col2:
        eval_difficulty = st.selectbox(
            "⚡ Difficulty",
            ["Easy", "Medium", "Hard"]
        )

    st.markdown("---")

    # Question input
    eval_question = st.text_area(
        "📌 Enter the Interview Question",
        placeholder="e.g. What is the difference between supervised and unsupervised learning?",
        height=100
    )

    # Answer input
    eval_answer = st.text_area(
        "✍️ Enter Your Answer",
        placeholder="Type your answer here...",
        height=200
    )

    st.markdown("---")

    if st.button("🔍 Evaluate My Answer", use_container_width=True):

        if not eval_question.strip():
            st.warning("⚠️ Please enter a question.")
        elif not eval_answer.strip():
            st.warning("⚠️ Please enter your answer.")
        else:
            with st.spinner("Evaluating your answer..."):
                try:
                    result = evaluate_answer(
                        question=eval_question,
                        user_answer=eval_answer,
                        role=eval_role,
                        difficulty=eval_difficulty
                    )

                    st.success("✅ Evaluation Complete!")
                    st.markdown("---")

                    # Score - displayed prominently
                    st.markdown("## 📊 Score")
                    st.info(f"### {result['score']}")

                    # Two columns for strengths and weaknesses
                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("## ✅ Strengths")
                        st.success(result['strengths'])

                    with col2:
                        st.markdown("## ❌ Weaknesses")
                        st.error(result['weaknesses'])

                    # Missing concepts
                    st.markdown("## 🔍 Missing Concepts")
                    st.warning(result['missing_concepts'])

                    # Ideal answer
                    st.markdown("## 💡 Ideal Answer")
                    st.markdown(result['ideal_answer'])

                    # Follow up question
                    st.markdown("## ❓ Follow-up Question")
                    st.info(result['follow_up'])

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")