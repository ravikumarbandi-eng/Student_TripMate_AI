import json
import os

def load_history(student_name):
    """Load previous itineraries from file"""
    history_file = f"{student_name}_history.json"
    if os.path.exists(history_file):
        with open(history_file, "r") as f:
            return json.load(f)
    return []

def save_history(student_name, history):
    """Save itineraries to student file"""
    history_file = f"{student_name}_history.json"
    with open(history_file, "w") as f:
        json.dump(history, f, indent=2)
