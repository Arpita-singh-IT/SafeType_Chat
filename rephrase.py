# rephrase.py
# Human-centered rephrasing suggestions for SafeType moderation system
# Rule-based, supportive, and non-judgmental alternatives for toxic/warning messages

import re
import random

def get_rephrasing(text: str, label: str):
    """
    Generate polite, constructive rephrasing suggestions for potentially toxic messages.
    
    Args:
        text (str): The original user message detected as Warning or Toxic
        label (str): "Warning" or "Toxic" from the AI model
    
    Returns:
        dict: {
            "explanation": str - gentle message explaining the suggestion,
            "suggestions": list[str] - 2–3 polite alternative phrasings
        }
    
    This is a rule-based system focused on empathy and collaboration.
    It can later be replaced or enhanced with a generative LLM (e.g., Grok, Llama, or GPT)
    for more context-aware and personalized rephrasing.
    """
    text_lower = text.lower().strip()
    
    # Determine tone of feedback based on severity
    if label == "Toxic":
        explanation = (
            "This message might come across as hurtful or aggressive. "
            "Let's try expressing the same idea in a kinder way to keep the conversation positive! 💙"
        )
    else:  # Warning
        explanation = (
            "This message could be misinterpreted or sound a bit harsh. "
            "A slightly softer tone can help others feel more comfortable and understood 😊"
        )

    suggestions = []

    # Common pattern matching and softening templates
    if any(word in text_lower for word in ["you suck", "you're bad", "you're terrible", "you fail"]):
        suggestions.extend([
            "I'm finding this fustrating ",
            "I'm not getting the result I expected.",
            "This isn't working for me yet. "
        ])

    elif any(word in text_lower for word in ["stupid", "idiot", "dumb", "moron"]):
        suggestions.extend([
            "I'm confused by this part — can you explain it differently?",
            "This doesn't make sense to me yet. Could you clarify?",
            "I don't quite follow — would you mind rephrasing?"
        ])

    elif any(word in text_lower for word in ["hate", "annoying", "worst", "awful", "terrible"]):
        suggestions.extend([
            "I'm not really enjoying this experience.",
            "This is frustrating for me right now.",
            "I'd prefer if things worked differently."
        ])

    elif any(word in text_lower for word in ["you always", "you never", "you're always", "you're never"]):
        suggestions.extend([
            "I've noticed this happening a few times — can we talk about it?",
            "It feels like this comes up often. How can we improve it?",
            "Sometimes I feel like this pattern repeats. What do you think?"
        ])

    elif "why" in text_lower and ("so slow" in text_lower or "so bad" in text_lower or "not working" in text_lower):
        suggestions.extend([
            "I'm having trouble with this — is there something I'm missing?",
            "Could you help me understand what's causing the delay?",
            "It seems to be taking longer than expected. Any ideas?"
        ])

    # Generic fallbacks if no specific pattern matched
    if not suggestions:
        suggestions = [
            "Let me try saying that more kindly...",
            "Here's a more positive way to express that:",
            "How about something like:"
        ]
        # Add generic softened versions
        suggestions.extend([
            "I feel frustrated when this happens. ",
            "I'm having a hard time with this. ",
            "I'd appreciate it if we could approach this differently.",
            "I need some time , will catch up later "
        ])

    # Shuffle and limit to 3 suggestions for variety
    random.shuffle(suggestions)
    selected_suggestions = suggestions[:3]

    return {
        "explanation": explanation,
        "suggestions": selected_suggestions
    }

# Example usage (for testing during development)
if __name__ == "__main__":
    examples = [
        ("You're so stupid!", "Toxic"),
        ("This app is annoying", "Warning"),
        ("Why are you always late?", "Warning"),
        ("I hate this feature", "Toxic")
    ]

    print("Rephrasing Suggestions Demo\n" + "="*50)
    for text, label in examples:
        result = get_rephrasing(text, label)
        print(f"Original: \"{text}\" ({label})")
        print(f"Explanation: {result['explanation']}")
        print("Suggestions:")
        for i, sug in enumerate(result['suggestions'], 1):
            print(f"  {i}. \"{sug}\"")
        print("-" * 50)