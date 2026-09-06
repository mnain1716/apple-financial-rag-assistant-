from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

if not os.getenv("GEMINI_API_KEY"):
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.7-flash",
    contents="Reply with exactly: Gemini connection successful."
)

print(response.text)