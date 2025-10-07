import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Fetch API key
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Default port for Streamlit
PORT = 8501
