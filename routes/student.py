from flask import Blueprint, render_template, session, redirect, url_for, request
from services.ai.client_ai import get_client_reply
from services.ai.evaluator_ai import evaluate_student_question



# -------------------------------------------------
# Blueprint MUST be defined FIRST
# -------------------------------------------------
student_bp = Blueprint("student", __name__, url_prefix="/student")


# -------------------------------------------------
# TEMPORARY: Student Level Logic (MVP)
# -------------------------------------------------
def get_student_level():
    return 2


# -------------------------------------------------
# Student Dashboard
# -------------------------------------------------
@student_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))

    level = get_student_level()
    return render_template(
        "student/dashboard.html",
        level=level
    )


# -------------------------------------------------
# AI Mock Client (TEXT-BASED MVP)
# -------------------------------------------------
@student_bp.route("/mock-client", methods=["GET", "POST"])
def mock_client():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))

    # Clear session if requested
    if request.args.get("clear") == "true":
        session["mock_chat"] = []
        session.modified = True
        return redirect(url_for("student.mock_client"))

    # Initialize conversation memory
    if "mock_chat" not in session:
        session["mock_chat"] = []

    if request.method == "POST":
        question = request.form.get("question", "").strip()

        if question:
            reply = get_client_reply(
                conversation_history=session["mock_chat"],
                student_question=question
            )

            evaluation = evaluate_student_question(question)

            session["mock_chat"].append({
                "question": question,
                "reply": reply,
                "evaluation": evaluation
            })

            session.modified = True

    return render_template("student/mock_client.html", chat=session["mock_chat"])




# -------------------------------------------------
# Document Practice (Placeholder)
# -------------------------------------------------
@student_bp.route("/document-practice")
def document_practice():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))

    return render_template("student/document_practice.html")


# -------------------------------------------------
# Feedback & Evaluation (Placeholder)
# -------------------------------------------------
@student_bp.route("/feedback")
def feedback():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))

    return render_template("student/feedback.html")
