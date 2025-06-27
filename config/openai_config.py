from dotenv import load_dotenv
import requests
load_dotenv()
import os
import base64
from openai import OpenAI, AsyncOpenAI


API_KEY = os.getenv("API_KEY")

text_client = OpenAI(
  api_key=API_KEY
)

speech_client = AsyncOpenAI(api_key=API_KEY)
