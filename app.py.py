import streamlit as st
from ai_client import generate_itinerary
from planner import load_history, save_history

# Streamlit page setup
st.set_page_config(page_title="Student TripMate AI ✈️", layout="wide")

# Login system
if "student_name" not in st.session_state:
    st.title("🎓 Student TripMate AI ✈️")
    st.write("_Plan affordable and fun trips anywhere — made easy for students by AI!_")
    
    student_name = st.text_input("Enter your name to start:")
    if st.button("Start Planning 🚀") and student_name:
        st.session_state.student_name = student_name
        st.stop()  # Stops execution; main UI appears in next rerun
    st.stop()

# After login
student_name = st.session_state.student_name

# **Display project title & tagline even after login**
st.markdown("## 🎓 Student TripMate AI ✈️")
st.markdown("_Plan affordable and fun trips anywhere — made easy for students by AI!_")
st.markdown("---")

# Sidebar
st.sidebar.title(f"👤 {student_name}")
st.sidebar.header("Make Your Trip ✈️")
city = st.sidebar.text_input("Enter city name:")
days = st.sidebar.number_input("Number of days:", min_value=1, max_value=30, value=3)
budget = st.sidebar.number_input("Budget (₹):", min_value=1000, step=500, value=5000)
preferences = st.sidebar.text_area("Preferences:", placeholder="e.g., food, adventure, shopping")

# Tabs
tab1, tab2 = st.tabs(["Plan Trip 📝", "Previous Itineraries 📜"])

# Generate itinerary
with tab1:
    if st.button("Generate Itinerary ✨"):
        with st.spinner("AI is generating your travel plan..."):
            itinerary = generate_itinerary(city, days, budget, preferences)

        st.subheader("🌟 Your AI-Powered Trip Plan")
        st.success(itinerary)

        # Save itinerary for this student
        history = load_history(student_name)
        history.append({
            "city": city,
            "days": days,
            "budget": budget,
            "preferences": preferences,
            "itinerary": itinerary
        })
        save_history(student_name, history)

# Display previous itineraries
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
