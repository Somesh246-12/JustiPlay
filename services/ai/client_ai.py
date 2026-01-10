import os
import google.generativeai as genai

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.0-flash-exp")


def get_client_reply(conversation_history, student_question, scenario_context=None):
    """
    Generates a client-style reply using Gemini,
    while preserving conversation context and using dynamic scenario.
    """
    
    # Default scenario if none provided (Fallback)
    if not scenario_context:
        scenario_role = "Tenant"
        scenario_bg = """
- You are a tenant.
- Your landlord stopped accepting rent.
- You were threatened with eviction verbally.
- You received NO written notice.
- You are anxious and confused.
"""
    else:
        scenario_role = scenario_context.get("role", "Client")
        scenario_bg = f"""
- You are: {scenario_role}
- Situation: {scenario_context.get('context', 'No context provided')}
"""

    prompt = f"""
You are simulating a LEGAL CLIENT for educational purposes ONLY.

STRICT RULES (YOU MUST FOLLOW ALL):
- You are NOT a lawyer.
- You do NOT give legal advice.
- You do NOT suggest actions, remedies, or next steps.
- You ONLY answer questions as {scenario_role}.
- You speak in simple, emotional, uncertain language.
- You answer ONLY from your personal experience.
- If asked for advice, say you are not sure and feel overwhelmed.

CASE BACKGROUND:
{scenario_bg}

STYLE:
- Short responses (2–4 sentences).
- Natural, human tone.
- No legal terminology.
- No bullet points.

Remember: You are a CLIENT, not an advisor.
""".strip() + "\n\n"

    if conversation_history:
        prompt += "Conversation so far:\n"
        for turn in conversation_history:
            prompt += f"Student: {turn['question']}\n"
            prompt += f"Client: {turn['reply']}\n"

    prompt += f"\nStudent: {student_question}\nClient:"

    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        print(f"Error generating client reply: {e}")
        return "I... I'm not sure what to say about that. Can you explain?"

