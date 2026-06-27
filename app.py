import os
import streamlit as st
import matplotlib.pyplot as plt

from analyzer import (
    extract_text_from_pdf,
    extract_skills,
    calculate_match_score,
    get_missing_skills
)

from ai_helper import generate_feedback
from pdf_generator import create_pdf

# ===================================
# PAGE CONFIGURATION
# ===================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)

# ===================================
# CUSTOM CSS
# ===================================

st.markdown("""
<style>

/* Background */
.stApp{
    background:#f5f7fb;
}

/* Buttons */
.stButton>button{
    width:100%;
    height:50px;
    border-radius:12px;
    font-size:16px;
    font-weight:bold;
}

/* Upload Box */
[data-testid="stFileUploader"]{
    border:2px dashed #4F46E5;
    border-radius:15px;
    padding:15px;
}

/* Text Areas */
textarea{
    border-radius:10px !important;
}

/* Expander */
.streamlit-expanderHeader{
    font-size:18px;
    font-weight:bold;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:white;
}

</style>
""", unsafe_allow_html=True)

# ===================================
# SIDEBAR
# ===================================

with st.sidebar:

    st.title("🤖 AI Resume Analyzer")

    st.markdown("---")

    st.info(
        """
### Features

✅ Resume Upload

✅ ATS Score

✅ Skill Detection

✅ Missing Skills

✅ Gemini AI Feedback

✅ PDF Report
"""
    )

    st.markdown("---")

    st.success("🚀 AI Resume Analyzer V2")

    st.caption("👩‍💻 Developed by Sakshi Singh")

# ===================================
# HERO HEADER
# ===================================

st.markdown(
    """
<div style="text-align:center;padding:20px;">

<h1>🤖 AI Resume Analyzer</h1>

<p style="font-size:18px;color:gray;">

Analyze your resume using AI, compare it with a Job Description,
calculate ATS score and receive professional feedback.

</p>

</div>
""",
    unsafe_allow_html=True
)

st.divider()

# ===================================
# Job Description
# ===================================

job_description = st.text_area(
    "📋 Job Description",
    height=220,
    placeholder="Paste the Job Description here..."
)

# ===================================
# Upload Resume
# ===================================

uploaded_file = st.file_uploader(
    "📄 Upload Resume",
    type=["pdf"]
)

# ===================================
# Process Resume
# ===================================

if uploaded_file is not None:

    resume_text = extract_text_from_pdf(uploaded_file)

    skills = extract_skills(resume_text)

    total_skills = len(skills)

    st.success("✅ Resume uploaded successfully!")

    with st.expander("📄 View Extracted Resume", expanded=False):

        st.text_area(
            "",
            resume_text,
            height=250
        )

    with st.expander("🛠 Detected Skills", expanded=True):

        if skills:

            cols = st.columns(3)

            for index, skill in enumerate(skills):

                cols[index % 3].success(f"✔ {skill.title()}")

        else:

            st.warning("No skills detected in the resume.")

    if job_description.strip():

        score = calculate_match_score(
            skills,
            job_description
        )

        missing_skills = get_missing_skills(
            skills,
            job_description
        )

        st.divider()

        st.subheader("📊 Dashboard Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div style="background:#2563eb;
                        color:white;
                        padding:20px;
                        border-radius:15px;
                        text-align:center;">
                <h3>🎯 ATS Score</h3>
                <h1>{score}%</h1>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div style="background:#16a34a;
                        color:white;
                        padding:20px;
                        border-radius:15px;
                        text-align:center;">
                <h3>🛠 Skills Found</h3>
                <h1>{total_skills}</h1>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div style="background:#dc2626;
                        color:white;
                        padding:20px;
                        border-radius:15px;
                        text-align:center;">
                <h3>❌ Missing Skills</h3>
                <h1>{len(missing_skills)}</h1>
            </div>
            """, unsafe_allow_html=True)

        st.subheader("📈 ATS Match Progress")

        st.progress(min(score/100,1.0))

        st.write(f"### 🎯 Current ATS Score: **{score}%**")

        if score >= 90:
            st.success("🏆 Outstanding! Your resume is highly optimized.")

        elif score >= 80:
            st.success("🟢 Excellent Resume Match")

        elif score >= 60:
            st.warning("🟡 Good Match - A few improvements can increase your chances.")

        elif score >= 40:
            st.warning("🟠 Fair Match - Consider adding more relevant skills.")

        else:
            st.error("🔴 Low Match - Your resume needs significant improvement.")

        with st.expander("❌ Missing Skills", expanded=True):

            if missing_skills:

                cols = st.columns(3)

                for index, skill in enumerate(missing_skills):

                    cols[index % 3].error(f"❌ {skill.title()}")

            else:

                st.success("🎉 Great! No Missing Skills Found.")

        # ===================================
        # Resume Analytics
        # ===================================

        st.divider()

        st.subheader("📊 Resume Analytics")

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:

            fig, ax = plt.subplots(figsize=(4, 4))

            ax.pie(
                [len(skills), len(missing_skills)],
                labels=["Skills Found", "Missing Skills"],
                autopct="%1.1f%%",
                startangle=90
            )

            ax.set_title("Skills Distribution")

            st.pyplot(fig)

        with col_chart2:

            fig2, ax2 = plt.subplots(figsize=(4, 4))

            ax2.bar(
                ["ATS Score"],
                [score]
            )

            ax2.set_ylim(0, 100)

            ax2.set_ylabel("Score")

            ax2.set_title("ATS Score")

            st.pyplot(fig2)

        # ===================================
        # AI Feedback
        # ===================================

        st.divider()

        st.info(
            "💡 Click the button below to generate personalized AI feedback."
        )

        if st.button("🤖 Generate AI Feedback"):

            with st.spinner("Gemini AI is analyzing your resume..."):

                feedback = generate_feedback(
                    resume_text,
                    job_description
                )

            st.subheader("🤖 AI Career Assistant")

            st.success("✅ AI Analysis Completed Successfully!")

            st.markdown(
                f"""
<div style="
background:#f8f9fa;
padding:25px;
border-radius:15px;
border-left:8px solid #22c55e;
box-shadow:0px 3px 12px rgba(0,0,0,0.15);
">

{feedback.replace(chr(10), "<br>")}

</div>
""",
                unsafe_allow_html=True
            )

            # ===================================
            # PDF Report
            # ===================================

            try:

                create_pdf(
                    "resume_report.pdf",
                    score,
                    skills,
                    missing_skills,
                    feedback
                )

                st.success("📄 PDF Report Generated Successfully!")

                with open(
                    "resume_report.pdf",
                    "rb"
                ) as pdf_file:

                    st.download_button(
                        "📥 Download AI Report",
                        pdf_file,
                        file_name="AI_Resume_Report.pdf",
                        mime="application/pdf"
                    )

            except Exception as e:

                st.error(f"PDF Generation Error: {e}")

# ===================================
# FOOTER
# ===================================

st.divider()

st.markdown(
    """
<div style="text-align:center;color:gray;">

Made with ❤️ using Python, Streamlit & Google Gemini AI

<br><br>

© 2026 Sakshi Singh

</div>
""",
    unsafe_allow_html=True
)