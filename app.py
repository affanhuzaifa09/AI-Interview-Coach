# app.py
# Main entry point of AI Interview Coach application.

import streamlit as st
from modules.question_generator import generate_questions
from modules.mock_interview import start_interview, chat, build_chat_history
from modules.evaluator import evaluate_answer
from modules.resume_analyzer import analyze_resume
from modules.rag_engine import process_uploaded_pdf, answer_question
from utils.pdf_loader import extract_text_from_pdf, get_pdf_info

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

    eval_question = st.text_area(
        "📌 Enter the Interview Question",
        placeholder="e.g. What is the difference between supervised and unsupervised learning?",
        height=100
    )

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

                    st.markdown("## 📊 Score")
                    st.info(f"### {result['score']}")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("## ✅ Strengths")
                        st.success(result['strengths'])

                    with col2:
                        st.markdown("## ❌ Weaknesses")
                        st.error(result['weaknesses'])

                    st.markdown("## 🔍 Missing Concepts")
                    st.warning(result['missing_concepts'])

                    st.markdown("## 💡 Ideal Answer")
                    st.markdown(result['ideal_answer'])

                    st.markdown("## ❓ Follow-up Question")
                    st.info(result['follow_up'])

                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# ============================================================
# MODULE 4: RESUME ANALYZER
# ============================================================
elif module == "📄 Resume Analyzer":

    st.title("📄 Resume Analyzer")
    st.markdown("Upload your resume and get personalized interview questions.")
    st.markdown("---")

    resume_role = st.selectbox(
        "👔 Target Job Role",
        ["Data Scientist", "Machine Learning Engineer", "Data Analyst",
         "Backend Developer", "AI Engineer", "GenAI Developer",
         "Data Engineer", "Full Stack Developer", "Software Engineer"]
    )

    st.markdown("---")

    uploaded_resume = st.file_uploader(
        "📎 Upload Your Resume (PDF only)",
        type=["pdf"]
    )

    if uploaded_resume is not None:

        pdf_info = get_pdf_info(uploaded_resume)
        st.info(f"📄 File: **{pdf_info['filename']}** | Pages: **{pdf_info['pages']}**")

        st.markdown("---")

        if st.button("🔍 Analyze Resume", use_container_width=True):

            with st.spinner("Reading your resume..."):
                resume_text = extract_text_from_pdf(uploaded_resume)

            if "Error" in resume_text or "Could not extract" in resume_text:
                st.error(f"❌ {resume_text}")
            else:
                with st.spinner("Analyzing resume and generating questions..."):
                    try:
                        result = analyze_resume(
                            resume_text=resume_text,
                            job_role=resume_role
                        )

                        st.success("✅ Resume Analyzed Successfully!")
                        st.markdown("---")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("## 🛠️ Extracted Skills")
                            st.success(result['skills'])

                        with col2:
                            st.markdown("## ⚙️ Technologies Used")
                            st.info(result['technologies'])

                        st.markdown("## 📁 Projects")
                        st.markdown(result['projects'])
                        st.markdown("---")

                        st.markdown("## 🎯 Personalized Interview Questions")
                        st.warning(result['questions'])
                        st.markdown("---")

                        col1, col2 = st.columns(2)

                        with col1:
                            st.markdown("## ✅ Resume Strengths")
                            st.success(result['strengths'])

                        with col2:
                            st.markdown("## 📈 Resume Improvements")
                            st.error(result['improvements'])

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
    else:
        st.info("👆 Please upload your resume PDF to get started.")

# ============================================================
# MODULE 5: RAG KNOWLEDGE BASE
# ============================================================
elif module == "📚 RAG Knowledge Base":

    st.title("📚 RAG Knowledge Base")
    st.markdown("Upload study material and ask questions — AI answers from your document.")
    st.markdown("---")

    # Initialize session state for RAG
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "rag_ready" not in st.session_state:
        st.session_state.rag_ready = False
    if "rag_filename" not in st.session_state:
        st.session_state.rag_filename = ""

    # --- UPLOAD SECTION ---
    uploaded_notes = st.file_uploader(
        "📎 Upload Study Material (PDF only)",
        type=["pdf"]
    )

    if uploaded_notes is not None:

        if st.button("⚙️ Process Document", use_container_width=True):

            with st.spinner("Reading and chunking document..."):
                try:
                    vectorstore, chunk_count = process_uploaded_pdf(uploaded_notes)
                    st.session_state.vectorstore = vectorstore
                    st.session_state.rag_ready = True
                    st.session_state.rag_filename = uploaded_notes.name
                    st.success(f"✅ Document processed! Created {chunk_count} chunks.")

                except Exception as e:
                    st.error(f"❌ Error processing document: {str(e)}")

    # --- Q&A SECTION ---
    if st.session_state.rag_ready:

        st.markdown("---")
        st.info(f"📄 Active document: **{st.session_state.rag_filename}**")
        st.markdown("### 💬 Ask Questions About Your Study Material")

        user_question = st.text_input(
            "Your Question",
            placeholder="e.g. What is gradient descent? Explain backpropagation."
        )

        if st.button("🔍 Get Answer", use_container_width=True):

            if not user_question.strip():
                st.warning("⚠️ Please enter a question.")
            else:
                with st.spinner("Searching document and generating answer..."):
                    try:
                        result = answer_question(
                            vectorstore=st.session_state.vectorstore,
                            question=user_question
                        )

                        st.markdown("---")
                        st.markdown("## 💡 Answer")
                        st.markdown(result['answer'])

                        # Show retrieved context
                        with st.expander("📄 View Retrieved Context from Document"):
                            st.markdown(result['context'])

                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")

        # Reset button
        st.markdown("---")
        if st.button("🔄 Upload New Document", use_container_width=True):
            st.session_state.vectorstore = None
            st.session_state.rag_ready = False
            st.session_state.rag_filename = ""
            st.rerun()

    else:
        if uploaded_notes is None:
            st.info("👆 Upload a PDF study material to get started.")