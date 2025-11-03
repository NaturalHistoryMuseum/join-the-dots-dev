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
