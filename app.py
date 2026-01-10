from flask import Flask
from config import Config
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Verify critical environment variables are loaded
if not os.getenv("GCP_PROJECT_ID"):
    print("⚠️ WARNING: GCP_PROJECT_ID not found in environment variables!")
if not os.getenv("GEMINI_API_KEY"):
    print("⚠️ WARNING: GEMINI_API_KEY not found in environment variables!")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = app.config["SECRET_KEY"]

    # ===============================
    # Blueprint Registration
    # ===============================
    from routes.auth import auth_bp
    from routes.student import student_bp
    from routes.citizen import citizen_bp
    from routes.document import document_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp, url_prefix="/student")
    app.register_blueprint(citizen_bp, url_prefix="/citizen")
    app.register_blueprint(document_bp, url_prefix="/document")

    @app.route("/")
    def index():
        from flask import redirect, url_for
        return redirect(url_for("auth.login"))

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
