# ai_model.py - Better toxicity detection with unitary/toxic-bert

from transformers import pipeline

# Load a more balanced general toxicity model
# unitary/toxic-bert is excellent for chat/comments — less over-sensitive
classifier = pipeline(
    "text-classification",
    model="unitary/toxic-bert",
    return_all_scores=True,  # Get all toxicity categories
    device=-1  # CPU (change to 0 for GPU)
)

def analyze_text(text: str):
    """
    Analyze text for toxicity using a balanced multi-label model.
    Returns Safe/Warning/Toxic with confidence (max score across categories).
    """
    if not text or not text.strip():
        return {"label": "Safe", "confidence": 1.0}

    results = classifier(text.strip())[0]

    # results is list of dicts: [{'label': 'toxic', 'score': 0.99}, {'label': 'insult', 'score': 0.8}, ...]
    # Find the highest toxicity score
    max_score = max(r['score'] for r in results)
    toxic_label = max(results, key=lambda x: x['score'])['label']

    # Adjusted thresholds for fewer false positives
    if max_score < 0.3:
        label = "Safe"
        confidence = 1.0 - max_score
    elif max_score < 0.6:
        label = "Warning"
        confidence = max_score
    else:
        label = "Toxic"
        confidence = max_score

    return {
        "label": label,
        "confidence": round(confidence, 4)
    }