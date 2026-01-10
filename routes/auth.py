from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from services.firestore_service import create_user, get_user
import hashlib

auth_bp = Blueprint("auth", __name__)

def hash_password(password):
    """Simple password hashing for demo purposes"""
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        username = request.form.get("username")
        password = request.form.get("password")

        if not role or not username or not password:
            flash("All fields are required", "error")
            return redirect(url_for("auth.login"))

        # Hash the password
        password_hash = hash_password(password)
        
        # Generate user ID
        user_id = f"{role}_{username}".lower().replace(" ", "_")
        
        try:
            # Check if user exists in Firestore
            user = get_user(user_id)
            
            if user:
                # User exists - verify password
                if user.get('password_hash') == password_hash:
                    # Successful login
                    session["user_id"] = user_id
                    session["username"] = username
                    session["full_name"] = user.get('name', username)
                    session["role"] = role
                    
                    # Initialize role-specific data
                    if role == "student":
                        session["student_xp"] = user.get('xp', 0)
                        session["role_title"] = user.get('role_title', 'Junior Clerk')
                        return redirect(url_for("student.dashboard"))
                    else:  # citizen
                        return redirect(url_for("citizen.dashboard"))
                else:
                    flash("Invalid password", "error")
                    return redirect(url_for("auth.login"))
            else:
                flash("User not found. Please sign up first.", "error")
                return redirect(url_for("auth.login"))
                
        except Exception as e:
            print(f"Login error: {e}")
            flash("Login failed. Please try again.", "error")
            return redirect(url_for("auth.login"))

    return render_template("auth/login.html")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    role = request.form.get("role")
    username = request.form.get("username")
    full_name = request.form.get("full_name")
    password = request.form.get("password")

    if not all([role, username, full_name, password]):
        flash("All fields are required", "error")
        return redirect(url_for("auth.login"))

    # Validate password length
    if len(password) < 6:
        flash("Password must be at least 6 characters", "error")
        return redirect(url_for("auth.login"))

    # Generate user ID
    user_id = f"{role}_{username}".lower().replace(" ", "_")
    
    try:
        # Check if user already exists
        existing_user = get_user(user_id)
        if existing_user:
            flash("Username already taken. Please choose another.", "error")
            return redirect(url_for("auth.login"))
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user in Firestore
        create_user(
            user_id=user_id,
            name=full_name,
            role=role,
            level=1
        )
        
        # Also store password hash (update user)
        from services.firestore_service import update_user
        update_user(user_id, password_hash=password_hash, xp=0, role_title='Junior Clerk' if role == 'student' else 'Citizen')
        
        # Auto-login after signup
        session["user_id"] = user_id
        session["username"] = username
        session["full_name"] = full_name
        session["role"] = role
        
        # Initialize role-specific data
        if role == "student":
            session["student_xp"] = 0
            session["role_title"] = "Junior Clerk"
            flash(f"Welcome to JustiPlay, {full_name}!", "success")
            return redirect(url_for("student.dashboard"))
        else:  # citizen
            flash(f"Welcome to JustiPlay, {full_name}!", "success")
            return redirect(url_for("citizen.dashboard"))
            
    except Exception as e:
        print(f"Signup error: {e}")
        flash("Signup failed. Please try again.", "error")
        return redirect(url_for("auth.login"))


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out successfully.", "info")
    return redirect(url_for("auth.login"))
