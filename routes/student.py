from flask import Blueprint, render_template, session, redirect, url_for, request
from services.ai.client_ai import get_client_reply
from services.ai.evaluator_ai import evaluate_student_question



# -------------------------------------------------
# Blueprint MUST be defined FIRST
# -------------------------------------------------
student_bp = Blueprint("student", __name__, url_prefix="/student")


# -------------------------------------------------
# Student Level Logic (Single Source of Truth)
# -------------------------------------------------
LEVEL_CONFIG = [
    {"level": 1, "name": "Junior Clerk", "min_xp": 0, "next_xp": 100},
    {"level": 2, "name": "Legal Researcher", "min_xp": 100, "next_xp": 300},
    {"level": 3, "name": "Junior Associate", "min_xp": 300, "next_xp": 700},
    {"level": 4, "name": "Senior Partner", "min_xp": 700, "next_xp": 1500},
    {"level": 5, "name": "Legal Mastermind", "min_xp": 1500, "next_xp": None},
]

def get_student_stats(xp):
    current_level = LEVEL_CONFIG[0]
    for config in LEVEL_CONFIG:
        if xp >= config["min_xp"]:
            current_level = config
        else:
            break
    
    if current_level["next_xp"]:
        needed_for_next = current_level["next_xp"] - current_level["min_xp"]
        earned_in_level = xp - current_level["min_xp"]
        percent = int((earned_in_level / needed_for_next) * 100)
        to_next = current_level["next_xp"] - xp
    else:
        percent = 100
        to_next = 0

    return {
        "level": current_level["level"],
        "level_name": current_level["name"],
        "xp": xp,
        "next_level_xp": current_level["next_xp"],
        "progress_percent": percent,
        "to_next": to_next
    }

def get_leaderboard(current_user_xp, current_username):
    # Mock users
    others = [
        {"username": "legal_eagle", "xp": 1250, "level": 4},
        {"username": "judge_dredd", "xp": 900, "level": 4},
        {"username": "pro_bono", "xp": 450, "level": 3},
        {"username": "case_master", "xp": 200, "level": 2},
    ]
    
    # Add current user
    stats = get_student_stats(current_user_xp)
    me = {"username": current_username, "xp": current_user_xp, "level": stats["level"], "is_me": True}
    others.append(me)
    
    # Sort by XP
    sorted_board = sorted(others, key=lambda x: x["xp"], reverse=True)
    
    # Add Rank
    for i, user in enumerate(sorted_board):
        user["rank"] = i + 1
        
    return sorted_board

# -------------------------------------------------
# Student Dashboard
# -------------------------------------------------
@student_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))

    xp = session.get("student_xp", 0)
    username = session.get("username", "alex_mercer")
    
    stats = get_student_stats(xp)
    leaderboard = get_leaderboard(xp, username)
    history = session.get("student_history", [])[:5]
    
    return render_template(
        "student/dashboard.html",
        stats=stats,
        user_context={
            "full_name": session.get("full_name", "Alex Mercer"),
            "username": username,
            "user_id": session.get("user_id", "USR001")
        },
        leaderboard=leaderboard,
        history=history
    )

@student_bp.route("/profile/update", methods=["POST"])
def update_profile():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))
    
    new_name = request.form.get("full_name")
    new_username = request.form.get("username")
    
    if new_name:
        session["full_name"] = new_name
    if new_username:
        # Simple slugify for username
        session["username"] = new_username.lower().replace(" ", "_")
        
    session.modified = True
    return redirect(url_for("student.profile"))

@student_bp.route("/profile")
def profile():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))

    xp = session.get("student_xp", 0)
    username = session.get("username", "alex_mercer")
    
    stats = get_student_stats(xp)
    leaderboard = get_leaderboard(xp, username)
    my_rank = next((u["rank"] for u in leaderboard if u.get("is_me")), 5)
    
    # Mock skill grades
    skills = [
        {"name": "Ethics", "grade": "A-", "color": "text-primary"},
        {"name": "Logic", "grade": "B+", "color": "text-blue-400"},
        {"name": "Research", "grade": "A", "color": "text-purple-400"},
        {"name": "Negotiation", "grade": "B", "color": "text-orange-400"},
    ]
    
    return render_template(
        "student/profile.html",
        stats=stats,
        user_context={
            "full_name": session.get("full_name", "Alex Mercer"),
            "username": username,
            "user_id": session.get("user_id", "USR001")
        },
        my_rank=my_rank,
        skills=skills,
        history=session.get("student_history", []),
        LEVEL_CONFIG=LEVEL_CONFIG
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

            # Append to chat history
            session["mock_chat"].append({
                "question": question,
                "reply": reply,
                "evaluation": evaluation
            })

            # Initialize history if not exists
            if "student_history" not in session:
                session["student_history"] = []

            # Calculate XP based on evaluation
            earned_score = evaluation.get("total_score", 50)
            xp_reward = int(earned_score * 0.5) # Max 50 XP per prompt for now
            
            # Save to history
            session["student_history"].insert(0, {
                "case_name": "AI Consultation: " + question[:20] + "...",
                "type": "Mock Client",
                "date": "Today",
                "score": earned_score,
                "xp_earned": xp_reward
            })

            # Award XP
            session["student_xp"] = session.get("student_xp", 0) + xp_reward
            session.modified = True

    return render_template(
        "student/mock_client.html", 
        chat=session["mock_chat"],
        user_context={
            "full_name": session.get("full_name", "Alex Mercer"),
            "username": session.get("username", "alex_mercer"),
            "user_id": session.get("user_id", "USR001")
        },
        stats=get_student_stats(session.get("student_xp", 0))
    )




# -------------------------------------------------
# Document Drafting (NEW)
# -------------------------------------------------
@student_bp.route("/document-drafting", methods=["GET", "POST"])
def document_drafting():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        from services.ai.document_evaluator import evaluate_document
        
        document_text = request.form.get("document_text", "").strip()
        document_type = request.form.get("document_type", "Legal Document")
        
        if document_text:
            # Evaluate the document
            evaluation = evaluate_document(document_text, document_type)
            
            # Calculate XP reward (max 100 XP per document)
            xp_reward = evaluation.get("total_score", 50)
            
            # Initialize history if not exists
            if "student_history" not in session:
                session["student_history"] = []
            
            # Save to history
            session["student_history"].insert(0, {
                "case_name": f"Document: {document_type}",
                "type": "Document Drafting",
                "date": "Today",
                "score": evaluation.get("total_score", 50),
                "xp_earned": xp_reward
            })
            
            # Award XP
            session["student_xp"] = session.get("student_xp", 0) + xp_reward
            session.modified = True
            
            # Render result page
            return render_template(
                "student/document_result.html",
                evaluation=evaluation,
                document_type=document_type,
                document_text=document_text,
                xp_earned=xp_reward,
                user_context={
                    "full_name": session.get("full_name", "Alex Mercer"),
                    "username": session.get("username", "alex_mercer"),
                    "user_id": session.get("user_id", "USR001")
                },
                stats=get_student_stats(session.get("student_xp", 0))
            )
    
    # GET request - show drafting form
    return render_template(
        "student/document_drafting.html",
        user_context={
            "full_name": session.get("full_name", "Alex Mercer"),
            "username": session.get("username", "alex_mercer"),
            "user_id": session.get("user_id", "USR001")
        },
        stats=get_student_stats(session.get("student_xp", 0)),
        history=session.get("student_history", [])[:5]
    )


# -------------------------------------------------
# Overall Student Evaluation (NEW)
# -------------------------------------------------
@student_bp.route("/evaluation")
def evaluation():
    if session.get("role") != "student":
        return redirect(url_for("auth.login"))
    
    from services.ai.student_evaluator import evaluate_student_progress
    
    xp = session.get("student_xp", 0)
    username = session.get("username", "alex_mercer")
    history = session.get("student_history", [])
    
    stats = get_student_stats(xp)
    
    # Get AI evaluation of overall progress
    progress_eval = evaluate_student_progress(history, xp, stats["level_name"])
    
    return render_template(
        "student/evaluation.html",
        stats=stats,
        evaluation=progress_eval,
        user_context={
            "full_name": session.get("full_name", "Alex Mercer"),
            "username": username,
            "user_id": session.get("user_id", "USR001")
        },
        history=history[:10]
    )

