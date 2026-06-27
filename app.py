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
# Page Configuration
# ===================================

st.set_page_config(
    page_title="AI Resume Analyzer",
    page_icon="🤖",
    layout="wide"
)
st.markdown("""
<style>

/* Main background */
.stApp{
    background-color:#f5f7fb;
}

/* Buttons */
.stButton > button{
    width:100%;
    border-radius:12px;
    height:50px;
    font-size:17px;
    font-weight:bold;
}

/* Upload box */
[data-testid="stFileUploader"]{
    border:2px dashed #4F46E5;
    border-radius:15px;
    padding:15px;
}

/* Text Area */
textarea{
    border-radius:12px !important;
}

/* Metric Cards */
[data-testid="metric-container"]{
    border-radius:15px;
    padding:15px;
    box-shadow:0px 4px 15px rgba(0,0,0,0.08);
}

/* Expanders */
.streamlit-expanderHeader{
    font-size:18px;
    font-weight:bold;
}

/* Sidebar */
section[data-testid="stSidebar"]{
    background:#ffffff;
}

</style>
""", unsafe_allow_html=True)

# ===================================
# Sidebar
# ===================================

with st.sidebar:

    st.title("🤖 AI Resume Analyzer")

    st.markdown("---")

    st.info(
        """
### Welcome!

This application can:

✅ Extract Resume Text

✅ Detect Technical Skills

✅ Calculate ATS Match Score

✅ Find Missing Skills

✅ Generate AI Resume Feedback
"""
    )

    st.markdown("---")

    st.caption("👩‍💻 Developed by Sakshi Singh")

# ===================================
# Main Heading
# ===================================

# ===================================
# HERO HEADER
# ===================================

st.markdown(
    """
    <div style="text-align:center; padding:20px;">
        <h1>🤖 AI Resume Analyzer</h1>
        <p style="font-size:18px; color:gray;">
        Analyze your resume using AI • Get ATS Score • Improve Instantly
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

    # ============================
    # Continue only if JD exists
    # ============================

    if job_description.strip():

        score = calculate_match_score(
            skills,
            job_description
        )

        missing_skills = get_missing_skills(
            skills,
            job_description
        )
            # ===================================
        # Dashboard Metrics
        # ===================================

        st.divider()

        st.subheader("📊 Dashboard Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(
                f"""
                <div style="
                    background:#2563eb;
                    color:white;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                ">
                    <h3>🎯 ATS Score</h3>
                    <h1>{score}%</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div style="
                    background:#16a34a;
                    color:white;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                ">
                    <h3>🛠 Skills Found</h3>
                    <h1>{len(skills)}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div style="
                    background:#dc2626;
                    color:white;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                ">
                    <h3>❌ Missing Skills</h3>
                    <h1>{len(missing_skills)}</h1>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ===================================
        # Progress Bar
        # ===================================

        st.subheader("📈 ATS Match Progress")

    st.progress(int(score))

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
        # ===================================
        # Missing Skills
        # ===================================

    with st.expander("❌ Missing Skills", expanded=True):

        if missing_skills:

            cols = st.columns(3)

            for index, skill in enumerate(missing_skills):

                cols[index % 3].error(f"❌ {skill.title()}")

        else:

            st.success("🎉 Great! No Missing Skills Found.")

            st.divider()
        
    # ===================================
    # Resume Analytics
    # ===================================

    st.subheader("📊 Resume Analytics")

    col1, col2 = st.columns(2)

    # -------- Chart 1 --------

    with col1:

        fig, ax = plt.subplots(figsize=(4,4))

        ax.pie(
            [len(skills), len(missing_skills)],
            labels=["Skills Found", "Missing Skills"],
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Skills Distribution")

        st.pyplot(fig)

    # -------- Chart 2 --------

    with col2:

        fig2, ax2 = plt.subplots(figsize=(4,4))

        ax2.bar(
            ["ATS Score"],
            [score]
        )

        ax2.set_ylim(0,100)

        ax2.set_ylabel("Score")

        ax2.set_title("ATS Score")

        st.pyplot(fig2)

        # ===================================
        # AI Feedback
        # ===================================

        if st.button("🤖 Generate AI Feedback"):

            with st.spinner("Analyzing your resume with Gemini AI..."):

                feedback = generate_feedback(
                    resume_text,
                    job_description
                )

            st.subheader("🤖 AI Career Assistant")

        st.success("✅ AI Analysis Completed Successfully!")

        with st.container():

            st.markdown(
                f"""
        <div style="
        background-color:#f8f9fa;
        padding:25px;
        border-radius:15px;
        border-left:8px solid #4CAF50;
        box-shadow:0px 3px 10px rgba(0,0,0,0.15);
        ">

        {feedback.replace(chr(10), "<br>")}

        </div>
        """,
                unsafe_allow_html=True
            )
                    # ===================================
            # Create PDF Report
            # ===================================

            try:

                create_pdf(
                    "resume_report.pdf",
                    score,
                    skills,
                    missing_skills,
                    feedback
                )

                st.success("✅ PDF Report Generated")

                if os.path.exists("resume_report.pdf"):

                    with open(
                        "resume_report.pdf",
                        "rb"
                    ) as pdf_file:

                        st.download_button(
                            label="📥 Download AI Report",
                            data=pdf_file,
                            file_name="AI_Resume_Report.pdf",
                            mime="application/pdf"
                        )

            except Exception as e:

                st.error(
                    f"PDF Generation Error: {e}"
                )


# ===================================
# Footer
# ===================================

st.markdown("---")

st.caption(
    "Built with ❤️ using Python, Streamlit and Google Gemini"
)