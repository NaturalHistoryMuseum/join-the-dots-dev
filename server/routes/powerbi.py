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


@powerbi_bp.route('/data/<table>')
@require_api_key
def return_data(table):
    allowed_tables = [
        'unit_assessment_criterion',
        'unit_assessment_rank',
        'collection_unit_metric',
        'collection_unit_metric_definition',
        'collection_unit',
        'curatorial_unit_definition',
        'preservation_method',
        'item_type',
        'bibliographic_level',
        'taxon',
        'category',
        'criterion',
        'rank',
        'site',
        'building',
        'floor',
        'storage_room',
        'storage_container',
        'department',
        'division',
        'section',
        'vw_weighted_average_history',
        'vw_weighted_average_review',
        'vw_metrics_current',
        'vw_criteria_rank_current',
        'vw_collection_units_denormalised',
        'vw_all_current_scores_no_comments',
    ]
    # Check if the table is allowed
    if table not in allowed_tables:
        return jsonify({'error': 'Table is not allowed'}), 400
    if table == 'collection_unit':
        # Special case for collection_unit to exclude sensitive fields
        query_template = f"""SELECT cu.*, COALESCE(CONCAT(p.first_name, ' ', p.last_name), u.display_name) AS responsible_curator
        FROM {database_name}.collection_unit cu
        LEFT JOIN {database_name}.users u ON u.user_id = cu.responsible_curator_id
        LEFT JOIN {database_name}.person p ON p.person_id = u.person_id"""
    else:
        # Fetch the data
        query_template = f'SELECT * FROM {database_name}.{{table}}'

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query_template.format(table=table))
    data = cursor.fetchall()
    cursor.close()
    conn.close()

    # Return the data as JSON
    return jsonify(data)
