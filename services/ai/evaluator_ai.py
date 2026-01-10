import json
import os
import google.generativeai as genai

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

from services.ai.prompts.evaluation_prompt import EVALUATION_PROMPT

model = genai.GenerativeModel("gemini-2.0-flash-exp")


def evaluate_student_question(student_question):
    """
    Evaluates the quality of a student's question.
    Returns structured educational feedback.
    """

    prompt = (
        EVALUATION_PROMPT.strip()
        + "\n\nStudent Question:\n"
        + student_question
        + "\n\nEvaluation:"
    )

    response = model.generate_content(prompt)

    try:
        text = response.text.strip()
        if text.startswith("```json"):
            text = text[7:-3].strip()
        elif text.startswith("```"):
            text = text[3:-3].strip()
        return json.loads(text)
    except Exception:
        # Safe fallback (never break the app)
        return {
            "clarity": "Average",
            "relevance": "Medium",
            "ethics": "Safe",
            "total_score": 50,
            "feedback": "Try to ask clearer, more specific questions to understand the client's situation better."
        }
