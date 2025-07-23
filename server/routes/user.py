from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required

from server.utils import execute_query, fetch_data

user_bp = Blueprint('user', __name__)


@user_bp.route('/user/<azure_id>', methods=['GET'])
@jwt_required()
def get_user(azure_id):
    data = fetch_data(
        """SELECT *
            FROM jtd_live.users
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
    name = data.get('name')
    email = data.get('email')

    if not azure_id or not name or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        execute_query(
            """
            INSERT INTO jtd_live.users (azure_id, name, email)
            VALUES (%s, %s, %s)
        """,
            (azure_id, name, email),
        )

        return jsonify({'message': 'User added successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/edit-user-role', methods=['PUT'])
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
            UPDATE jtd_live.users u
            SET u.role_id = %s
            WHERE u.user_id = %s
        """,
            (
                role_id,
                user_id,
            ),
        )

        return jsonify({'message': 'Role successfully changed'}), 201

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
            DELETE FROM jtd_live.assigned_units
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
                INSERT INTO jtd_live.assigned_units (user_id, collection_unit_id)
                VALUES (%s, %s)
            """,
                (user_id, unit),
            )

        return jsonify({'message': 'Units successfully assigned'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/all-roles', methods=['GET'])
@jwt_required()
def get_all_roles():
    data = fetch_data("""SELECT r.*
                   FROM jtd_live.roles r
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
        """UPDATE jtd_live.users u
            SET u.division_id = %s
            WHERE u.user_id = %s
                   """,
        (division_id, user_id),
    )
    return jsonify(data)
