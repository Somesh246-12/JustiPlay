from flask import Blueprint, jsonify

document_bp = Blueprint("document", __name__)

@document_bp.route("/health")
def health():
    return jsonify({"document": "service ready"})
