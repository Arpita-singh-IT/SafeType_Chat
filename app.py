# app.py - SafeType AI Backend API
from flask import Flask, request, jsonify
from flask_cors import CORS  # 1. IMPORT CORS
from ai_model import analyze_text
from rephrase import get_rephrasing # To make sure suggestions work
import tkinter as tk
import random


# Initialize the app
if __name__ == "__main__":
    root = tk.Tk()
    app = CelebrationApp(root)
    root.mainloop()  # This line MUST be here to keep the window open!

app = Flask(__name__)
CORS(app)  # 2. ENABLE CORS FOR ALL ROUTES

@app.route('/analyze-text', methods=['POST'])
def analyze_text_endpoint():
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()
    user_text = data.get('text', '').strip()

    if not user_text:
        return jsonify({"label": "Safe", "message": "No text provided."})

    try:
        # Get AI Prediction
        result = analyze_text(user_text)
        label = result["label"]
        confidence = result["confidence"]

        # Get Human-centered suggestions from your rephrase.py
        rephrase_data = get_rephrasing(user_text, label)

        # 3. RETURN DATA IN THE FORMAT YOUR KEYBOARD.JS EXPECTS
        return jsonify({
            "label": label,
            "confidence": confidence,
            "message": rephrase_data["explanation"],
            "suggestions": rephrase_data["suggestions"]
        })

    except Exception as e:
        print(f"AI error: {e}")
        return jsonify({"label": "Safe", "message": "AI error - passing through."})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "running", "service": "SafeType AI"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)