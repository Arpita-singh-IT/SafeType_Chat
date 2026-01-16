# app.py
# SafeType AI Backend - Flask API for toxicity analysis
# Updated for 2026 - works with current PyTorch/Transformers versions

from flask import Flask, request, jsonify
from ai_model import analyze_text  # Import the AI inference function

app = Flask(__name__)

@app.route('/analyze-text', methods=['POST'])
def analyze_text_endpoint():
    """
    POST endpoint for analyzing user message toxicity.
    
    Expected JSON:
    {
        "text": "user message here"
    }
    
    Returns:
    {
        "label": "Safe" | "Warning" | "Toxic",
        "confidence": float (0.0 - 1.0),
        "message": "Friendly feedback"
    }
    """
    # Check if request is JSON
    if not request.is_json:
        return jsonify({"error": "Request must be JSON"}), 400

    data = request.get_json()

    # Validate input
    if 'text' not in data or not isinstance(data['text'], str):
        return jsonify({"error": "Missing or invalid 'text' field"}), 400

    user_text = data['text'].strip()

    # Handle empty message
    if not user_text:
        return jsonify({
            "label": "Safe",
            "confidence": 1.0,
            "message": "Nothing to send yet!"
        }), 200

    try:
        # Call AI model (from ai_model.py)
        result = analyze_text(user_text)

        label = result.get("label", "Safe")
        confidence = result.get("confidence", 0.0)

        # Friendly user-facing message
        if label == "Safe":
            friendly_message = "Looks good! Sending your message 😊"
        elif label == "Warning":
            friendly_message = "This could sound a bit strong. Consider softening it?"
        else:  # Toxic
            friendly_message = "This message may be hurtful. Let's rephrase it kindly 💙"

        response = {
            "label": label,
            "confidence": round(confidence, 4),
            "message": friendly_message
        }

        return jsonify(response), 200

    except Exception as e:
        print(f"Error during analysis: {e}")
        # Fallback - never block user completely in hackathon demo
        return jsonify({
            "label": "Safe",
            "confidence": 0.0,
            "message": "Temporary issue — message sent safely."
        }), 200


@app.route('/', methods=['GET'])
def health_check():
    """Simple health check"""
    return jsonify({
        "status": "running",
        "service": "SafeType AI Backend",
        "version": "hackathon-2026"
    }), 200


if __name__ == '__main__':
    print("SafeType AI Backend starting...")
    print("API available at: http://localhost:5000/analyze-text")
    print("Health check: http://localhost:5000/")
    
    # Accessible on local network for demo
    app.run(host='0.0.0.0', port=5000, debug=True)