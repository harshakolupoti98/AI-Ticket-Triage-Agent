import os
from dotenv import load_dotenv
from google import genai

# Load the .env file
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API key not found!")
    exit()

print("✅ API key loaded successfully!")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Say hello in one sentence."
)

print("\nGemini says:")
print(response.text)