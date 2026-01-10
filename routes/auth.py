from flask import Blueprint, render_template, request, redirect, session, url_for

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")

        if not role:
            return "Role is required", 400

        # MOCK AUTHENTICATION (For MVP)
        # In a real app, we would verify against a database
        if username and password:
             session["user"] = username
        else:
             session["user"] = "Guest " + role.capitalize()

        session["role"] = role

        if role == "student":
            # Set name from login form
            if username:
                session["full_name"] = username
                session["username"] = username.lower().replace(" ", "_")
            
            # Initialize Student stats if not exists
            if "student_xp" not in session:
                session["user_id"] = "USR" + (username.upper()[:3] if username else "ALE") + "01"
                if not username:
                    session["username"] = "alex_mercer"
                    session["full_name"] = "Alex Mercer"
                session["student_xp"] = 0
                session["role_title"] = "Junior Clerk"
            
            return redirect(url_for("student.dashboard"))
        elif role == "citizen":
            # Initialize Citizen stats if not exists
            if "citizen_data" not in session:
                session["username"] = username if username else "citizen_user"
                session["full_name"] = username if username else "Anonymous Citizen"
                session["citizen_data"] = {
                    "location": "Not Set",
                    "interests": [],
                    "history": []
                }
            return redirect(url_for("citizen.dashboard"))
        else:
            return "Invalid role", 400

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
