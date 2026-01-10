# services/ai/document_evaluator.py

import os
import google.generativeai as genai

# Initialize Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def evaluate_document(document_text: str, document_type: str = "Legal Document") -> dict:
    """
    Evaluates a student-drafted legal document using Gemini AI.
    
    Returns evaluation scores for:
    - Clarity (structure, language, readability)
    - Relevance (legal accuracy, appropriate content)
    - Ethics (ethical compliance, professional standards)
    """
    
    if not document_text or len(document_text.strip()) < 50:
        return {
            "clarity_score": 0,
            "relevance_score": 0,
            "ethics_score": 0,
            "total_score": 0,
            "feedback": {
                "clarity": "Document is too short to evaluate.",
                "relevance": "Please provide more content.",
                "ethics": "Insufficient content for ethical review."
            },
            "suggestions": ["Write at least 50 characters to receive evaluation."],
            "grade": "Incomplete"
        }
    
    prompt = f"""You are an expert legal educator evaluating a law student's drafted document.

Document Type: {document_type}
Document Content:
---
{document_text[:5000]}
---

Evaluate this document on THREE criteria and provide scores (0-100):

1. CLARITY (Structure, Language, Readability):
   - Is the document well-structured with clear sections?
   - Is the language professional and precise?
   - Is it easy to understand?

2. RELEVANCE (Legal Accuracy, Appropriate Content):
   - Is the legal content accurate and appropriate?
   - Does it address the intended purpose?
   - Are legal terms used correctly?

3. ETHICS (Ethical Compliance, Professional Standards):
   - Does it maintain professional ethics?
   - Are there any ethical concerns?
   - Does it follow legal professional standards?

Respond in JSON format:
{{
    "clarity_score": <0-100>,
    "relevance_score": <0-100>,
    "ethics_score": <0-100>,
    "feedback": {{
        "clarity": "<2-3 sentences on clarity>",
        "relevance": "<2-3 sentences on relevance>",
        "ethics": "<2-3 sentences on ethics>"
    }},
    "suggestions": ["<improvement 1>", "<improvement 2>", "<improvement 3>"],
    "strengths": ["<strength 1>", "<strength 2>"],
    "overall_comment": "<1-2 sentences overall assessment>"
}}

Be constructive and educational in your feedback."""

    try:
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
        
        result = eval(response.text)
        
        # Calculate total score and grade
        total_score = round((result["clarity_score"] + result["relevance_score"] + result["ethics_score"]) / 3)
        result["total_score"] = total_score
        
        # Assign grade
        if total_score >= 90:
            result["grade"] = "A+"
        elif total_score >= 85:
            result["grade"] = "A"
        elif total_score >= 80:
            result["grade"] = "A-"
        elif total_score >= 75:
            result["grade"] = "B+"
        elif total_score >= 70:
            result["grade"] = "B"
        elif total_score >= 65:
            result["grade"] = "B-"
        elif total_score >= 60:
            result["grade"] = "C+"
        elif total_score >= 55:
            result["grade"] = "C"
        else:
            result["grade"] = "Needs Improvement"
        
        return result
        
    except Exception as e:
        print(f"Error evaluating document: {e}")
        return {
            "clarity_score": 50,
            "relevance_score": 50,
            "ethics_score": 50,
            "total_score": 50,
            "grade": "C",
            "feedback": {
                "clarity": "Unable to evaluate at this time.",
                "relevance": "Please try again.",
                "ethics": "Evaluation service temporarily unavailable."
            },
            "suggestions": ["Ensure your document is well-formatted and try again."],
            "strengths": ["Document submitted successfully."],
            "overall_comment": "Technical error occurred during evaluation."
        }
