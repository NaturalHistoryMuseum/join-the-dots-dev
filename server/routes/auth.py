from flask import Blueprint, redirect, request, session, jsonify
from flask import current_app as app
import msal
import os
import jwt
# Test user database
from server.database import get_test_db_connection

auth_bp = Blueprint("auth", __name__)

# Database connection
def fetch_data(query, params=None):
    """Helper function to execute a database query."""
    connection = get_test_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# Azure AD Config
CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
TENANT_ID = os.environ.get("AZURE_TENANT_ID")

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
REDIRECT_URI = os.environ.get("AZURE_REDIRECT_URI")
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
    auth_url = msal_app.get_authorization_request_url(SCOPES, redirect_uri=REDIRECT_URI)
    return jsonify({"auth_url": auth_url})

# @auth_bp.route("/login/azure/authorized")
# def auth_redirect():
#     """Handles Azure AD login redirect"""
#     code = request.args.get("code")
#     if not code:
#         return jsonify({"error": "No auth code provided"}), 400

#     token_response = msal_app.acquire_token_by_authorization_code(code, SCOPES, redirect_uri=REDIRECT_URI)

#     if "access_token" in token_response:
#         user_info = token_response.get("id_token_claims")
#         # Save user info in session
#         session["user"] = user_info
#         # Generate JWT Token
#         jwt_payload = {
#             "user_name": user_info['name'],
#             "email": user_info['preferred_username'],
#             "user_id": user_info['oid']
#             } 
#         jwt_token = jwt.encode(jwt_payload, JWT_SECRET, algorithm="HS256")
#         # Redirect to home page with user info in token
#         frontend_url = f"http://localhost:5173/?token={jwt_token}"
#         return redirect(frontend_url)
    
#     return jsonify({"error": "Authentication failed"}), 401

@auth_bp.route("/login/azure/authorized")
def auth_redirect():
    """Handles Azure AD login redirect"""
    code = request.args.get("code")
    if not code:
        return jsonify({"error": "No auth code provided"}), 400

    token_response = msal_app.acquire_token_by_authorization_code(code, SCOPES, redirect_uri=REDIRECT_URI)

    if "access_token" in token_response:
        user_info = token_response.get("id_token_claims")
        print('before fetch')
        # Get user from db

        connection = get_test_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""SELECT *
                      FROM jtd_test.users
                      WHERE azure_id = %s
                   """, (str(user_info["oid"]),))
        user = cursor.fetchone()
        print('after fetch')
        print('first get : ',user)

        
        if not user:
            print('inserting')
            # Add user if not present
            cursor.execute("INSERT INTO jtd_test.users (azure_id, name, email, role) VALUES (%s, %s, %s, %s)", (user_info["oid"], user_info["name"], user_info["preferred_username"], 'user'))
            connection.commit()
            # fetch user again
            cursor.execute("""SELECT *
                      FROM jtd_test.users
                      WHERE azure_id = %s
                   """, (str(user_info["oid"]),))
            user = cursor.fetchone()
            print('user after second get', user)
        print(user)
        # Store user info in session
        session["user"] = user
        # Generate JWT token
        jwt_payload = {
            "user_id": user["user_id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
        jwt_token = jwt.encode(jwt_payload, JWT_SECRET, algorithm="HS256")

        session["jwt_token"] = jwt_token  # Store in session for later retrieval

        return jsonify({"message": "Login successful"}), 200

    return jsonify({"error": "Authentication failed"}), 401

@auth_bp.route("/auth/status")
def auth_status():
    """Check if the user has logged in and return their JWT token"""
    # Get JWT token from session or request headers
    token = session.get("jwt_token") or request.headers.get("Authorization")
    # If no token is found, return an error
    if not token:
        return jsonify({"error": "Not authenticated"}), 401
    # If token is in header remove 'Bearer' prefix
    if token.startswith("Bearer "):
        token = token.split(" ")[1]
    
    decode_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])

    user_id = decode_token.get("user_id")
    # Get current user details
    user_details = fetch_data("SELECT * FROM jtd_test.users WHERE user_id = %s", (user_id,))
    # If no user is found, return an error
    if not user_details:
        return jsonify({"error": "User not found"}), 404
    # Return token and user details
    return jsonify({"token": token, "user": user_details[0]}), 200

    # if "jwt_token" in session:
    #     return jsonify({"token": session["jwt_token"], "user": session["user"]}), 200


@auth_bp.route("/logout")
def logout():
    """Logs the user out by clearing the session"""
    session.clear()
    return jsonify({"message": "Logged out"})
