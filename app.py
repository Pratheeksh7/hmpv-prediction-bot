from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pickle
#import os

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)

# Load the trained model
with open('hmpv_model.pkl', 'rb') as file:
    model = pickle.load(file)

# Define global variables for the chat state
questions = [
    "What is your body temperature in Fahrenheit? (e.g., 98.6)",
    "Do you have a cough? (yes/no)",
    "Do you have a runny nose? (yes/no)",
    "Are you experiencing difficulty breathing? (yes/no)",
    "What is your age?",
    "Are you experiencing any fatigue? (yes/no)"
]
responses = []


@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)


@app.route('/')
def serve_welcome():
    """Serve the welcome HTML file."""
    return send_from_directory(app.static_folder, 'welcome.html')


@app.route('/start', methods=['GET'])
def start_chat():
    """Start the chatbot interaction."""
    global responses
    responses = []  # Reset responses
    return jsonify({"question": questions[0]})


@app.route('/next', methods=['POST'])
def next_question():
    """Handle user responses and return the next question or prediction."""
    global responses

    # Parse user response
    data = request.json
    user_response = data.get("response", "").strip().lower()

    # Validate responses
    if len(responses) == 0:  # Temperature validation
        try:
            temperature = float(user_response)
            if temperature<92 or temperature>105:
                raise ValueError({"error": "Please provide a valid temperature (e.g., 98.6)."})
            responses.append(temperature)
        except ValueError:
            return jsonify({"error": "Please provide a valid temperature (e.g., 98.6)."})
    elif len(responses) == 4:  # Age validation
        try:
            age = int(user_response)
            if age<=0 or age>100:
                raise ValueError({"error":"Please provide a valid age(e.g., 30)."})
            responses.append(age)
        except ValueError:
            return jsonify({"error": "Please provide a valid age (e.g., 30)."})
    elif user_response in ["yes", "no"]:  # Yes/No validation
        responses.append(1 if user_response == "yes" else 0)
    else:
        return jsonify({"error": "Please answer with 'yes', 'no', or a valid number."})

    # Ask the next question or make a prediction
    if len(responses) < len(questions):
        return jsonify({"question": questions[len(responses)]})
    else:
        # Make prediction
        input_data = [responses]
        prediction = model.predict(input_data)[0]
        result = "Positive for HMPV.Please consult a doctor as early as possible." if prediction == 1 else "Negative for HMPV"
        return jsonify({"prediction": result})


if __name__ == '__main__':
    app.run(debug=True)
