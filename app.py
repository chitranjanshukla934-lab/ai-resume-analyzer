import streamlit as st
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="ResumeIQ | AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e293b 100%);
        color: #f8fafc;
    }

    .hero {
        padding: 35px;
        border-radius: 22px;
        background: linear-gradient(135deg, #1d4ed8, #7c3aed);
        text-align: center;
        margin-bottom: 30px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.3);
    }

    .hero h1 {
        font-size: 46px;
        margin-bottom: 8px;
        color: white;
    }

    .hero p {
        font-size: 18px;
        color: #e0e7ff;
    }

    .upload-box {
        padding: 25px;
        border-radius: 18px;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.15);
        margin-bottom: 25px;
    }

    .feature-card {
        padding: 22px;
        border-radius: 16px;
        background: rgba(255,255,255,0.07);
        text-align: center;
        min-height: 130px;
        border: 1px solid rgba(255,255,255,0.1);
    }

    .feature-card h3 {
        color: #c4b5fd;
    }

    .stButton > button {
        width: 100%;
        border-radius: 12px;
        padding: 12px;
        font-size: 17px;
        font-weight: bold;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        color: white;
        border: none;
    }

    .result-box {
        padding: 25px;
        border-radius: 18px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        margin-top: 25px;
    }

    footer {
        text-align: center;
        margin-top: 45px;
        color: #94a3b8;
    }
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="hero">
    <h1>📄 ResumeIQ</h1>
    <p>AI-Powered Resume Analysis & Career Intelligence</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FEATURES ----------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>📊 Smart Scoring</h3>
        <p>Get an AI-powered resume score out of 100.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>🎯 Skill Analysis</h3>
        <p>Discover strengths and missing skills.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>🚀 ATS Optimization</h3>
        <p>Improve your resume for applicant tracking systems.</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# ---------------- API ----------------
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found. Please configure your API key.")
    st.stop()

client = Groq(api_key=api_key)

# ---------------- UPLOAD ----------------
st.markdown('<div class="upload-box">', unsafe_allow_html=True)

st.subheader("📤 Upload Your Resume")
st.write("Upload a PDF resume to receive detailed AI-powered feedback.")

uploaded_file = st.file_uploader(
    "Choose your resume PDF",
    type=["pdf"]
)

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- ANALYSIS ----------------
if uploaded_file:

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

    st.success("✅ Resume uploaded successfully!")

    if st.button("🔍 Analyze My Resume"):

        with st.spinner("🤖 AI is analyzing your resume..."):

            prompt = f"""
You are an expert AI Resume Analyzer and Career Consultant.

Analyze the following resume:

{resume_text}

Provide a professional analysis with these sections:

## 📊 OVERALL RESUME SCORE
Give a score out of 100 and explain the score.

## 📝 RESUME SUMMARY
Summarize the candidate profile.

## 💪 KEY STRENGTHS
List the strongest aspects of the resume.

## ⚠️ WEAKNESSES
Identify important weaknesses.

## 🛠️ TECHNICAL SKILLS FOUND
List all technical skills found.

## 🎯 MISSING OR RECOMMENDED SKILLS
Suggest relevant skills to learn.

## 💡 PROJECT SUGGESTIONS
Suggest 3 relevant projects.

## 📈 ATS OPTIMIZATION
Give ATS improvement suggestions.

## 🚀 FINAL CAREER ADVICE
Give practical career advice.

Be honest, specific, and professional.
"""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3,
                max_tokens=4000
            )

            result = response.choices[0].message.content

            st.markdown("---")

            st.markdown(
                '<div class="result-box">',
                unsafe_allow_html=True
            )

            st.header("📊 AI Resume Analysis")

            st.markdown(result)

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

# ---------------- FOOTER ----------------
st.markdown("""
<footer>
    Built with ❤️ using Streamlit & Generative AI
</footer>
""", unsafe_allow_html=True)
