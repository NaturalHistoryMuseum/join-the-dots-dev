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


def execute_query(query, params=None):
    """
    Helper function to execute a database query with commit.
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Format the query with the database name
    formatted_query = query.format(database_name=database_name)
    cursor.execute(formatted_query, params or ())
    connection.commit()
    cursor.close()
    connection.close()
