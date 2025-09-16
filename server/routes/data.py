import json
from collections import defaultdict
from datetime import datetime

from flask import Blueprint, Response, jsonify, request, stream_with_context
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)

from server.database import get_db_connection
from server.routes.queries.data_queries import *
from server.utils import database_name, execute_query, fetch_data, refreshJWTToken

data_bp = Blueprint('data', __name__)


# After a request, refresh the JWT token if it is about to expire
@data_bp.after_request
def refresh_expiring_jwts(response):
    return refreshJWTToken(response)


# Rescore routes
@data_bp.route('/unit-scores/<unitId>', methods=['GET'])
@jwt_required()
def get_unit_scores(unitId):
    data = fetch_data(UNIT_SCORES % int(unitId))
    return jsonify(data)


@data_bp.route('/mark-rescore-open', methods=['POST'])
@jwt_required()
def get_mark_rescore_open():
    data = request.get_json()
    units = data.get('units')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    if not units:
        return jsonify({'error': 'Units are required'}), 400

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # Insert session
        query = f"""
            INSERT INTO {database_name}.rescore_session (user_id, status)
            VALUES (%s, 'in_progress');
        """
        # formatted_query = query.format(database_name=database_name)
        cursor.execute(query, (user_id,))

        # Get ID of last inserted row
        rescore_session_id = cursor.lastrowid

        category_ids = [0, 1, 2, 3, 4]

        # Insert units into session
        for unit in units:
            query = f"""
                INSERT INTO {database_name}.rescore_session_units (rescore_session_id, collection_unit_id)
                VALUES (%s, %s);
            """
            cursor.execute(query, (rescore_session_id, unit))
            # Get ID of last inserted row
            rescore_session_units_id = cursor.lastrowid
            for category_id in category_ids:
                query = f"""
                    INSERT INTO {database_name}.unit_category_draft (rescore_session_units_id, category_id, complete)
                    VALUES (%s, %s, 0);
                """
                cursor.execute(query, (rescore_session_units_id, category_id))

        connection.commit()
        return jsonify({'rescore_session_id': rescore_session_id, 'success': True}), 201

    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@data_bp.route('/rescore-complete', methods=['POST'])
@jwt_required()
def submit_rescore_complete():
    data = request.get_json()
    rescore_session_id = data.get('rescore_session_id')
    if not rescore_session_id:
        return jsonify({'error': 'rescore_session_id is required'}), 400
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        connection.start_transaction()
        # Submit draft comments

        cursor.execute(
            f""" insert into {database_name}.unit_comment (collection_unit_id, unit_comment, date_added)
                select rsu.collection_unit_id , ucd.unit_comment , NOW() as date_added
                from {database_name}.unit_comment_draft ucd
                join {database_name}.rescore_session_units rsu ON ucd.rescore_session_units_id = rsu.rescore_session_units_id
                JOIN {database_name}.rescore_session rs ON rsu.rescore_session_id = rs.rescore_session_id
                where rsu.rescore_session_id = %s AND rs.user_id = %s AND rs.status = 'in_progress';
            """,
            (rescore_session_id, user_id),
        )
        # Remove draft comments
        cursor.execute(
            f""" DELETE ucd
                    FROM {database_name}.unit_comment_draft ucd
                    JOIN {database_name}.rescore_session_units rsu ON ucd.rescore_session_units_id = rsu.rescore_session_units_id
                    JOIN {database_name}.rescore_session rs ON rsu.rescore_session_id = rs.rescore_session_id
                    WHERE rsu.rescore_session_id = %s AND rs.user_id = %s AND rs.status = 'in_progress';
            """,
            (rescore_session_id, user_id),
        )

        # Submit draft metrics

        # Set old metrics that are about to be inserted as not current
        cursor.execute(
            f"""
                UPDATE {database_name}.collection_unit_metric cum
                JOIN (
                    SELECT rsu.collection_unit_id, umd.collection_unit_metric_definition_id
                    FROM {database_name}.unit_metric_draft umd
                    JOIN {database_name}.rescore_session_units rsu
                        ON umd.rescore_session_units_id = rsu.rescore_session_units_id
                    JOIN {database_name}.rescore_session rs
                        ON rsu.rescore_session_id = rs.rescore_session_id
                    WHERE rsu.rescore_session_id = %s
                        AND rs.user_id = %s
                        AND rs.status = 'in_progress'
                ) AS targets
                ON cum.collection_unit_id = targets.collection_unit_id
                AND cum.collection_unit_metric_definition_id = targets.collection_unit_metric_definition_id
                SET cum.current = 'no', date_to = NOW()
                WHERE cum.current = 'yes'
            """,
            (rescore_session_id, user_id),
        )

        # Insert metrics from drafts
        cursor.execute(
            f""" insert into {database_name}.collection_unit_metric (collection_unit_id, collection_unit_metric_definition_id ,metric_value, confidence_level, date_from, `current`)
                select rsu.collection_unit_id, umd.collection_unit_metric_definition_id, umd.metric_value, umd.confidence_level, NOW() as date_from, 'yes' as `current`
                from {database_name}.unit_metric_draft umd
                join {database_name}.rescore_session_units rsu ON umd.rescore_session_units_id = rsu.rescore_session_units_id
                JOIN {database_name}.rescore_session rs ON rsu.rescore_session_id = rs.rescore_session_id
                where rsu.rescore_session_id = %s AND rs.user_id = %s AND rs.status = 'in_progress';
            """,
            (rescore_session_id, user_id),
        )

        # Remove draft metrics
        cursor.execute(
            f""" DELETE umd
                    FROM {database_name}.unit_metric_draft umd
                    JOIN {database_name}.rescore_session_units rsu ON umd.rescore_session_units_id = rsu.rescore_session_units_id
                    JOIN {database_name}.rescore_session rs ON rsu.rescore_session_id = rs.rescore_session_id
                    WHERE rsu.rescore_session_id = %s AND rs.user_id = %s AND rs.status = 'in_progress';
            """,
            (rescore_session_id, user_id),
        )

        # Submit draft ranks
        # Set old ranks that are about to be inserted as not current
        cursor.execute(
            f"""
            UPDATE {database_name}.unit_assessment_criterion uac
            JOIN (
                SELECT rsu.collection_unit_id, urd.criterion_id
                FROM {database_name}.unit_rank_draft urd
                JOIN {database_name}.unit_category_draft ucd
                    ON urd.category_draft_id = ucd.category_draft_id
                JOIN {database_name}.rescore_session_units rsu
                    ON ucd.rescore_session_units_id = rsu.rescore_session_units_id
                JOIN {database_name}.rescore_session rs
                    ON rsu.rescore_session_id = rs.rescore_session_id
                WHERE rsu.rescore_session_id = %s
                    AND rs.user_id = %s
                    AND rs.status = 'in_progress'
            ) AS targets
            ON uac.collection_unit_id = targets.collection_unit_id
            AND uac.criterion_id = targets.criterion_id
            SET uac.current = 'no', date_to = NOW()
            WHERE uac.current = 'yes'
            """,
            (rescore_session_id, user_id),
        )

        # Get draft ranks
        cursor.execute(
            f"""
                SELECT rsu.collection_unit_id, urd.*
                 FROM {database_name}.unit_rank_draft urd
                 JOIN {database_name}.unit_category_draft ucd ON urd.category_draft_id = ucd.category_draft_id
                 JOIN {database_name}.rescore_session_units rsu ON ucd.rescore_session_units_id = rsu.rescore_session_units_id
                 JOIN {database_name}.rescore_session rs ON rsu.rescore_session_id = rs.rescore_session_id
                 WHERE rsu.rescore_session_id = %s AND rs.user_id = %s AND rs.status = 'in_progress';
            """,
            (rescore_session_id, user_id),
        )
        draft_rows = cursor.fetchall()
        # Group rows by collection_unit_id and criterion_id
        grouped_assessment = defaultdict(list)
        for row in draft_rows:
            key = (row['collection_unit_id'], row['criterion_id'])
            grouped_assessment[key].append(row)
        # Insert assessment_criterion rows
        inserted_ids = {}
        for (
            collection_unit_id,
            criterion_id,
        ), group_rows in grouped_assessment.items():
            cursor.execute(
                f"""
                INSERT INTO {database_name}.unit_assessment_criterion (
                    collection_unit_id, criterion_id, assessor_id,
                    date_assessed, date_from, current
                ) VALUES (%s, %s, %s, NOW(), NOW(), 'yes')
            """,
                (collection_unit_id, criterion_id, user_id),
            )
            inserted_id = cursor.lastrowid

            inserted_ids[(collection_unit_id, criterion_id)] = inserted_id

        # Insert all ranks referencing the correct assessment_criterion_id
        for row in draft_rows:
            criterion_key = (row['collection_unit_id'], row['criterion_id'])
            assessment_criterion_id = inserted_ids[criterion_key]
            cursor.execute(
                f"""
                INSERT INTO {database_name}.unit_assessment_rank (
                    unit_assessment_criterion_id, rank_id, percentage, comment
                ) VALUES (%s, %s, %s, %s)
            """,
                (
                    assessment_criterion_id,
                    row['rank_id'],
                    row['percentage'],
                    row['comment'],
                ),
            )
        # Remove draft ranks
        cursor.execute(
            f""" DELETE urd
                    FROM {database_name}.unit_rank_draft urd
                    JOIN {database_name}.unit_category_draft ucd ON ucd.category_draft_id = urd.category_draft_id
                    JOIN {database_name}.rescore_session_units rsu ON ucd.rescore_session_units_id = rsu.rescore_session_units_id
                    JOIN {database_name}.rescore_session rs ON rsu.rescore_session_id = rs.rescore_session_id
                    WHERE rsu.rescore_session_id = %s AND rs.user_id = %s AND rs.status = 'in_progress';
            """,
            (rescore_session_id, user_id),
        )
        # Remove draft categories
        cursor.execute(
            f""" DELETE ucd
                    FROM {database_name}.unit_category_draft ucd
                    JOIN {database_name}.rescore_session_units rsu ON ucd.rescore_session_units_id = rsu.rescore_session_units_id
                    JOIN {database_name}.rescore_session rs ON rsu.rescore_session_id = rs.rescore_session_id
                    WHERE rsu.rescore_session_id = %s AND rs.user_id = %s AND rs.status = 'in_progress';
            """,
            (rescore_session_id, user_id),
        )
        # Close the rescore session
        cursor.execute(
            f"""UPDATE {database_name}.rescore_session
                        SET status = 'complete', completed_at = NOW()
                        WHERE rescore_session_id = %s AND user_id = %s;
                   """,
            (rescore_session_id, user_id),
        )
        connection.commit()

        return jsonify(
            {'message': 'Rescore session marked as complete', 'success': True}
        ), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


@data_bp.route('/open-rescore', methods=['GET'])
@jwt_required()
def get_open_rescore():
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    data = fetch_data(
        """SELECT *
                        FROM {database_name}.rescore_session
                      WHERE status = 'in_progress' AND user_id = %s;
                   """,
        (user_id,),
    )
    return jsonify(data)


@data_bp.route('/rescore-units/<rescore_session_id>', methods=['GET'])
@jwt_required()
def get_rescore_units(rescore_session_id):
    data = fetch_data(RESCORE_UNITS % int(rescore_session_id))
    return jsonify(data)


@data_bp.route('/submit-draft-rank', methods=['POST'])
@jwt_required()
def submit_draft_rank():
    data = request.get_json()
    rescore_session_units_id = data.get('rescore_session_units_id')
    collection_unit_id = data.get('collection_unit_id')
    criterion_id = data.get('criterion_id')
    ranks = data.get('ranks')
    category_draft_id = data.get('category_draft_id')

    if not category_draft_id:
        return jsonify({'error': 'category_draft_id is required'}), 400
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    if not rescore_session_units_id:
        return jsonify({'error': 'rescore_session_units_id is required'}), 400
    if not criterion_id:
        return jsonify({'error': 'criterion_id is required'}), 400
    handle_draft_rank(criterion_id, ranks, category_draft_id)
    return jsonify({'message': 'Draft rank submitted successfully'}), 201


def handle_draft_rank(criterion_id, ranks, category_draft_id):
    try:
        data = fetch_data(
            """
                    select urd.*
                    from {database_name}.unit_rank_draft urd
                    join {database_name}.unit_category_draft ucd ON urd.category_draft_id = ucd.category_draft_id
                    where urd.criterion_id = %s and urd.category_draft_id = %s ;
                   """,
            (criterion_id, category_draft_id),
        )
        # Loop through the ranks and update or insert them
        for sumbit_rank in ranks:
            in_db = False
            rank_id = sumbit_rank['rank_id']
            percentage = sumbit_rank['percentage']
            comment = sumbit_rank['comment']
            # Check if the rank already exists in the database and update it if it does
            for db_rank in data:
                if db_rank['rank_id'] == sumbit_rank['rank_id']:
                    execute_query(
                        """UPDATE {database_name}.unit_rank_draft
                                SET percentage = %s, comment = %s, updated_at = NOW()
                                WHERE category_draft_id = %s AND criterion_id = %s AND rank_id = %s;
                        """,
                        (percentage, comment, category_draft_id, criterion_id, rank_id),
                    )
                    in_db = True

            # If the rank does not exist, insert it
            if not in_db:
                execute_query(
                    """INSERT INTO {database_name}.unit_rank_draft (category_draft_id, criterion_id, rank_id, percentage, comment)
                            VALUES (%s, %s, %s, %s, %s);
                    """,
                    (category_draft_id, criterion_id, rank_id, percentage, comment),
                )
        return jsonify(
            {'message': 'Draft rank submitted successfully', 'success': True}
        ), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/submit-draft-metrics', methods=['POST'])
@jwt_required()
def submit_draft_metrics():
    data = request.get_json()
    rescore_session_units_id = data.get('rescore_session_units_id')
    collection_unit_id = data.get('collection_unit_id')
    metric_json = data.get('metric_json')

    if not rescore_session_units_id:
        return jsonify({'error': 'rescore_session_units_id is required'}), 400
    if not collection_unit_id:
        return jsonify({'error': 'collection_unit_id is required'}), 400
    if not metric_json:
        return jsonify({'error': 'metric_json are required'}), 400

    handle_draft_metrics(rescore_session_units_id, metric_json)
    return jsonify(
        {'message': 'Draft metrics submitted successfully', 'success': True}
    ), 201


def handle_draft_metrics(rescore_session_units_id, metric_json):
    try:
        # Loop through the metrics and update or insert them
        for metric in metric_json:
            collection_unit_metric_definition_id = metric[
                'collection_unit_metric_definition_id'
            ]
            metric_value = metric['metric_value']
            confidence_level = metric['confidence_level']
            if metric_value is not None or confidence_level is not None:
                # Check if the metric already exists in the database and update it if it does
                existing_metric = fetch_data(
                    """
                            SELECT * FROM {database_name}.unit_metric_draft
                            WHERE rescore_session_units_id = %s AND collection_unit_metric_definition_id = %s;
                        """,
                    (rescore_session_units_id, collection_unit_metric_definition_id),
                )

                if existing_metric:
                    execute_query(
                        """UPDATE {database_name}.unit_metric_draft
                                SET metric_value = %s, confidence_level = %s, updated_at = NOW()
                                WHERE rescore_session_units_id = %s AND collection_unit_metric_definition_id = %s;
                        """,
                        (
                            metric_value,
                            confidence_level,
                            rescore_session_units_id,
                            collection_unit_metric_definition_id,
                        ),
                    )
                else:
                    execute_query(
                        """INSERT INTO {database_name}.unit_metric_draft (rescore_session_units_id, collection_unit_metric_definition_id, metric_value, confidence_level)
                                VALUES (%s, %s, %s, %s);
                        """,
                        (
                            rescore_session_units_id,
                            collection_unit_metric_definition_id,
                            metric_value,
                            confidence_level,
                        ),
                    )
        return jsonify({'message': 'Draft metrics submitted successfully'}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/submit-draft-comment', methods=['POST'])
@jwt_required()
def submit_draft_comment():
    data = request.get_json()
    rescore_session_units_id = data.get('rescore_session_units_id')
    unit_comment = data.get('unit_comment')

    if not rescore_session_units_id:
        return jsonify({'error': 'rescore_session_units_id is required'}), 400
    if not unit_comment:
        return jsonify({'error': 'unit_comment is required'}), 400

    handle_draft_comment(rescore_session_units_id, unit_comment)
    return jsonify(
        {'message': 'Draft comment submitted successfully', 'success': True}
    ), 201


def handle_draft_comment(rescore_session_units_id, unit_comment):
    try:
        existing_comment = fetch_data(
            """
                    SELECT * FROM {database_name}.unit_comment_draft
                    WHERE rescore_session_units_id = %s;
                """,
            (rescore_session_units_id,),
        )
        if existing_comment:
            # If a comment already exists, update it
            execute_query(
                """UPDATE {database_name}.unit_comment_draft
                        SET unit_comment = %s, updated_at = NOW()
                        WHERE rescore_session_units_id = %s;
                """,
                (unit_comment, rescore_session_units_id),
            )
        else:
            # If no comment exists, insert a new one
            execute_query(
                """INSERT INTO {database_name}.unit_comment_draft (rescore_session_units_id, unit_comment)
                            VALUES (%s, %s);
                    """,
                (rescore_session_units_id, unit_comment),
            )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/bulk-upload-rescore', methods=['POST'])
@jwt_required()
def bulk_upload_rescore():
    data = request.get_json()
    units = data.get('units')
    rescore_data = data.get('rescore_data')

    success_count = 0

    for unit in units:
        collection_unit_id = unit.get('collection_unit_id')
        rescore_session_units_id = unit.get('rescore_session_units_id')

        if not collection_unit_id or not rescore_session_units_id:
            return jsonify(
                {
                    'error': 'collection_unit_id and rescore_session_units_id are required'
                }
            ), 400

        # Handle ranks
        if 'ranks_json' in rescore_data:
            # Loop through all of the score changes
            for criterion_ranks in rescore_data['ranks_json']:
                # Get the criterion_id for this score change
                criterion_id = criterion_ranks[0]['criterion_id']
                category_id = criterion_ranks[0]['category_id']
                # Find category_draft_id
                category_tracking = unit['category_tracking']
                current_category = [
                    category
                    for category in category_tracking
                    if category.get('category_id') == category_id
                ]
                category_draft_id = current_category[0]['category_draft_id']
                # Make the score change
                handle_draft_rank(criterion_id, criterion_ranks, category_draft_id)

        # Handle metrics
        if 'metric_json' in rescore_data:
            handle_draft_metrics(rescore_session_units_id, rescore_data['metric_json'])

        # Handle comment
        if 'unit_comment' in rescore_data:
            handle_draft_comment(rescore_session_units_id, rescore_data['unit_comment'])

        # Increase success counter
        success_count += 1
    return jsonify(
        {
            'message': 'Bulk drafts submitted successfully',
            'success_count': success_count,
            'total_units': len(units),
            'success': True,
        }
    ), 201


@data_bp.route('/end-rescore/<rescore_session_id>', methods=['POST'])
@jwt_required()
def update_end_rescore(rescore_session_id):
    date = datetime.now()
    data = execute_query(
        """UPDATE {database_name}.rescore_session
                        SET status = 'complete', completed_at = %s
                        WHERE rescore_session_id =%s;
                   """,
        (
            date,
            rescore_session_id,
        ),
    )
    return jsonify(data)


@data_bp.route('/complete-category', methods=['POST'])
@jwt_required()
def update_complete_category():
    data = request.get_json()
    rescore_session_units_id = data.get('rescore_session_units_id')
    category_ids_arr = data.get('category_ids_arr')
    new_val = data.get('new_val')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    if not rescore_session_units_id:
        return jsonify({'error': 'rescore_session_units_id is required'}), 400
    if not category_ids_arr:
        return jsonify({'error': 'category_ids_arr is required'}), 400
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    if not isinstance(category_ids_arr, list):
        return jsonify({'error': 'category_ids_arr should be a list'}), 400

    # Dynamically build placeholders for each category_id
    placeholders = ', '.join(['%s'] * len(category_ids_arr))

    try:
        data = execute_query(
            f"""UPDATE {database_name}.unit_category_draft ucd
                             JOIN {database_name}.rescore_session_units rsu ON ucd.rescore_session_units_id = rsu.rescore_session_units_id
                             JOIN {database_name}.rescore_session rs ON rsu.rescore_session_id = rs.rescore_session_id
                            SET complete = %s
                            WHERE ucd.rescore_session_units_id =%s and ucd.category_id IN ({placeholders}) && rs.user_id = %s;
                    """,
            (new_val, rescore_session_units_id, *category_ids_arr, user_id),
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify(data)


# Unit routes
@data_bp.route('/submit-unit', methods=['POST'])
@jwt_required()
def submit_unit():
    data = request.get_json()
    unit_data = data.get('unit_data')
    score_data = data.get('score_data')
    metric_json = score_data.get('metric_json')
    ranks_json = score_data.get('ranks_json')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    # Filter the data to remove None values and the collection_unit_id
    filter_unit_data = {
        key: value
        for key, value in unit_data.items()
        if value is not None and key != 'collection_unit_id'
    }
    # Extract fields and values
    keys = list(filter_unit_data.keys())
    values = list(filter_unit_data.values())

    # Construct the SQL dynamically
    placeholders = ', '.join(['%s'] * len(keys))  # %s placeholders
    columns = ', '.join([f'`{key}`' for key in keys])  # column names with backticks
    sql_query = f'INSERT INTO {database_name}.collection_unit ({columns}) VALUES ({placeholders})'

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # Execute the query and return the new unit ID
        cursor.execute(sql_query, values)
        new_unit_id = cursor.lastrowid
        print(f'new unit id - {new_unit_id}')

        if new_unit_id is None:
            return jsonify({'error': 'Failed to create new unit'}), 500

        # Handle metrics
        if metric_json:
            for metric in metric_json:
                collection_unit_metric_definition_id = metric.get(
                    'collection_unit_metric_definition_id'
                )
                metric_value = metric.get('metric_value')
                confidence_level = metric.get('confidence_level')
                if metric_value is not None or confidence_level is not None:
                    cursor.execute(
                        f"""INSERT INTO {database_name}.collection_unit_metric (collection_unit_id, collection_unit_metric_definition_id, metric_value, confidence_level, date_from, `current`)
                            VALUES (%s, %s, %s, %s, NOW(), 'yes');
                        """,
                        (
                            new_unit_id,
                            collection_unit_metric_definition_id,
                            metric_value,
                            confidence_level,
                        ),
                    )
        # Handle ranks
        if ranks_json:
            for criterion in ranks_json:
                criterion_id = criterion[0]['criterion_id']
                # Add the criterion to the unit_assessment_criterion table and get the new id
                cursor.execute(
                    f"""
                    INSERT INTO {database_name}.unit_assessment_criterion (
                        collection_unit_id, criterion_id, assessor_id,
                        date_assessed, date_from, current
                    ) VALUES (%s, %s, %s, NOW(), NOW(), 'yes')
                    """,
                    (new_unit_id, criterion_id, user_id),
                )
                unit_assessment_criterion_id = cursor.lastrowid
                for rank in criterion:
                    rank_id = rank['rank_id']
                    percentage = rank['percentage']
                    comment = rank['comment']
                    cursor.execute(
                        f"""
                        INSERT INTO {database_name}.unit_assessment_rank (
                            unit_assessment_criterion_id, rank_id, percentage, comment
                        ) VALUES (%s, %s, %s, %s)
                        """,
                        (
                            unit_assessment_criterion_id,
                            rank_id,
                            percentage,
                            comment,
                        ),
                    )

        # Commit the transaction queries
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'collection_unit_id': new_unit_id, 'success': True}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def column_exists(field_name, new_value):
    try:
        field_is_valid = fetch_data(
            """
                    SELECT COUNT(*)
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE table_schema = {database_name} AND table_name = %s AND column_name = %s
                    """,
            [field_name, new_value],
        )
        return field_is_valid
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/submit-field', methods=['POST'])
@jwt_required()
def submit_field():
    data = request.get_json()
    field_name = data.get('field_name')
    new_value = data.get('new_value')
    collection_unit_id = data.get('collection_unit_id')

    if not field_name:
        return jsonify({'error': 'field_name is required'}), 400
    # if new_value is None:
    #     return jsonify({'error': 'new_value is required'}), 400
    if not collection_unit_id:
        return jsonify({'error': 'collection_unit_id is required'}), 400

    try:
        if column_exists(field_name=field_name, new_value=new_value):
            data = execute_query(
                f"""
                UPDATE {database_name}.collection_unit
                SET `{field_name}` = %s
                WHERE collection_unit_id = %s;
                """,
                [new_value, collection_unit_id],
            )
            return jsonify({'data': data, 'success': True})
        else:
            return jsonify({'error: column does not exist'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/split-unit', methods=['POST'])
@jwt_required()
def split_unit():
    data = request.get_json()
    unit_id = data.get('unit_id')
    new_count = data.get('new_count')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    if not unit_id:
        return jsonify({'error': 'unit_id is required'}), 400
    if not new_count:
        return jsonify({'error': 'new_count is required'}), 400

    new_units = []

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # Create new units
        for i in range(new_count):
            # Copy the original primary unit
            new_unit_id = copy_unit(
                cursor=cursor,
                unit_id_to_copy=unit_id,
                user_id=user_id,
                unit_name_addition=(' ' + str(i + 1)),
            )
            new_units.append(new_unit_id)
        cursor.execute(
            f"""
                    UPDATE {database_name}.collection_unit
                        SET unit_active = 'no'
                        WHERE collection_unit_id = %s;
                    """,
            (unit_id,),
        )
        # Commit the transaction queries
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'new_units': new_units, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/combine-unit', methods=['POST'])
@jwt_required()
def combine_unit():
    data = request.get_json()
    primary_unit_id = data.get('primary_unit_id')
    unit_id_list = data.get('unit_id_list')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    if not primary_unit_id:
        return jsonify({'error': 'primary_unit_id is required'}), 400

    try:
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        # Copy the original primary unit
        new_unit_id = copy_unit(
            cursor=cursor, unit_id_to_copy=primary_unit_id, user_id=user_id
        )

        # Mark old units as not active
        for unit_id in unit_id_list:
            cursor.execute(
                f"""
                    UPDATE {database_name}.collection_unit
                        SET unit_active = 'no'
                        WHERE collection_unit_id = %s;
                    """,
                (unit_id,),
            )

        # Commit the transaction queries
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'new_unit_id': new_unit_id, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def copy_unit(cursor, unit_id_to_copy, user_id, unit_name_addition=''):
    # Create a new unit
    cursor.execute(
        f"""
                    INSERT INTO {database_name}.collection_unit
                        (unit_name,public_unit_name, section_id, unit_active, responsible_curator_id, curatorial_unit_definition_id, taxon_life_science_id, taxon_palaeontology_id, storage_room_id, storage_container_id, geographic_origin_id, library_and_archives_function_id, geological_time_period_from_id, geological_time_period_to_id, type_collection_flag, publish_flag, informal_taxon, named_collection, es_recent_specimen_flag, archives_fond_ref, count_curatorial_units_flag, sort_order)
                    SELECT CONCAT(unit_name, '{unit_name_addition}') ,public_unit_name, section_id, unit_active, responsible_curator_id, curatorial_unit_definition_id, taxon_life_science_id, taxon_palaeontology_id, storage_room_id, storage_container_id, geographic_origin_id, library_and_archives_function_id, geological_time_period_from_id, geological_time_period_to_id, type_collection_flag, publish_flag, informal_taxon, named_collection, es_recent_specimen_flag, archives_fond_ref, count_curatorial_units_flag, sort_order
                    FROM {database_name}.collection_unit
                    WHERE collection_unit_id = %s
                        """,
        (unit_id_to_copy,),
    )
    new_unit_id = cursor.lastrowid
    # Assign unit to current user
    cursor.execute(
        f"""INSERT INTO {database_name}.assigned_units (user_id, collection_unit_id) VALUES (%s, %s)
                        """,
        (user_id, new_unit_id),
    )
    # Insert the comment
    cursor.execute(
        f"""INSERT INTO {database_name}.unit_comment (collection_unit_id, unit_comment, date_added)
                        SELECT %s AS collection_unit_id, unit_comment, date_added
                        FROM {database_name}.unit_comment
                        WHERE collection_unit_id = %s
                    """,
        (new_unit_id, unit_id_to_copy),
    )
    # Select the current assessment criterion
    cursor.execute(
        f"""
        SELECT unit_assessment_criterion_id, criterion_id, assessor_id, criteria_assessment,
            date_assessed, date_from, date_to, `current`
        FROM {database_name}.unit_assessment_criterion
        WHERE collection_unit_id = %s AND `current` = 'yes'
        """,
        (unit_id_to_copy,),
    )
    criteria_to_copy = cursor.fetchall()
    # Go through each criterion
    for criterion in criteria_to_copy:
        # Insert the current criterion
        cursor.execute(
            f"""
            INSERT INTO {database_name}.unit_assessment_criterion
                (collection_unit_id, criterion_id, assessor_id, criteria_assessment,
                date_assessed, date_from, date_to, `current`)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (
                new_unit_id,
                criterion['criterion_id'],
                criterion['assessor_id'],
                criterion['criteria_assessment'],
                criterion['date_assessed'],
                criterion['date_from'],
                criterion['date_to'],
                criterion['current'],
            ),
        )
        # Get the last id
        new_criterion_id = cursor.lastrowid

        # Copy ranks belonging to this criterion
        cursor.execute(
            f"""
            INSERT INTO {database_name}.unit_assessment_rank
                (unit_assessment_criterion_id, rank_id, percentage, comment)
            SELECT %s, rank_id, percentage, comment
            FROM {database_name}.unit_assessment_rank
            WHERE unit_assessment_criterion_id = %s
            """,
            (new_criterion_id, criterion['unit_assessment_criterion_id']),
        )
    # Insert Unit Metrics
    cursor.execute(
        f"""INSERT INTO {database_name}.collection_unit_metric (collection_unit_id, collection_unit_metric_definition_id, metric_value, confidence_level, date_from, date_to, `current`)
                        SELECT %s AS collection_unit_id, collection_unit_metric_definition_id, metric_value, confidence_level, date_from, date_to, `current`
                        FROM {database_name}.collection_unit_metric
                        WHERE collection_unit_id = %s AND `current` = 'yes'
                    """,
        (new_unit_id, unit_id_to_copy),
    )
    return new_unit_id


@data_bp.route('/unit-department', methods=['GET'])
@jwt_required()
def get_units_and_departments():
    data = fetch_data("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, department.department_name, unit.unit_active, division.division_id, unit.responsible_curator_id, users.name AS curator_name
                   FROM {database_name}.collection_unit AS unit
                    LEFT JOIN {database_name}.section AS section ON unit.section_id = section.section_id
                    LEFT JOIN {database_name}.division AS division ON section.division_id = division.division_id
                    LEFT JOIN {database_name}.department AS department ON division.department_id = department.department_id
                    LEFT JOIN {database_name}.users AS users ON users.user_id = unit.responsible_curator_id
                      WHERE unit.unit_active = 'yes';
                   """)
    return jsonify(data)


@data_bp.route('/unit/<unit_id>', methods=['GET'])
@jwt_required()
def get_unit(unit_id):
    data = fetch_data(
        """SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, department.department_name, unit.*
                   FROM {database_name}.collection_unit AS unit
                    LEFT JOIN {database_name}.section AS section ON unit.section_id = section.section_id
                    LEFT JOIN {database_name}.division AS division ON section.division_id = division.division_id
                    LEFT JOIN {database_name}.department AS department ON division.department_id = department.department_id
                    WHERE  unit.collection_unit_id = %u;
                   """
        % int(unit_id)
    )
    return jsonify(data)


@data_bp.route('/full-unit/<unit_id>', methods=['GET'])
@jwt_required()
def get_full_unit(unit_id):
    data = fetch_data(
        """SELECT  cu.*, concat(p.first_name, ' ', p.last_name) AS responsible_curator,
                    uc.unit_comment, DATE(uc.date_added) AS date_comment_added
                    FROM {database_name}.collection_unit cu
                    LEFT JOIN {database_name}.person p ON p.person_id = cu.responsible_curator_id
                    LEFT JOIN {database_name}.unit_comment uc ON uc.collection_unit_id = cu.collection_unit_id
                    WHERE cu.collection_unit_id = %u;
                   """
        % int(unit_id)
    )
    return jsonify(data)


@data_bp.route('/all-assigned-users/<unit_id>', methods=['GET'])
@jwt_required()
def get_assigned_users(unit_id):
    data = fetch_data(
        """SELECT au.user_id, u.name AS user_name
        FROM {database_name}.assigned_units au
        JOIN {database_name}.users u ON u.user_id = au.user_id
        WHERE au.collection_unit_id = %s
                   """
        % int(unit_id)
    )
    return jsonify(data)


@data_bp.route('/units-assigned', methods=['GET'])
@jwt_required()
def get_units_assigned():
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    try:
        # Fetch user level
        user = fetch_data(
            """SELECT *
            FROM {database_name}.users
            WHERE user_id = %s
                    """,
            (user_id,),
        )
        match user[0]['role_id']:
            case 1:
                return jsonify({'error': 'You are not autorised.'}), 500
            case 2:
                data = fetch_data(
                    """SELECT u.*, cu.*, s.section_name, d.division_name, u.name AS curator_name, cu.responsible_curator_id,
                    (
                        SELECT JSON_ARRAYAGG(
	                        au.user_id
	                    )
                        FROM {database_name}.assigned_units au
                        JOIN {database_name}.users u ON u.user_id = au.user_id
                        WHERE au.collection_unit_id = cu.collection_unit_id
                    ) AS assigned_editors
                    FROM {database_name}.assigned_units au
                    JOIN {database_name}.users u ON u.user_id = au.user_id
                    JOIN {database_name}.collection_unit cu ON cu.collection_unit_id = au.collection_unit_id
                    JOIN {database_name}.section s ON s.section_id = cu.section_id
                    JOIN {database_name}.division d ON d.division_id = s.division_id
                    WHERE au.user_id = %s AND cu.unit_active = 'yes'
                            """,
                    (user_id,),
                )
            case 3:
                data = fetch_data(
                    """SELECT cu.*, s.section_name, d.division_name, u.name AS curator_name, cu.responsible_curator_id,
                    (
                        SELECT JSON_ARRAYAGG(
	                        au.user_id
	                    )
                        FROM {database_name}.assigned_units au
                        JOIN {database_name}.users u ON u.user_id = au.user_id
                        WHERE au.collection_unit_id = cu.collection_unit_id
                    ) AS assigned_editors
                    FROM {database_name}.collection_unit cu
                    JOIN {database_name}.users u ON u.user_id = cu.responsible_curator_id
                    JOIN {database_name}.section s ON s.section_id = cu.section_id
                    JOIN {database_name}.division d ON d.division_id = s.division_id
                    WHERE d.division_id = %s AND cu.unit_active = 'yes'
                            """,
                    (user[0]['division_id'],),
                )
            case 4:
                data = fetch_data(
                    """SELECT cu.*,
                    FROM {database_name}.collection_unit cu
                    WHERE cu.unit_active = 'yes'
                            """
                )
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/units-by-division/<division_id>', methods=['GET'])
@jwt_required()
def get_units_by_division(division_id):
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    try:
        data = fetch_data(
            """SELECT cu.*
        FROM {database_name}.collection_unit cu
        JOIN {database_name}.section s ON s.section_id = cu.section_id
        WHERE cu.unit_active = 'yes' AND s.division_id = %s
                """,
            (division_id,),
        )
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/division-users', methods=['GET'])
@jwt_required()
def get_division_users():
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    try:
        # Fetch user level
        user = fetch_data(
            """SELECT *
            FROM {database_name}.users
            WHERE user_id = %s
                    """,
            (user_id,),
        )
        role_id = user[0]['role_id']
        if role_id >= 3:
            data = fetch_data(
                """SELECT u.user_id, u.role_id, u.name, u.email, d.division_name, u.division_id, r.role,
                (
                    SELECT JSON_ARRAYAGG(
                        au.collection_unit_id
                    )
                    FROM {database_name}.assigned_units au
                    JOIN {database_name}.collection_unit cu ON cu.collection_unit_id = au.collection_unit_id
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
                JOIN {database_name}.roles r ON r.role_id = u.role_id
                JOIN {database_name}.division d ON d.division_id = u.division_id
                WHERE u.division_id = %s
                        """,
                (user[0]['division_id'],),
            )
            return jsonify(data)
        else:
            return jsonify({'error': 'You are not autorised.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/reassign-responsible-curator', methods=['POST'])
@jwt_required()
def reassign_responsible_curator():
    data = request.get_json()
    old_user_id = data.get('old_user_id')
    new_user_id = data.get('new_user_id')

    try:
        #
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        # Transfer units the old user was responsible for to the new user
        cursor.execute(f"""
                    INSERT INTO {database_name}.assigned_units (user_id, collection_unit_id)
                    SELECT {new_user_id} AS user_id, collection_unit_id
                    FROM {database_name}.collection_unit
                    WHERE responsible_curator_id = {old_user_id}
                """)
        # Remove all units assigned to old user
        cursor.execute(f"""
                    DELETE FROM {database_name}.assigned_units
                    WHERE user_id = {old_user_id}
                """)
        # Change the responsible_curator_id from the old user, to the new
        cursor.execute(f"""
                    UPDATE {database_name}.collection_unit
                    SET responsible_curator_id = {new_user_id}
                    WHERE responsible_curator_id = {old_user_id};
                """)
        connection.commit()
        # Close the cursor and connection
        cursor.close()
        connection.close()
        return jsonify({'message': 'Units successfully reassigned', 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/submit-unit-assigned', methods=['POST'])
@jwt_required()
def set_unit_assigned():
    data = request.get_json()
    unit_id = data.get('unit_id')
    assigned_users = data.get('assigned_users')

    if not unit_id:
        return jsonify({'error': 'unit_id is required'}), 400

    if not assigned_users:
        return jsonify({'error': 'assigned_users is required'}), 400

    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    try:
        # Get the current assigned users
        current_assigned = fetch_data(
            """SELECT user_id
            FROM {database_name}.assigned_units
            WHERE collection_unit_id = %s
                    """,
            (unit_id,),
        )
        current_assigned = set(
            row['user_id'] for row in current_assigned
        )  # if fetch_data returns dicts
        assigned_users = set(assigned_users)
        # Compare lists
        users_to_add = assigned_users - current_assigned
        users_to_remove = current_assigned - assigned_users
        # Insert new assigned users
        if users_to_add:
            for user_id in users_to_add:
                execute_query(
                    """INSERT INTO {database_name}.assigned_units (user_id, collection_unit_id)
                    VALUES (%s, %s)""",
                    (user_id, unit_id),
                )
        # Remove unassigned users
        if users_to_remove:
            for user_id in users_to_remove:
                execute_query(
                    """DELETE FROM {database_name}.assigned_units
                    WHERE user_id = %s AND collection_unit_id = %s""",
                    (user_id, unit_id),
                )
        return jsonify(
            {'message': 'Unit assigned users updated successfully', 'success': True}
        ), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/submit-user-assigned', methods=['POST'])
@jwt_required()
def set_user_assigned():
    data = request.get_json()
    user_id = data.get('user_id')
    assigned_units = data.get('assigned_units')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    if not assigned_units:
        return jsonify({'error': 'assigned_units is required'}), 400

    try:
        # Fetch current assigned units for this user
        current_assigned = fetch_data(
            """SELECT collection_unit_id
               FROM {database_name}.assigned_units
               WHERE user_id = %s""",
            (user_id,),
        )
        # Normalize both sets to integers
        current_assigned = set(
            int(row['collection_unit_id']) for row in current_assigned
        )
        assigned_units = set(int(unit_id) for unit_id in assigned_units)

        # Determine diffs
        units_to_add = assigned_units - current_assigned
        units_to_remove = current_assigned - assigned_units

        # Insert new assignments
        for unit_id in units_to_add:
            execute_query(
                """INSERT INTO {database_name}.assigned_units (user_id, collection_unit_id)
                   VALUES (%s, %s)""",
                (user_id, unit_id),
            )

        # Remove old assignments
        for unit_id in units_to_remove:
            execute_query(
                """DELETE FROM {database_name}.assigned_units
                   WHERE user_id = %s AND collection_unit_id = %s""",
                (user_id, unit_id),
            )

        return jsonify(
            {'message': 'User assigned units updated successfully', 'success': True}
        ), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/criterion', methods=['GET'])
@jwt_required()
def get_criterion():
    data = fetch_data("""SELECT cat.*, crit.criterion_id, crit.criterion_name, crit.criterion_code, crit.definition
                   FROM {database_name}.criterion crit
                    LEFT JOIN {database_name}.category cat ON crit.category_id = cat.category_id;
                   """)
    return jsonify(data)


@data_bp.route('/units-metrics/<unit_id>', methods=['GET'])
@jwt_required()
def get_units_metrics(unit_id):
    data = fetch_data(
        """SELECT cum.*, cumd.*
                        FROM {database_name}.collection_unit_metric cum
                        JOIN {database_name}.collection_unit_metric_definition cumd ON cum.collection_unit_metric_definition_id  = cumd.collection_unit_metric_definition_id
                        WHERE cum.current = 'yes' AND cum.collection_unit_id = %s;
                      """,
        (unit_id,),
    )
    return jsonify(data)


@data_bp.route('/category', methods=['GET'])
@jwt_required()
def get_roles():
    data = fetch_data("""SELECT cat.*
                   FROM {database_name}.category cat;
                   """)
    return jsonify(data)


@data_bp.route('/all-roles', methods=['GET'])
@jwt_required()
def get_category():
    data = fetch_data("""SELECT *
                   FROM {database_name}.roles;
                   """)
    return jsonify(data)


@data_bp.route('/metric-definitions', methods=['GET'])
@jwt_required()
def get_metric_definitions():
    data = fetch_data("""SELECT *
                   FROM {database_name}.collection_unit_metric_definition;
                   """)
    return jsonify(data)


@data_bp.route('/all-sections', methods=['GET'])
@jwt_required()
def get_all_sections():
    data = fetch_data("""SELECT sect.*, divis.department_id, divis.division_name, dept.department_name, sect.section_id AS value, sect.section_name AS label
                   FROM {database_name}.section sect
                    LEFT JOIN {database_name}.division divis ON divis.division_id = sect.division_id
                    LEFT JOIN {database_name}.department dept ON dept.department_id = divis.department_id;
                   """)
    return jsonify(data)


@data_bp.route('/all-geographic-origin', methods=['GET'])
@jwt_required()
def get_all_geographic_origin():
    data = fetch_data("""SELECT *, geographic_origin_name AS label, geographic_origin_id AS value
                   FROM {database_name}.geographic_origin;
                   """)
    return jsonify(data)


@data_bp.route('/all-geological-time-period', methods=['GET'])
@jwt_required()
def get_all_geological_time_period():
    data = fetch_data("""SELECT *, geological_time_period_id AS value, period_name AS label
                   FROM {database_name}.geological_time_period;
                   """)
    return jsonify(data)


@data_bp.route('/all-divisions', methods=['GET'])
@jwt_required()
def get_all_divisions():
    data = fetch_data("""SELECT divis.*
                   FROM {database_name}.division divis;
                   """)
    return jsonify(data)


@data_bp.route('/all-departments', methods=['GET'])
@jwt_required()
def get_all_departments():
    data = fetch_data("""SELECT *
                   FROM {database_name}.department ;
                   """)
    return jsonify(data)


@data_bp.route('/container-data', methods=['GET'])
@jwt_required()
def get_all_containers():
    data = fetch_data("""SELECT *, storage_container_id AS value, container_name AS label
                   FROM {database_name}.storage_container ;
                   """)
    return jsonify(data)


@data_bp.route('/all-taxon', methods=['GET'])
@jwt_required()
def get_all_taxon():
    data = fetch_data("""SELECT *, taxon_id AS value, CONCAT(taxon_name, ' ', taxon_rank) AS label
                   FROM {database_name}.taxon ;
                   """)
    return jsonify(data)


@data_bp.route('/all-curatorial-definition', methods=['GET'])
@jwt_required()
def get_all_curatorial_definition():
    data = fetch_data("""SELECT cud.*, bl.*, it.*, pm.*, cud.curatorial_unit_definition_id as value, cud.description as label
                    FROM {database_name}.curatorial_unit_definition cud
                    LEFT JOIN {database_name}.bibliographic_level bl ON bl.bibliographic_level_id = cud.bibliographic_level_id
                    LEFT JOIN {database_name}.item_type it ON it.item_type_id = cud.item_type_id
                    LEFT JOIN {database_name}.preservation_method pm ON pm.preservation_method_id = cud.preservation_method_id  ;
                   """)
    return jsonify(data)


@data_bp.route('/room-data', methods=['GET'])
@jwt_required()
def get_all_rooms():
    data = fetch_data("""SELECT sr.*, f.*, b.*, s.*, sr.storage_room_id AS value, sr.room_code AS label
                        FROM {database_name}.storage_room sr
                        JOIN {database_name}.floor f ON f.floor_id = sr.floor_id
                        JOIN {database_name}.building b ON b.building_id = f.building_id
                        JOIN {database_name}.site s ON s.site_id = b.site_id ;
                   """)
    return jsonify(data)


@data_bp.route('/all-lib-function', methods=['GET'])
@jwt_required()
def get_all_lib_function():
    data = fetch_data("""SELECT *, library_and_archives_function_id AS value, function_name AS label
                        FROM {database_name}.library_and_archives_function;
                   """)
    return jsonify(data)


@data_bp.route('/all-curators', methods=['GET'])
@jwt_required()
def get_all_curators():
    data = fetch_data("""
        SELECT u.name AS label, u.user_id AS value, u.email
        FROM {database_name}.users u
        WHERE u.role_id = 2 OR u.role_id = 2 OR 3
        """)
    return jsonify(data)


@data_bp.route('/units-by-user', methods=['GET'])
@jwt_required()
def get_units_by_user():
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    data = fetch_data(
        """SELECT cu.*, (
                            SELECT MAX(DATE(rs.completed_at))
                            FROM {database_name}.rescore_session_units rsu
                            JOIN {database_name}.rescore_session rs ON rs.rescore_session_id = rsu.rescore_session_id
                            WHERE rsu.collection_unit_id = cu.collection_unit_id
                        ) AS last_rescored
                        FROM {database_name}.collection_unit cu
                        JOIN {database_name}.assigned_units au ON au.collection_unit_id = cu.collection_unit_id
                        WHERE au.user_id = %s AND cu.unit_active = 'yes';
                        """,
        (user_id,),
    )
    return jsonify(data)


# Export routes


@data_bp.route('/export-view/<view>', methods=['GET'])
@jwt_required()
def get_view(view):
    try:
        # Connect to db
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = """SELECT *
                        FROM {database_name}.%s;
                        """ % str(
            view,
        )
        # Format the query with the database name
        formatted_query = query.format(database_name=database_name)
        # Execute query
        cursor.execute(formatted_query)
        # Fetch rows
        data = cursor.fetchall()

        # Get the column names
        col_names = [desc[0] for desc in cursor.description]

        # Create CSV response
        def generate():
            # Make headers
            header = ','.join(col_names)
            # Convert JSON objects to a comma-separated string
            rows = '\n'.join(
                ','.join(str(row[col]) for col in col_names) for row in data
            )
            # Return both
            return f'{header}\n{rows}'

        # Create Response with CSV MIME type
        response = Response(generate(), mimetype='text/csv')
        response.headers['Content-Disposition'] = (
            'attachment; filename=' + view + '.csv'
        )

        return response

    except Exception as e:
        return str(e)

    finally:
        cursor.close()
        connection.close()


def generate_json():
    data = fetch_data(LTC_EXPORT)
    if data:
        try:
            # Extract JSON
            json_data = json.loads(data[0]['ltc_export'])
        except json.JSONDecodeError as e:
            yield '{"error": "Invalid JSON format"}'
            return
        # Stream the JSON array directly
        yield '[\n'
        for i, item in enumerate(json_data):
            comma = ',' if i < len(json_data) - 1 else ''
            yield f'  {json.dumps(item)}{comma}\n'
        yield ']\n'


@data_bp.route('/export-ltc-json', methods=['GET'])
@jwt_required()
def get_ltc_json():
    return Response(
        stream_with_context(generate_json()),
        content_type='application/json',
        headers={'Content-Disposition': 'attachment; filename=data.json'},
    )


# Unit actions routes


@data_bp.route('/delete-units', methods=['POST'])
@jwt_required()
def delete_units():
    data = request.get_json()
    unit_ids = data.get('unit_ids')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    if not unit_ids:
        return jsonify({'error': 'unit_ids is required'}), 400
    if not isinstance(unit_ids, list):
        return jsonify({'error': 'unit_ids should be a list'}), 400

    try:
        for unit_id in unit_ids:
            # Delete units from collection_unit table
            execute_query(
                """UPDATE {database_name}.collection_unit cu JOIN {database_name}.assigned_units au ON au.collection_unit_id = cu.collection_unit_id
                    SET cu.unit_active = 'no'
                    WHERE cu.collection_unit_id = %s
                    AND au.user_id = %s;""",
                (
                    unit_id,
                    user_id,
                ),
            )

        return jsonify({'message': 'Units deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
