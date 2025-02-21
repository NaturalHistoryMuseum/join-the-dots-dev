from flask import Blueprint, jsonify, request
from server.database import get_test_db_connection

user_bp = Blueprint('user', __name__)

def execute_query(query, params=None):
    """Helper function to execute a database query with commit."""
    connection = get_test_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    connection.commit()
    cursor.close()
    connection.close()

def fetch_data(query, params=None):
    """Helper function to execute a database query."""
    connection = get_test_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

# @user_bp.route('/all-users', methods=['GET'])
# def get_all_users():
#     data = fetch_data("""SELECT *
#                       FROM jtd_test.users
#                    """)
#     return jsonify(data)


@user_bp.route('/user/<azure_id>', methods=['GET'])
def get_user(azure_id):
    data = fetch_data("""SELECT *
                      FROM jtd_test.users
                      WHERE azure_id = %s
                   """ % str(azure_id))
    if data == []:
        print("No user found")
    return jsonify(data)

@user_bp.route('/add-user', methods=['POST'])
def add_user():
    data = request.get_json()

    # Extract user details from request JSON
    azure_id = data.get('azure_id')
    name = data.get('name')
    email = data.get('email')

    if not azure_id or not name or not email:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        execute_query("""
            INSERT INTO jtd_test.users (azure_id, name, email)
            VALUES (%s, %s, %s)
        """, (azure_id, name, email))

        return jsonify({"message": "User added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@user_bp.route('/edit-role', methods=['PUT'])
def edit_role():
    data = request.get_json()
    role = data.get('role')
    user_id = data.get('user_id')

    if not role:
        return jsonify({'error': 'Role is required'}), 400

    # Update role and commit changes
    try:
        execute_query("""
            UPDATE jtd_test.users u
            SET u.role = %s
            WHERE u.user_id = %s
        """, (role, user_id,))

        return jsonify({"message": "Role successfully changed"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@user_bp.route('/add-sections', methods=['POST'])
def add_user_sections():
    data = request.get_json()
    sections = data.get('sections')
    user_id = data.get('user_id')

    if not sections:
        return jsonify({'error': 'Sections are required'}), 400

    # Delete current user sections
    try:
        execute_query("""
            DELETE FROM jtd_test.user_sections
            WHERE user_id = %s
        """, (user_id,))
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    # Create insert query
    values = ''
    for section in sections:
        values += '(' + str(user_id) + ',' + str(section) + '),'
    values = values[:-1]
    # Insert new sections
    try:
        execute_query("""
            INSERT INTO jtd_test.user_sections (user_id, section_id)
            VALUES %s
        """ % values)
        return jsonify({"message": "Sections successfully added"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@user_bp.route('/get-sections/<user_id>', methods=['GET'])
def get_user_sections(user_id):
    # data = request.get_json()
    # user_id = data.get('user_id')

    data = fetch_data("""SELECT us.section_id
                      FROM jtd_test.user_sections us
                      WHERE us.user_id = %s
                   """ % str(user_id))
    return jsonify(data)