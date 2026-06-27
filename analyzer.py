import pdfplumber


def extract_text_from_pdf(pdf_file):
    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text

def extract_skills(text):

    skills_database = [
        "python",
        "java",
        "c",
        "c++",
        "sql",
        "mysql",
        "html",
        "css",
        "javascript",
        "react",
        "streamlit",
        "git",
        "github",
        "pandas",
        "numpy",
        "power bi",
        "excel",
        "machine learning",
        "deep learning",
        "data analytics"
    ]

    text = text.lower()

    found_skills = []

    for skill in skills_database:

        if skill in text:
            found_skills.append(skill)

    return found_skills
def calculate_match_score(resume_skills, job_description):

    job_description = job_description.lower()

    matched_skills = 0

    for skill in resume_skills:

        if skill in job_description:
            matched_skills += 1

    if len(resume_skills) == 0:
        return 0

    score = (matched_skills / len(resume_skills)) * 100

    return round(score, 2)
def get_missing_skills(resume_skills, job_description):

    job_description = job_description.lower()

    skills_database = [
        "python",
        "java",
        "c",
        "c++",
        "sql",
        "mysql",
        "html",
        "css",
        "javascript",
        "react",
        "streamlit",
        "git",
        "github",
        "pandas",
        "numpy",
        "power bi",
        "excel",
        "machine learning",
        "deep learning",
        "data analytics",
        "docker",
        "aws",
        "azure",
        "linux"
    ]

    missing_skills = []

    for skill in skills_database:

        if skill in job_description and skill not in resume_skills:
            missing_skills.append(skill)

    return missing_skills