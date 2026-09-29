"""Optional Gemini connectivity smoke test."""
import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
key=os.getenv('GEMINI_API_KEY')
model=os.getenv('GEMINI_MODEL','gemini-3.8-flash')
if not key: raise SystemExit('Set GEMINI_API_KEY in .env first.')
client=genai.Client(api_key=key)
r=client.models.generate_content(model=model, contents='Reply with exactly: PocketSmart AI Gemini connection OK')
print(r.text)
