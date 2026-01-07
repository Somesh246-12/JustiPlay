from flask import Blueprint, render_template, request, redirect, session, url_for

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")

        if role not in ["student", "citizen"]:
            return "Invalid role", 400

        session["role"] = role

        if role == "student":
            return redirect(url_for("student.dashboard"))
        else:
            return redirect(url_for("citizen.dashboard"))

    return render_template("auth/login.html")
