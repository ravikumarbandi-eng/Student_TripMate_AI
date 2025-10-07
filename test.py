from ai_client import generate_itinerary

print("Testing Gemini AI connection...\n")
output = generate_itinerary("Goa", 3, 5000, "beach, food")
print(output)
