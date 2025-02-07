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

@user_bp.route('/all-users', methods=['GET'])
def get_all_users():
    print("getall users")
    data = fetch_data("""SELECT *
                      FROM jtd_test.users
                   """)
    return jsonify(data)


@user_bp.route('/user/<azure_id>', methods=['GET'])
def get_user(azure_id):
    print("getall users")
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
