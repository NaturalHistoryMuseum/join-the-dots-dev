import secrets

import msal
import requests
from flask import Blueprint, jsonify, make_response, request, session
from flask import current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
)
from sqlalchemy import insert, select, update

from server.config import Config
from server.database import db
from server.models import Person, Users
from server.utils import get_user_by_id

auth_bp = Blueprint('auth', __name__)

SCOPES = []


def get_msal_app():
    """
    Lazily create the MSAL app only when Azure auth is actually used.
    """
    if app.config.get('TEST_AUTH_ENABLED'):
        # Don't use Azure in CI mode
        raise RuntimeError('MSAL should not be used in CI mode')

    authority = f'https://login.microsoftonline.com/{Config.TENANT_ID}'

    return msal.ConfidentialClientApplication(
        Config.CLIENT_ID,
        authority=authority,
        client_credential=Config.CLIENT_SECRET,
    )


@auth_bp.route('/login')
def login():
    """
    Redirects user to Microsoft Login page.
    """
    msal_app = get_msal_app()
    auth_url = msal_app.get_authorization_request_url(
        SCOPES, redirect_uri=app.config.get('REDIRECT_URI')
    )
    return jsonify({'auth_url': auth_url})


@auth_bp.route('/login/azure/authorized')
def auth_redirect():
    """
    Handles Azure AD login redirect.
    """
    msal_app = get_msal_app()
    code = request.args.get('code')
    if not code:
        return jsonify({'error': 'No auth code provided'}), 400

    token_response = msal_app.acquire_token_by_authorization_code(
        code, scopes=SCOPES, redirect_uri=app.config.get('REDIRECT_URI')
    )

    if 'access_token' in token_response:
        user_info = token_response.get('id_token_claims')
        # Get user from db
        user = db.session.execute(
            select(Users).where(Users.azure_id == str(user_info['oid']))
        ).scalar()

        if not user:
            # Add user if not present
            db.session.execute(
                insert(Users).values(
                    azure_id=user_info['oid'],
                    email=user_info['preferred_username'],
                    display_name=user_info['name'],
                    role_id=1,
                )
            )
            db.session.commit()
            db.session.expire_all()
            # fetch user again
            user = db.session.execute(
                select(Users).where(Users.azure_id == str(user_info['oid']))
            ).scalar()
        else:
            # Check if the user has a person_id
            if user.roles.role_id > 1 and not user.person_id:
                # Add a new person record
                insert_person_to_existing_user(
                    user.user_id,
                    user_info['name'].split(' ')[0],
                    user_info['name'].split(' ', 1)[1],
                )
            # Check if name and email are up to date
            if user.display_name != user_info['name']:
                db.session.execute(
                    update(Users)
                    .where(Users.user_id == user.user_id)
                    .values(display_name=user_info['name'])
                )
                db.session.commit()
            if user.email != user_info['preferred_username']:
                db.session.execute(
                    update(Users)
                    .where(Users.user_id == user.user_id)
                    .values(email=user_info['preferred_username'])
                )
                db.session.commit()
        # Store user info in session
        user_data = {
            'user_id': user.user_id,
            'display_name': user.display_name,
            'email': user.email,
            'role_id': user.role_id,
            'role': user.roles.role,
            'division_id': user.division_id,
            'level': user.roles.level,
        }
        session['user'] = user_data
        session.modified = True
        # Generate JWT token

        # Create access token with user identity and extra claims
        jwt_token = create_access_token(
            identity=str(user.user_id),
            additional_claims=user_data,
        )
        # Create refresh token
        refresh_token = create_refresh_token(identity=str(user.user_id))
        # Store in session for later retrieval
        session['jwt_token'] = jwt_token

        # Generate CSRF token
        csrf_access_token = secrets.token_urlsafe(32)
        response = make_response(jsonify({'message': 'Login successful'}))
        # Set jwt token as access token in cookies
        set_access_cookies(response, jwt_token)
        set_refresh_cookies(response, refresh_token)

        return response

    return jsonify({'error': 'Authentication failed'}), 401


@auth_bp.route('/status')
@jwt_required()
def auth_status():
    """
    Check if the user has logged in and return their user details.
    """
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    # Get current user details
    user_details = get_user_by_id(user_id)
    # If no user is found, return an error
    if not user_details:
        return jsonify({'error': 'User not found'}), 404
    # Return token and user details
    return jsonify({'user': user_details}), 200


@auth_bp.route('/logout')
def logout():
    """
    Logs the user out by clearing the session.
    """
    session.clear()
    response = jsonify({'msg': 'Logout successful'})
    # Remove the access tokens from the cookies
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    response.delete_cookie('csrf_access_token')
    return response


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    response = jsonify({'msg': 'Token refreshed'})
    response.set_cookie(
        'access_token', new_access_token, httponly=True, secure=True, samesite='Lax'
    )
    return response


def insert_person_to_existing_user(user_id, first_name, last_name, job_title=None):
    """
    Insert a new person into the database.
    """
    result = db.session.execute(
        insert(Person)
        .values(first_name=first_name, last_name=last_name, job_title=job_title)
        .returning(Person.person_id)
    )
    new_person_id = result.scalar()

    db.session.execute(
        insert(Users).where(Users.user_id == user_id).values(person_id=new_person_id)
    )
    db.session.commit()
    return new_person_id


GRAPH_API_URL = 'https://graph.microsoft.com/v1.0'


@auth_bp.route('/azure/user', methods=['POST'])
@jwt_required()  # Require login
def get_user_by_email():
    """
    Look up a user in Azure AD by email address.
    """
    msal_app = get_msal_app()
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({'error': 'Email query parameter is required'}), 400

    # Get an access token for Microsoft Graph
    token_response = msal_app.acquire_token_for_client(
        scopes=['https://graph.microsoft.com/.default']
    )

    if 'access_token' not in token_response:
        return jsonify(
            {'error': 'Could not acquire token', 'details': token_response}
        ), 401

    access_token = token_response['access_token']

    # Call Microsoft Graph
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    url = f'https://graph.microsoft.com/v1.0/users/{email}'
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify(
            {
                'error': 'Failed to fetch user',
                'status_code': response.status_code,
                'details': response.json(),
            }
        ), response.status_code
