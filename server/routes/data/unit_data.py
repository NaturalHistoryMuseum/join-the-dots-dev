from flask import jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy import case, func, select, union_all, update
from sqlalchemy.orm import joinedload

from server.database import db
from server.models import (
    AssignedUnits,
    BibliographicLevel,
    Building,
    Category,
    CollectionUnit,
    CollectionUnitMetric,
    CollectionUnitMetricDefinition,
    Criterion,
    CuratorialUnitDefinition,
    Department,
    Division,
    Floor,
    GeographicOrigin,
    GeologicalTimePeriod,
    ItemType,
    LibraryAndArchivesFunction,
    PreservationMethod,
    Roles,
    Section,
    Site,
    StorageContainer,
    StorageRoom,
    Taxon,
    UnitAssessmentCriterion,
    Users,
)
from server.routes.queries.data_queries import UNIT_SCORES
from server.schemas import *
from server.utils import (
    get_user_by_id,
)

from . import data_bp
from .utils import *


@data_bp.route('/unit-scores/<unitId>', methods=['GET'])
@jwt_required()
def get_unit_scores(unitId):
    """
    Get all unit data, including scores and metrics.
    """
    data = db.session.execute(
        text(UNIT_SCORES), {'collection_unit_id': unitId}
    ).fetchall()

    return jsonify([dict(row._mapping) for row in data])


@data_bp.route('/unit-department', methods=['GET'])
@jwt_required()
def get_units_and_departments():
    """
    Get a unit and its department data.
    """
    query = (
        select(CollectionUnit, Users)
        .join(Section, Section.section_id == CollectionUnit.section_id)
        .join(Division, Division.division_id == Section.division_id)
        .join(Department, Department.department_id == Division.department_id)
        .join(Users, Users.user_id == CollectionUnit.responsible_curator_id)
        .where(CollectionUnit.unit_active == 'yes')
    )

    data = db.session.execute(query).all()

    return [
        {
            'collection_unit_id': row.CollectionUnit.collection_unit_id,
            'unit_name': row.CollectionUnit.unit_name,
            'named_collection': row.CollectionUnit.named_collection,
            'unit_active': row.CollectionUnit.unit_active,
            'draft_unit': row.CollectionUnit.draft_unit,
            'responsible_curator_id': row.CollectionUnit.responsible_curator_id,
            'section_id': row.CollectionUnit.section.section_id,
            'section_name': row.CollectionUnit.section.section_name,
            'division_id': row.CollectionUnit.section.division.division_id,
            'division_name': row.CollectionUnit.section.division.division_name,
            'department_id': row.CollectionUnit.section.division.department.department_id,
            'department_name': row.CollectionUnit.section.division.department.department_name,
            'curator_name': row.Users.display_name,
        }
        for row in data
    ]


@data_bp.route('/full-unit/<unit_id>', methods=['GET'])
@jwt_required()
def get_full_unit(unit_id):
    """
    Get the full unit metadata.
    """
    max_comment = (
        select(func.max(UnitComment.unit_comment_id))
        .where(UnitComment.collection_unit_id == CollectionUnit.collection_unit_id)
        .correlate(CollectionUnit)
        .scalar_subquery()
    )

    query = (
        select(CollectionUnit, Users, UnitComment)
        .join(Users, Users.user_id == CollectionUnit.responsible_curator_id)
        .outerjoin(UnitComment, UnitComment.unit_comment_id == max_comment)
        .where(CollectionUnit.collection_unit_id == unit_id)
    )
    data = db.session.execute(query).all()

    return [
        {
            **{
                c.name: getattr(row.CollectionUnit, c.name)
                for c in CollectionUnit.__table__.columns
            },
            'unit_comment': row.UnitComment.unit_comment if row.UnitComment else None,
            'date_comment_added': row.UnitComment.date_added
            if row.UnitComment
            else None,
            'responsible_curator': row.Users.display_name,
        }
        for row in data
    ]


@data_bp.route('/all-assigned-users/<unit_id>', methods=['GET'])
@jwt_required()
def get_assigned_users(unit_id):
    """
    Gets all users that are assigned to a specific unit.
    """
    query = (
        select(AssignedUnits, Users)
        .join(Users, Users.user_id == AssignedUnits.user_id)
        .where(AssignedUnits.collection_unit_id == unit_id)
    )
    data = db.session.execute(query).all()

    return [
        {
            'user_id': row.AssignedUnits.user_id,
            'user_name': row.AssignedUnits.users.display_name
            if row.AssignedUnits
            else None,
        }
        for row in data
    ]


@data_bp.route('/units-assigned', methods=['GET'])
@jwt_required()
def get_units_assigned():
    """
    Gets all units that are assigned to the current user.
    """
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    try:
        # Fetch user level
        user = get_user_by_id(user_id)

        au_subquery = (
            select(func.JSON_ARRAYAGG(AssignedUnits.user_id))
            .where(
                AssignedUnits.collection_unit_id == CollectionUnit.collection_unit_id
            )
            .correlate(CollectionUnit)
            .scalar_subquery()
        )

        where_query = [
            CollectionUnit.unit_active == 'yes',
            CollectionUnit.draft_unit == 0,
        ]
        if user['role_id'] == 3:
            where_query.append(Division.division_id == user['role_id'])

        if user['role_id'] == 2:
            where_query.append(AssignedUnits.user_id == user_id)

        query = (
            select(
                CollectionUnit,
                au_subquery.label('assigned_editors'),
                Section,
                Division,
                Users,
            )
            .join(Section, Section.section_id == CollectionUnit.section_id)
            .join(Division, Division.division_id == Section.division_id)
            .join(Users, Users.user_id == CollectionUnit.responsible_curator_id)
            .where(and_(*where_query))
        )

        data = db.session.execute(query).all()

        return [
            {
                **{
                    c.name: getattr(row.CollectionUnit, c.name)
                    for c in CollectionUnit.__table__.columns
                },
                'display_name': row.Users.display_name,
                'section_name': row.Section.section_name,
                'division_name': row.Division.division_name,
                'assigned_editors': row.assigned_editors,
            }
            for row in data
        ]
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/units-by-division/<division_id>', methods=['GET'])
@jwt_required()
def get_units_by_division(division_id):
    """
    Gets units for a specific division.
    """
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    try:
        query = select(CollectionUnit).where(
            CollectionUnit.unit_active == 'yes',
            CollectionUnit.draft_unit == 0,
            Section.division_id == division_id,
        )
        data = db.session.execute(query).scalars().all()

        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/division-users', methods=['GET'])
@jwt_required()
def get_division_users():
    """
    Gets all the users assigned to a division.
    """
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    try:
        # Fetch user level
        user = get_user_by_id(user_id)
        role_id = user['role_id']
        if role_id >= 3:
            au_subquery = (
                select(func.JSON_ARRAYAGG(AssignedUnits.collection_unit_id))
                .join(
                    CollectionUnit,
                    CollectionUnit.collection_unit_id
                    == AssignedUnits.collection_unit_id,
                )
                .where(
                    AssignedUnits.user_id == Users.user_id,
                    CollectionUnit.unit_active == 'yes',
                    CollectionUnit.draft_unit == 0,
                )
                .correlate(Users)
                .scalar_subquery()
            )

            ru_subquery = (
                select(func.JSON_ARRAYAGG(CollectionUnit.collection_unit_id))
                .where(
                    CollectionUnit.responsible_curator_id == Users.user_id,
                    CollectionUnit.unit_active == 'yes',
                    CollectionUnit.draft_unit == 0,
                )
                .correlate(Users)
                .scalar_subquery()
            )

            where_query = [Users.role_id > 1]
            # Only return one divisions for managers
            if role_id < 4:
                where_query.append(Users.division_id == user['division_id'])

            query = (
                select(
                    Users,
                    Roles,
                    Division,
                    au_subquery.label('assigned_units'),
                    ru_subquery.label('responsible_units'),
                )
                .join(Roles, Roles.role_id == Users.role_id)
                .join(Division, Division.division_id == Users.division_id)
                .where(and_(*where_query))
                .order_by(Users.display_name)
            )
            data = db.session.execute(query).all()
            return [
                {
                    **{
                        c.name: getattr(row.Users, c.name)
                        for c in Users.__table__.columns
                    },
                    'name': row.Users.display_name,
                    'role': row.Roles.role,
                    'assigned_units': row.assigned_units,
                    'responsible_units': row.responsible_units,
                }
                for row in data
            ]
        else:
            return jsonify({'error': 'You are not autorised.'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/reassign-responsible-curator', methods=['POST'])
@jwt_required()
def reassign_responsible_curator():
    """
    Reassign units responsiblility from one user to another.
    """
    data = request.get_json()
    old_user_id = data.get('old_user_id')
    new_user_id = data.get('new_user_id')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    try:
        # Transfer units the old user was responsible for to the new user
        owned_units = db.session.execute(
            select(CollectionUnit.collection_unit_id).where(
                CollectionUnit.responsible_curator_id == old_user_id
            )
        ).all()

        for unit in owned_units:
            new_assigned_unit = AssignedUnits(
                user_id=new_user_id, collection_unit_id=unit.collection_unit_id
            )
            db.session.add(new_assigned_unit)

        # Remove all units assigned to old user
        db.session.execute(
            delete(AssignedUnits).where(AssignedUnits.user_id == old_user_id)
        )
        # Change the responsible_curator_id from the old user, to the new
        db.session.execute(
            update(CollectionUnit)
            .where(CollectionUnit.responsible_curator_id == old_user_id)
            .values(responsible_curator_id=new_user_id)
        )

        db.session.commit()
        return jsonify({'message': 'Units successfully reassigned', 'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/submit-unit-assigned', methods=['POST'])
@jwt_required()
def set_unit_assigned():
    """
    Set the users that are assigned to edit a specific unit.
    """
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
        update_unit_assigned(unit_id, assigned_users)

        # Close the cursor and connection
        db.session.commit()
        return jsonify(
            {'message': 'Unit assigned users updated successfully', 'success': True}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/bulk-submit-unit-permissions', methods=['POST'])
@jwt_required()
def set_bulk_unit_permissions():
    """
    Edit muliple units permissions.
    """
    data = request.get_json()
    unit_ids = data.get('unit_ids')
    assigned_users = data.get('assigned_users')
    responsible_curator_id = data.get('responsible_curator_id')

    if not unit_ids:
        return jsonify({'error': 'unit_id is required'}), 400
    if not assigned_users and not responsible_curator_id:
        return jsonify(
            {'error': 'assigned_users or responsible_curator_id is required'}
        ), 400

    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    try:
        # add assinged users per unit
        if assigned_users:
            for unit_id in unit_ids:
                update_unit_assigned(unit_id, assigned_users)
        # add respsonsible curator
        if responsible_curator_id:
            db.session.execute(
                update(CollectionUnit)
                .where(CollectionUnit.collection_unit_id.in_(unit_ids))
                .values(responsible_curator_id=responsible_curator_id)
            )

        db.session.commit()
        return jsonify(
            {'message': 'Units permissions updated successfully', 'success': True}
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/submit-user-assigned', methods=['POST'])
@jwt_required()
def set_user_assigned():
    """
    Edit the units a user is assigned.
    """
    data = request.get_json()
    user_id = data.get('user_id')
    assigned_units = data.get('assigned_units')

    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400

    if not assigned_units:
        return jsonify({'error': 'assigned_units is required'}), 400

    try:
        # Fetch current assigned units for this user
        current_assigned = (
            db.session.execute(
                select(AssignedUnits).where(AssignedUnits.user_id == user_id)
            )
            .scalars()
            .all()
        )
        # Normalize both sets to integers
        current_assigned = set(int(row.collection_unit_id) for row in current_assigned)
        assigned_units = set(int(unit_id) for unit_id in assigned_units)

        # Determine diffs
        units_to_add = assigned_units - current_assigned
        units_to_remove = current_assigned - assigned_units

        # Insert new assignments
        for unit_id in units_to_add:
            new_assignment = AssignedUnits(user_id=user_id, collection_unit_id=unit_id)
            db.session.add(new_assignment)

        # Remove old assignments
        for unit_id in units_to_remove:
            db.session.execute(
                delete(AssignedUnits).where(
                    AssignedUnits.user_id == user_id,
                    AssignedUnits.collection_unit_id == unit_id,
                )
            )

        db.session.commit()

        return jsonify(
            {'message': 'User assigned units updated successfully', 'success': True}
        )

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/criterion', methods=['GET'])
@jwt_required()
def get_criterion():
    """
    Get the full criterion definitions.

    Filters out criterion_id: 3 as it is no longer used.
    """
    query = (
        select(Criterion, Category)
        .join(Category, Category.category_id == Criterion.category_id)
        .where(Criterion.criterion_id != 3)
    )
    data = db.session.execute(query).all()

    return [
        {
            'criterion_id': row.Criterion.criterion_id,
            'criterion_name': row.Criterion.criterion_name,
            'criterion_code': row.Criterion.criterion_code,
            'definition': row.Criterion.definition,
            'category_id': row.Criterion.category_id,
            'category_code': row.Criterion.category.category_code,
            'description': row.Criterion.category.description,
        }
        for row in data
    ]


@data_bp.route('/category', methods=['GET'])
@jwt_required()
def get_category():
    """
    Get all category data.
    """
    data = Category.query.all()
    return jsonify(data)


@data_bp.route('/all-roles', methods=['GET'])
@jwt_required()
def get_roles():
    """
    Get all roles data.
    """
    data = Roles.query.all()
    return jsonify(data)


@data_bp.route('/metric-definitions', methods=['GET'])
@jwt_required()
def get_metric_definitions():
    """
    Get all metrics definitions data.
    """
    data = CollectionUnitMetricDefinition.query.all()
    return jsonify(data)


@data_bp.route('/all-sections', methods=['GET'])
@jwt_required()
def get_all_sections():
    """
    Get all sections data in dropdown format.
    """
    sections = Section.query.options(
        joinedload(Section.division).joinedload(Division.department)
    ).all()

    return [
        {
            'section_id': section.section_id if section.section_id else None,
            'section_name': section.section_name if section.section_name else None,
            'division_name': section.division.division_name
            if section.division
            else None,
            'department_id': section.division.department_id
            if section.division
            else None,
            'department_name': section.division.department.department_name
            if section.division and section.division.department
            else None,
            'value': section.section_id,
            'label': section.section_name,
        }
        for section in sections
    ]
    return jsonify(data)


@data_bp.route('/all-geographic-origin', methods=['GET'])
@jwt_required()
def get_all_geographic_origin():
    """
    Get all geographic origin data in dropdown format.
    """
    data = GeographicOrigin.query.all()
    schema = GeographicOriginDDSchema(many=True)
    return jsonify(schema.dump(data))


@data_bp.route('/all-geological-time-period', methods=['GET'])
@jwt_required()
def get_all_geological_time_period():
    """
    Get all geological-time-period data in dropdown format.
    """
    data = GeologicalTimePeriod.query.all()
    schema = GeologicalTimePeriodDDSchema(many=True)
    return jsonify(schema.dump(data))


@data_bp.route('/all-divisions', methods=['GET'])
@jwt_required()
def get_all_divisions():
    """
    Get all division data in dropdown format.
    """
    data = Division.query.all()
    schema = DivisionDDSchema(many=True)
    return jsonify(schema.dump(data))


@data_bp.route('/container-data', methods=['GET'])
@jwt_required()
def get_all_containers():
    """
    Get all container data in dropdown format.
    """
    data = StorageContainer.query.all()
    schema = StorageContainerDDSchema(many=True)
    return jsonify(schema.dump(data))


taxon_dd_schema = TaxonDDSchema(many=True)


@data_bp.route('/all-taxon', methods=['GET'])
@jwt_required()
def get_all_taxon():
    """
    Get all taxon data in dropdown format.

    Also adds the department tag to the label name.
    """
    label_prefix = case(
        (Taxon.taxon_life_science_id == None, 'ES '),
        (Taxon.taxon_palaeontology_id == None, 'LS '),
        else_='',
    )
    label = func.concat(label_prefix, Taxon.taxon_name, ' ', Taxon.taxon_rank).label(
        'label'
    )

    stmt = select(Taxon.taxon_id.label('value'), label)
    rows = db.session.execute(stmt).mappings().all()
    return jsonify(taxon_dd_schema.dump(rows))


@data_bp.route('/all-curatorial-definition', methods=['GET'])
@jwt_required()
def get_all_curatorial_definition():
    """
    Get all curatorial definitions in dropdown format.
    """
    curatorial_unit_dd_schema = CuratorialUnitDefinitionDDSchema(many=True)

    query = (
        select(
            CuratorialUnitDefinition, BibliographicLevel, ItemType, PreservationMethod
        )
        .outerjoin(
            BibliographicLevel,
            BibliographicLevel.bibliographic_level_id
            == CuratorialUnitDefinition.bibliographic_level_id,
        )
        .outerjoin(
            ItemType, ItemType.item_type_id == CuratorialUnitDefinition.item_type_id
        )
        .outerjoin(
            PreservationMethod,
            PreservationMethod.preservation_method_id
            == CuratorialUnitDefinition.preservation_method_id,
        )
    )

    resp = db.session.execute(query).scalars().all()
    return jsonify(curatorial_unit_dd_schema.dump(resp))


@data_bp.route('/all-room-data', methods=['GET'])
@jwt_required()
def get_all_rooms():
    """
    Get all room data in dropdown format.
    """
    query = (
        select(
            StorageRoom,
            Floor,
            Building,
            Site,
        )
        .join(Floor, Floor.floor_id == StorageRoom.floor_id)
        .join(Building, Building.building_id == Floor.building_id)
        .join(Site, Site.site_id == Building.site_id)
    )
    data = db.session.execute(query).scalars().all()
    schema = StorageRoomDDSchema(many=True)
    return jsonify(schema.dump(data))


@data_bp.route('/public-room-data', methods=['GET'])
@jwt_required()
def get_all_public_rooms():
    """
    Get all room data (that is not considered sensitive) in dropdown format.
    """
    query = (
        select(
            StorageRoom,
            Floor,
            Building,
            Site,
        )
        .join(Floor, Floor.floor_id == StorageRoom.floor_id)
        .join(Building, Building.building_id == Floor.building_id)
        .join(Site, Site.site_id == Building.site_id)
        .where(StorageRoom.room_code.notilike('%UNDEFINED%'))
    )
    data = db.session.execute(query).scalars().all()
    schema = StorageRoomDDSchema(many=True)
    return jsonify(schema.dump(data))


@data_bp.route('/all-lib-function', methods=['GET'])
@jwt_required()
def get_all_lib_function():
    """
    Get all lib functions in dropdown format.
    """
    data = db.session.execute(select(LibraryAndArchivesFunction)).scalars().all()
    schema = LibraryAndArchivesFunctionDDSchema(many=True)
    return jsonify(schema.dump(data))


@data_bp.route('/all-curators', methods=['GET'])
@jwt_required()
def get_all_curators():
    """
    Get all curators in dropdown format.
    """
    query = select(
        Users,
    ).where(
        Users.role_id >= 2,
        Users.display_name != None,
    )
    data = db.session.execute(query).scalars().all()
    schema = UsersDDSchema(many=True)
    return jsonify(schema.dump(data))


@data_bp.route('/units-by-user', methods=['GET'])
@jwt_required()
def get_units_by_user():
    """
    Get all units assigned to a user.

    Additionally return when the unit was last rescored and assessed.
    """
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    # Fetch user level
    user = get_user_by_id(user_id)
    role_id = user['role_id']

    # make subquery for the last time units where rescored
    last_rescored_union = union_all(
        select(
            func.max(func.date(UnitAssessmentCriterion.date_from)).label('latest_date')
        )
        .where(
            and_(
                UnitAssessmentCriterion.collection_unit_id
                == CollectionUnit.collection_unit_id,
                UnitAssessmentCriterion.current == 'yes',
            )
        )
        .correlate(CollectionUnit),
        select(func.max(func.date(CollectionUnitMetric.date_from)).label('latest_date'))
        .where(
            and_(
                CollectionUnitMetric.collection_unit_id
                == CollectionUnit.collection_unit_id,
                CollectionUnitMetric.current == 'yes',
            )
        )
        .correlate(CollectionUnit),
        select(func.max(func.date(UnitComment.date_added)).label('latest_date'))
        .where(UnitComment.collection_unit_id == CollectionUnit.collection_unit_id)
        .correlate(CollectionUnit),
    ).subquery()

    last_rescored_subquery = (
        select(func.max(last_rescored_union.c.latest_date))
        .correlate(CollectionUnit)
        .scalar_subquery()
    )

    # make subquery for the last time units were assessed
    last_assessed_union = union_all(
        select(
            func.max(func.date(UnitAssessmentCriterion.date_from)).label('latest_date')
        )
        .where(
            and_(
                UnitAssessmentCriterion.collection_unit_id
                == CollectionUnit.collection_unit_id,
                UnitAssessmentCriterion.current == 'yes',
            )
        )
        .correlate(CollectionUnit),
        select(func.max(func.date(CollectionUnitMetric.date_from)).label('latest_date'))
        .where(
            and_(
                CollectionUnitMetric.collection_unit_id
                == CollectionUnit.collection_unit_id,
                CollectionUnitMetric.current == 'yes',
            )
        )
        .correlate(CollectionUnit),
        select(func.max(func.date(UnitComment.date_added)).label('latest_date'))
        .where(UnitComment.collection_unit_id == CollectionUnit.collection_unit_id)
        .correlate(CollectionUnit),
        select(
            func.max(func.date(UnitAssessmentCriterion.date_assessed)).label(
                'latest_date'
            )
        )
        .where(
            and_(
                UnitAssessmentCriterion.collection_unit_id
                == CollectionUnit.collection_unit_id,
                UnitAssessmentCriterion.current == 'yes',
            )
        )
        .correlate(CollectionUnit),
    ).subquery()

    last_assessed_subquery = (
        select(func.max(last_assessed_union.c.latest_date))
        .correlate(CollectionUnit)
        .scalar_subquery()
    )

    # return all units if admin
    if role_id == 4:
        # make the query
        query = (
            select(
                CollectionUnit,
                Section,
                Division,
                last_rescored_subquery.label('last_rescored'),
                last_assessed_subquery.label('last_assessed'),
            )
            .join(Section, Section.section_id == CollectionUnit.section_id)
            .join(Division, Division.division_id == Section.division_id)
            .where(
                and_(
                    CollectionUnit.unit_active == 'yes', CollectionUnit.draft_unit == 0
                )
            )
            .group_by(CollectionUnit.collection_unit_id)
        )
    else:
        # make the query
        query = (
            select(
                CollectionUnit,
                Section,
                Division,
                last_rescored_subquery.label('last_rescored'),
                last_assessed_subquery.label('last_assessed'),
            )
            .outerjoin(
                AssignedUnits,
                AssignedUnits.collection_unit_id == CollectionUnit.collection_unit_id,
            )
            .join(Section, Section.section_id == CollectionUnit.section_id)
            .join(Division, Division.division_id == Section.division_id)
            .where(
                and_(
                    CollectionUnit.unit_active == 'yes',
                    CollectionUnit.draft_unit == 0,
                    AssignedUnits.user_id == user_id,
                )
            )
            .group_by(CollectionUnit.collection_unit_id)
        )

    # execute query
    data = db.session.execute(query).all()

    for row in data:
        row.CollectionUnit.last_rescored = row.last_rescored
        row.CollectionUnit.last_assessed = row.last_assessed

    schema = UnitByUsersSchema(many=True)
    return jsonify(schema.dump([row.CollectionUnit for row in data]))
