import streamlit as st
from pypdf import PdfReader
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="📄",
    layout="wide"
)

st.title("📄 AI Resume Analyzer")
st.write("Upload your resume and get AI-powered feedback.")

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("GROQ_API_KEY not found in .env file.")
    st.stop()

client = Groq(api_key=api_key)

uploaded_file = st.file_uploader(
    "Upload your Resume PDF",
    type=["pdf"]
)

if uploaded_file:

    reader = PdfReader(uploaded_file)

    resume_text = ""

    for page in reader.pages:
        text = page.extract_text()
        if text:
            resume_text += text + "\n"

    st.success("Resume uploaded successfully!")

    if st.button("🔍 Analyze Resume"):

        with st.spinner("AI is analyzing your resume..."):

            prompt = f"""
You are an expert AI Resume Analyzer.

Analyze this resume:

{resume_text}

Provide:

1. Overall Resume Score out of 100
2. Resume Summary
3. Key Strengths
4. Weaknesses
5. Technical Skills Found
6. Missing Skills
7. Project Suggestions
8. ATS Optimization Suggestions
9. Final Career Advice

Give a clear, professional and detailed answer.
"""

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )

            result = response.choices[0].message.content

            st.markdown("---")
            st.header("📊 Resume Analysis")
            st.markdown(result)