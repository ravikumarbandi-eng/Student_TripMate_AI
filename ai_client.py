# ai_client.py
from google import genai
import os
from dotenv import load_dotenv

# Load the .env file for the API key
load_dotenv()

# Get the Gemini API key from environment
api_key = os.getenv("GEMINI_API_KEY")

# Validate the key
if not api_key:
    raise ValueError("❌ GEMINI_API_KEY not found. Please set it in your .env file or Streamlit secrets.")

# Initialize the Gemini client
client = genai.Client(api_key=api_key)

def generate_itinerary(city, days, budget, preferences=""):
    """
    Generates a travel itinerary using the Gemini model.
    
    Args:
        city (str): Destination city name.
        days (int): Number of travel days.
        budget (int): Total trip budget in ₹.
        preferences (str): Optional user preferences like adventure, food, etc.

    Returns:
        str: AI-generated travel plan.
    """

    prompt = f"""
    You are an expert student travel planner.
    Create a detailed {days}-day itinerary for {city} with a total budget of ₹{budget}.
    Focus on affordable and educational experiences.
    Student preferences: {preferences}.
    Format clearly with day-wise breakdown and travel tips.
    """

    # Generate content using Gemini
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        return f"⚠️ Error generating itinerary: {str(e)}"
