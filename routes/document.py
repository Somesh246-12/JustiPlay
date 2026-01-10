# routes/document.py

import os
import re
from flask import Blueprint, render_template, request, redirect, send_file, flash
from services.ai.ocr_client import extract_text
from services.ai.document_analyzer import analyze_document
from services.pdf_exporter import generate_pdf

document_bp = Blueprint("document", __name__, url_prefix="/document")

TMP = "tmp_docs"
os.makedirs(TMP, exist_ok=True)


def highlight_text(text: str, clauses: list) -> str:
    """
    Highlight clause text in the document based on risk levels.
    
    Args:
        text: Full document text
        clauses: List of clause dictionaries with 'text' and 'risk' fields
        
    Returns:
        str: HTML with highlighted text using <mark> tags
    """
    highlighted = text
    
    # Sort clauses by text length (longest first) to avoid partial matches
    sorted_clauses = sorted(clauses, key=lambda c: len(c.get('text', '')), reverse=True)
    
    for clause in sorted_clauses:
        clause_text = clause.get('text', '').strip()
        risk = clause.get('risk', 'Medium')
        
        if not clause_text or len(clause_text) < 10:
            continue
        
        # Map risk to CSS class
        risk_class = f"risk-{risk.lower()}"
        
        # Try exact match first
        if clause_text in highlighted:
            highlighted = highlighted.replace(
                clause_text,
                f'<mark class="{risk_class}">{clause_text}</mark>',
                1  # Replace only first occurrence
            )
        else:
            # Try fuzzy match: normalize whitespace and try again
            normalized_clause = ' '.join(clause_text.split())
            
            # Create a regex pattern that allows flexible whitespace
            pattern = re.escape(normalized_clause)
            pattern = pattern.replace(r'\ ', r'\s+')
            
            match = re.search(pattern, highlighted, re.IGNORECASE)
            if match:
                matched_text = match.group(0)
                highlighted = highlighted.replace(
                    matched_text,
                    f'<mark class="{risk_class}">{matched_text}</mark>',
                    1
                )
    
    return highlighted


@document_bp.route("/upload")
def upload():
    """Render the document upload page."""
    return render_template("citizen/document_analysis.html")


@document_bp.route("/analyze", methods=["POST"])
def analyze():
    """Process uploaded document and display analysis results."""
    from flask import session
    from services.storage_service import upload_document
    from services.firestore_service import create_document, get_user, create_user
    
    file = request.files.get("doc")
    if not file:
        flash("Please select a document to upload.", "error")
        return redirect("/document/upload")

    # Read file content
    content = file.read()
    mime = file.mimetype
    
    if not content:
        flash("Uploaded file is empty.", "error")
        return redirect("/document/upload")

    # Extract text (with smart OCR detection)
    print(f"📤 Processing: {file.filename} ({mime})")
    text = extract_text(content, mime)
    
    if not text or len(text.strip()) < 50:
        flash("Could not extract meaningful text from document.", "error")
        return redirect("/document/upload")

    # Analyze document with Gemini
    result = analyze_document(text)
    
    if "error" in result and not result.get("clauses"):
        flash("Analysis failed. Please try again.", "error")
        return redirect("/document/upload")

    # Highlight clause text in document
    highlighted = highlight_text(text, result.get("clauses", []))

    # Generate PDF report
    doc_id = "doc_" + str(len(os.listdir(TMP)))
    pdf_path = os.path.join(TMP, f"{doc_id}.pdf")
    
    try:
        generate_pdf(result, pdf_path)
    except Exception as e:
        print(f"⚠️ PDF generation failed: {e}")
        # Continue anyway, user can still see web results

    # ========== FIREBASE INTEGRATION ==========
    try:
        # Get user ID from session (or create a default one)
        user_id = session.get("user_id", "default_user")
        username = session.get("full_name", "Anonymous User")
        
        # Ensure user exists in Firestore
        user = get_user(user_id)
        if not user:
            create_user(user_id, username, role="citizen")
        
        # Try to upload to Cloud Storage (optional)
        file_url = None
        try:
            # Reset file pointer for upload
            file.seek(0)
            storage_result = upload_document(file, user_id, file.filename)
            file_url = storage_result['file_url']
            print(f"✅ File uploaded to Cloud Storage")
        except Exception as storage_error:
            print(f"⚠️ Cloud Storage upload failed: {storage_error}")
            # Use local PDF path as fallback
            file_url = f"/document/download_pdf/{doc_id}"
        
        # Extract risk data
        risk_flags = [clause.get('text', '')[:100] for clause in result.get('clauses', []) if clause.get('risk') in ['High', 'Critical']]
        risk_score = result.get('overall_risk_score', 50)
        
        # Save to Firestore (even if storage failed)
        firestore_doc_id = create_document(
            owner_id=user_id,
            title=file.filename or "Untitled Document",
            summary=result.get('summary', 'No summary available')[:500],
            risk_flags=risk_flags[:5],  # Limit to 5 flags
            risk_score=risk_score,
            file_url=file_url
        )
        
        print(f"✅ Document saved to Firestore: {firestore_doc_id}")
        
        # Store Firestore doc ID in session for later retrieval
        session['last_doc_id'] = firestore_doc_id
        
    except Exception as e:
        print(f"⚠️ Firebase save failed: {e}")
        # Continue anyway - analysis still works without Firebase

    return render_template(
        "citizen/analysis_result.html",
        result=result,
        highlighted_text=highlighted,
        doc_id=doc_id
    )


@document_bp.route("/download_pdf/<doc_id>")
def download(doc_id):
    """Download the generated PDF report."""
    # Sanitize doc_id to prevent directory traversal
    doc_id = re.sub(r'[^a-zA-Z0-9_-]', '', doc_id)
    pdf_path = os.path.join(TMP, f"{doc_id}.pdf")
    
    if not os.path.exists(pdf_path):
        flash("PDF report not found.", "error")
        return redirect("/document/upload")
    
    return send_file(pdf_path, as_attachment=True, download_name=f"justiplay_report_{doc_id}.pdf")
