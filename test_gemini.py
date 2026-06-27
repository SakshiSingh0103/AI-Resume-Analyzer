import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load .env file
load_dotenv()

# Read API key
api_key = os.getenv("GEMINI_API_KEY")

print("API Key Loaded:", api_key is not None)

# Configure Gemini
genai.configure(api_key=api_key)

# Load model
model = genai.GenerativeModel("gemini-2.5-flash")

# Ask Gemini a question
response = model.generate_content(
    "Explain Python in one sentence."
)

print(response.text)