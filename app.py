from flask import Flask
from config import Config

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
    def health_check():
        return {"status": "JustiPlay MVP running"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
