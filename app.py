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
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =====================================================
# PREMIUM DARK CSS
# =====================================================

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(60, 80, 190, 0.22), transparent 30%),
        radial-gradient(circle at 90% 0%, rgba(130, 70, 200, 0.18), transparent 30%),
        #080b14;
    color: #f5f7ff;
    font-family: 'DM Sans', sans-serif;
}

#MainMenu,
header,
footer {
    visibility: hidden;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.5rem;
    padding-bottom: 4rem;
}

/* NAVBAR */

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 17px 24px;
    margin-bottom: 55px;
    border-radius: 18px;
    background: rgba(18, 23, 40, 0.80);
    border: 1px solid rgba(255,255,255,0.08);
}

.logo {
    font-size: 24px;
    font-weight: 800;
    color: white;
}

.logo span {
    color: #8998ff;
}

.nav-badge {
    color: #b5beff;
    font-size: 12px;
    padding: 8px 15px;
    border-radius: 999px;
    background: rgba(124,140,255,0.10);
    border: 1px solid rgba(124,140,255,0.25);
}

/* WELCOME */

.welcome-label {
    text-align: center;
    color: #8d9aff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 3px;
    margin-bottom: 18px;
}

.hero {
    text-align: center;
    max-width: 900px;
    margin: auto;
}

.hero h1 {
    font-size: 62px;
    line-height: 1.05;
    letter-spacing: -3px;
    color: white;
    margin-bottom: 22px;
}

.hero h1 span {
    background: linear-gradient(90deg, #8f9eff, #c88aff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #929bb1;
    font-size: 18px;
    line-height: 1.75;
}

.hero-line {
    height: 3px;
    width: 75px;
    margin: 30px auto 0;
    border-radius: 10px;
    background: linear-gradient(90deg, #7186ff, #c179ff);
}

/* SECTION */

.section-heading {
    text-align: center;
    margin: 60px 0 28px;
}

.section-heading h2 {
    color: white;
    font-size: 28px;
    margin-bottom: 10px;
}

.section-heading p {
    color: #7f899f;
}

/* FEATURE CARDS */

.feature-card {
    min-height: 205px;
    padding: 30px;
    border-radius: 22px;
    background: linear-gradient(
        145deg,
        rgba(27,34,59,0.96),
        rgba(12,16,29,0.96)
    );
    border: 1px solid rgba(255,255,255,0.08);
    transition: all 0.35s ease;
}

.feature-card:hover {
    transform: translateY(-10px);
    border-color: rgba(137,151,255,0.55);
    box-shadow: 0 22px 45px rgba(0,0,0,0.35);
}

.feature-number {
    color: #8f9cff;
    font-size: 11px;
    letter-spacing: 2px;
    font-weight: 700;
    margin-bottom: 22px;
}

.feature-card h3 {
    color: #eef0ff;
    font-size: 19px;
    margin-bottom: 13px;
}

.feature-card p {
    color: #858fa6;
    font-size: 14px;
    line-height: 1.75;
}

/* WORKFLOW */

.workflow {
    margin-top: 45px;
    padding: 22px;
    border-radius: 18px;
    text-align: center;
    background: rgba(17,22,39,0.65);
    border: 1px solid rgba(255,255,255,0.07);
}

.workflow-text {
    color: #8d97ad;
    font-size: 14px;
}

.workflow-text span {
    color: #aab4ff;
    font-weight: 700;
}

/* UPLOAD CARD */

.upload-card {
    margin-top: 50px;
    padding: 34px;
    border-radius: 24px;
    background: linear-gradient(
        145deg,
        rgba(22,28,48,0.96),
        rgba(12,16,29,0.96)
    );
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 25px 80px rgba(0,0,0,0.35);
}

.upload-title {
    color: white;
    font-size: 23px;
    font-weight: 700;
}

.upload-subtitle {
    color: #7f899f;
    font-size: 14px;
    margin-top: 6px;
}

.secure-badge {
    color: #7ef0bd;
    font-size: 12px;
    padding: 8px 13px;
    border-radius: 999px;
    background: rgba(74,222,128,0.08);
    border: 1px solid rgba(74,222,128,0.18);
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background: rgba(255,255,255,0.025);
    border: 1.5px dashed rgba(132,148,255,0.55);
    border-radius: 18px;
    padding: 22px;
}

/* FILE INFO */

.file-info {
    display: flex;
    gap: 12px;
    margin: 20px 0;
}

.file-tag {
    color: #aeb9ff;
    font-size: 12px;
    padding: 9px 14px;
    border-radius: 9px;
    background: rgba(124,140,255,0.08);
    border: 1px solid rgba(124,140,255,0.18);
}

/* THANK YOU */

.thank-you {
    text-align: center;
    margin: 22px 0;
    padding: 18px;
    border-radius: 14px;
    color: #9eeac2;
    background: rgba(74,222,128,0.06);
    border: 1px solid rgba(74,222,128,0.15);
}

/* BUTTON */

.stButton > button {
    width: 100%;
    height: 54px;
    border-radius: 14px;
    border: 1px solid rgba(155,167,255,0.35);
    background: linear-gradient(100deg, #5267e8, #8957d8);
    color: white;
    font-size: 16px;
    font-weight: 700;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 16px 38px rgba(112,101,255,0.35);
}

/* ANALYSIS */

.analysis-header {
    margin-top: 55px;
    padding: 30px;
    border-radius: 20px;
    background: linear-gradient(
        120deg,
        rgba(73,88,196,0.32),
        rgba(112,61,155,0.25)
    );
    border: 1px solid rgba(144,155,255,0.20);
}

.analysis-header h2 {
    color: white;
}

.analysis-header p {
    color: #a2abc0;
}

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
}

.score-number {
    color: white;
    font-size: 54px;
    font-weight: 800;
    margin: 8px 0;
}

.score-subtitle {
    color: #8d98b0;
    font-size: 13px;
}

.report-box {
    margin-top: 20px;
    padding: 35px;
    border-radius: 20px;
    background: rgba(14,18,31,0.95);
    border: 1px solid rgba(255,255,255,0.08);
    line-height: 1.8;
}

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

st.markdown(
    '<div class="navbar"><div class="logo">Resume<span>IQ</span></div><div class="nav-badge">AI Resume Intelligence Platform</div></div>',
    unsafe_allow_html=True
)


# =====================================================
# WELCOME
# =====================================================

st.markdown(
    '<div class="welcome-label">WELCOME TO RESUMEIQ</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero"><h1>Turn your resume into<br><span>career intelligence.</span></h1><p>Upload your resume and let AI uncover your strengths, skill gaps, ATS opportunities, and the next steps in your career.</p><div class="hero-line"></div></div>',
    unsafe_allow_html=True
)


# =====================================================
# FEATURES
# =====================================================

st.markdown(
    '<div class="section-heading"><h2>Make your next career move with confidence.</h2><p>Everything you need to understand and improve your resume.</p></div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(
        '<div class="feature-card"><div class="feature-number">01 / ANALYZE</div><h3>Understand Your Profile</h3><p>Get a clear AI-powered view of your resume, professional strengths, weaknesses, and overall impact.</p></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div class="feature-card"><div class="feature-number">02 / DISCOVER</div><h3>Find Your Skill Gaps</h3><p>Discover the skills you already have and identify what you should learn to reach your career goals.</p></div>',
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        '<div class="feature-card"><div class="feature-number">03 / IMPROVE</div><h3>Become ATS Ready</h3><p>Improve your resume structure and content to perform better in modern hiring systems.</p></div>',
        unsafe_allow_html=True
    )


# =====================================================
# WORKFLOW
# =====================================================

st.markdown(
    '<div class="workflow"><div class="workflow-text">Upload your resume <span>→</span> AI analyzes your profile <span>→</span> Discover your next career move</div></div>',
    unsafe_allow_html=True
)


# =====================================================
# API
# =====================================================

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY is not configured.")
    st.stop()

client = Groq(api_key=api_key)


# =====================================================
# UPLOAD
# =====================================================

st.markdown(
    '<div class="upload-card"><div class="upload-title">Upload your resume</div><div class="upload-subtitle">Upload a PDF and let ResumeIQ analyze your professional profile.</div><br><div class="secure-badge">Secure Analysis</div></div>',
    unsafe_allow_html=True
)

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

    st.markdown(
        f'<div class="file-info"><div class="file-tag">PDF Document</div><div class="file-tag">{page_count} Page(s)</div><div class="file-tag">AI Analysis Ready</div></div>',
        unsafe_allow_html=True
    )

    st.success("Resume successfully uploaded.")

    st.markdown(
        '<div class="thank-you">Thank you for trusting ResumeIQ with your resume. Your AI-powered analysis is ready to begin.</div>',
        unsafe_allow_html=True
    )

    if st.button("Analyze Resume"):

        with st.spinner("AI is analyzing your resume..."):

            prompt = f"""
You are an expert AI Resume Analyst and Career Consultant.

Analyze this resume:

{resume_text}

Provide a professional structured analysis with:

1. OVERALL RESUME SCORE out of 100
2. PROFESSIONAL SUMMARY
3. KEY STRENGTHS
4. WEAKNESSES AND AREAS FOR IMPROVEMENT
5. TECHNICAL SKILLS FOUND
6. MISSING OR RECOMMENDED SKILLS
7. THREE RELEVANT PROJECT SUGGESTIONS
8. ATS OPTIMIZATION SUGGESTIONS
9. FINAL CAREER ADVICE

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

            score_match = re.search(
                r"(\d{1,3})\s*(?:/100|out of 100)",
                result,
                re.IGNORECASE
            )

            score = score_match.group(1) if score_match else "—"

            st.markdown(
                '<div class="analysis-header"><h2>Resume Analysis Report</h2><p>AI-generated insights based on your uploaded resume.</p></div>',
                unsafe_allow_html=True
            )

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(
                    f'<div class="score-card"><div class="score-title">Overall Resume Score</div><div class="score-number">{score}</div><div class="score-subtitle">Out of 100</div></div>',
                    unsafe_allow_html=True
                )

            with col2:
                st.markdown(
                    '<div class="score-card"><div class="score-title">Analysis Status</div><div class="score-number">AI</div><div class="score-subtitle">Personalized career insights generated</div></div>',
                    unsafe_allow_html=True
                )

            st.markdown(
                '<div class="report-box">',
                unsafe_allow_html=True
            )

            st.markdown(result)

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            st.download_button(
                label="Download Analysis Report",
                data=result,
                file_name="ResumeIQ_Analysis_Report.txt",
                mime="text/plain"
            )


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    '<div class="custom-footer">ResumeIQ · Generative AI powered resume intelligence</div>',
    unsafe_allow_html=True
)
