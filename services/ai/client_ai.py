import vertexai
from vertexai.preview.generative_models import GenerativeModel
from services.ai.prompts.client_prompts import CLIENT_ROLE_PROMPT

# Update these once, reuse everywhere
PROJECT_ID = "legalease-ai-471416"
LOCATION = "asia-south1"

vertexai.init(project=PROJECT_ID, location=LOCATION)

model = GenerativeModel("gemini-2.5-flash")


def get_client_reply(conversation_history, student_question):
    """
    Generates a client-style reply using Gemini,
    while preserving conversation context.
    """

    prompt = CLIENT_ROLE_PROMPT.strip() + "\n\n"

    if conversation_history:
        prompt += "Conversation so far:\n"
        for turn in conversation_history:
            prompt += f"Student: {turn['question']}\n"
            prompt += f"Client: {turn['reply']}\n"

    prompt += f"\nStudent: {student_question}\nClient:"

    response = model.generate_content(prompt)

    return response.text.strip()
