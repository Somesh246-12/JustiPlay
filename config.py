import os

class Config:
    # ===============================
    # Flask Core Config
    # ===============================
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

    # ===============================
    # Google / Gemini Configuration
    # ===============================
    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get(
        "GOOGLE_APPLICATION_CREDENTIALS",
        "credentials.json"  # local dev fallback
    )

    GEMINI_MODEL_NAME = os.environ.get(
        "GEMINI_MODEL_NAME",
        "models/gemini-1.5-flash"
    )

    # ===============================
    # App Mode
    # ===============================
    ENV = os.environ.get("FLASK_ENV", "development")
    DEBUG = ENV == "development"
