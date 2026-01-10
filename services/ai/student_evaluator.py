# services/ai/student_evaluator.py

import os
import google.generativeai as genai

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate_student_progress(student_history: list, xp: int, level_name: str) -> dict:
    """
    Evaluates overall student progress and provides comprehensive assessment.
    
    Returns:
    - Skills breakdown (Ethics, Logic, Research, Negotiation)
    - Strengths and weaknesses
    - Learning recommendations
    - Progress summary
    """
    
    if not student_history or len(student_history) == 0:
        return {
            "skills": {
                "Ethics": {"grade": "B", "score": 70, "description": "Getting started"},
                "Logic": {"grade": "B", "score": 70, "description": "Building foundation"},
                "Research": {"grade": "B", "score": 70, "description": "Learning basics"},
                "Negotiation": {"grade": "B", "score": 70, "description": "Developing skills"}
            },
            "strengths": ["Eager to learn", "Consistent participation"],
            "areas_for_improvement": ["Complete more practice sessions", "Engage with diverse case types"],
            "recommendations": [
                "Start with the AI Mock Client to build communication skills",
                "Practice document drafting regularly",
                "Review feedback from each session carefully"
            ],
            "overall_assessment": "You're just getting started on your legal learning journey. Keep practicing!",
            "progress_level": "Beginner"
        }
    
    # Prepare history summary
    history_summary = "\n".join([
        f"- {item.get('case_name', 'Activity')}: Score {item.get('score', 50)}/100, XP: {item.get('xp_earned', 0)}"
        for item in student_history[:10]
    ])
    
    prompt = f"""You are an expert legal educator evaluating a law student's overall progress.

Student Level: {level_name}
Total XP: {xp}
Recent Activity History:
{history_summary}

Evaluate the student's progress across FOUR key skills:

1. ETHICS - Understanding of legal ethics and professional responsibility
2. LOGIC - Legal reasoning and analytical thinking
3. RESEARCH - Ability to find and apply legal information
4. NEGOTIATION - Communication and persuasion skills

For each skill, provide:
- Grade (A+, A, A-, B+, B, B-, C+, C, or D)
- Score (0-100)
- Brief description (5-8 words)

Also provide:
- 2-3 key strengths
- 2-3 areas for improvement
- 3-4 personalized learning recommendations
- Overall assessment (2-3 sentences)
- Progress level (Beginner, Intermediate, or Advanced)

Respond in JSON format:
{{
    "skills": {{
        "Ethics": {{"grade": "A-", "score": 88, "description": "Strong ethical awareness"}},
        "Logic": {{"grade": "B+", "score": 82, "description": "Good analytical reasoning"}},
        "Research": {{"grade": "A", "score": 90, "description": "Excellent research skills"}},
        "Negotiation": {{"grade": "B", "score": 75, "description": "Developing communication"}}
    }},
    "strengths": ["strength 1", "strength 2", "strength 3"],
    "areas_for_improvement": ["area 1", "area 2", "area 3"],
    "recommendations": ["rec 1", "rec 2", "rec 3", "rec 4"],
    "overall_assessment": "<2-3 sentences>",
    "progress_level": "Intermediate"
}}

Be encouraging and constructive."""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
        
        result = eval(response.text)
        return result
        
    except Exception as e:
        print(f"Error evaluating student progress: {e}")
        # Return default evaluation
        return {
            "skills": {
                "Ethics": {"grade": "B+", "score": 82, "description": "Good ethical foundation"},
                "Logic": {"grade": "B", "score": 78, "description": "Solid reasoning skills"},
                "Research": {"grade": "B+", "score": 80, "description": "Effective research ability"},
                "Negotiation": {"grade": "B", "score": 75, "description": "Growing communication skills"}
            },
            "strengths": ["Consistent effort", "Willingness to learn", "Good engagement"],
            "areas_for_improvement": ["Practice more complex scenarios", "Deepen legal knowledge", "Refine writing skills"],
            "recommendations": [
                "Continue regular practice with the Mock Client",
                "Draft more legal documents to improve writing",
                "Review feedback carefully and apply suggestions",
                "Challenge yourself with advanced scenarios"
            ],
            "overall_assessment": "You're making steady progress in your legal education. Keep up the good work and focus on consistent practice.",
            "progress_level": "Intermediate"
        }
