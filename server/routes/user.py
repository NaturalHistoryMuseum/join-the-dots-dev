import msal
import requests
from flask import Blueprint, jsonify, request
from flask import current_app as app
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.config import Config
from server.utils import execute_query, fetch_data

user_bp = Blueprint('user', __name__)


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


@user_bp.route('/user/<azure_id>', methods=['GET'])
@jwt_required()
def get_user(azure_id):
    data = fetch_data(
        """SELECT *
            FROM {database_name}.users
            WHERE azure_id = %s
                   """
        % str(azure_id)
    )
    if data == []:
        return jsonify({'message': 'no user found'})
    return jsonify(data)


@user_bp.route('/add-user', methods=['POST'])
@jwt_required()
def add_user():
    data = request.get_json()

    # Extract user details from request JSON
    azure_id = data.get('azure_id')
    display_name = data.get('display_name')
    email = data.get('email')
    division_id = data.get('division_id')
    role_id = data.get('role_id')

    if not azure_id or not display_name or not email or not division_id or not role_id:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        execute_query(
            """
            INSERT INTO {database_name}.users (azure_id, display_name, email, division_id, role_id)
            VALUES (%s, %s, %s, %s, %s)
        """,
            (azure_id, display_name, email, division_id, role_id),
        )

        return jsonify({'message': 'User added successfully', 'success': True}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/edit-user-role', methods=['POST'])
@jwt_required()
def edit_user_role():
    data = request.get_json()
    role_id = data.get('role_id')
    user_id = data.get('user_id')

    if not role_id:
        return jsonify({'error': 'Role is required'}), 400

    # Update role and commit changes
    try:
        execute_query(
            """
            UPDATE {database_name}.users u
            SET u.role_id = %s
            WHERE u.user_id = %s
        """,
            (
                role_id,
                user_id,
            ),
        )

        return jsonify({'message': 'Role successfully changed', 'success': True}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/assign-units', methods=['POST'])
@jwt_required()
def edit_assign_units():
    data = request.get_json()
    user_id = data.get('user_id')
    units = data.get('units')

    if not units:
        return jsonify({'error': 'Units are required'}), 400
    if not user_id:
        return jsonify({'error': 'User is required'}), 400

    # Delete current user units
    try:
        execute_query(
            """
            DELETE FROM {database_name}.assigned_units
            WHERE user_id = %s
        """,
            (user_id,),
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Update current user units
    try:
        for unit in units:
            execute_query(
                """
                INSERT INTO {database_name}.assigned_units (user_id, collection_unit_id)
                VALUES (%s, %s)
            """,
                (user_id, unit),
            )

        return jsonify({'message': 'Units successfully assigned'}), 201

    except Exception as e:
        return jsonify({'error': str(e), 'success': True}), 500


@user_bp.route('/all-roles', methods=['GET'])
@jwt_required()
def get_all_roles():
    data = fetch_data("""SELECT r.*
                   FROM {database_name}.roles r
                   """)
    return jsonify(data)


@user_bp.route('/update-division', methods=['POST'])
@jwt_required()
def edit_user_division():
    data = request.get_json()
    division_id = data.get('division_id')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    data = execute_query(
        """UPDATE {database_name}.users u
            SET u.division_id = %s
            WHERE u.user_id = %s
                   """,
        (division_id, user_id),
    )
    return jsonify({'data': data, 'success': True}), 201


@user_bp.route('/upgrade-viewer', methods=['POST'])
@jwt_required()
def upgrade_viewer():
    data = request.get_json()
    user_id = data.get('user_id')
    division_id = data.get('division_id')

    data = execute_query(
        """UPDATE {database_name}.users u
            SET u.role_id = 2, u.division_id = %s
            WHERE u.user_id = %s
                   """,
        (
            division_id,
            user_id,
        ),
    )
    return jsonify({'data': data, 'success': True}), 201


@user_bp.route('/check-user-by-email', methods=['POST'])
@jwt_required()
def check_user_by_email():
    data = request.get_json()
    email = data.get('email')
    try:
        data = fetch_data(
            """SELECT *
                FROM {database_name}.users u
                WHERE u.email = %s
                    """,
            (email,),
        )
        return jsonify({'data': data, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/all-viewers', methods=['GET'])
@jwt_required()
def all_viewers():
    data = fetch_data(
        """SELECT u.*, r.role, FALSE AS selected
            FROM {database_name}.users u
            JOIN {database_name}.roles r ON u.role_id = r.role_id
            WHERE u.role_id = 1
            """
    )
    return jsonify(data)


GRAPH_API_URL = 'https://graph.microsoft.com/v1.0'


@user_bp.route('/azure/user', methods=['POST'])
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
        return jsonify({'success': True, 'user': response.json()}), 200
    else:
        return jsonify({'success': False})
