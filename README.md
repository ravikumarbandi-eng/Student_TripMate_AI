# 🎓 Student TripMate AI ✈️
[![Open in Streamlit](https://img.shields.io/badge/Run%20App-Streamlit-blue?logo=streamlit)](https://studenttripmateai-bandiravikumar88.streamlit.app/)


**Project Description:**  
Student TripMate AI is an AI-powered travel planner designed specifically for students. It generates personalized travel itineraries based on the city, number of days, budget, and preferences. The app also saves previous itineraries individually for each student, enabling easy reference.

---

## **Technologies Used**

- **Python 3.x** – Programming language  
- **Streamlit** – Web app framework for interactive UI  
- **Google Gemini AI API** – For generating travel itineraries  
- **JSON** – For saving/loading itineraries per student  
- **dotenv** – To securely load API keys from `.env`  
- **Pyngrok** (Optional) – For exposing local Streamlit app via public URL  

---

## **File Structure**

| File | Purpose |
|------|---------|
| `app.py` | Main Streamlit application file |
| `ai_client.py` | Contains function to call Google Gemini AI API and generate itinerary |
| `planner.py` | Handles saving/loading student itineraries using JSON |
| `.env` | Stores Gemini API key securely |
| `requirements.txt` | Lists all dependencies required for the project |
| `README.md` | Project documentation and explanation |
| `test.py` | (Optional) File to test functions independently |
| `config.py` | (Optional) Contains configuration variables like API versions |

---

## **Step-by-Step Explanation of Code**

### **1. API Key Setup (`.env`)**
We store the Gemini AI API key in a `.env` file to avoid hardcoding sensitive credentials.

```python
from getpass import getpass
import os

GEMINI_API_KEY = getpass("Paste your Gemini API Key here (hidden): ")

with open(".env", "w") as f:
    f.write(f"GEMINI_API_KEY={GEMINI_API_KEY}\n")
```

---

### **2. Main App (`app.py`)**
The Streamlit app handles login, input collection, itinerary generation, and history display.

```python
import streamlit as st
from ai_client import generate_itinerary
from planner import load_history, save_history
import json

st.set_page_config(page_title="Student TripMate AI ✈️", layout="wide")
```

---

### **3. Login System**
```python
if "student_name" not in st.session_state:
    st.title("🎓 Student TripMate AI ✈️")
    st.write("_Plan affordable and fun trips anywhere — made easy for students by AI!_")
    
    student_name = st.text_input("Enter your name to start:")
    if st.button("Start Planning 🚀") and student_name:
        st.session_state.student_name = student_name
        st.experimental_rerun()
    st.stop()
```

---

### **4. Sidebar Inputs & Tabs**
```python
student_name = st.session_state.student_name

st.sidebar.title(f"👤 {student_name}")
st.sidebar.header("Make Your Trip ✈️")

city = st.sidebar.text_input("Enter city name:")
days = st.sidebar.number_input("Number of days:", min_value=1, max_value=30, value=3)
budget = st.sidebar.number_input("Budget (₹):", min_value=1000, step=500, value=5000)
preferences = st.sidebar.text_area("Preferences:", placeholder="e.g., food, adventure, shopping")

tab1, tab2 = st.tabs(["Plan Trip 📝", "Previous Itineraries 📜"])
```

---

### **5. Generate Itinerary**
```python
with tab1:
    if st.button("Generate Itinerary ✨"):
        with st.spinner("AI is generating your travel plan..."):
            itinerary = generate_itinerary(city, days, budget, preferences)

        st.subheader("🌟 Your AI-Powered Trip Plan")
        st.success(itinerary)

        # Save itinerary
        history = load_history(student_name)
        history.append({
            "city": city,
            "days": days,
            "budget": budget,
            "preferences": preferences,
            "itinerary": itinerary
        })
        save_history(student_name, history)
```

---

### **6. Display Previous Itineraries**
```python
with tab2:
    st.subheader("📜 Your Past Trips")
    history = load_history(student_name)
    if history:
        for i, h in enumerate(reversed(history[-3:]), 1):
            st.markdown(f"### {i}. {h['city']} ({h['days']} days, ₹{h['budget']})")
            st.write(f"**Preferences:** {h['preferences']}")
            st.info(h["itinerary"])
            st.markdown("---")
    else:
        st.write("No previous itineraries found.")
```

---

### **7. AI Client (`ai_client.py`)**
```python
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def generate_itinerary(city, days, budget, preferences):
    prompt = f"Create a {days}-day travel itinerary for {city} with budget ₹{budget}. Preferences: {preferences}"
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    return response.text
```

---

### **8. Planner (`planner.py`)**
```python
import json
import os

def load_history(student_name):
    file_name = f"{student_name}_history.json"
    if os.path.exists(file_name):
        with open(file_name, "r") as f:
            return json.load(f)
    return []

def save_history(student_name, history):
    file_name = f"{student_name}_history.json"
    with open(file_name, "w") as f:
        json.dump(history, f, indent=2)
```

---

### **9. Requirements**
```
streamlit
google-genai
python-dotenv
pyngrok
```

Install dependencies with:
```bash
pip install -r requirements.txt
```

---

### **10. How the Project Works**

1. **User opens app** → sees project title & tagline.  
2. **Student enters name** → input disappears after login.  
3. **Sidebar inputs** → city, days, budget, preferences.  
4. **Generate itinerary** → AI generates plan → shown with spinner.  
5. **Previous trips** → saved per student → last 3 trips displayed.  
6. **Individual storage** → JSON file for each student ensures privacy.  
7. **Deployment** → Run locally with Streamlit or use Pyngrok for public access.


