import json
import vertexai
from vertexai.preview.generative_models import GenerativeModel
from services.ai.prompts.evaluation_prompt import EVALUATION_PROMPT

PROJECT_ID = "legalease-ai-471416"
LOCATION = "asia-south1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

model = GenerativeModel("gemini-2.5-flash")


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
        return json.loads(response.text)
    except Exception:
        # Safe fallback (never break the app)
        return {
            "clarity": "Average",
            "relevance": "Medium",
            "ethics": "Safe",
            "total_score": 50,
            "feedback": "Try to ask clearer, more specific questions to understand the client's situation better."
        }
