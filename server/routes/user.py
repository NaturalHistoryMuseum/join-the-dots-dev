import msal
import requests
from flask import Blueprint, Config, jsonify, request
from flask import current_app as app
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import delete, insert, literal, select, update

from server.database import db
from server.models import AssignedUnits, Roles, Users

user_bp = Blueprint('user', __name__)
GRAPH_API_URL = 'https://graph.microsoft.com/v1.0'


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
    """
    Get a user by their Azure ID.
    """
    data = db.session.execute(select(Users).where(Users.azure_id == str(azure_id)))
    if data == []:
        return jsonify({'message': 'no user found'})
    return jsonify(data)


@user_bp.route('/add-user', methods=['POST'])
@jwt_required()
def add_user():
    """
    Add a new user.
    """
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
        db.session.execute(
            insert(Users).values(
                azure_id=azure_id,
                display_name=display_name,
                email=email,
                division_id=division_id,
                role_id=role_id,
            )
        )
        return jsonify({'message': 'User added successfully', 'success': True}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/edit-user-role', methods=['POST'])
@jwt_required()
def edit_user_role():
    """
    Amend a users role.
    """
    data = request.get_json()
    role_id = data.get('role_id')
    user_id = data.get('user_id')

    if not role_id:
        return jsonify({'error': 'Role is required'}), 400

    # Update role and commit changes
    try:
        db.session.execute(
            update(Users).where(Users.user_id == user_id).values(role_id=role_id)
        )
        db.session.commit()
        return jsonify({'message': 'Role successfully changed', 'success': True}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/assign-units', methods=['POST'])
@jwt_required()
def edit_assign_units():
    """
    Assign units to a user.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    units = data.get('units')

    if not units:
        return jsonify({'error': 'Units are required'}), 400
    if not user_id:
        return jsonify({'error': 'User is required'}), 400

    # Delete current user units
    try:
        db.session.execute(
            delete(AssignedUnits).where(AssignedUnits.user_id == user_id)
        )
        db.session.flush()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    # Update current user units
    try:
        for unit in units:
            db.session.execute(
                insert(AssignedUnits).values(user_id=user_id, collection_unit_id=unit)
            )

        db.session.commit()
        return jsonify({'message': 'Units successfully assigned'}), 201

    except Exception as e:
        return jsonify({'error': str(e), 'success': True}), 500


@user_bp.route('/all-roles', methods=['GET'])
@jwt_required()
def get_all_roles():
    """
    Get all roles.
    """
    data = db.session.execute(select(Roles))
    return jsonify(data)


@user_bp.route('/update-division', methods=['POST'])
@jwt_required()
def edit_user_division():
    """
    Update a users assigned division.
    """
    data = request.get_json()
    division_id = data.get('division_id')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    db.session.execute(
        update(Users).where(Users.user_id == user_id).values(division_id=division_id)
    )
    db.session.commit()
    return jsonify({'success': True}), 201


@user_bp.route('/upgrade-viewer', methods=['POST'])
@jwt_required()
def upgrade_viewer():
    """
    Increase a users role from viewer to editor and assign a division.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    division_id = data.get('division_id')

    db.session.execute(
        update(Users)
        .where(Users.user_id == user_id)
        .values(division_id=division_id, role_id=2)
    )
    db.session.commit()
    return jsonify({'success': True}), 201


@user_bp.route('/check-user-by-email', methods=['POST'])
@jwt_required()
def check_user_by_email():
    """
    Check if a user exists by their email address.
    """
    data = request.get_json()
    email = data.get('email')
    try:
        data = db.session.execute(select(Users).where(Users.email == email))
        return jsonify({'data': data, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/all-viewers', methods=['GET'])
@jwt_required()
def all_viewers():
    """
    Get all users with the viewer role.
    """
    query = (
        select(*Users.__table__.columns, Roles.role, literal(False).label('selected'))
        .join(Roles, Roles.role_id == Users.role_id)
        .where(Users.role_id == 1)
    )

    data = db.session.execute(query).mappings().all()
    return jsonify([dict(row) for row in data])


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

    if not token_response or 'access_token' not in token_response:
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
