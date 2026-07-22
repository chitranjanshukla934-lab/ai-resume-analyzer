import streamlit as st
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os
import re

load_dotenv()

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ResumeIQ | AI Resume Intelligence",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# PREMIUM DARK UI
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(61, 80, 190, 0.25), transparent 30%),
        radial-gradient(circle at 90% 0%, rgba(132, 67, 190, 0.20), transparent 30%),
        #080b14;
    color: #f5f7ff;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu,
footer,
header {
    visibility: hidden;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

/* ================= NAVBAR ================= */

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 17px 23px;
    border-radius: 18px;
    background: rgba(18, 23, 40, 0.75);
    border: 1px solid rgba(255,255,255,0.09);
    backdrop-filter: blur(20px);
    margin-bottom: 55px;
}

.logo {
    font-size: 24px;
    font-weight: 800;
    color: white;
}

.logo span {
    color: #8292ff;
}

.nav-badge {
    font-size: 12px;
    color: #b2bcff;
    padding: 8px 15px;
    border-radius: 999px;
    background: rgba(124,140,255,0.10);
    border: 1px solid rgba(124,140,255,0.25);
}

/* ================= HERO ================= */

.hero {
    text-align: center;
    max-width: 900px;
    margin: auto;
}

.hero h1 {
    font-size: 60px;
    line-height: 1.08;
    letter-spacing: -2.5px;
    color: white;
    margin-bottom: 20px;
}

.hero h1 span {
    background: linear-gradient(90deg, #8c9cff, #c487ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    font-size: 18px;
    line-height: 1.7;
    color: #929bb2;
}

.hero-line {
    height: 3px;
    width: 70px;
    background: linear-gradient(90deg, #7285ff, #bd77ff);
    border-radius: 5px;
    margin: 27px auto 0;
}

/* ================= FEATURE CARDS ================= */

.section-heading {
    text-align: center;
    margin: 55px 0 25px;
}

.section-heading h2 {
    font-size: 26px;
    color: white;
    margin-bottom: 8px;
}

.section-heading p {
    color: #7e889e;
}

.feature-card {
    min-height: 175px;
    padding: 27px;
    border-radius: 20px;
    background: rgba(18, 23, 40, 0.78);
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.3s ease;
}

.feature-card:hover {
    transform: translateY(-5px);
    border-color: rgba(132, 147, 255, 0.45);
    box-shadow: 0 18px 40px rgba(0,0,0,0.28);
}

.feature-number {
    font-size: 12px;
    letter-spacing: 2px;
    color: #8997ff;
    font-weight: 700;
    margin-bottom: 18px;
}

.feature-card h3 {
    font-size: 18px;
    color: #e2e6ff;
    margin-bottom: 12px;
}

.feature-card p {
    color: #818ba3;
    font-size: 14px;
    line-height: 1.65;
}

/* ================= UPLOAD CARD ================= */

.upload-card {
    margin-top: 50px;
    padding: 34px;
    border-radius: 24px;
    background: linear-gradient(
        145deg,
        rgba(22, 28, 48, 0.96),
        rgba(12, 16, 29, 0.96)
    );
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 25px 80px rgba(0,0,0,0.35);
}

.upload-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 25px;
}

.upload-title {
    font-size: 23px;
    font-weight: 700;
    color: white;
}

.upload-subtitle {
    color: #7f899f;
    font-size: 14px;
    margin-top: 6px;
}

.secure-badge {
    color: #7ef0bd;
    background: rgba(74,222,128,0.08);
    border: 1px solid rgba(74,222,128,0.18);
    padding: 8px 13px;
    border-radius: 999px;
    font-size: 12px;
}

/* ================= FILE UPLOADER ================= */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.025);
    border: 1.5px dashed rgba(132,148,255,0.55);
    border-radius: 18px;
    padding: 22px;
}

[data-testid="stFileUploader"]:hover {
    background: rgba(124,140,255,0.06);
    border-color: #8e9cff;
}

/* ================= FILE INFO ================= */

.file-info {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin: 20px 0;
}

.file-tag {
    background: rgba(124,140,255,0.08);
    border: 1px solid rgba(124,140,255,0.18);
    color: #aeb9ff;
    padding: 9px 14px;
    border-radius: 9px;
    font-size: 12px;
}

/* ================= BUTTON ================= */

.stButton > button {
    width: 100%;
    height: 54px;
    border-radius: 14px;
    border: 1px solid rgba(155,167,255,0.35);
    background: linear-gradient(100deg, #5267e8, #8957d8);
    color: white;
    font-size: 16px;
    font-weight: 700;
    box-shadow: 0 10px 30px rgba(83,101,225,0.25);
    transition: 0.25s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 38px rgba(112,101,255,0.35);
}

/* ================= ANALYSIS HEADER ================= */

.analysis-header {
    margin-top: 55px;
    padding: 30px;
    border-radius: 20px;
    background:
        linear-gradient(
            120deg,
            rgba(73,88,196,0.32),
            rgba(112,61,155,0.25)
        ),
        rgba(17,22,38,0.9);
    border: 1px solid rgba(144,155,255,0.20);
}

.analysis-header h2 {
    color: white;
    margin-bottom: 8px;
}

.analysis-header p {
    color: #a2abc0;
}

/* ================= SCORE DASHBOARD ================= */

.score-card {
    margin-top: 20px;
    padding: 30px;
    border-radius: 20px;
    text-align: center;
    background: linear-gradient(
        135deg,
        rgba(77,93,205,0.28),
        rgba(123,65,174,0.25)
    );
    border: 1px solid rgba(144,155,255,0.20);
}

.score-title {
    color: #aeb9d0;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.score-number {
    font-size: 54px;
    font-weight: 800;
    color: white;
    margin: 8px 0;
}

.score-subtitle {
    color: #8d98b0;
    font-size: 13px;
}

/* ================= REPORT ================= */

.report-box {
    margin-top: 20px;
    padding: 35px;
    border-radius: 20px;
    background: rgba(14,18,31,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    line-height: 1.8;
}

/* ================= FOOTER ================= */

.custom-footer {
    text-align: center;
    color: #5f687d;
    font-size: 13px;
    margin-top: 75px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# NAVBAR
# =====================================================

st.markdown("""
<div class="navbar">
    <div class="logo">Resume<span>IQ</span></div>
    <div class="nav-badge">AI Resume Intelligence Platform</div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# HERO
# =====================================================

st.markdown("""
<div class="hero">
    <h1>Turn your resume into<br><span>career intelligence.</span></h1>

    <p>
        Analyze your resume with Generative AI and discover strengths,
        skill gaps, ATS improvements, and career opportunities hidden in your profile.
    </p>

    <div class="hero-line"></div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# FEATURES — TOP
# =====================================================

st.markdown("""
<div class="section-heading">
    <h2>Everything you need to improve your resume</h2>
    <p>AI-powered insights designed to help you stand out.</p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-number">01</div>
        <h3>Resume Intelligence</h3>
        <p>
            Understand your resume quality, strengths,
            weaknesses, and overall professional impact.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-number">02</div>
        <h3>Skill Gap Analysis</h3>
        <p>
            Discover valuable skills you already have
            and identify what you should learn next.
        </p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-number">03</div>
        <h3>ATS Readiness</h3>
        <p>
            Improve your resume visibility and compatibility
            with modern recruitment systems.
        </p>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# API SETUP
# =====================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()

client = Groq(api_key=api_key)


# =====================================================
# UPLOAD SECTION
# =====================================================

st.markdown("""
<div class="upload-card">

    <div class="upload-header">

        <div>
            <div class="upload-title">Upload your resume</div>

            <div class="upload-subtitle">
                Upload a PDF and let ResumeIQ analyze your professional profile.
            </div>
        </div>

        <div class="secure-badge">
            Secure Analysis
        </div>

    </div>

</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Drop your PDF resume here",
    type=["pdf"]
)


# =====================================================
# PROCESS RESUME
# =====================================================

if uploaded_file:

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:

        text = page.extract_text()

        if text:
            resume_text += text + "\n"

    page_count = len(reader.pages)

    st.markdown(f"""
    <div class="file-info">
        <div class="file-tag">PDF Document</div>
        <div class="file-tag">{page_count} Page(s)</div>
        <div class="file-tag">AI Analysis Ready</div>
    </div>
    """, unsafe_allow_html=True)

    st.success("Resume successfully uploaded.")

    if st.button("Analyze Resume"):

        with st.spinner("AI is analyzing your resume..."):

            prompt = f"""
You are an expert AI Resume Analyst and Career Consultant.

Analyze the following resume:

{resume_text}

Give a professional structured report containing:

1. OVERALL RESUME SCORE
Give a score out of 100.

2. PROFESSIONAL SUMMARY
Summarize the candidate.

3. KEY STRENGTHS
List the strongest aspects.

4. WEAKNESSES
Identify areas for improvement.

5. TECHNICAL SKILLS FOUND
List technical skills.

6. MISSING OR RECOMMENDED SKILLS
Suggest skills to learn.

7. PROJECT SUGGESTIONS
Suggest three relevant projects.

8. ATS OPTIMIZATION
Give ATS improvement suggestions.

9. FINAL CAREER ADVICE
Give practical next steps.

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

            # Extract score if AI provides one
            score_match = re.search(
                r'(\d{1,3})\s*(?:/100|out of 100)',
                result,
                re.IGNORECASE
            )

            score = score_match.group(1) if score_match else "—"

            st.markdown("""
            <div class="analysis-header">

                <h2>Resume Analysis Report</h2>

                <p>
                    AI-generated insights based on your uploaded resume.
                </p>

            </div>
            """, unsafe_allow_html=True)

            col_score, col_info = st.columns([1, 2])

            with col_score:

                st.markdown(f"""
                <div class="score-card">

                    <div class="score-title">
                        Overall Resume Score
                    </div>

                    <div class="score-number">
                        {score}
                    </div>

                    <div class="score-subtitle">
                        Out of 100
                    </div>

                </div>
                """, unsafe_allow_html=True)

            with col_info:

                st.markdown("""
                <div class="score-card">

                    <div class="score-title">
                        Analysis Complete
                    </div>

                    <div class="score-number">
                        AI
                    </div>

                    <div class="score-subtitle">
                        Personalized career intelligence generated
                    </div>

                </div>
                """, unsafe_allow_html=True)

            st.markdown(
                '<div class="report-box">',
                unsafe_allow_html=True
            )

            st.markdown(result)

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            # Download report
            st.download_button(
                label="Download Analysis Report",
                data=result,
                file_name="ResumeIQ_Analysis_Report.txt",
                mime="text/plain"
            )


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="custom-footer">
    ResumeIQ · Generative AI powered resume intelligence
</div>
""", unsafe_allow_html=True)
