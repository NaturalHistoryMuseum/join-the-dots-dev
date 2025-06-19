import os

import jwt
import msal
from flask import Blueprint, jsonify, request, session

# Test user database
from server.database import get_db_connection

auth_bp = Blueprint('auth', __name__)


# Database connection
def fetch_data(query, params=None):
    """
    Helper function to execute a database query.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


# Azure AD Config
# FOR K8S
# CLIENT_ID = os.environ.get("AZURE_CLIENT_ID")
# CLIENT_SECRET = os.environ.get("AZURE_CLIENT_SECRET")
# TENANT_ID = os.environ.get("AZURE_TENANT_ID")
# REDIRECT_URI = os.environ.get("AZURE_REDIRECT_URI")
# FOR LOCAL TESTING
CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
CLIENT_SECRET = os.getenv('AZURE_CLIENT_SECRET')
TENANT_ID = os.getenv('AZURE_TENANT_ID')
REDIRECT_URI = os.getenv('AZURE_REDIRECT_URI')

AUTHORITY = f'https://login.microsoftonline.com/{TENANT_ID}'

SCOPES = []

# JWT Secret Key
JWT_SECRET = os.getenv('JWT_SECRET', 'super-secret-key')

# Initialize MSAL
msal_app = msal.ConfidentialClientApplication(
    CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
)


@auth_bp.route('/login')
def login():
    """
    Redirects user to Microsoft Login page.
    """
    auth_url = msal_app.get_authorization_request_url(SCOPES, redirect_uri=REDIRECT_URI)
    return jsonify({'auth_url': auth_url})


@auth_bp.route('/login/azure/authorized')
def auth_redirect():
    """
    Handles Azure AD login redirect.
    """
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No auth code provided'}), 400

    token_response = msal_app.acquire_token_by_authorization_code(
        code, SCOPES, redirect_uri=REDIRECT_URI
    )

    if 'access_token' in token_response:
        user_info = token_response.get('id_token_claims')
        # Get user from db

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            """SELECT u.*, r.role, r.`level`
                      FROM jtd_live.users u
                      LEFT JOIN jtd_live.roles r ON u.role_id = r.role_id
                      WHERE azure_id = %s
                   """,
            (str(user_info['oid']),),
        )
        user = cursor.fetchone()

        if not user:
            # Add user if not present
            cursor.execute(
                'INSERT INTO jtd_live.users (azure_id, name, email, role_id) VALUES (%s, %s, %s, %s)',
                (
                    user_info['oid'],
                    user_info['name'],
                    user_info['preferred_username'],
                    1,
                ),
            )
            connection.commit()
            # fetch user again
            cursor.execute(
                """SELECT u.*, r.role, r.`level`
                      FROM jtd_live.users u
                      LEFT JOIN jtd_live.roles r ON u.role_id = r.role_id
                      WHERE azure_id = %s
                   """,
                (str(user_info['oid']),),
            )
            user = cursor.fetchone()
        # Store user info in session
        session['user'] = user
        session.modified = True
        # Generate JWT token
        jwt_payload = {
            'user_id': user['user_id'],
            'name': user['name'],
            'email': user['email'],
            'role_id': user['role_id'],
            'role': user['role'],
            'division_id': user['division_id'],
            'level': user['level'],
        }
        jwt_token = jwt.encode(jwt_payload, JWT_SECRET, algorithm='HS256')

        session['jwt_token'] = jwt_token  # Store in session for later retrieval

        return jsonify({'message': 'Login successful'}), 200

    return jsonify({'error': 'Authentication failed'}), 401


@auth_bp.route('/auth/status')
def auth_status():
    """
    Check if the user has logged in and return their JWT token.
    """
    # Get JWT token from session or request headers
    token = session.get('jwt_token') or request.headers.get('Authorization')
    # If no token is found, return an error
    if not token:
        return jsonify({'error': 'Not authenticated'}), 401
    # If token is in header remove 'Bearer' prefix
    if token.startswith('Bearer '):
        token = token.split(' ')[1]

    decode_token = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])

    user_id = decode_token.get('user_id')
    # Get current user details
    user_details = fetch_data(
        """SELECT u.*, r.role, r.`level`,
                        (
                            SELECT JSON_ARRAYAGG( au.collection_unit_id )
                            FROM jtd_live.assigned_units au
                            where au.user_id = u.user_id
                        ) AS assigned_units
                      FROM jtd_live.users u
                      LEFT JOIN jtd_live.roles r ON u.role_id = r.role_id
                      WHERE user_id = %s""",
        (user_id,),
    )
    # If no user is found, return an error
    if not user_details:
        return jsonify({'error': 'User not found'}), 404
    # Return token and user details
    return jsonify({'token': token, 'user': user_details[0]}), 200

    # if "jwt_token" in session:
    #     return jsonify({"token": session["jwt_token"], "user": session["user"]}), 200


@auth_bp.route('/logout')
def logout():
    """
    Logs the user out by clearing the session.
    """
    session.clear()
    return jsonify({'message': 'Logged out'})
