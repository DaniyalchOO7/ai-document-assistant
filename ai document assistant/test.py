import os
from dotenv import load_dotenv
import google.genai as genai

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Try listing models
for m in genai.list_models():
    print(m.name)