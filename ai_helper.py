import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Load Gemini model
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_feedback(resume_text, job_description):

    prompt = f"""
You are an ATS Resume Reviewer.

Resume:
{resume_text}

Job Description:
{job_description}

Please provide:

1. Overall Feedback
2. Strengths
3. Weaknesses
4. Missing Skills
5. Suggestions for Improvement
6. ATS Score out of 100

Keep the response concise and professional.
"""

    response = model.generate_content(prompt)

    return response.text