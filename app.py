import streamlit as st
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="ResumeIQ | AI Resume Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# PREMIUM DARK UI
# =========================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(55, 80, 180, 0.22), transparent 30%),
        radial-gradient(circle at 90% 10%, rgba(120, 55, 200, 0.18), transparent 28%),
        #080b14;
    color: #f4f7ff;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.8rem;
    padding-bottom: 4rem;
}

/* TOP NAV */
.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 22px;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    background: rgba(16, 20, 34, 0.72);
    backdrop-filter: blur(20px);
    margin-bottom: 65px;
}

.logo {
    font-size: 23px;
    font-weight: 800;
    letter-spacing: -0.5px;
}

.logo span {
    color: #7c8cff;
}

.nav-badge {
    font-size: 12px;
    color: #aeb9ff;
    background: rgba(124,140,255,0.1);
    border: 1px solid rgba(124,140,255,0.25);
    padding: 8px 14px;
    border-radius: 999px;
}

/* HERO */
.hero {
    text-align: center;
    max-width: 850px;
    margin: auto;
}

.hero h1 {
    font-size: 62px;
    line-height: 1.05;
    letter-spacing: -2.5px;
    margin-bottom: 22px;
    color: #ffffff;
}

.hero h1 span {
    background: linear-gradient(90deg, #8ea0ff, #c48cff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #929bb5;
    font-size: 18px;
    line-height: 1.7;
}

.hero-line {
    width: 70px;
    height: 3px;
    background: linear-gradient(90deg, #7185ff, #b875ff);
    margin: 28px auto 0;
    border-radius: 5px;
}

/* UPLOAD CARD */
.upload-wrapper {
    margin-top: 55px;
    padding: 34px;
    border-radius: 24px;
    background: linear-gradient(
        145deg,
        rgba(21, 27, 46, 0.95),
        rgba(12, 16, 29, 0.95)
    );
    border: 1px solid rgba(255,255,255,0.1);
    box-shadow:
        0 25px 80px rgba(0,0,0,0.35),
        inset 0 1px 0 rgba(255,255,255,0.04);
}

.upload-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.upload-title {
    font-size: 22px;
    font-weight: 700;
}

.upload-subtitle {
    color: #7f899f;
    font-size: 14px;
    margin-top: 5px;
}

.upload-status {
    color: #7ef0bd;
    font-size: 12px;
    padding: 7px 12px;
    border-radius: 999px;
    background: rgba(74, 222, 128, 0.08);
    border: 1px solid rgba(74, 222, 128, 0.18);
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.025);
    border: 1.5px dashed rgba(132, 148, 255, 0.5);
    border-radius: 18px;
    padding: 22px;
    transition: 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #8c9aff;
    background: rgba(124,140,255,0.06);
}

/* BUTTON */
.stButton > button {
    height: 55px;
    width: 100%;
    border-radius: 14px;
    border: 1px solid rgba(155, 167, 255, 0.35);
    background: linear-gradient(100deg, #5267e8, #8957d8);
    color: white;
    font-size: 16px;
    font-weight: 700;
    letter-spacing: 0.2px;
    box-shadow: 0 10px 30px rgba(83, 101, 225, 0.25);
    transition: all 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 38px rgba(112, 101, 255, 0.35);
}

/* FEATURES */
.section-heading {
    text-align: center;
    margin: 75px 0 25px;
}

.section-heading h2 {
    font-size: 26px;
    color: #ffffff;
}

.section-heading p {
    color: #7f899f;
}

.feature-card {
    min-height: 170px;
    padding: 26px;
    border-radius: 20px;
    background: rgba(18, 23, 39, 0.72);
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(133, 147, 255, 0.4);
    box-shadow: 0 15px 35px rgba(0,0,0,0.25);
}

.feature-card h3 {
    color: #dce2ff;
    font-size: 17px;
    margin-bottom: 12px;
}

.feature-card p {
    color: #818ba3;
    font-size: 14px;
    line-height: 1.65;
}

/* RESULT */
.result-header {
    margin-top: 55px;
    padding: 28px;
    border-radius: 20px;
    background:
        linear-gradient(120deg, rgba(73, 88, 196, 0.3), rgba(112, 61, 155, 0.25)),
        rgba(17, 22, 38, 0.9);
    border: 1px solid rgba(144, 155, 255, 0.2);
}

.result-header h2 {
    color: white;
    margin-bottom: 8px;
}

.result-header p {
    color: #a2abc0;
}

.result-box {
    margin-top: 18px;
    padding: 35px;
    border-radius: 20px;
    background: rgba(14, 18, 31, 0.92);
    border: 1px solid rgba(255,255,255,0.08);
    line-height: 1.8;
}

/* SUCCESS */
.stAlert {
    border-radius: 12px;
}

/* FOOTER */
.footer {
    text-align: center;
    color: #5f687d;
    font-size: 13px;
    margin-top: 75px;
}

</style>
""", unsafe_allow_html=True)


# =========================
# NAVBAR
# =========================
st.markdown("""
<div class="navbar">
    <div class="logo">Resume<span>IQ</span></div>
    <div class="nav-badge">AI Resume Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)


# =========================
# HERO
# =========================
st.markdown("""
<div class="hero">
    <h1>Turn your resume into<br><span>career intelligence.</span></h1>
    <p>
        Analyze your resume with Generative AI and discover the strengths,
        skill gaps, ATS improvements, and career opportunities hidden in your profile.
    </p>
    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)


# =========================
# API
# =========================
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()

client = Groq(api_key=api_key)


# =========================
# UPLOAD
# =========================
st.markdown("""
<div class="upload-wrapper">
    <div class="upload-header">
        <div>
            <div class="upload-title">Upload your resume</div>
            <div class="upload-subtitle">
                Upload a PDF and let AI analyze your professional profile.
            </div>
        </div>
        <div class="upload-status">Secure Analysis</div>
    </div>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your PDF resume here",
    type=["pdf"],
    label_visibility="visible"
)


# =========================
# ANALYSIS
# =========================
if uploaded_file:

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    st.success("Resume successfully uploaded.")

    if st.button("Analyze Resume"):

        with st.spinner("AI is analyzing your resume..."):

            prompt = f"""
You are an expert AI Resume Analyst and Career Consultant.

Analyze the following resume:

{resume_text}

Give a professional structured report with:

1. Overall Resume Score out of 100
2. Professional Summary
3. Key Strengths
4. Weaknesses and Areas for Improvement
5. Technical Skills Found
6. Missing or Recommended Skills
7. Three Relevant Project Suggestions
8. ATS Optimization Suggestions
9. Final Career Advice

Be specific, honest, practical, and professional.
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
            <div class="result-header">
                <h2>Resume Analysis Report</h2>
                <p>AI-generated insights based on your uploaded resume.</p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                '<div class="result-box">',
                unsafe_allow_html=True
            )

            st.markdown(result)

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


# =========================
# FEATURES
# =========================
st.markdown("""
<div class="section-heading">
    <h2>Built for smarter career decisions</h2>
    <p>From resume quality to career direction, get actionable insights in seconds.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <h3>Resume Intelligence</h3>
        <p>
            Understand your resume quality, structure, strengths,
            and the areas that need improvement.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <h3>Skill Gap Analysis</h3>
        <p>
            Identify important technical skills and discover
            what you should learn next for your career goals.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <h3>ATS Optimization</h3>
        <p>
            Improve your resume visibility and make it more
            compatible with modern recruitment systems.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =========================
# FOOTER
# =========================
st.markdown("""
<div class="footer">
    ResumeIQ · Generative AI powered resume intelligence
</div>
""", unsafe_allow_html=True)
