from flask import Blueprint, jsonify, session, redirect
from flask_dance.contrib.azure import azure
from ..services.auth_service import fetch_user_info

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/callback")
def auth_callback():
    if not azure.authorized:
        return jsonify({"error": "User not authorized"}), 401

    user_info = fetch_user_info()
    if not user_info:
        return jsonify({"error": "Failed to fetch user info"}), 500

    session["user"] = {
        "email": user_info.get("userPrincipalName"),
        "name": user_info.get("displayName"),
    }
    return redirect("http://localhost:5173/")

@auth_bp.route("/logout")
def logout():
    session.clear()
    return {"message": "Logged out"}

@auth_bp.route("/check")
def check_authorization():
    return "User is authorized" if azure.authorized else "User is not authorized", 401
