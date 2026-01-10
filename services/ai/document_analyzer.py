# services/ai/document_analyzer.py

import os
import json
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Configure model with JSON response mode
model = genai.GenerativeModel(
    "gemini-2.0-flash-exp",
    generation_config={
        "response_mime_type": "application/json",
        "temperature": 0.3,
    }
)

PROMPT = """
You are a legal document analysis assistant for educational purposes only.

Analyze the provided legal document and return a JSON object with the following structure:

{
  "document_type": "string (e.g., 'Rental Agreement', 'Employment Contract', 'NDA')",
  "summary": "string (5-6 sentences summarizing the document's purpose and key terms)",
  "overall_risk": "string (must be exactly 'Low', 'Medium', or 'High')",
  "risk_drivers": ["array of 2-4 strings explaining main risk factors"],
  "clauses": [
    {
      "title": "string (short clause name, e.g., 'Termination Clause')",
      "text": "string (exact text excerpt from document, 1-3 sentences)",
      "risk": "string (must be exactly 'Low', 'Medium', or 'High')",
      "suggestion": "string (educational suggestion, 1-2 sentences, NOT legal advice)"
    }
  ]
}

IMPORTANT RULES:
1. Risk levels must be EXACTLY: "Low", "Medium", or "High" (case-sensitive)
2. Extract 3-6 clauses from the document
3. Suggestions should be educational (e.g., "Consider reviewing this clause with a legal professional")
4. DO NOT provide specific legal advice or recommendations
5. DO NOT suggest specific actions like "sign" or "don't sign"
6. Focus on awareness and understanding, not legal guidance
7. Clause text should be actual excerpts from the document

Example suggestion formats:
✓ "This clause may limit your rights. Consider seeking professional legal review."
✓ "Understanding termination conditions is important for both parties."
✗ "You should not sign this contract." (too directive)
✗ "Negotiate for better terms." (legal advice)
"""


def analyze_document(text: str) -> dict:
    """
    Analyze a legal document using Gemini AI.
    
    Args:
        text: Extracted document text
        
    Returns:
        dict: Structured analysis with document_type, summary, risks, and clauses
    """
    # Limit text to avoid token limits (approximately 10k chars = ~2500 tokens)
    truncated_text = text[:10000]
    
    if len(text) > 10000:
        print(f"⚠️ Document truncated from {len(text)} to 10000 characters for analysis")
    
    try:
        # Generate analysis with JSON mode
        response = model.generate_content(
            PROMPT + "\n\nDOCUMENT TEXT:\n" + truncated_text
        )
        
        # Parse JSON response
        result = json.loads(response.text)
        
        # Validate required fields
        required_fields = ["document_type", "summary", "overall_risk", "risk_drivers", "clauses"]
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Missing required field: {field}")
        
        # Validate risk levels
        valid_risks = {"Low", "Medium", "High"}
        if result["overall_risk"] not in valid_risks:
            result["overall_risk"] = "Medium"  # Default fallback
        
        for clause in result.get("clauses", []):
            if clause.get("risk") not in valid_risks:
                clause["risk"] = "Medium"  # Default fallback
        
        print(f"✅ Analysis complete: {result['document_type']} - {result['overall_risk']} risk")
        return result
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error: {e}")
        return {
            "error": "Failed to parse AI response",
            "document_type": "Unknown",
            "summary": "Unable to analyze document. Please try again.",
            "overall_risk": "Medium",
            "risk_drivers": ["Analysis failed"],
            "clauses": []
        }
    
    except Exception as e:
        print(f"❌ Analysis error: {e}")
        return {
            "error": str(e),
            "document_type": "Unknown",
            "summary": "An error occurred during analysis. Please try again.",
            "overall_risk": "Medium",
            "risk_drivers": ["Analysis error occurred"],
            "clauses": []
        }
