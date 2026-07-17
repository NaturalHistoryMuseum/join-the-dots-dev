from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy import func, update

from server.database import db
from server.models import (
    CollectionUnit,
    RescoreSession,
    RescoreSessionUnits,
    Users,
)
from server.routes.data.utils import rescore_units_query
from server.utils import get_person_id

from . import data_bp
from .utils import *


@data_bp.route('/mark-rescore-open', methods=['POST'])
@jwt_required()
def get_mark_rescore_open():
    """
    Create a new rescore session with provided units.
    """
    data = request.get_json()
    units = data.get('units')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    if not units:
        return jsonify({'error': 'Units are required'}), 400
    try:
        rescore_session_id, rescore_session_units_ids = create_rescore_session(
            units, user_id
        )
        print(rescore_session_id, rescore_session_units_ids)
        db.session.commit()
        return jsonify({'rescore_session_id': rescore_session_id, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
        connection.close()


@data_bp.route('/rescore-complete', methods=['POST'])
@jwt_required()
def submit_rescore_complete():
    """
    Mark the rescore as completed and upgrade all ranks/metrics from drafts.
    """
    data = request.get_json()
    rescore_session_id = data.get('rescore_session_id')
    if not rescore_session_id:
        return jsonify({'error': 'rescore_session_id is required'}), 400
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    person_id = get_person_id(user_id)

    try:
        # Submit draft comments
        upgrade_draft_comments(rescore_session_id)

        # Submit draft metrics
        upgrade_draft_metrics(rescore_session_id)

        # Submit draft ranks
        upgrade_draft_ranks(rescore_session_id, person_id)

        # Close the rescore and remove draft categories
        close_rescore(rescore_session_id)

        db.session.commit()

        return jsonify(
            {'message': 'Rescore session marked as complete', 'success': True}
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/open-rescore', methods=['GET'])
@jwt_required()
def get_open_rescore():
    """
    Find if a user has a rescore session currently open.
    """
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    query = (
        select(RescoreSession, RescoreSessionUnits, CollectionUnit)
        .join(
            RescoreSessionUnits,
            RescoreSession.rescore_session_id == RescoreSessionUnits.rescore_session_id,
        )
        .join(
            CollectionUnit,
            CollectionUnit.collection_unit_id == RescoreSessionUnits.collection_unit_id,
        )
        .where(
            RescoreSession.status == 'in_progress',
            RescoreSession.user_id == user_id,
            CollectionUnit.draft_unit != 1,
        )
    )
    data = db.session.execute(query).scalars().all()
    return jsonify(data)


@data_bp.route('/all-open-rescores', methods=['GET'])
@jwt_required()
def get_all_open_rescores():
    """
    Retrieve all current open rescores.
    """
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    query = (
        select(
            RescoreSession.rescore_session_id,
            RescoreSession.status,
            RescoreSession.user_id,
            RescoreSession.created_at,
            RescoreSession.completed_at,
            func.COUNT(RescoreSessionUnits.rescore_session_units_id).label(
                'unit_count'
            ),
            Users.display_name.label('curator_name'),
        )
        .join(
            RescoreSessionUnits,
            RescoreSessionUnits.rescore_session_id == RescoreSession.rescore_session_id,
        )
        .join(Users, Users.user_id == RescoreSession.user_id)
        .join(
            CollectionUnit,
            CollectionUnit.collection_unit_id == RescoreSessionUnits.collection_unit_id,
        )
        .where(RescoreSession.status == 'in_progress', CollectionUnit.draft_unit != 1)
        .group_by(RescoreSession.rescore_session_id)
        .order_by(RescoreSession.rescore_session_id)
    )
    data = db.session.execute(query).mappings().all()
    return jsonify([dict(row) for row in data])


@data_bp.route('/rescore-units/<rescore_session_id>', methods=['GET'])
@jwt_required()
def get_rescore_units(rescore_session_id):
    """
    Get all units in the rescores scores and metrics data, as well as the category
    tracking.

    These provide all the data needed to display and edit units on the rescore page.
    """

    query = rescore_units_query(rescore_session_id)
    data = db.session.execute(query).all()

    return [
        {
            'rescore_session_id': row.RescoreSession.rescore_session_id,
            'status': row.RescoreSession.status,
            'created_at': row.RescoreSession.created_at,
            'completed_at': row.RescoreSession.completed_at,
            'rescore_session_units_id': row.RescoreSessionUnits.rescore_session_units_id,
            'collection_unit_id': row.CollectionUnit.collection_unit_id,
            'division_name': row.Division.division_name,
            'section_name': row.Section.section_name,
            'responsible_curator': row.Users.display_name,
            'curatorial_unit_type': row.CuratorialUnitDefinition.description,
            'unit_name': row.CollectionUnit.unit_name,
            'sort_order': row.CollectionUnit.sort_order,
            'metric_json': row.metric_json,
            'unit_comment': row.unit_comment,
            'unit_comment_date_added': row.unit_comment_date_added,
            'ranks_json': row.ranks_json,
            'category_tracking': row.category_tracking,
        }
        for row in data
    ]


@data_bp.route('/submit-draft-rank', methods=['POST'])
@jwt_required()
def submit_draft_rank():
    """
    Save a rank change as a draft.
    """
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

    # Handle the draft ranks
    handle_draft_rank(criterion_id, ranks, category_draft_id)
    db.session.commit()

    return jsonify({'message': 'Draft rank submitted successfully'})


@data_bp.route('/submit-draft-metrics', methods=['POST'])
@jwt_required()
def submit_draft_metrics():
    """
    Save a metric change as a draft.
    """
    data = request.get_json()
    rescore_session_units_id = data.get('rescore_session_units_id')
    collection_unit_id = data.get('collection_unit_id')
    metric_json = data.get('metric_json')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    if not rescore_session_units_id:
        return jsonify({'error': 'rescore_session_units_id is required'}), 400
    if not collection_unit_id:
        return jsonify({'error': 'collection_unit_id is required'}), 400
    if not metric_json:
        return jsonify({'error': 'metric_json are required'}), 400

    # Handle the draft metrics
    handle_draft_metrics(rescore_session_units_id, metric_json)
    db.session.commit()

    return jsonify({'message': 'Draft metrics submitted successfully', 'success': True})


@data_bp.route('/submit-draft-comment', methods=['POST'])
@jwt_required()
def submit_draft_comment():
    """
    Save a comment change as a draft.
    """
    data = request.get_json()
    rescore_session_units_id = data.get('rescore_session_units_id')
    unit_comment = data.get('unit_comment')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    if not rescore_session_units_id:
        return jsonify({'error': 'rescore_session_units_id is required'}), 400
    if not unit_comment:
        return jsonify({'error': 'unit_comment is required'}), 400

    # Handle the draft comments
    handle_draft_comment(rescore_session_units_id, unit_comment)
    db.session.commit()

    return jsonify({'message': 'Draft comment submitted successfully', 'success': True})


@data_bp.route('/bulk-upload-rescore', methods=['POST'])
@jwt_required()
def bulk_upload_rescore():
    """
    Make bulk draft changes to multiple units.
    """
    data = request.get_json()
    units = data.get('units')
    rescore_data = data.get('rescore_data')
    # Get user_id from the jwt token
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
    db.session.commit()
    return jsonify(
        {
            'message': 'Bulk drafts submitted successfully',
            'success_count': success_count,
            'total_units': len(units),
            'success': True,
        }
    )


@data_bp.route('/end-rescore/<rescore_session_id>', methods=['POST'])
@jwt_required()
def update_end_rescore(rescore_session_id):
    """
    Mark the rescore session as complete and mark the date.
    """
    date = datetime.now()
    db.session.execute(
        update(RescoreSession)
        .where(RescoreSession.rescore_session_id == rescore_session_id)
        .values(status='complete', completed_at=date)
    )
    db.session.commit()
    return jsonify(
        {
            'success': True,
        }
    )


@data_bp.route('/complete-category', methods=['POST'])
@jwt_required()
def update_complete_category():
    """
    Make bulk draft changes to multiple units.
    """
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

    try:
        db.session.execute(
            update(UnitCategoryDraft)
            .where(
                UnitCategoryDraft.rescore_session_units_id == rescore_session_units_id,
                UnitCategoryDraft.category_id.in_(category_ids_arr),
            )
            .values(complete=new_val)
        )
        db.session.commit()
        return jsonify(
            {
                'success': True,
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500
