# from flask import Blueprint, jsonify

# from server.database import get_db_connection
# from server.powerbi_utils import microsoft_jwt_required  # your custom decorator

# powerbi_bp = Blueprint('powerbi', __name__)


# @powerbi_bp.route('/data', methods=['GET'])
# # @microsoft_jwt_required(scope="read.data")
# @microsoft_jwt_required(role='PowerBI.Read')
# def get_powerbi_data():
#     """
#     Endpoint for Power BI to fetch reporting data.

#     Returns JSON rows from MySQL.
#     """
#     conn = get_db_connection()

#     cursor = conn.cursor(dictionary=True)
#     cursor.execute('SELECT * FROM jtd_live.collection_unit LIMIT 1000;')
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return jsonify(rows)


# from flask import Flask, request, jsonify, Blueprint
# import jwt
# import datetime
# from server.database import get_db_connection

# app = Flask(__name__)
# SECRET_KEY = "supersecretkey"  # Use a secure environment variable in production
# powerbi_bp = Blueprint("powerbi", __name__)

# # Example endpoint
# @powerbi_bp.route("/data", methods=["GET"])
# def get_data():
#     token = request.headers.get("Authorization")
#     if not token or not token.startswith("Bearer "):
#         return jsonify({"error": "Missing token"}), 401

#     token = token.replace("Bearer ", "")
#     try:
#         jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
#     except jwt.ExpiredSignatureError:
#         return jsonify({"error": "Token expired"}), 403
#     except jwt.InvalidTokenError:
#         return jsonify({"error": "Invalid token"}), 403

#     conn = get_db_connection()

#     cursor = conn.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM jtd_live.collection_unit LIMIT 1000;")
#     rows = cursor.fetchall()
#     cursor.close()
#     conn.close()
#     return jsonify(rows)

# # Generate a test token (for Power BI)
# @powerbi_bp.route("/token")
# def generate_token():
#     payload = {"exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)}
#     token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
#     return jsonify({"token": token})


from flask import Blueprint, abort, jsonify, request

from server.config import Config
from server.database import get_db_connection
from server.utils import database_name

powerbi_bp = Blueprint('powerbi', __name__)


def require_api_key(f):
    from functools import wraps

    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check for API key in headers
        provided_key = request.headers.get('x-api-key')
        if provided_key and provided_key == Config.EXPECTED_API_KEY:
            return f(*args, **kwargs)
        # Abort if unauthorised
        abort(401)

    return decorated_function


def auto_fetch(tables):
    results = {}
    query_template = f'SELECT * FROM {database_name}.{{view}}'

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    for table in tables:
        cursor.execute(query_template.format(view=table))
        rows = cursor.fetchall()
        results[table] = rows
    cursor.close()
    conn.close()
    return jsonify(results)


@powerbi_bp.route('/units_view')
@require_api_key
def return_units_view():
    views = ['vw_collection_units_denormalised']
    return auto_fetch(views)


@powerbi_bp.route('/ranks_view')
@require_api_key
def return_ranks_view():
    views = ['vw_criteria_rank_current']
    return auto_fetch(views)


@powerbi_bp.route('/metrics_view')
@require_api_key
def return_metrics_view():
    views = ['vw_metrics_current']
    return auto_fetch(views)


@powerbi_bp.route('/average_view')
@require_api_key
def return_average_view():
    views = ['vw_weighted_average_review']
    return auto_fetch(views)


@powerbi_bp.route('/average_history_view')
@require_api_key
def return_average_history_view():
    views = ['vw_weighted_average_history']
    return auto_fetch(views)


@powerbi_bp.route('/department_tables')
@require_api_key
def return_dept_tables():
    tables = ['department', 'division', 'section']
    return auto_fetch(tables)


@powerbi_bp.route('/site_tables')
@require_api_key
def return_site_tables():
    tables = ['site', 'building', 'floor', 'storage_room', 'storage_container']
    return auto_fetch(tables)


@powerbi_bp.route('/category_tables')
@require_api_key
def return_category_tables():
    tables = ['category', 'criterion', 'rank']
    return auto_fetch(tables)


@powerbi_bp.route('/collection_unit_data')
@require_api_key
def return_collection_unit_data():
    tables = [
        'collection_unit',
        'curatorial_unit_definition',
        'preservation_method',
        'item_type',
    ]
    return auto_fetch(tables)


@powerbi_bp.route('/score_data')
@require_api_key
def return_score_data():
    tables = ['unit_assessment_criterion', 'unit_assessment_rank']
    return auto_fetch(tables)
