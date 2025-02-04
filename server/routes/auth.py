from flask import Blueprint, redirect, request, session, jsonify
from flask import current_app as app
import msal
import os
import jwt

auth_bp = Blueprint("auth", __name__)

CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
TENANT_ID = os.getenv("AZURE_TENANT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = os.getenv("AZURE_REDIRECT_URI")
SCOPES = []

# JWT Secret Key
JWT_SECRET = os.getenv("JWT_SECRET", "super-secret-key")

# Initialize MSAL
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)

@auth_bp.route("/login")
def login():
    """Redirects user to Microsoft Login page"""
    print('login route')
    auth_url = msal_app.get_authorization_request_url(SCOPES, redirect_uri=REDIRECT_URI)
    print('/login did the thing')
    print(auth_url)
    return jsonify({"auth_url": auth_url})

@auth_bp.route("/login/azure/authorized")
def auth_redirect():
    """Handles Azure AD login redirect"""
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No auth code provided"}), 400

    token_response = msal_app.acquire_token_by_authorization_code(code, SCOPES, redirect_uri=REDIRECT_URI)

    if "access_token" in token_response:
        user_info = token_response.get("id_token_claims")
        # Save user info in session
        session["user"] = user_info
        print(user_info)
        # Generate JWT Token
        jwt_payload = {
            "user_name": user_info['name'],
            "email": user_info['preferred_username'],
            "user_id": user_info['oid']
            } 
        jwt_token = jwt.encode(jwt_payload, JWT_SECRET, algorithm="HS256")

        # Redirect to home page with user info in token
        frontend_url = f"http://localhost:5173/?token={jwt_token}"
        return redirect(frontend_url)
    
    return jsonify({"error": "Authentication failed"}), 401

@auth_bp.route("/logout")
def logout():
    """Logs the user out by clearing the session"""
    session.clear()
    return jsonify({"message": "Logged out"})
