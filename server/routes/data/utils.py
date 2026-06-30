from collections import defaultdict
from datetime import datetime

from flask import jsonify
from sqlalchemy import and_, delete, desc, insert, select, text

from server.config import Config
from server.database import db

# Data models
from server.models import (
    AssignedUnits,
    CollectionUnit,
    CollectionUnitMetric,
    RescoreSession,
    RescoreSessionUnits,
    StructuralChangesBasic,
    StructuralChangesComments,
    StructuralChangesHigher,
    UnitAssessmentCriterion,
    UnitAssessmentRank,
    UnitCategoryDraft,
    UnitComment,
    UnitCommentDraft,
    UnitMetricDraft,
    UnitRankDraft,
)

database_name = Config.MYSQL_DB


def create_rescore_session(units, user_id):
    """
    Create a rescore session by adding the session and adding the units to the session.

    It will then add category drafts for each of the units in the rescore.
    """
    try:
        # Insert session

        new_rescore_session = RescoreSession(user_id=user_id, status='in_progress')
        db.session.add(new_rescore_session)
        # adds new row but doesnt commit
        db.session.flush()

        # Get ID of last inserted row
        rescore_session_id = new_rescore_session.rescore_session_id
        # rescore_session_id = cursor.lastrowid

        category_ids = [0, 1, 2, 3, 4]
        category_draft_ids = []
        # Insert units into session
        for unit in units:
            new_rescore_session_units = RescoreSessionUnits(
                rescore_session_id=rescore_session_id, collection_unit_id=unit
            )
            db.session.add(new_rescore_session_units)
            # adds new row but doesnt commit
            db.session.flush()
            # Get ID of last inserted row
            rescore_session_units_id = (
                new_rescore_session_units.rescore_session_units_id
            )

            for category_id in category_ids:
                # Add new category draft
                new_unit_category_draft = UnitCategoryDraft(
                    rescore_session_units_id=rescore_session_units_id,
                    category_id=category_id,
                    complete=0,
                )
                db.session.add(new_unit_category_draft)
                db.session.flush()
                category_draft_id = new_unit_category_draft.category_draft_id

                category_draft_ids.append(
                    {
                        'category_id': category_id,
                        'category_draft_id': category_draft_id,
                        'rescore_session_units_id': rescore_session_units_id,
                    }
                )

        return (rescore_session_id, category_draft_ids)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


def complete_draft_unit(unit_id, user_id, person_id):
    """
    Remove draft tag and upgrade the data points (scores, metrics, comment) from drafts.
    """
    try:
        # Get the rescore_session_id
        rescore_session = RescoreSession.query.filter(
            RescoreSession.rescore_session_units.any(
                RescoreSessionUnits.collection_unit.has(
                    CollectionUnit.collection_unit_id == unit_id
                )
            )
        ).first()
        rescore_session_id = rescore_session.rescore_session_id

        unit = CollectionUnit.query.filter(
            CollectionUnit.collection_unit_id == unit_id
        ).update({'draft_unit': 0})
        db.session.flush()

        # Submit draft comments
        upgrade_draft_comments(rescore_session_id)

        # Submit draft metrics
        upgrade_draft_metrics(rescore_session_id)

        # Submit draft ranks
        upgrade_draft_ranks(rescore_session_id, person_id)

        # Close the rescore and remove draft categories
        close_rescore(rescore_session_id)

    except Exception as e:
        raise


def column_exists(table_name, column_name):
    try:
        data = db.session.execute(
            text(f"""
            SELECT COUNT(*) as count
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE table_schema = '{database_name}' AND table_name = :table_name AND column_name = :column_name
            """),
            {'table_name': table_name, 'column_name': column_name},
        ).fetchone()

        field_is_valid = True if data.count == 1 else False
        return field_is_valid
    except Exception as e:
        raise


def copy_unit(unit_id_to_copy, user_id, unit_name_addition=''):
    """
    Duplicate all aspects of a unit.
    """
    # Create a new unit

    original_unit = CollectionUnit.query.filter(
        CollectionUnit.collection_unit_id == unit_id_to_copy
    ).first()
    db.session.flush()
    # create new unit
    new_unit = CollectionUnit(
        unit_name=original_unit.unit_name + unit_name_addition,
        public_unit_name=original_unit.public_unit_name,
        section_id=original_unit.section_id,
        unit_active=original_unit.unit_active,
        responsible_curator_id=original_unit.responsible_curator_id,
        curatorial_unit_definition_id=original_unit.curatorial_unit_definition_id,
        storage_room_id=original_unit.storage_room_id,
        storage_container_id=original_unit.storage_container_id,
        geographic_origin_id=original_unit.geographic_origin_id,
        library_and_archives_function_id=original_unit.library_and_archives_function_id,
        geological_time_period_from_id=original_unit.geological_time_period_from_id,
        geological_time_period_to_id=original_unit.geological_time_period_to_id,
        type_collection_flag=original_unit.type_collection_flag,
        publish_flag=original_unit.publish_flag,
        informal_taxon=original_unit.informal_taxon,
        named_collection=original_unit.named_collection,
        es_recent_specimen_flag=original_unit.es_recent_specimen_flag,
        archives_fond_ref=original_unit.archives_fond_ref,
        count_curatorial_units_flag=original_unit.count_curatorial_units_flag,
        sort_order=original_unit.sort_order,
        taxon_id=original_unit.taxon_id,
        draft_unit=original_unit.draft_unit,
    )
    db.session.add(new_unit)
    db.session.flush()

    new_unit_id = new_unit.collection_unit_id

    # Assign unit to current user
    new_assignment = AssignedUnits(user_id=user_id, collection_unit_id=new_unit_id)
    db.session.add(new_assignment)

    # Insert the comment
    original_unit_comment = (
        UnitComment.query.filter(UnitComment.collection_unit_id == unit_id_to_copy)
        .order_by(desc(UnitComment.unit_comment_id))
        .first()
    )

    if original_unit_comment:
        new_unit_comment = UnitComment(
            collection_unit_id=new_unit_id,
            unit_comment=original_unit_comment.unit_comment,
            date_added=original_unit_comment.date_added,
        )
        db.session.add(new_unit_comment)

    # Select the current assessment criterion
    criteria_to_copy = UnitAssessmentCriterion.query.filter(
        UnitAssessmentCriterion.collection_unit_id == unit_id_to_copy,
        UnitAssessmentCriterion.current == 'yes',
    ).all()

    # Go through each criterion
    for criterion in criteria_to_copy:
        # Insert the current criterion
        new_uac = UnitAssessmentCriterion(
            collection_unit_id=new_unit_id,
            criterion_id=criterion.criterion_id,
            assessor_id=criterion.assessor_id,
            criteria_assessment=criterion.criteria_assessment,
            date_assessed=criterion.date_assessed,
            date_from=criterion.date_from,
            date_to=criterion.date_to,
            current=criterion.current,
        )
        db.session.add(new_uac)
        db.session.flush()

        # Get the last id
        new_criterion_id = new_uac.unit_assessment_criterion_id

        # Copy ranks belonging to this criterion
        existing_ranks = UnitAssessmentRank.query.filter(
            UnitAssessmentRank.unit_assessment_criterion_id
            == criterion.unit_assessment_criterion_id
        ).all()
        db.session.flush()
        for rank in existing_ranks:
            new_rank = UnitAssessmentRank(
                unit_assessment_criterion_id=new_criterion_id,
                rank_id=rank.rank_id,
                percentage=rank.percentage,
                comment=rank.comment,
            )
            db.session.add(new_rank)

    # Insert Unit Metrics
    existing_metrics = CollectionUnitMetric.query.filter(
        CollectionUnitMetric.collection_unit_id == unit_id_to_copy,
        CollectionUnitMetric.current == 'yes',
    ).all()
    db.session.flush()
    for metric in existing_metrics:
        new_metric = CollectionUnitMetric(
            collection_unit_id=new_unit_id,
            collection_unit_metric_definition_id=metric.collection_unit_metric_definition_id,
            metric_value=metric.metric_value,
            confidence_level=metric.confidence_level,
            date_from=metric.date_from,
            date_to=metric.date_to,
            current=metric.current,
        )
        db.session.add(new_metric)

    return new_unit_id


def close_rescore(rescore_session_id):
    """
    Mark a rescore session as completed.
    """
    # Remove draft categories
    UnitCategoryDraft.query.filter(
        UnitCategoryDraft.rescore_session_units.has(
            RescoreSessionUnits.rescore_session.has(
                and_(
                    RescoreSession.rescore_session_id == rescore_session_id,
                    RescoreSession.status == 'in_progress',
                )
            )
        )
    ).delete()
    # Close the rescore session
    completed_at = datetime.now()
    RescoreSession.query.filter(
        RescoreSession.rescore_session_id == rescore_session_id
    ).update({'status': 'complete', 'completed_at': completed_at})
    db.session.flush()


def upgrade_draft_comments(rescore_session_id):
    """
    Duplicate comments from the draft table to the main table.

    Remove draft comment.
    """
    # Insert comments
    date_added = datetime.now()
    existing_unit_comment_drafts = UnitCommentDraft.query.filter(
        UnitCommentDraft.rescore_session_units.has(
            RescoreSessionUnits.rescore_session.has(
                and_(
                    RescoreSession.rescore_session_id == rescore_session_id,
                    RescoreSession.status == 'in_progress',
                )
            )
        )
    ).all()

    for comment in existing_unit_comment_drafts:
        new_comment = UnitComment(
            collection_unit_id=comment.rescore_session_units.collection_unit_id,
            unit_comment=comment.unit_comment,
            date_added=date_added,
        )
        db.session.add(new_comment)

    # Remove draft comments
    UnitCommentDraft.query.filter(
        UnitCommentDraft.rescore_session_units.has(
            RescoreSessionUnits.rescore_session.has(
                and_(
                    RescoreSession.rescore_session_id == rescore_session_id,
                    RescoreSession.status == 'in_progress',
                )
            )
        )
    ).delete()


def upgrade_draft_metrics(rescore_session_id):
    """
    Duplicate metrics from the draft table to the main table.

    Remove draft metrics.
    """
    # Set old metrics that are about to be inserted as not current
    date_now = datetime.now()
    # Get the draft metrics
    draft_unit_metrics = UnitMetricDraft.query.filter(
        UnitMetricDraft.rescore_session_units.has(
            RescoreSessionUnits.rescore_session.has(
                and_(
                    RescoreSession.status == 'in_progress',
                    RescoreSession.rescore_session_id == rescore_session_id,
                )
            )
        )
    ).all()
    for metric_draft in draft_unit_metrics:
        # Set old metrics that are about to be inserted as not current
        CollectionUnitMetric.query.filter(
            CollectionUnitMetric.collection_unit_id
            == metric_draft.rescore_session_units.collection_unit_id,
            CollectionUnitMetric.collection_unit_metric_definition_id
            == metric_draft.collection_unit_metric_definition_id,
            CollectionUnitMetric.current == 'yes',
        ).update({'current': 'no', 'date_to': date_now})

        # Insert metrics from drafts
        new_metrics = CollectionUnitMetric(
            collection_unit_id=metric_draft.rescore_session_units.collection_unit_id,
            collection_unit_metric_definition_id=metric_draft.collection_unit_metric_definition_id,
            metric_value=metric_draft.metric_value,
            confidence_level=metric_draft.confidence_level,
            date_from=date_now,
            current='yes',
        )
        db.session.add(new_metrics)
        # Remove draft metrics
        db.session.delete(metric_draft)


def upgrade_draft_ranks(rescore_session_id, person_id):
    """
    Duplicate ranks from the draft table to the main table.

    Remove draft ranks.
    """
    # Set old ranks that are about to be inserted as not current
    date_now = datetime.now()
    # Get the draft ranks
    draft_rows = UnitRankDraft.query.filter(
        UnitRankDraft.unit_category_draft.has(
            UnitCategoryDraft.rescore_session_units.has(
                RescoreSessionUnits.rescore_session.has(
                    and_(
                        RescoreSession.status == 'in_progress',
                        RescoreSession.rescore_session_id == rescore_session_id,
                    )
                )
            )
        )
    ).all()

    for draft_rank in draft_rows:
        # Set old ranks that are about to be inserted as not current
        UnitAssessmentCriterion.query.filter(
            UnitAssessmentCriterion.collection_unit_id
            == draft_rank.unit_category_draft.rescore_session_units.collection_unit_id,
            UnitAssessmentCriterion.criterion_id == draft_rank.criterion_id,
        ).update({'current': 'no', 'date_to': date_now})

    # Group rows by collection_unit_id and criterion_id
    grouped_assessment = defaultdict(list)
    for row in draft_rows:
        key = (
            row.unit_category_draft.rescore_session_units.collection_unit_id,
            row.criterion_id,
        )
        grouped_assessment[key].append(row)
    # Insert assessment_criterion rows
    inserted_ids = {}
    for (
        collection_unit_id,
        criterion_id,
    ), group_rows in grouped_assessment.items():
        new_criterion = UnitAssessmentCriterion(
            collection_unit_id=collection_unit_id,
            criterion_id=criterion_id,
            assessor_id=person_id,
            date_assessed=date_now,
            date_from=date_now,
            current='yes',
        )
        db.session.add(new_criterion)
        db.session.flush()
        inserted_id = new_criterion.unit_assessment_criterion_id

        inserted_ids[(collection_unit_id, criterion_id)] = inserted_id

    # Insert all ranks referencing the correct assessment_criterion_id
    for row in draft_rows:
        criterion_key = (
            row.unit_category_draft.rescore_session_units.collection_unit_id,
            row.criterion_id,
        )
        assessment_criterion_id = inserted_ids[criterion_key]

        new_rank = UnitAssessmentRank(
            unit_assessment_criterion_id=assessment_criterion_id,
            rank_id=row.rank_id,
            percentage=row.percentage,
            comment=row.comment,
        )
        db.session.add(new_rank)
        db.session.flush()
        # Delete draft rank
        db.session.delete(row)


def add_structural_change(
    person_id, higher_operation, operation, collection_unit_id, date, comment=None
):
    """
    Insert new structural change to the relevant tables.
    """
    # Add structural change entry
    new_change_higher = StructuralChangesHigher(
        higher_operation=higher_operation,
        effective_date=date,
        change_agent_id=person_id,
        cause='Requested by curator',
    )
    db.session.add(new_change_higher)
    db.session.flush()
    structural_changes_higher_id = new_change_higher.structural_changes_higher_id

    # Basic structural change
    new_change_basic = StructuralChangesBasic(
        structural_changes_higher_id=structural_changes_higher_id,
        collection_unit_id=collection_unit_id,
        operation=operation,
    )
    db.session.add(new_change_basic)
    db.session.flush()
    if comment:
        new_change_comments = StructuralChangesComments(
            structural_changes_higher_id=structural_changes_higher_id,
            comment=comment,
            date_added=date,
        )
        db.session.add(new_change_comments)
        db.session.flush()


def handle_draft_rank(criterion_id, ranks, category_draft_id, insert_only=False):
    """
    Save draft rank changes.

    It will insert a new row if none exists or update if it does.
    """
    try:
        # Only check if it exists if we dont know if we need to insert - saves time
        if not insert_only:
            data = UnitRankDraft.query.filter(
                UnitRankDraft.criterion_id == criterion_id,
                UnitRankDraft.category_draft_id == category_draft_id,
            ).all()
        # Loop through the ranks and update or insert them
        for sumbit_rank in ranks:
            in_db = False
            rank_id = sumbit_rank['rank_id']
            percentage = sumbit_rank['percentage']
            comment = sumbit_rank['comment']
            if not insert_only and data is not None:
                # Check if the rank already exists in the database and update it if it does
                for db_rank in data:
                    if db_rank.rank_id == sumbit_rank['rank_id']:
                        updated_at = datetime.now()
                        UnitRankDraft.query.filter(
                            UnitRankDraft.category_draft_id == category_draft_id,
                            UnitRankDraft.criterion_id == criterion_id,
                            UnitRankDraft.rank_id == rank_id,
                        ).update(
                            {
                                'percentage': percentage,
                                'comment': comment,
                                'updated_at': updated_at,
                            }
                        )
                        in_db = True

            # If the rank does not exist, insert it
            if not in_db:
                new_rank_draft = UnitRankDraft(
                    category_draft_id=category_draft_id,
                    criterion_id=criterion_id,
                    rank_id=rank_id,
                    percentage=percentage,
                    comment=comment,
                )

                db.session.add(new_rank_draft)
        db.session.flush()
        return jsonify(
            {'message': 'Draft rank submitted successfully', 'success': True}
        )

    except Exception as e:
        raise


def handle_draft_metrics(rescore_session_units_id, metric_json):
    """
    Save draft metrics changes.

    It will insert a new row if none exists or update if it does.
    """
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

                existing_metric = UnitMetricDraft.query.filter(
                    UnitMetricDraft.rescore_session_units_id
                    == rescore_session_units_id,
                    UnitMetricDraft.collection_unit_metric_definition_id
                    == collection_unit_metric_definition_id,
                ).first()
                if existing_metric:
                    updated_at = datetime.now()
                    existing_metric.metric_value = metric_value
                    existing_metric.confidence_level = confidence_level
                    existing_metric.updated_at = updated_at
                    db.session.flush()
                else:
                    new_metric_draft = UnitMetricDraft(
                        rescore_session_units_id=rescore_session_units_id,
                        collection_unit_metric_definition_id=collection_unit_metric_definition_id,
                        metric_value=metric_value,
                        confidence_level=confidence_level,
                    )
                    db.session.add(new_metric_draft)
                    db.session.flush()
        return jsonify({'message': 'Draft metrics submitted successfully'})

    except Exception as e:
        raise


def handle_draft_comment(rescore_session_units_id, unit_comment):
    """
    Save draft comment changes.

    It will insert a new row if none exists or update if it does.
    """
    try:
        existing_comment = UnitCommentDraft.query.filter(
            UnitCommentDraft.rescore_session_units_id == rescore_session_units_id
        ).first()
        if existing_comment:
            # If a comment already exists, update it
            updated_at = datetime.now()
            existing_comment.unit_comment = unit_comment
            existing_comment.updated_at = updated_at
        else:
            # If no comment exists, insert a new one
            new_comment_draft = UnitCommentDraft(
                rescore_session_units_id=rescore_session_units_id,
                unit_comment=unit_comment,
            )
            db.session.add(new_comment_draft)
        db.session.flush()
    except Exception as e:
        raise


def update_unit_assigned(unit_id, assigned_users):
    """
    Update the user assigned to a unit.
    """
    # Get the current assigned users
    query = select(AssignedUnits).where(AssignedUnits.collection_unit_id == unit_id)
    current_assigned = db.session.execute(query).scalars().all()

    current_assigned = set(
        row.user_id for row in current_assigned
    )  # if fetch_data returns dicts
    assigned_users = set(int(user) for user in assigned_users)
    # Compare lists
    users_to_add = assigned_users - current_assigned
    users_to_remove = current_assigned - assigned_users
    # Insert new assigned users
    if users_to_add:
        for user_id in users_to_add:
            insert_query = insert(AssignedUnits).values(
                user_id=user_id, collection_unit_id=unit_id
            )
            db.session.execute(insert_query)
    # Remove unassigned users
    if users_to_remove:
        for user_id in users_to_remove:
            delete_query = delete(AssignedUnits).where(
                AssignedUnits.collection_unit_id == unit_id,
                AssignedUnits.user_id == user_id,
            )
            db.session.execute(delete_query)
