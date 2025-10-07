import streamlit as st
import os
from dotenv import load_dotenv
from ai_client import generate_itinerary
import json

# Load API key for local testing (optional)
load_dotenv() if os.path.exists(".env") else None

st.set_page_config(
    page_title="Student TripMate AI ✈️",
    layout="wide"
)

# Always show the project title & tagline
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("## 🎓 Student TripMate AI ✈️", unsafe_allow_html=True)
    st.markdown("_Plan affordable and fun trips anywhere — made easy for students by AI!_")

st.markdown("---")

# Student login by name (no password)
student_name = st.text_input("Enter your name to start your personalized trip planner:")

if not student_name:
    st.warning("Please enter your name to continue.")
    st.stop()  # Stop until name is entered

# Show user name top-left with user emoji
st.markdown(f"**👤 {student_name}**")

# Internal storage file per student
history_file = f"{student_name}_history.json"

# Load previous itineraries for this student
if "history" not in st.session_state:
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            st.session_state.history = json.load(f)
    else:
        st.session_state.history = []

# Sidebar for trip inputs
st.sidebar.header("Plan Your Trip ✍️")
city = st.sidebar.text_input("Enter city name:")
days = st.sidebar.number_input("Number of days:", min_value=1, max_value=30, value=3)
budget = st.sidebar.number_input("Budget (₹):", min_value=1000, step=500, value=5000)
preferences = st.sidebar.text_area("Preferences (optional):", placeholder="e.g., food, adventure, shopping")
st.sidebar.markdown("---")

# Tabs for Generate & History
tab1, tab2 = st.tabs(["Generate Itinerary 📝", "Previous Itineraries 📜"])

with tab1:
    if st.button("Generate Itinerary 🚀"):
        itinerary_text = generate_itinerary(city, days, budget, preferences)
        st.subheader("🌟 Your AI-Powered Student Itinerary")
        st.success(itinerary_text)

        # Save history
        itinerary = {
            "city": city,
            "days": days,
            "budget": budget,
            "preferences": preferences,
            "itinerary": itinerary_text
        }
        st.session_state.history.append(itinerary)
        with open(history_file, "w") as f:
            json.dump(st.session_state.history, f, indent=2)

with tab2:
    st.subheader("Previous Itineraries (Last 3 shown)")
    if st.session_state.history:
        last_items = list(reversed(st.session_state.history))[:3]
        for idx, item in enumerate(last_items, 1):
            with st.container():
                st.markdown(f"### {idx}. {item['city']} ({item['days']} days, ₹{item['budget']})")
                st.write(f"**Preferences:** {item['preferences']}")
                st.info(item['itinerary'])
                st.markdown("---")
    else:
        st.write("No previous itineraries found.")

