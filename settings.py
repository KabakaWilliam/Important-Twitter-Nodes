import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_KEY_SECRET = os.getenv("API_KEY_SECRET")
API_BEARER_TOKEN = os.getenv("API_BEARER_TOKEN")
API_ACCESS_TOKEN = os.getenv("API_ACCESS_TOKEN")
API_TOKEN_SECRET = os.getenv("API_TOKEN_SECRET")