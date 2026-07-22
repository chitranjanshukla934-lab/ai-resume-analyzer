import streamlit as st
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="ResumeIQ | AI Resume Intelligence",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>

    /* Main background */
    .stApp {
        background: #f7f9fc;
        color: #172033;
    }

    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* Main content width */
    .block-container {
        max-width: 1180px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    /* Top navigation */
    .topbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 18px 0 30px 0;
        border-bottom: 1px solid #e7ebf2;
        margin-bottom: 45px;
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #172033;
    }

    .brand span {
        color: #356ae6;
    }

    .status {
        background: #edf4ff;
        color: #356ae6;
        border: 1px solid #d8e6ff;
        padding: 7px 14px;
        border-radius: 30px;
        font-size: 13px;
        font-weight: 600;
    }

    /* Hero */
    .hero {
        text-align: center;
        max-width: 800px;
        margin: 0 auto 45px auto;
    }

    .hero h1 {
        font-size: 48px;
        line-height: 1.1;
        letter-spacing: -1.5px;
        color: #172033;
        margin-bottom: 18px;
    }

    .hero h1 span {
        color: #356ae6;
    }

    .hero p {
        font-size: 18px;
        line-height: 1.7;
        color: #68748a;
        margin-bottom: 0;
    }

    /* Upload card */
    .upload-card {
        background: white;
        border: 1px solid #e4e9f1;
        border-radius: 20px;
        padding: 30px;
        box-shadow: 0 10px 35px rgba(30, 45, 70, 0.06);
        margin-bottom: 35px;
    }

    .section-label {
        font-size: 14px;
        font-weight: 700;
        color: #356ae6;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 750;
        color: #172033;
        margin-bottom: 6px;
    }

    .section-description {
        color: #768196;
        margin-bottom: 20px;
    }

    /* File uploader */
    [data-testid="stFileUploader"] {
        background: #f8faff;
        border: 2px dashed #b9cdf7;
        border-radius: 16px;
        padding: 18px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        height: 52px;
        border-radius: 12px;
        border: none;
        background: #356ae6;
        color: white;
        font-size: 16px;
        font-weight: 700;
        transition: all 0.2s ease;
    }

    .stButton > button:hover {
        background: #2858c9;
        box-shadow: 0 8px 20px rgba(53, 106, 230, 0.25);
    }

    /* Feature section */
    .feature-title {
        text-align: center;
        font-size: 26px;
        font-weight: 750;
        color: #172033;
        margin: 50px 0 22px 0;
    }

    .feature-card {
        background: white;
        border: 1px solid #e4e9f1;
        border-radius: 16px;
        padding: 24px;
        height: 155px;
        box-shadow: 0 8px 25px rgba(30, 45, 70, 0.04);
    }

    .feature-card h3 {
        font-size: 17px;
        color: #172033;
        margin-bottom: 10px;
    }

    .feature-card p {
        font-size: 14px;
        line-height: 1.6;
        color: #768196;
    }

    /* Analysis */
    .analysis-header {
        background: #172033;
        color: white;
        padding: 28px;
        border-radius: 18px;
        margin-top: 35px;
        margin-bottom: 20px;
    }

    .analysis-header h2 {
        color: white;
        margin-bottom: 6px;
    }

    .analysis-header p {
        color: #b9c3d4;
        margin-bottom: 0;
    }

    .result-container {
        background: white;
        border: 1px solid #e4e9f1;
        border-radius: 18px;
        padding: 32px;
        box-shadow: 0 10px 35px rgba(30, 45, 70, 0.06);
    }

    /* Footer */
    .custom-footer {
        text-align: center;
        padding-top: 55px;
        color: #98a2b3;
        font-size: 13px;
    }

</style>
""", unsafe_allow_html=True)


# =========================
# TOP BAR
# =========================
st.markdown("""
<div class="topbar">
    <div class="brand">Resume<span>IQ</span></div>
    <div class="status">AI Resume Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)


# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="hero">
    <h1>Make your resume work <span>smarter.</span></h1>
    <p>
        ResumeIQ uses Generative AI to analyze your resume, identify improvement areas,
        evaluate your skills, and provide practical career recommendations.
    </p>
</div>
""", unsafe_allow_html=True)


# =========================
# API SETUP
# =========================
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()

client = Groq(api_key=api_key)


# =========================
# UPLOAD SECTION
# =========================
st.markdown("""
<div class="upload-card">
    <div class="section-label">Resume Analysis</div>
    <div class="section-title">Upload your resume</div>
    <div class="section-description">
        Upload your resume in PDF format and receive an AI-powered professional analysis.
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a PDF resume",
    type=["pdf"],
    label_visibility="collapsed"
)


# =========================
# RESUME PROCESSING
# =========================
if uploaded_file:

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    st.success("Resume uploaded successfully.")

    st.write("")

    if st.button("Analyze Resume"):

        with st.spinner("Analyzing your resume with Generative AI..."):

            prompt = f"""
You are an expert Resume Analyst, ATS Consultant, and Career Advisor.

Analyze the following resume carefully:

{resume_text}

Provide a structured professional report containing:

1. OVERALL RESUME SCORE
Give a score out of 100 and explain the reasoning.

2. PROFESSIONAL SUMMARY
Summarize the candidate profile.

3. KEY STRENGTHS
Identify the strongest parts of the resume.

4. AREAS FOR IMPROVEMENT
Identify weaknesses and issues.

5. TECHNICAL SKILLS FOUND
List the technical skills detected.

6. RECOMMENDED SKILLS
Suggest important skills the candidate should learn.

7. PROJECT RECOMMENDATIONS
Suggest three relevant projects.

8. ATS OPTIMIZATION
Suggest improvements for ATS compatibility.

9. CAREER RECOMMENDATIONS
Provide practical next steps.

Be specific, honest, and professional.
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

            st.markdown("""
            <div class="analysis-header">
                <h2>Resume Analysis Report</h2>
                <p>AI-generated insights based on your resume profile.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="result-container">', unsafe_allow_html=True)

            st.markdown(result)

            st.markdown('</div>', unsafe_allow_html=True)


# =========================
# FEATURES
# =========================
st.markdown(
    '<div class="feature-title">Built for better career decisions</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>Resume Intelligence</h3>
        <p>Understand how strong your resume is and what can be improved.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>Skill Gap Insights</h3>
        <p>Discover relevant skills that can strengthen your professional profile.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>Career Direction</h3>
        <p>Get practical recommendations to improve your future opportunities.</p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# FOOTER
# =========================
st.markdown("""
<div class="custom-footer">
    ResumeIQ · AI-powered resume intelligence for modern careers
</div>
""", unsafe_allow_html=True)
