from flask import Blueprint, render_template, session, redirect, url_for, request

citizen_bp = Blueprint("citizen", __name__, url_prefix="/citizen")

# -------------------------------------------------
# Citizen Dashboard (Learner Discovery)
# -------------------------------------------------
@citizen_bp.route("/dashboard")
def dashboard():
    if session.get("role") != "citizen":
        return redirect(url_for("auth.login"))

    learners = [
        {
            "id": 1,
            "name": "Sarah Jenkins",
            "domain": "Tenancy Law",
            "level": "Advanced",
            "achievements": 6
        },
        {
            "id": 2,
            "name": "Alex Mercer",
            "domain": "Contract Law",
            "level": "Intermediate",
            "achievements": 4
        }
    ]

    return render_template(
        "citizen/dashboard.html",
        learners=learners
    )


# -------------------------------------------------
# Learner Profile
# -------------------------------------------------
@citizen_bp.route("/learner/<int:learner_id>")
def learner_profile(learner_id):
    if session.get("role") != "citizen":
        return redirect(url_for("auth.login"))

    learner = {
        "id": learner_id,
        "name": "Sarah Jenkins",
        "about": "Final-year law student focused on tenancy and consumer law.",
        "expertise": ["Tenancy Law", "Consumer Rights", "Contracts"],
        "achievements": [
            "Clear Communicator",
            "Document Analysis Pro",
            "Ethics Aware"
        ],
        "endorsements": {
            "Tenancy Law": 3,
            "Consumer Rights": 2
        }
    }

    return render_template(
        "citizen/learner_profile.html",
        learner=learner
    )


# -------------------------------------------------
# Document Analysis
# -------------------------------------------------
@citizen_bp.route("/document-analysis")
def document_analysis():
    if session.get("role") != "citizen":
        return redirect(url_for("auth.login"))

    return render_template("citizen/document_analysis.html")


# -------------------------------------------------
# Educational Endorsement Submission (Mock)
# -------------------------------------------------
@citizen_bp.route("/endorse/<int:learner_id>", methods=["POST"])
def endorse_learner(learner_id):
    if session.get("role") != "citizen":
        return redirect(url_for("auth.login"))

    domain = request.form.get("domain")
    comment = request.form.get("comment")

    # For MVP: just log it (no DB yet)
    print("ENDORSEMENT RECEIVED")
    print("Learner ID:", learner_id)
    print("Domain:", domain)
    print("Comment:", comment)

    # In future:
    # - Save to DB
    # - Update endorsement count
    # - Attach to learner profile

    return redirect(url_for("citizen.learner_profile", learner_id=learner_id))

