from datetime import datetime, timedelta, timezone

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
)

from server.database import get_db_connection

database_name = 'jtd_live'


def fetch_data(query, params=None):
    """
    Helper function to execute a database query.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Format the query with the database name
    formatted_query = query.format(database_name=database_name)
    cursor.execute(formatted_query, params or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def execute_query(query, params=None, return_lastrowid=False):
    """
    Helper function to execute a database query with commit.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    # Get user details
    user_details = get_user_by_id(user_id)
    person_id = user_details['person_id'] if user_details else None
    cursor.execute('SET @current_person_id = %s', (person_id,))
    # Format the query with the database name
    formatted_query = query.format(database_name=database_name)
    cursor.execute(formatted_query, params or ())
    connection.commit()
    # If last row ID is requested, get it
    last_id = cursor.lastrowid if return_lastrowid else None
    # Close the cursor and connection
    cursor.close()
    connection.close()
    # Return the last row ID if requested
    if return_lastrowid:
        return last_id


def refreshJWTToken(response):
    """
    Refresh the JWT token in the response if it is about to expire.
    """
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
        # if the token is about to expire in 10 mins, create a new one
        if target_timestamp > exp_timestamp:
            user_id = get_jwt_identity()
            # Generate a new access token
            new_access_token = create_access_token(identity=user_id)
            set_access_cookies(response, new_access_token)
            return response
        # Return if token is not about to expire
        else:
            return response

    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


def get_user_by_id(user_id):
    user_details = fetch_data(
        """SELECT u.*, r.role, r.`level`, p.*, COALESCE(CONCAT(p.first_name, ' ', p.last_name), u.display_name) AS name,
            (
                SELECT JSON_ARRAYAGG( au.collection_unit_id )
                FROM {database_name}.assigned_units au
                JOIN {database_name}.collection_unit cu ON au.collection_unit_id = cu.collection_unit_id
                WHERE au.user_id = u.user_id AND cu.unit_active = 'yes'
            ) AS assigned_units,
            (
                SELECT JSON_ARRAYAGG(
                    cu.collection_unit_id
                )
                FROM {database_name}.collection_unit cu
                WHERE cu.responsible_curator_id = u.user_id AND cu.unit_active = 'yes'
            ) AS responsible_units
            FROM {database_name}.users u
            LEFT JOIN {database_name}.roles r ON u.role_id = r.role_id
            LEFT JOIN {database_name}.person p ON u.person_id = p.person_id
            WHERE user_id = %s;""",
        (user_id,),
    )
    return user_details[0] if user_details else None
