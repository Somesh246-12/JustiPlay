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
        },
        {
            "id": 3,
            "name": "Priya Sharma",
            "domain": "Consumer Rights",
            "level": "Advanced",
            "achievements": 8
        },
        {
            "id": 4,
            "name": "James Chen",
            "domain": "Employment Law",
            "level": "Intermediate",
            "achievements": 5
        },
        {
            "id": 5,
            "name": "Maya Patel",
            "domain": "Family Law",
            "level": "Expert",
            "achievements": 10
        },
        {
            "id": 6,
            "name": "David Wilson",
            "domain": "Property Law",
            "level": "Advanced",
            "achievements": 7
        }
    ]

    return render_template(
        "citizen/dashboard.html",
        learners=learners,
        user_context={
            "full_name": session.get("full_name", "Anonymous Citizen"),
            "username": session.get("username", "citizen_user")
        }
    )


# -------------------------------------------------
# Learner Profile
# -------------------------------------------------
@citizen_bp.route("/learner/<int:learner_id>")
def learner_profile(learner_id):
    if session.get("role") != "citizen":
        return redirect(url_for("auth.login"))

    # Mock learner database with comprehensive profiles
    learners_db = {
        1: {
            "id": 1,
            "name": "Sarah Jenkins",
            "domain": "Tenancy Law",
            "level": "Advanced",
            "achievements_count": 6,
            "about": "Final-year law student specializing in tenancy and housing law. Passionate about helping citizens understand their rights as tenants.",
            "expertise": ["Tenancy Law", "Housing Rights", "Landlord Disputes", "Lease Agreements"],
            "badges": [
                {"name": "Clear Communicator", "icon": "communication"},
                {"name": "Document Analysis Pro", "icon": "description"},
                {"name": "Ethics Aware", "icon": "verified_user"},
                {"name": "Quick Responder", "icon": "bolt"},
                {"name": "Helpful Guide", "icon": "support_agent"},
                {"name": "Top Rated", "icon": "star"}
            ],
            "stats": {
                "cases_helped": 24,
                "response_time": "< 2 hours",
                "satisfaction": 98
            },
            "recent_topics": ["Eviction Notice Review", "Security Deposit Dispute", "Lease Termination"]
        },
        2: {
            "id": 2,
            "name": "Alex Mercer",
            "domain": "Contract Law",
            "level": "Intermediate",
            "achievements_count": 4,
            "about": "Third-year law student with focus on contract law and business agreements. Helping citizens understand complex contractual terms.",
            "expertise": ["Contract Law", "Business Agreements", "Terms & Conditions", "Breach of Contract"],
            "badges": [
                {"name": "Contract Expert", "icon": "gavel"},
                {"name": "Detail Oriented", "icon": "search"},
                {"name": "Patient Teacher", "icon": "school"},
                {"name": "Reliable", "icon": "verified"}
            ],
            "stats": {
                "cases_helped": 18,
                "response_time": "< 3 hours",
                "satisfaction": 95
            },
            "recent_topics": ["Employment Contract Review", "Service Agreement Analysis", "NDA Explanation"]
        },
        3: {
            "id": 3,
            "name": "Priya Sharma",
            "domain": "Consumer Rights",
            "level": "Advanced",
            "achievements_count": 8,
            "about": "Experienced law student dedicated to consumer protection and rights advocacy. Expert in product liability and consumer disputes.",
            "expertise": ["Consumer Rights", "Product Liability", "Refund Policies", "Warranty Claims"],
            "badges": [
                {"name": "Consumer Champion", "icon": "shield"},
                {"name": "Problem Solver", "icon": "lightbulb"},
                {"name": "Top Performer", "icon": "emoji_events"},
                {"name": "Trusted Advisor", "icon": "verified_user"},
                {"name": "Quick Thinker", "icon": "psychology"},
                {"name": "Empathetic", "icon": "favorite"},
                {"name": "Detailed", "icon": "fact_check"},
                {"name": "Responsive", "icon": "notifications_active"}
            ],
            "stats": {
                "cases_helped": 32,
                "response_time": "< 1 hour",
                "satisfaction": 99
            },
            "recent_topics": ["Defective Product Claim", "Online Purchase Dispute", "Service Complaint"]
        },
        4: {
            "id": 4,
            "name": "James Chen",
            "domain": "Employment Law",
            "level": "Intermediate",
            "achievements_count": 5,
            "about": "Law student specializing in employment and labor law. Helping workers understand their workplace rights and obligations.",
            "expertise": ["Employment Law", "Workplace Rights", "Termination Issues", "Discrimination"],
            "badges": [
                {"name": "Worker's Advocate", "icon": "work"},
                {"name": "Fair Play", "icon": "balance"},
                {"name": "Knowledgeable", "icon": "menu_book"},
                {"name": "Supportive", "icon": "support"},
                {"name": "Professional", "icon": "business_center"}
            ],
            "stats": {
                "cases_helped": 21,
                "response_time": "< 4 hours",
                "satisfaction": 94
            },
            "recent_topics": ["Wrongful Termination", "Salary Dispute", "Workplace Harassment"]
        },
        5: {
            "id": 5,
            "name": "Maya Patel",
            "domain": "Family Law",
            "level": "Expert",
            "achievements_count": 10,
            "about": "Senior law student with extensive knowledge in family law matters. Compassionate guide for sensitive family legal issues.",
            "expertise": ["Family Law", "Divorce Proceedings", "Child Custody", "Adoption", "Domestic Issues"],
            "badges": [
                {"name": "Compassionate Guide", "icon": "favorite"},
                {"name": "Family Expert", "icon": "family_restroom"},
                {"name": "Trusted Counselor", "icon": "psychology"},
                {"name": "Top Rated", "icon": "star"},
                {"name": "Experienced", "icon": "workspace_premium"},
                {"name": "Sensitive Handler", "icon": "health_and_safety"},
                {"name": "Clear Explainer", "icon": "chat"},
                {"name": "Patient Listener", "icon": "hearing"},
                {"name": "Ethical", "icon": "verified_user"},
                {"name": "Dedicated", "icon": "loyalty"}
            ],
            "stats": {
                "cases_helped": 45,
                "response_time": "< 2 hours",
                "satisfaction": 99
            },
            "recent_topics": ["Custody Agreement", "Divorce Consultation", "Adoption Process"]
        },
        6: {
            "id": 6,
            "name": "David Wilson",
            "domain": "Property Law",
            "level": "Advanced",
            "achievements_count": 7,
            "about": "Law student focused on property and real estate law. Helping citizens navigate property transactions and disputes.",
            "expertise": ["Property Law", "Real Estate", "Property Disputes", "Title Issues", "Boundary Conflicts"],
            "badges": [
                {"name": "Property Pro", "icon": "home"},
                {"name": "Detail Master", "icon": "fact_check"},
                {"name": "Reliable Guide", "icon": "verified"},
                {"name": "Problem Solver", "icon": "build"},
                {"name": "Clear Communicator", "icon": "forum"},
                {"name": "Thorough", "icon": "checklist"},
                {"name": "Knowledgeable", "icon": "school"}
            ],
            "stats": {
                "cases_helped": 28,
                "response_time": "< 3 hours",
                "satisfaction": 96
            },
            "recent_topics": ["Property Boundary Dispute", "Sale Agreement Review", "Title Verification"]
        }
    }

    learner = learners_db.get(learner_id, learners_db[1])

    return render_template(
        "citizen/learner_profile.html",
        learner=learner,
        user_context={
            "full_name": session.get("full_name", "Anonymous Citizen"),
            "username": session.get("username", "citizen_user")
        }
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


# -------------------------------------------------
# Document Library (Firebase Integration)
# -------------------------------------------------
@citizen_bp.route("/library")
def document_library():
    """Display user's document library with filtering and sorting"""
    if session.get("role") != "citizen":
        return redirect(url_for("auth.login"))
    
    from services.firestore_service import get_user_documents
    
    # Get filter parameters
    sort_by = request.args.get('sort', 'newest')
    search_query = request.args.get('search', '').strip()
    risk_filter = request.args.get('risk', None)
    
    # Get user ID
    user_id = session.get("user_id", "default_user")
    
    # Fetch documents from Firestore
    try:
        documents = get_user_documents(
            owner_id=user_id,
            sort_by=sort_by,
            search_query=search_query if search_query else None,
            risk_filter=risk_filter
        )
    except Exception as e:
        print(f"⚠️ Error fetching documents: {e}")
        documents = []
    
    return render_template(
        "citizen/document_library.html",
        documents=documents,
        sort_by=sort_by,
        search_query=search_query,
        risk_filter=risk_filter,
        user_context={
            "full_name": session.get("full_name", "Anonymous Citizen"),
            "username": session.get("username", "citizen_user")
        }
    )


@citizen_bp.route("/document/<doc_id>")
def view_document(doc_id):
    """View individual document analysis"""
    if session.get("role") != "citizen":
        return redirect(url_for("auth.login"))
    
    from services.firestore_service import get_document
    
    try:
        document = get_document(doc_id)
        if not document:
            return "Document not found", 404
        
        # Verify ownership
        user_id = session.get("user_id", "default_user")
        if document.get('ownerId') != user_id:
            return "Unauthorized", 403
        
        return render_template(
            "citizen/view_analysis.html",
            document=document,
            user_context={
                "full_name": session.get("full_name", "Anonymous Citizen"),
                "username": session.get("username", "citizen_user")
            }
        )
    except Exception as e:
        print(f"⚠️ Error fetching document: {e}")
        return "Error loading document", 500
