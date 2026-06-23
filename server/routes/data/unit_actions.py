from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy import text

from server.database import db
from server.models import (
    AssignedUnits,
    CollectionUnit,
    CollectionUnitMetric,
    RescoreSession,
    RescoreSessionUnits,
    UnitAssessmentCriterion,
    UnitAssessmentRank,
)
from server.routes.queries.data_queries import RESCORE_UNITS
from server.utils import (
    get_person_id,
)

from . import data_bp
from .utils import *


@data_bp.route('/delete-units', methods=['POST'])
@jwt_required()
def delete_units():
    data = request.get_json()
    unit_ids = data.get('unit_ids')
    justification = data.get('justification')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    person_id = get_person_id(user_id)
    date_now = datetime.now()

    if not unit_ids:
        return jsonify({'error': 'unit_ids is required'}), 400
    if not isinstance(unit_ids, list):
        return jsonify({'error': 'unit_ids should be a list'}), 400

    try:
        for unit_id in unit_ids:
            CollectionUnit.query.filter(
                CollectionUnit.assigned_units.any(
                    AssignedUnits.user_id == user_id,
                ),
                CollectionUnit.collection_unit_id == unit_id,
            ).update({'unit_active': 'no'})

            # Add the change to the structural changes log
            add_structural_change(
                person_id=person_id,
                higher_operation='delete',
                operation='delete',
                collection_unit_id=unit_id,
                comment=justification,
                date=date_now,
            )
        # Commit the transaction queries
        db.session.commit()

        return jsonify({'message': 'Units deleted successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/update-assessed-date', methods=['POST'])
@jwt_required()
def update_assessed_date():
    data = request.get_json()
    unit_ids = data.get('unit_ids')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    date_now = datetime.now()
    try:
        # Update the assessed date
        UnitAssessmentCriterion.query.filter(
            UnitAssessmentCriterion.collection_unit_id.in_(unit_ids)
        ).update({'date_assessed': date_now})
        db.session.commit()
        return jsonify(
            {'message': 'Assessed date updated successfully', 'success': True}
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
    person_id = get_person_id(user_id)
    date_now = datetime.now()
    # Filter the data to remove None values and the collection_unit_id
    filter_unit_data = {
        key: value
        for key, value in unit_data.items()
        if value is not None and key != 'collection_unit_id'
    }

    try:
        new_unit = CollectionUnit(**filter_unit_data)
        db.session.add(new_unit)
        db.session.flush()
        new_unit_id = new_unit.collection_unit_id

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
                    new_metric = CollectionUnitMetric(
                        collection_unit_id=new_unit_id,
                        collection_unit_metric_definition_id=collection_unit_metric_definition_id,
                        metric_value=metric_value,
                        confidence_level=confidence_level,
                        date_from=date_now,
                        current='yes',
                    )
                    db.session.add(new_metric)
                    db.session.flush()
        # Handle ranks
        if ranks_json:
            for criterion in ranks_json:
                criterion_id = criterion[0]['criterion_id']
                # Add the criterion to the unit_assessment_criterion table and get the new id
                new_criterion_assess = UnitAssessmentCriterion(
                    collection_unit_id=new_unit_id,
                    criterion_id=criterion_id,
                    assessor_id=person_id,
                    date_assessed=date_now,
                    date_from=date_now,
                    current='yes',
                    criteria_assessment='known',
                )
                db.session.add(new_criterion_assess)
                db.session.flush()
                unit_assessment_criterion_id = (
                    new_criterion_assess.unit_assessment_criterion_id
                )

                for rank in criterion:
                    rank_id = rank['rank_id']
                    percentage = rank['percentage']
                    comment = rank['comment']
                    new_rank = UnitAssessmentRank(
                        unit_assessment_criterion_id=unit_assessment_criterion_id,
                        rank_id=rank_id,
                        percentage=percentage,
                        comment=comment,
                    )
                    db.session.add(new_rank)
        # Add the change to the structural changes log
        add_structural_change(
            person_id=person_id,
            higher_operation='create',
            operation='create',
            collection_unit_id=new_unit_id,
            date=date_now,
        )

        # Commit the transaction queries
        db.session.commit()

        return jsonify({'collection_unit_id': new_unit_id, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/submit-draft-unit', methods=['POST'])
@jwt_required()
def submit_draft_unit():
    data = request.get_json()
    unit_data = data.get('unit_data')
    unit_id = unit_data.get('collection_unit_id')
    draft_unit = unit_data.get('draft_unit')
    score_data = data.get('score_data')
    metric_json = score_data.get('metric_json')
    ranks_json = score_data.get('ranks_json')
    category_tracking = score_data.get('category_tracking')
    unit_comment = score_data.get('unit_comment')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    person_id = get_person_id(user_id)
    if unit_id is None or unit_id == 0:
        insert_mode = True
    else:
        insert_mode = False

    try:
        # Check if the draft is being insered or updated
        if insert_mode:
            # Filter the data to remove None values and the collection_unit_id
            filter_unit_data = {
                key: value
                for key, value in unit_data.items()
                if value is not None and key != 'collection_unit_id'
            }
            new_unit = CollectionUnit(**filter_unit_data)
            db.session.add(new_unit)
            db.session.flush()
            unit_id = new_unit.collection_unit_id
            if unit_id is None:
                return jsonify({'error': 'Failed to create new unit'}), 500
            # Create the rescore session if we are adding the draft
            rescore_session_id, category_draft_ids = create_rescore_session(
                [unit_id], user_id
            )
            rescore_session_units_id = category_draft_ids[0]['rescore_session_units_id']
        else:
            # Filter the data to remove None values and the collection_unit_id
            filtered = {
                key: value
                for key, value in unit_data.items()
                if value is not None
                and key != 'collection_unit_id'
                and column_exists(table_name='collection_unit', column_name=key)
            }
            CollectionUnit.query.filter(
                CollectionUnit.collection_unit_id == unit_id
            ).update(filtered)
            db.session.flush()
            # Create the rescore session if we are adding the draft
            category_draft_ids = None
            rescore_session_units_id = score_data.get('rescore_session_units_id')

        # Handle ranks
        if ranks_json:
            # Loop through all of the score changes
            for criterion_ranks in ranks_json:
                # Get the criterion_id for this score change
                criterion_id = criterion_ranks[0]['criterion_id']
                category_id = criterion_ranks[0]['category_id']
                # If rescore was just added
                if category_draft_ids is not None:
                    # Find category_draft_id
                    current_category = [
                        category
                        for category in category_draft_ids
                        if category.get('category_id') == category_id
                    ]
                    category_draft_id = current_category[0]['category_draft_id']
                elif category_tracking is not None:
                    # Find category_draft_id
                    category_tracking = score_data['category_tracking']
                    current_category = [
                        category
                        for category in category_tracking
                        if category.get('category_id') == category_id
                    ]
                    category_draft_id = current_category[0]['category_draft_id']
                # Make the score change
                handle_draft_rank(
                    criterion_id,
                    criterion_ranks,
                    category_draft_id,
                    insert_only=insert_mode,
                )

        # Handle metrics
        if metric_json is not None:
            handle_draft_metrics(rescore_session_units_id, metric_json)
        # Handle comment
        if unit_comment is not None:
            handle_draft_comment(rescore_session_units_id, unit_comment)
        # If no longer draft, upgrade to full unit
        if draft_unit == 0:
            complete_draft_unit(unit_id, user_id, person_id)

        # Commit the transaction queries
        db.session.commit()

        return jsonify({'collection_unit_id': unit_id, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/draft-scores/<unit_id>', methods=['GET'])
@jwt_required()
def get_draft_scores(unit_id):
    rescore_session = RescoreSession.query.filter(
        RescoreSession.status == 'in_progress',
        RescoreSession.rescore_session_units.any(
            RescoreSessionUnits.collection_unit_id == unit_id
        ),
    ).first()
    rescore_session_id = rescore_session.rescore_session_id
    data = db.session.execute(
        text(RESCORE_UNITS), {'rescore_session_id': rescore_session_id}
    ).fetchall()

    return jsonify([dict(row._mapping) for row in data])


@data_bp.route('/submit-field', methods=['POST'])
@jwt_required()
def submit_field():
    data = request.get_json()
    field_name = data.get('field_name')
    new_value = data.get('new_value')
    collection_unit_id = data.get('collection_unit_id')

    if not field_name:
        return jsonify({'error': 'field_name is required'}), 400
    if not collection_unit_id:
        return jsonify({'error': 'collection_unit_id is required'}), 400

    try:
        if column_exists(column_name=field_name, table_name='collection_unit'):
            CollectionUnit.query.filter(
                CollectionUnit.collection_unit_id == collection_unit_id
            ).update({field_name: new_value})
            db.session.commit()
            return jsonify({'success': True})
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
    person_id = get_person_id(user_id)
    date_now = datetime.now()
    if not unit_id:
        return jsonify({'error': 'unit_id is required'}), 400
    if not new_count:
        return jsonify({'error': 'new_count is required'}), 400

    new_units = []

    try:
        # Add structural change entry
        new_change_higher = StructuralChangesHigher(
            higher_operation='split',
            effective_date=date_now,
            change_agent_id=person_id,
            cause='Requested by curator',
        )
        db.session.add(new_change_higher)
        db.session.flush()
        structural_changes_higher_id = new_change_higher.structural_changes_higher_id

        # Create new units
        for i in range(new_count):
            # Copy the original primary unit
            new_unit_id = copy_unit(
                unit_id_to_copy=unit_id,
                user_id=user_id,
                unit_name_addition=(' ' + str(i + 1)),
            )
            new_units.append(new_unit_id)

            # Basic structural change
            new_change_basic = StructuralChangesBasic(
                structural_changes_higher_id=structural_changes_higher_id,
                collection_unit_id=new_unit_id,
                operation='create',
            )
            db.session.add(new_change_basic)
            db.session.flush()

        CollectionUnit.query.filter(
            CollectionUnit.collection_unit_id == unit_id
        ).update({'unit_active': 'no'})
        # Basic structural change
        change_ = StructuralChangesBasic(
            structural_changes_higher_id=structural_changes_higher_id,
            collection_unit_id=unit_id,
            operation='delete',
        )
        db.session.add(new_change_basic)
        # Commit the transaction queries
        db.session.commit()
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
    person_id = get_person_id(user_id)
    date_now = datetime.now()
    if not primary_unit_id:
        return jsonify({'error': 'primary_unit_id is required'}), 400

    try:
        # Add structural change entry
        new_change_higher = StructuralChangesHigher(
            higher_operation='merge',
            effective_date=date_now,
            change_agent_id=person_id,
            cause='Requested by curator',
        )
        db.session.add(new_change_higher)
        db.session.flush()
        structural_changes_higher_id = new_change_higher.structural_changes_higher_id

        # Copy the original primary unit
        new_unit_id = copy_unit(unit_id_to_copy=primary_unit_id, user_id=user_id)
        new_change_basic = StructuralChangesBasic(
            structural_changes_higher_id=structural_changes_higher_id,
            collection_unit_id=new_unit_id,
            operation='create',
        )
        db.session.add(new_change_basic)
        db.session.flush()
        # Mark old units as not active
        for unit_id in unit_id_list:
            CollectionUnit.query.filter(
                CollectionUnit.collection_unit_id == unit_id
            ).update({'unit_active': 'no'})
            # Basic structural change
            change_ = StructuralChangesBasic(
                structural_changes_higher_id=structural_changes_higher_id,
                collection_unit_id=unit_id,
                operation='delete',
            )

        # Commit the transaction queries
        db.session.commit()
        return jsonify({'new_unit_id': new_unit_id, 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
