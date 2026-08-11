from collections import defaultdict
from datetime import datetime

from flask import jsonify
from sqlalchemy import (
    and_,
    delete,
    desc,
    exists,
    func,
    insert,
    literal,
    null,
    select,
    text,
    update,
)

from server.config import Config
from server.database import db

# Data models
from server.models import (
    AssignedUnits,
    CollectionUnit,
    CollectionUnitMetric,
    CollectionUnitMetricDefinition,
    CuratorialUnitDefinition,
    Division,
    Rank,
    RescoreSession,
    RescoreSessionUnits,
    Section,
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
    Users,
)
from server.models.utils import StatusEnum

database_name = Config.MYSQL_DB


def create_rescore_session(units, user_id):
    """
    Create a rescore session by adding the session and adding the units to the session.

    It will then add category drafts for each of the units in the rescore.
    """
    # Insert session
    new_rescore_session = db.session.execute(
        insert(RescoreSession).values(
            user_id=user_id, status=StatusEnum.in_progress, completed_at=None
        )
    )
    # Get ID of last inserted row
    rescore_session_id = new_rescore_session.lastrowid
    # adds new row but doesnt commit
    db.session.flush()

    category_ids = [0, 1, 2, 3, 4]
    category_draft_ids = []
    # Insert units into session
    for unit in units:
        result = db.session.execute(
            insert(RescoreSessionUnits).values(
                rescore_session_id=rescore_session_id, collection_unit_id=unit
            )
        )
        # Get ID of last inserted row
        rescore_session_units_id = result.lastrowid
        # adds new row but doesnt commit
        db.session.flush()

        for category_id in category_ids:
            # Add new category draft
            result = db.session.execute(
                insert(UnitCategoryDraft).values(
                    rescore_session_units_id=rescore_session_units_id,
                    category_id=category_id,
                    complete=0,
                )
            )
            category_draft_id = result.lastrowid
            db.session.flush()

            category_draft_ids.append(
                {
                    'category_id': category_id,
                    'category_draft_id': category_draft_id,
                    'rescore_session_units_id': rescore_session_units_id,
                }
            )

    return (rescore_session_id, category_draft_ids)


def complete_draft_unit(unit_id, person_id):
    """
    Remove draft tag and upgrade the data points (scores, metrics, comment) from drafts.
    """
    # Get the rescore_session_id
    rescore_session = db.session.execute(
        select(RescoreSession).filter(
            RescoreSession.rescore_session_units.any(
                RescoreSessionUnits.collection_unit.has(
                    CollectionUnit.collection_unit_id == unit_id
                )
            )
        )
    ).scalar()
    if rescore_session:
        rescore_session_id = rescore_session.rescore_session_id

        db.session.execute(
            update(CollectionUnit)
            .where(CollectionUnit.collection_unit_id == unit_id)
            .values(
                draft_unit='no',
            )
        )
        db.session.flush()

        # Submit draft comments
        upgrade_draft_comments(rescore_session_id)

        # Submit draft metrics
        upgrade_draft_metrics(rescore_session_id)

        # Submit draft ranks
        upgrade_draft_ranks(rescore_session_id, person_id)

        # Close the rescore and remove draft categories
        close_rescore(rescore_session_id)


def column_exists(table_name, column_name):
    """
    Check if a column exists in a table in the database.
    """
    data = db.session.execute(
        text(f"""
        SELECT COUNT(*) as count
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE table_schema = '{database_name}'
            AND table_name = :table_name
            AND column_name = :column_name
        """),
        {'table_name': table_name, 'column_name': column_name},
    ).fetchone()

    field_is_valid = True if data and data.count == 1 else False
    return field_is_valid


def copy_unit(unit_id_to_copy, user_id, unit_name_addition=''):
    """
    Duplicate all aspects of a unit.
    """
    # Create a new unit
    original_unit = db.session.execute(
        select(CollectionUnit).filter(
            CollectionUnit.collection_unit_id == unit_id_to_copy
        )
    ).scalar()

    if original_unit is None:
        return None

    db.session.flush()
    # create new unit
    result = db.session.execute(
        insert(CollectionUnit).values(
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
    )
    new_unit_id = result.lastrowid
    db.session.flush()

    # Assign unit to current user
    db.session.execute(
        insert(AssignedUnits).values(user_id=user_id, collection_unit_id=new_unit_id)
    )

    # Insert the comment
    original_unit_comment = db.session.execute(
        select(UnitComment)
        .filter(UnitComment.collection_unit_id == unit_id_to_copy)
        .order_by(desc(UnitComment.unit_comment_id))
    ).scalar()

    if original_unit_comment:
        db.session.execute(
            insert(UnitComment).values(
                collection_unit_id=new_unit_id,
                unit_comment=original_unit_comment.unit_comment,
                date_added=original_unit_comment.date_added,
            )
        )

    # Select the current assessment criterion
    criteria_to_copy = (
        db.session.execute(
            select(UnitAssessmentCriterion).filter(
                UnitAssessmentCriterion.collection_unit_id == unit_id_to_copy,
                UnitAssessmentCriterion.current == 'yes',
            )
        )
        .scalars()
        .all()
    )

    # Go through each criterion
    for criterion in criteria_to_copy:
        # Insert the current criterion
        result = db.session.execute(
            insert(UnitAssessmentCriterion).values(
                collection_unit_id=new_unit_id,
                criterion_id=criterion.criterion_id,
                assessor_id=criterion.assessor_id,
                criteria_assessment=criterion.criteria_assessment,
                date_assessed=criterion.date_assessed,
                date_from=criterion.date_from,
                date_to=criterion.date_to,
                current=criterion.current,
            )
        )
        # Get the last id
        new_criterion_id = result.lastrowid
        db.session.flush()

        # Copy ranks belonging to this criterion
        existing_ranks = (
            db.session.execute(
                select(UnitAssessmentRank).filter(
                    UnitAssessmentRank.unit_assessment_criterion_id
                    == criterion.unit_assessment_criterion_id
                )
            )
            .scalars()
            .all()
        )
        db.session.flush()
        for rank in existing_ranks:
            db.session.execute(
                insert(UnitAssessmentRank).values(
                    unit_assessment_criterion_id=new_criterion_id,
                    rank_id=rank.rank_id,
                    percentage=rank.percentage,
                    comment=rank.comment,
                )
            )

    # Insert Unit Metrics
    existing_metrics = (
        db.session.execute(
            select(CollectionUnitMetric).filter(
                CollectionUnitMetric.collection_unit_id == unit_id_to_copy,
                CollectionUnitMetric.current == 'yes',
            )
        )
        .scalars()
        .all()
    )
    db.session.flush()
    for metric in existing_metrics:
        db.session.execute(
            insert(CollectionUnitMetric).values(
                collection_unit_id=new_unit_id,
                collection_unit_metric_definition_id=metric.collection_unit_metric_definition_id,
                metric_value=metric.metric_value,
                confidence_level=metric.confidence_level,
                date_from=metric.date_from,
                date_to=metric.date_to,
                current=metric.current,
            )
        )

    return new_unit_id


def close_rescore(rescore_session_id):
    """
    Mark a rescore session as completed.
    """
    # Remove draft categories
    db.session.execute(
        delete(UnitCategoryDraft).where(
            UnitCategoryDraft.rescore_session_units.has(
                RescoreSessionUnits.rescore_session.has(
                    and_(
                        RescoreSession.rescore_session_id == rescore_session_id,
                        RescoreSession.status == 'in_progress',
                    )
                )
            )
        )
    )
    # Close the rescore session
    completed_at = datetime.now()

    db.session.execute(
        update(RescoreSession)
        .where(RescoreSession.rescore_session_id == rescore_session_id)
        .values(
            status=StatusEnum.complete,
            completed_at=completed_at,
        )
    )
    db.session.flush()


def upgrade_draft_comments(rescore_session_id):
    """
    Duplicate comments from the draft table to the main table.

    Remove draft comment.
    """
    # Insert comments
    date_added = datetime.now()
    existing_unit_comment_drafts = (
        db.session.execute(
            select(UnitCommentDraft).filter(
                UnitCommentDraft.rescore_session_units.has(
                    RescoreSessionUnits.rescore_session.has(
                        and_(
                            RescoreSession.rescore_session_id == rescore_session_id,
                            RescoreSession.status == 'in_progress',
                        )
                    )
                )
            )
        )
        .scalars()
        .all()
    )

    for comment in existing_unit_comment_drafts:
        db.session.execute(
            insert(UnitComment).values(
                collection_unit_id=comment.rescore_session_units.collection_unit_id,
                unit_comment=comment.unit_comment,
                date_added=date_added,
            )
        )

    # Remove draft comments
    db.session.execute(
        delete(UnitCategoryDraft).where(
            UnitCategoryDraft.rescore_session_units.has(
                RescoreSessionUnits.rescore_session.has(
                    and_(
                        RescoreSession.rescore_session_id == rescore_session_id,
                        RescoreSession.status == 'in_progress',
                    )
                )
            )
        )
    )


def upgrade_draft_metrics(rescore_session_id):
    """
    Duplicate metrics from the draft table to the main table.

    Remove draft metrics.
    """
    # Set old metrics that are about to be inserted as not current
    date_now = datetime.now()
    # Get the draft metrics
    draft_unit_metrics = (
        db.session.execute(
            select(UnitMetricDraft).filter(
                UnitMetricDraft.rescore_session_units.has(
                    RescoreSessionUnits.rescore_session.has(
                        and_(
                            RescoreSession.status == 'in_progress',
                            RescoreSession.rescore_session_id == rescore_session_id,
                        )
                    )
                )
            )
        )
        .scalars()
        .all()
    )
    for metric_draft in draft_unit_metrics:
        # Set old metrics that are about to be inserted as not current
        db.session.execute(
            update(CollectionUnitMetric)
            .where(
                CollectionUnitMetric.collection_unit_id
                == metric_draft.rescore_session_units.collection_unit_id,
                CollectionUnitMetric.collection_unit_metric_definition_id
                == metric_draft.collection_unit_metric_definition_id,
                CollectionUnitMetric.current == 'yes',
            )
            .values(
                current='no',
                date_to=date_now,
            )
        )
        db.session.flush()
        # Insert metrics from drafts
        db.session.execute(
            insert(CollectionUnitMetric).values(
                collection_unit_id=metric_draft.rescore_session_units.collection_unit_id,
                collection_unit_metric_definition_id=metric_draft.collection_unit_metric_definition_id,
                metric_value=metric_draft.metric_value,
                confidence_level=metric_draft.confidence_level,
                date_from=date_now,
                current='yes',
            )
        )
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
    draft_rows = (
        db.session.execute(
            select(UnitRankDraft).filter(
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
            )
        )
        .scalars()
        .all()
    )

    for draft_rank in draft_rows:
        # Set old ranks that are about to be inserted as not current
        db.session.execute(
            update(UnitAssessmentCriterion)
            .where(
                UnitAssessmentCriterion.collection_unit_id
                == draft_rank.unit_category_draft.rescore_session_units.collection_unit_id,
                UnitAssessmentCriterion.criterion_id == draft_rank.criterion_id,
            )
            .values(
                current='no',
                date_to=date_now,
            )
        )

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
        result = db.session.execute(
            insert(UnitAssessmentCriterion).values(
                collection_unit_id=collection_unit_id,
                criterion_id=criterion_id,
                assessor_id=person_id,
                date_assessed=date_now,
                date_from=date_now,
                current='yes',
            )
        )
        inserted_id = result.lastrowid
        db.session.flush()

        inserted_ids[(collection_unit_id, criterion_id)] = inserted_id

    # Insert all ranks referencing the correct assessment_criterion_id
    for row in draft_rows:
        criterion_key = (
            row.unit_category_draft.rescore_session_units.collection_unit_id,
            row.criterion_id,
        )
        assessment_criterion_id = inserted_ids[criterion_key]

        db.session.execute(
            insert(UnitAssessmentRank).values(
                unit_assessment_criterion_id=assessment_criterion_id,
                rank_id=row.rank_id,
                percentage=row.percentage,
                comment=row.comment,
            )
        )
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
    result = db.session.execute(
        insert(StructuralChangesHigher).values(
            higher_operation=higher_operation,
            effective_date=date,
            change_agent_id=person_id,
            cause='Requested by curator',
        )
    )
    structural_changes_higher_id = result.lastrowid
    db.session.flush()

    # Basic structural change
    db.session.execute(
        insert(StructuralChangesBasic).values(
            structural_changes_higher_id=structural_changes_higher_id,
            collection_unit_id=collection_unit_id,
            operation=operation,
        )
    )
    db.session.flush()
    if comment:
        db.session.execute(
            insert(StructuralChangesComments).values(
                structural_changes_higher_id=structural_changes_higher_id,
                comment=comment,
                date_added=date,
            )
        )
        db.session.flush()


def handle_draft_rank(criterion_id, ranks, category_draft_id, insert_only=False):
    """
    Save draft rank changes.

    It will insert a new row if none exists or update if it does.
    """
    try:
        data = None
        # Only check if it exists if we dont know if we need to insert - saves time
        if not insert_only:
            data = (
                db.session.execute(
                    select(UnitRankDraft).filter(
                        UnitRankDraft.criterion_id == criterion_id,
                        UnitRankDraft.category_draft_id == category_draft_id,
                    )
                )
                .scalars()
                .all()
            )

        # Loop through the ranks and update or insert them
        for sumbit_rank in ranks:
            in_db = False
            rank_id = sumbit_rank['rank_id']
            percentage = sumbit_rank['percentage']
            comment = sumbit_rank['comment']
            if not insert_only and data is not None:
                # Check if the rank already exists in the
                # database and update it if it does
                for db_rank in data:
                    if db_rank.rank_id == sumbit_rank['rank_id']:
                        updated_at = datetime.now()

                        db.session.execute(
                            update(UnitRankDraft)
                            .where(
                                UnitRankDraft.category_draft_id == category_draft_id,
                                UnitRankDraft.criterion_id == criterion_id,
                                UnitRankDraft.rank_id == rank_id,
                            )
                            .values(
                                percentage=percentage,
                                comment=comment,
                                updated_at=updated_at,
                            )
                        )
                        in_db = True

            # If the rank does not exist, insert it
            if not in_db:
                db.session.execute(
                    insert(UnitRankDraft).values(
                        category_draft_id=category_draft_id,
                        criterion_id=criterion_id,
                        rank_id=rank_id,
                        percentage=percentage,
                        comment=comment,
                    )
                )
        db.session.flush()
        return jsonify(
            {'message': 'Draft rank submitted successfully', 'success': True}
        )

    except Exception:
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
                existing_metric = db.session.execute(
                    select(UnitMetricDraft).filter(
                        UnitMetricDraft.rescore_session_units_id
                        == rescore_session_units_id,
                        UnitMetricDraft.collection_unit_metric_definition_id
                        == collection_unit_metric_definition_id,
                    )
                ).scalar()
                if existing_metric:
                    updated_at = datetime.now()
                    if metric_value is not None:
                        existing_metric.metric_value = metric_value
                    if confidence_level is not None:
                        existing_metric.confidence_level = confidence_level
                    existing_metric.updated_at = updated_at
                    db.session.flush()
                else:
                    db.session.execute(
                        insert(UnitMetricDraft).values(
                            rescore_session_units_id=rescore_session_units_id,
                            collection_unit_metric_definition_id=collection_unit_metric_definition_id,
                            metric_value=metric_value,
                            confidence_level=confidence_level,
                        )
                    )
                    db.session.flush()
        return jsonify({'message': 'Draft metrics submitted successfully'})

    except Exception:
        raise


def handle_draft_comment(rescore_session_units_id, unit_comment):
    """
    Save draft comment changes.

    It will insert a new row if none exists or update if it does.
    """
    existing_comment = db.session.execute(
        select(UnitCommentDraft).filter(
            UnitCommentDraft.rescore_session_units_id == rescore_session_units_id
        )
    ).scalar()
    if existing_comment:
        # If a comment already exists, update it
        updated_at = datetime.now()
        existing_comment.unit_comment = unit_comment
        existing_comment.updated_at = updated_at
    else:
        # If no comment exists, insert a new one
        db.session.execute(
            insert(UnitCommentDraft).values(
                rescore_session_units_id=rescore_session_units_id,
                unit_comment=unit_comment,
            )
        )
    db.session.flush()


def update_unit_assigned(unit_id, assigned_users):
    """
    Update the user assigned to a unit.
    """
    # Get the current assigned users
    query = select(AssignedUnits).where(AssignedUnits.collection_unit_id == unit_id)
    current_assigned = db.session.execute(query).scalars().all()

    current_assigned = set(row.user_id for row in current_assigned)
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


def rescore_units_query(rescore_session_id):
    """
    Get rescore units with their metrics, comments and ranks for a given rescore
    session.
    """
    # metrics subquery
    draft_metrics_query = select(
        null().label('collection_unit_metric_id'),
        UnitMetricDraft.metric_value,
        UnitMetricDraft.confidence_level,
        null().label('date_from'),
        UnitMetricDraft.collection_unit_metric_definition_id,
        literal(True).label('is_draft'),
    ).where(
        UnitMetricDraft.rescore_session_units_id
        == RescoreSessionUnits.rescore_session_units_id
    )

    real_metrics_query = select(
        CollectionUnitMetric.collection_unit_metric_id,
        CollectionUnitMetric.metric_value,
        CollectionUnitMetric.confidence_level,
        func.date(CollectionUnitMetric.date_from).label('date_from'),
        CollectionUnitMetric.collection_unit_metric_definition_id,
        literal(False).label('is_draft'),
    ).where(
        CollectionUnitMetric.collection_unit_id == CollectionUnit.collection_unit_id,
        CollectionUnitMetric.current == 'yes',
        ~exists(
            select(1).where(
                UnitMetricDraft.rescore_session_units_id
                == RescoreSessionUnits.rescore_session_units_id,
                UnitMetricDraft.collection_unit_metric_definition_id
                == CollectionUnitMetric.collection_unit_metric_definition_id,
            )
        ),
    )

    metrics = draft_metrics_query.union(real_metrics_query).subquery('metrics')

    metric_subquery = (
        select(
            func.JSON_ARRAYAGG(
                func.JSON_OBJECT(
                    'collection_unit_metric_id',
                    metrics.c.collection_unit_metric_id,
                    'metric_value',
                    metrics.c.metric_value,
                    'confidence_level',
                    metrics.c.confidence_level,
                    'date_from',
                    func.date(metrics.c.date_from),
                    'metric_name',
                    CollectionUnitMetricDefinition.metric_name,
                    'metric_definition',
                    CollectionUnitMetricDefinition.metric_definition,
                    'metric_units',
                    CollectionUnitMetricDefinition.metric_units,
                    'metric_datatype',
                    CollectionUnitMetricDefinition.metric_datatype,
                    'collection_unit_metric_definition_id',
                    metrics.c.collection_unit_metric_definition_id,
                )
            )
        )
        .select_from(metrics)
        .join(
            CollectionUnitMetricDefinition,
            metrics.c.collection_unit_metric_definition_id
            == CollectionUnitMetricDefinition.collection_unit_metric_definition_id,
        )
        .correlate(RescoreSessionUnits, CollectionUnit)
        .scalar_subquery()
    )

    # comments subquery
    draft_comments = select(
        UnitCommentDraft.unit_comment.label('unit_comment'),
        UnitCommentDraft.updated_at.label('date_added'),
        literal(True).label('is_draft'),
    ).where(
        UnitCommentDraft.rescore_session_units_id
        == RescoreSessionUnits.rescore_session_units_id
    )

    final_comments = select(
        UnitComment.unit_comment.label('unit_comment'),
        UnitComment.date_added,
        literal(False).label('is_draft'),
    ).where(UnitComment.collection_unit_id == CollectionUnit.collection_unit_id)

    comments_union = (
        draft_comments.union_all(final_comments)
        .order_by(text('date_added DESC'))
        .limit(1)
    )

    comments_lateral = comments_union.subquery().lateral('comments')

    # ranks query
    draft_ranks_query = (
        select(
            UnitRankDraft.percentage,
            UnitRankDraft.rank_id,
            UnitRankDraft.comment,
            UnitRankDraft.criterion_id,
            UnitRankDraft.updated_at.label('date_assessed'),
            literal(True).label('is_draft'),
        )
        .join(
            UnitCategoryDraft,
            UnitCategoryDraft.category_draft_id == UnitRankDraft.category_draft_id,
        )
        .where(
            UnitCategoryDraft.rescore_session_units_id
            == RescoreSessionUnits.rescore_session_units_id
        )
        .correlate(RescoreSessionUnits)
    )

    full_ranks_query = (
        select(
            UnitAssessmentRank.percentage,
            UnitAssessmentRank.rank_id,
            UnitAssessmentRank.comment,
            Rank.criterion_id,
            func.coalesce(
                UnitAssessmentCriterion.date_assessed, UnitAssessmentCriterion.date_from
            ).label('date_assessed'),
            literal(False).label('is_draft'),
        )
        .select_from(UnitAssessmentCriterion)
        .join(
            UnitAssessmentRank,
            UnitAssessmentRank.unit_assessment_criterion_id
            == UnitAssessmentCriterion.unit_assessment_criterion_id,
        )
        .join(Rank, Rank.rank_id == UnitAssessmentRank.rank_id)
        .where(
            UnitAssessmentCriterion.collection_unit_id
            == CollectionUnit.collection_unit_id,
            UnitAssessmentCriterion.current == 'yes',
            ~exists(
                select(1)
                .select_from(UnitCategoryDraft)
                .join(
                    UnitRankDraft,
                    UnitRankDraft.category_draft_id
                    == UnitCategoryDraft.category_draft_id,
                )
                .where(
                    UnitCategoryDraft.rescore_session_units_id
                    == RescoreSessionUnits.rescore_session_units_id,
                    UnitRankDraft.criterion_id == Rank.criterion_id,
                )
                .correlate(RescoreSessionUnits, Rank)
            ),
        )
        .correlate(CollectionUnit, RescoreSessionUnits)
    )

    ranks = draft_ranks_query.union(full_ranks_query).subquery('ranks')

    ranks_subquery = (
        select(
            func.JSON_ARRAYAGG(
                func.JSON_OBJECT(
                    'percentage',
                    ranks.c.percentage,
                    'rank_id',
                    ranks.c.rank_id,
                    'rank_value',
                    Rank.rank_value,
                    'comment',
                    ranks.c.comment,
                    'definition',
                    Rank.definition,
                    'criterion_id',
                    ranks.c.criterion_id,
                    'date_assessed',
                    ranks.c.date_assessed,
                    'is_draft',
                    ranks.c.is_draft,
                )
            )
        )
        .select_from(ranks)
        .join(Rank, Rank.rank_id == ranks.c.rank_id)
        .correlate(RescoreSessionUnits, CollectionUnit)
        .scalar_subquery()
    )

    # category tracking query
    tracking_subquery = (
        select(
            func.JSON_ARRAYAGG(
                func.JSON_OBJECT(
                    'category_draft_id',
                    UnitCategoryDraft.category_draft_id,
                    'rescore_session_units_id',
                    UnitCategoryDraft.rescore_session_units_id,
                    'category_id',
                    UnitCategoryDraft.category_id,
                    'complete',
                    UnitCategoryDraft.complete,
                    'updated_at',
                    UnitCategoryDraft.updated_at,
                )
            )
        )
        .where(
            UnitCategoryDraft.rescore_session_units_id
            == RescoreSessionUnits.rescore_session_units_id
        )
        .correlate(RescoreSessionUnits)
        .scalar_subquery()
    )

    # final query
    query = (
        select(
            RescoreSession,
            RescoreSessionUnits,
            CollectionUnit,
            Division,
            Section,
            Users,
            CuratorialUnitDefinition,
            metric_subquery.label('metric_json'),
            comments_lateral.c.unit_comment,
            comments_lateral.c.date_added.label('unit_comment_date_added'),
            comments_lateral.c.is_draft.label('unit_comment_is_draft'),
            ranks_subquery.label('ranks_json'),
            tracking_subquery.label('category_tracking'),
        )
        .select_from(RescoreSessionUnits)
        .join(
            CollectionUnit,
            CollectionUnit.collection_unit_id == RescoreSessionUnits.collection_unit_id,
        )
        .join(
            RescoreSession,
            RescoreSession.rescore_session_id == RescoreSessionUnits.rescore_session_id,
        )
        .join(Section, Section.section_id == CollectionUnit.section_id)
        .join(Division, Division.division_id == Section.division_id)
        .join(Users, Users.user_id == CollectionUnit.responsible_curator_id)
        .join(
            CuratorialUnitDefinition,
            CuratorialUnitDefinition.curatorial_unit_definition_id
            == CollectionUnit.curatorial_unit_definition_id,
        )
        .where(
            CollectionUnit.unit_active == 'yes',
            RescoreSession.rescore_session_id == rescore_session_id,
            RescoreSession.status == 'in_progress',
        )
    )
    return query
