import os
import time
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_itinerary(city, days, budget, preferences):
    prompt = f"""
    Create a {days}-day travel itinerary for {city} within a budget of ₹{budget}.
    Preferences: {preferences}
    Make the output structured and student-friendly.
    """

    # Retry logic for 503 errors (model overloaded)
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-1.5-flash",  # more stable than gemini-2.5-flash
                contents=prompt
            )
            return response.text
        
        except Exception as e:
            if "503" in str(e):
                time.sleep(3)  # wait and retry
                continue
            return f"⚠️ Error generating itinerary: {e}"

    return "⚠️ The AI service is currently busy. Please try again after a few minutes."
