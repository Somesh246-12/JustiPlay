import google.generativeai as genai
import os
import json

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_text_response(prompt: str) -> dict:
    """
    Generate a text response using Gemini API.
    
    Args:
        prompt: The prompt to send to Gemini
        
    Returns:
        A dictionary containing the parsed JSON response from Gemini
    """
    try:
        # Use gemini-pro model (compatible with current library version)
        model = genai.GenerativeModel("gemini-pro")
        
        # Generate content
        response = model.generate_content(prompt)
        
        # Try to parse as JSON
        try:
            result = json.loads(response.text)
            return result
        except json.JSONDecodeError:
            # If not valid JSON, return the text wrapped in a dict
            return {
                "summary": response.text,
                "risk_level": "Medium",
                "suggestions": []
            }
            
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {
            "summary": "Error analyzing document",
            "risk_level": "Unknown",
            "suggestions": ["Please try again"]
        }
