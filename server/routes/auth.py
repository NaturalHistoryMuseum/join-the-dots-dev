# import jwt
import secrets

import msal
from flask import Blueprint, jsonify, make_response, request, session
from flask import current_app as app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

from server.config import Config
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


AUTHORITY = f'https://login.microsoftonline.com/{Config.TENANT_ID}'

SCOPES = []

# Initialize MSAL
msal_app = msal.ConfidentialClientApplication(
    Config.CLIENT_ID, authority=AUTHORITY, client_credential={Config.CLIENT_SECRET}
)


@auth_bp.route('/login')
def login():
    """
    Redirects user to Microsoft Login page.
    """
    auth_url = msal_app.get_authorization_request_url(
        SCOPES, redirect_uri=app.config.get('REDIRECT_URI')
    )
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
        code, scopes=SCOPES, redirect_uri=app.config.get('REDIRECT_URI')
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

        # Create access token with user identity and extra claims
        jwt_token = create_access_token(
            identity=str(user['user_id']),
            additional_claims={
                'name': user['name'],
                'email': user['email'],
                'role_id': user['role_id'],
                'role': user['role'],
                'division_id': user['division_id'],
                'level': user['level'],
            },
        )
        # Store in session for later retrieval
        session['jwt_token'] = jwt_token

        # Generate CSRF token
        csrf_token = secrets.token_urlsafe(32)

        response = make_response(jsonify({'message': 'Login successful'}))
        # Set jwt token as access token in cookies
        response.set_cookie(
            'access_token', jwt_token, httponly=True, secure=True, samesite='Lax'
        )
        # Set csrf token in cookies
        response.set_cookie(
            'csrf_token', csrf_token, httponly=False, secure=False, samesite='Lax'
        )
        return response

    return jsonify({'error': 'Authentication failed'}), 401


@auth_bp.route('/auth/status')
@jwt_required()
def auth_status():
    """
    Check if the user has logged in and return their JWT token.
    """
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

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
            WHERE user_id = %s;""",
        (user_id,),
    )
    # If no user is found, return an error
    if not user_details:
        return jsonify({'error': 'User not found'}), 404
    # Return token and user details
    return jsonify({'user': user_details[0]}), 200


@auth_bp.route('/logout')
def logout():
    """
    Logs the user out by clearing the session.
    """
    session.clear()
    response = jsonify({'msg': 'Logout successful'})
    # Remove the access tokens from the cookies
    response.delete_cookie('access_token')
    return response
