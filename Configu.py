from openai import OpenAI
import os

from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.environ.get("GROQ"),
    base_url="https://api.groq.com/openai/v1",)

