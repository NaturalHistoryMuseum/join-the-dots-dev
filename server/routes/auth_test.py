from flask import Blueprint, current_app, jsonify, make_response, session
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    set_access_cookies,
    set_refresh_cookies,
)

auth_test_bp = Blueprint('auth_test', __name__)


@auth_test_bp.route('/__test/login', methods=['POST'])
def test_login():
    if not current_app.config.get('TEST_AUTH_ENABLED'):
        return jsonify({'error': 'Not available'}), 404

    # Minimal user payload matching your real claims
    user = {
        'user_id': 1,
        'display_name': 'Test User',
        'email': 'jointhedots@nhm.ac.uk',
        'role_id': 4,
        'role': 'admin',
        'division_id': None,
        'level': 4,
    }

    jwt_token = create_access_token(
        identity=str(user['user_id']),
        additional_claims={
            'display_name': user['display_name'],
            'email': user['email'],
            'role_id': user['role_id'],
            'role': user['role'],
            'division_id': user['division_id'],
            'level': user['level'],
        },
    )

    # response = jsonify({"msg": "ok"})
    # set_access_cookies(response, jwt_token)

    # Create refresh token
    refresh_token = create_refresh_token(identity=str(user['user_id']))
    # Store in session for later retrieval
    session['jwt_token'] = jwt_token

    response = make_response(jsonify({'message': 'Login successful'}))
    # Set jwt token as access token in cookies
    set_access_cookies(response, jwt_token)
    set_refresh_cookies(response, refresh_token)

    return response
