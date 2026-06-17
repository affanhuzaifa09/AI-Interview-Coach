# 🎯 AI Interview Coach

An AI-powered interview preparation assistant built with LangChain, Groq (Llama 3.3), FAISS, and Streamlit.

---

## 🚀 Features

### 🧠 Module 1 — Interview Question Generator
- Generate 10 interview questions instantly
- Filter by Topic, Role, and Difficulty
- Supports custom topics via free text input

### 🎤 Module 2 — Mock Interview
- Conversational AI interviewer
- Real-time feedback after every answer
- Full conversation memory across turns
- 5-question interview with final summary

### 📊 Module 3 — Answer Evaluator
- Score your answer out of 10
- Detailed Strengths and Weaknesses
- Missing Concepts identification
- Ideal Answer and Follow-up Question

### 📄 Module 4 — Resume Analyzer
- Upload your resume PDF
- Extract Skills, Projects, Technologies
- Generate personalized interview questions
- Resume Strengths and Improvement suggestions

### 📚 Module 5 — RAG Knowledge Base
- Upload any study material PDF
- Ask questions — AI answers from your document
- Built with FAISS vector search + embeddings
- View retrieved context from document

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Frontend | Streamlit |
| LLM | Groq (Llama 3.3 70B) |
| Framework | LangChain |
| Embeddings | all-MiniLM-L6-v2 |
| Vector Database | FAISS |
| PDF Processing | PyPDF |
| Language | Python 3.13 |

---

## 📁 Project Structure
AI-Interview-Coach/

│

├── app.py                          # Main Streamlit application

│

├── modules/

│   ├── question_generator.py       # Module 1: Question generation

│   ├── mock_interview.py           # Module 2: Mock interview logic

│   ├── evaluator.py                # Module 3: Answer evaluation

│   ├── resume_analyzer.py          # Module 4: Resume analysis

│   └── rag_engine.py               # Module 5: RAG pipeline

│

├── prompts/

│   ├── question_prompt.py          # Prompt for question generation

│   ├── evaluation_prompt.py        # Prompt for answer evaluation

│   └── interview_prompt.py         # Prompt for mock interview

│

├── utils/

│   ├── pdf_loader.py               # PDF text extraction

│   └── embeddings.py               # Embedding model setup

│

├── data/

│   ├── resumes/                    # Resume uploads

│   └── notes/                      # Study material uploads

│

├── vectorstore/                    # FAISS index storage

├── requirements.txt

├── .env

└── .gitignore

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/affanhuzaifa09/AI-Interview-Coach.git
cd AI-Interview-Coach
```

### 2. Create virtual environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory:
GROQ_API_KEY=your_groq_api_key_here
Get your free API key at [console.groq.com](https://console.groq.com)

### 5. Run the application
```bash
streamlit run app.py
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from console.groq.com |

---

## 💡 How RAG Works
PDF Upload → Text Extraction → Chunking (500 chars)

→ Embeddings (all-MiniLM-L6-v2) → FAISS Storage

→ Query → Similarity Search → Top 3 Chunks

→ LLM (Llama 3.3) → Answer from your document

---

## 👨‍💻 Author

**Affan Huzaifa**
- GitHub: [@affanhuzaifa09](https://github.com/affanhuzaifa09)
- Email: affanhuzaifap09@gmail.com

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
