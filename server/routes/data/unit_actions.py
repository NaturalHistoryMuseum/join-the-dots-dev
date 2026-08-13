from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy import insert, select, update

from server.database import db
from server.models import (
    AssignedUnits,
    CollectionUnit,
    CollectionUnitMetric,
    RescoreSession,
    RescoreSessionUnits,
    StructuralChangesBasic,
    StructuralChangesHigher,
    UnitAssessmentCriterion,
    UnitAssessmentRank,
)
from server.models.utils import (
    CriteriaAssessmentEnum,
    HigherOperationEnum,
    OperationEnum,
)
from server.routes.data.utils import (
    add_structural_change,
    column_exists,
    complete_draft_unit,
    copy_unit,
    create_rescore_session,
    handle_draft_comment,
    handle_draft_metrics,
    handle_draft_rank,
    rescore_units_query,
)
from server.utils import (
    get_person_id,
)

from . import data_bp


@data_bp.route('/delete-units', methods=['POST'])
@jwt_required()
def delete_units():
    """
    Mark presented units as no longer being active.
    """
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

    for unit_id in unit_ids:
        db.session.execute(
            update(CollectionUnit)
            .where(
                CollectionUnit.collection_unit_id == unit_id,
                CollectionUnit.assigned_units.any(
                    AssignedUnits.user_id == user_id,
                ),
            )
            .values(
                unit_active='no',
            )
        )
        # Add the change to the structural changes log
        add_structural_change(
            person_id=person_id,
            higher_operation=HigherOperationEnum.delete,
            operation=OperationEnum.delete,
            collection_unit_id=unit_id,
            comment=justification,
            date=date_now,
        )
    # Commit the transaction queries
    db.session.commit()

    return jsonify({'message': 'Units deleted successfully'}), 200


@data_bp.route('/update-assessed-date', methods=['POST'])
@jwt_required()
def update_assessed_date():
    """
    Update the date the unit was last assessed to today.
    """
    data = request.get_json()
    unit_ids = data.get('unit_ids')
    date_now = datetime.now()

    # Update the assessed date
    db.session.execute(
        update(UnitAssessmentCriterion)
        .where(UnitAssessmentCriterion.collection_unit_id.in_(unit_ids))
        .values(
            date_assessed=date_now,
        )
    )
    db.session.commit()
    return jsonify(
        {'message': 'Assessed date updated successfully', 'success': True}
    ), 200


@data_bp.route('/submit-unit', methods=['POST'])
@jwt_required()
def submit_unit():
    """
    Submit new unit to the database.
    """
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

    result = db.session.execute(insert(CollectionUnit).values(**filter_unit_data))
    new_unit_id = result.lastrowid
    db.session.flush()

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
                db.session.execute(
                    insert(CollectionUnitMetric).values(
                        collection_unit_id=new_unit_id,
                        collection_unit_metric_definition_id=collection_unit_metric_definition_id,
                        metric_value=metric_value,
                        confidence_level=confidence_level,
                        date_from=date_now,
                        current='yes',
                    )
                )
                db.session.flush()
    # Handle ranks
    if ranks_json:
        for criterion in ranks_json:
            criterion_id = criterion[0]['criterion_id']
            # Add the criterion to the unit_assessment_criterion table
            # and get the new id
            result = db.session.execute(
                insert(UnitAssessmentCriterion).values(
                    collection_unit_id=new_unit_id,
                    criterion_id=criterion_id,
                    assessor_id=person_id,
                    date_assessed=date_now,
                    date_from=date_now,
                    current='yes',
                    criteria_assessment=CriteriaAssessmentEnum.known,
                )
            )
            db.session.flush()
            unit_assessment_criterion_id = result.lastrowid

            for rank in criterion:
                rank_id = rank['rank_id']
                percentage = rank['percentage']
                comment = rank['comment']
                db.session.execute(
                    insert(UnitAssessmentRank).values(
                        unit_assessment_criterion_id=unit_assessment_criterion_id,
                        rank_id=rank_id,
                        percentage=percentage,
                        comment=comment,
                    )
                )
    # Add the change to the structural changes log
    add_structural_change(
        person_id=person_id,
        higher_operation=HigherOperationEnum.create,
        operation=OperationEnum.create,
        collection_unit_id=new_unit_id,
        date=date_now,
    )

    # Commit the transaction queries
    db.session.commit()

    return jsonify({'collection_unit_id': new_unit_id, 'success': True})


@data_bp.route('/submit-draft-unit', methods=['POST'])
@jwt_required()
def submit_draft_unit():
    """
    Save new unit as a draft.
    """
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

    # Check if the draft is being insered or updated
    if insert_mode:
        # Filter the data to remove None values and the collection_unit_id
        filter_unit_data = {
            key: value
            for key, value in unit_data.items()
            if value is not None and key != 'collection_unit_id'
        }
        result = db.session.execute(insert(CollectionUnit).values(**filter_unit_data))
        unit_id = result.lastrowid
        db.session.flush()
        if unit_id is None:
            return jsonify({'error': 'Failed to create new unit'}), 500
        # Create the rescore session if we are adding the draft
        rescore_session_id, category_draft_ids = create_rescore_session(
            [unit_id], user_id
        )
        print(category_draft_ids)
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

        db.session.execute(
            update(CollectionUnit)
            .where(CollectionUnit.collection_unit_id == unit_id)
            .values(**filtered)
        )
        db.session.flush()
        # Create the rescore session if we are adding the draft
        category_draft_ids = None
        rescore_session_units_id = score_data.get('rescore_session_units_id')

    # Handle ranks
    if ranks_json:
        # Loop through all of the score changes
        for criterion_ranks in ranks_json:
            print(criterion_ranks)
            # Get the criterion_id for this score change
            criterion_id = criterion_ranks[0]['criterion_id']
            category_id = criterion_ranks[0]['category_id']
            print(criterion_id)
            print(category_id)
            # If rescore was just added
            if category_draft_ids is not None and len(category_draft_ids) > 0:
                # Find category_draft_id
                current_category = [
                    category
                    for category in category_draft_ids
                    if category.get('category_id') == category_id
                ]
                print('current_category')
                print(len(current_category))
                print((current_category))
                category_draft_id = current_category[0]['category_draft_id']
            elif category_tracking is not None and len(category_tracking) > 0:
                # Find category_draft_id
                current_category = [
                    category
                    for category in category_tracking
                    if category.get('category_id') == category_id
                ]
                print('category_tracking')
                print(len(category_tracking))
                print((category_tracking))
                category_draft_id = current_category[0]['category_draft_id']
            else:
                raise
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
        complete_draft_unit(unit_id, person_id)

    # Commit the transaction queries
    db.session.commit()

    return jsonify({'collection_unit_id': unit_id, 'success': True})


@data_bp.route('/draft-scores/<unit_id>', methods=['GET'])
@jwt_required()
def get_draft_scores(unit_id):
    """
    Get the scores of a draft unit that can be edited.
    """
    rescore_session = db.session.execute(
        select(RescoreSession).where(
            RescoreSession.status == 'in_progress',
            RescoreSession.rescore_session_units.any(
                RescoreSessionUnits.collection_unit_id == unit_id
            ),
        )
    ).scalar()
    if rescore_session is None:
        return jsonify({'error': 'No draft scores found for this unit'})
    rescore_session_id = rescore_session.rescore_session_id

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


@data_bp.route('/submit-field', methods=['POST'])
@jwt_required()
def submit_field():
    """
    Submit a unit metadata change dymanically with the field name and value.
    """
    data = request.get_json()
    field_name = data.get('field_name')
    new_value = data.get('new_value')
    collection_unit_id = data.get('collection_unit_id')

    if not field_name:
        return jsonify({'error': 'field_name is required'}), 400
    if not collection_unit_id:
        return jsonify({'error': 'collection_unit_id is required'}), 400

    if column_exists(column_name=field_name, table_name='collection_unit'):
        db.session.execute(
            update(CollectionUnit)
            .where(CollectionUnit.collection_unit_id == collection_unit_id)
            .values(**{field_name: new_value})
        )
        db.session.commit()
        return jsonify({'success': True})
    else:
        return jsonify({'error: column does not exist'}), 500


@data_bp.route('/split-unit', methods=['POST'])
@jwt_required()
def split_unit():
    """
    Split a unit into multiple new units and mark the original as not active.
    """
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

    # Add structural change entry
    result = db.session.execute(
        insert(StructuralChangesHigher).values(
            higher_operation=HigherOperationEnum.split,
            effective_date=date_now,
            change_agent_id=person_id,
            cause='Requested by curator',
        )
    )
    structural_changes_higher_id = result.lastrowid
    db.session.flush()

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
        db.session.execute(
            insert(StructuralChangesBasic).values(
                structural_changes_higher_id=structural_changes_higher_id,
                collection_unit_id=new_unit_id,
                operation=OperationEnum.create,
            )
        )
        db.session.flush()

    db.session.execute(
        update(CollectionUnit)
        .where(CollectionUnit.collection_unit_id == unit_id)
        .values(
            unit_active='no',
        )
    )
    # Basic structural change
    db.session.execute(
        insert(StructuralChangesBasic).values(
            structural_changes_higher_id=structural_changes_higher_id,
            collection_unit_id=unit_id,
            operation=OperationEnum.delete,
        )
    )
    # Commit the transaction queries
    db.session.commit()
    return jsonify({'new_units': new_units, 'success': True})


@data_bp.route('/combine-unit', methods=['POST'])
@jwt_required()
def combine_unit():
    """
    Combine multiple units into one single unit, it will only retain the data of the
    primary unit.
    """
    data = request.get_json()
    primary_unit_id = data.get('primary_unit_id')
    unit_id_list = data.get('unit_id_list')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    person_id = get_person_id(user_id)
    date_now = datetime.now()
    if not primary_unit_id:
        return jsonify({'error': 'primary_unit_id is required'}), 400

    # Add structural change entry
    result = db.session.execute(
        insert(StructuralChangesHigher).values(
            higher_operation=HigherOperationEnum.merge,
            effective_date=date_now,
            change_agent_id=person_id,
            cause='Requested by curator',
        )
    )
    db.session.flush()
    structural_changes_higher_id = result.lastrowid

    # Copy the original primary unit
    new_unit_id = copy_unit(unit_id_to_copy=primary_unit_id, user_id=user_id)
    db.session.execute(
        insert(StructuralChangesBasic).values(
            structural_changes_higher_id=structural_changes_higher_id,
            collection_unit_id=new_unit_id,
            operation=OperationEnum.create,
        )
    )
    db.session.flush()
    # Mark old units as not active
    for unit_id in unit_id_list:
        db.session.execute(
            update(CollectionUnit)
            .where(CollectionUnit.collection_unit_id == unit_id)
            .values(
                unit_active='no',
            )
        )
        # Basic structural change
        db.session.execute(
            insert(StructuralChangesBasic).values(
                structural_changes_higher_id=structural_changes_higher_id,
                collection_unit_id=unit_id,
                operation=OperationEnum.delete,
            )
        )

    # Commit the transaction queries
    db.session.commit()
    return jsonify({'new_unit_id': new_unit_id, 'success': True})
