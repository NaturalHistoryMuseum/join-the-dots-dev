import enum
from dataclasses import dataclass
from datetime import datetime

from .database import db


class BooleanEnum(str, enum.Enum):
    yes = 'yes'
    no = 'no'


class CriteriaAssessmentEnum(str, enum.Enum):
    known = 'known'
    unknown = 'unknown'
    na = 'na'


class HigherOperationEnum(str, enum.Enum):
    create = 'create'
    delete = 'delete'
    split = 'split'
    merge = 'merge'
    update = 'update'


class OperationEnum(str, enum.Enum):
    create = 'create'
    delete = 'delete'
    update = 'update'


class StatusEnum(str, enum.Enum):
    in_progress = 'in_progress'
    complete = 'complete'


@dataclass
class AssignedUnits(db.Model):
    __tablename__ = 'assigned_units'
    # fields
    assigned_unit_id: assigned_unit_id = db.Column(db.Integer, primary_key=True)
    user_id: user_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False
    )
    collection_unit_id: collection_unit_id = db.Column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    # relationships
    users = db.relationship('Users', back_populates='assigned_units')
    collection_unit = db.relationship('CollectionUnit', back_populates='assigned_units')


@dataclass
class BibliographicLevel(db.Model):
    __tablename__ = 'bibliographic_level'
    # fields
    bibliographic_level_id: bibliographic_level_id = db.Column(
        db.Integer, primary_key=True
    )
    bibliographic_level: bibliographic_level = db.Column(db.String(255), nullable=False)
    # relationships
    curatorial_unit_definition = db.relationship(
        'CuratorialUnitDefinition', back_populates='bibliographic_level'
    )


@dataclass
class Building(db.Model):
    __tablename__ = 'building'
    # fields
    building_id: building_id = db.Column(db.Integer, primary_key=True)
    site_id: site_id = db.Column(
        db.Integer, db.ForeignKey('site.site_id'), nullable=False
    )
    building_name: building_name = db.Column(db.String(255), nullable=False)
    # relationships
    site = db.relationship('Site', back_populates='building')
    floor = db.relationship('Floor', back_populates='building')


@dataclass
class Category(db.Model):
    __tablename__ = 'category'
    # fields
    category_id: category_id = db.Column(db.Integer, primary_key=True)
    category_code: category_code = db.Column(db.String(255))
    description: description = db.Column(db.String(255))
    # relationships
    criterion = db.relationship('Criterion', back_populates='category')


@dataclass
class ChangeLog(db.Model):
    __tablename__ = 'change_log'
    # fields
    change_log_id: change_log_id = db.Column(db.Integer, primary_key=True)
    title: title = db.Column(db.String(100), nullable=False)
    log: log = db.Column(db.Text, nullable=False)
    date_added: date_added = db.Column(db.DateTime, nullable=False)


@dataclass
class CollectionUnit(db.Model):
    __tablename__ = 'collection_unit'
    # fields
    collection_unit_id: collection_unit_id = db.Column(db.Integer, primary_key=True)
    unit_name: unit_name = db.Column(db.String(255), nullable=False)
    public_unit_name: public_unit_name = db.Column(db.String(255))
    section_id: section_id = db.Column(
        db.Integer, db.ForeignKey('section.section_id'), nullable=False
    )
    unit_active: unit_active = db.Column(
        db.Enum(BooleanEnum), nullable=False, default='yes'
    )
    responsible_curator_id: responsible_curator_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id')
    )
    curatorial_unit_definition_id: curatorial_unit_definition_id = db.Column(
        db.Integer,
        db.ForeignKey('curatorial_unit_definition.curatorial_unit_definition_id'),
    )
    storage_room_id: storage_room_id = db.Column(
        db.Integer, db.ForeignKey('storage_room.storage_room_id')
    )
    storage_container_id: storage_container_id = db.Column(
        db.Integer, db.ForeignKey('storage_container.storage_container_id')
    )
    geographic_origin_id: geographic_origin_id = db.Column(
        db.Integer, db.ForeignKey('geographic_origin.geographic_origin_id')
    )
    library_and_archives_function_id: library_and_archives_function_id = db.Column(
        db.Integer,
        db.ForeignKey('library_and_archives_function.library_and_archives_function_id'),
    )
    geological_time_period_from_id: geological_time_period_from_id = db.Column(
        db.Integer, db.ForeignKey('geological_time_period.geological_time_period_id')
    )
    geological_time_period_to_id: geological_time_period_to_id = db.Column(
        db.Integer, db.ForeignKey('geological_time_period.geological_time_period_id')
    )
    type_collection_flag: type_collection_flag = db.Column(db.Enum(BooleanEnum))
    publish_flag: publish_flag = db.Column(db.Enum(BooleanEnum))
    informal_taxon: informal_taxon = db.Column(db.Text)
    named_collection: named_collection = db.Column(db.String(255))
    es_recent_specimen_flag: es_recent_specimen_flag = db.Column(db.Enum(BooleanEnum))
    archives_fond_ref: archives_fond_ref = db.Column(db.String(255))
    count_curatorial_units_flag: count_curatorial_units_flag = db.Column(
        db.Enum(BooleanEnum)
    )
    sort_order: sort_order = db.Column(db.Integer)
    taxon_id: taxon_id = db.Column(db.Integer, db.ForeignKey('taxon.taxon_id'))
    draft_unit: draft_unit = db.Column(db.Boolean, nullable=False, default=0)
    # relationships
    assigned_units = db.relationship('AssignedUnits', back_populates='collection_unit')
    section = db.relationship('Section', back_populates='collection_unit')
    responsible_curator = db.relationship('Users', back_populates='collection_unit')
    geological_time_period_from = db.relationship(
        'GeologicalTimePeriod',
        foreign_keys=[geological_time_period_from_id],
        back_populates='collection_unit_from',
    )
    geological_time_period_to = db.relationship(
        'GeologicalTimePeriod',
        foreign_keys=[geological_time_period_to_id],
        back_populates='collection_unit_to',
    )
    curatorial_unit_definition = db.relationship(
        'CuratorialUnitDefinition', back_populates='collection_unit'
    )
    geographic_origin = db.relationship(
        'GeographicOrigin', back_populates='collection_unit'
    )
    library_and_archives_function = db.relationship(
        'LibraryAndArchivesFunction', back_populates='collection_unit'
    )
    storage_container = db.relationship(
        'StorageContainer', back_populates='collection_unit'
    )
    storage_room = db.relationship('StorageRoom', back_populates='collection_unit')
    taxon = db.relationship('Taxon', back_populates='collection_unit')
    unit_comment = db.relationship('UnitComment', back_populates='collection_unit')
    unit_assessment_criterion = db.relationship(
        'UnitAssessmentCriterion', back_populates='collection_unit'
    )
    rescore_session_units = db.relationship(
        'RescoreSessionUnits', back_populates='collection_unit'
    )
    collection_unit_metric = db.relationship(
        'CollectionUnitMetric', back_populates='collection_unit'
    )
    structural_changes_basic = db.relationship(
        'StructuralChangesBasic', back_populates='collection_unit'
    )


@dataclass
class CollectionUnitMetric(db.Model):
    __tablename__ = 'collection_unit_metric'
    # fields
    collection_unit_metric_id: collection_unit_metric_id = db.Column(
        db.Integer, primary_key=True
    )
    collection_unit_id: collection_unit_id = db.Column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    collection_unit_metric_definition_id: collection_unit_metric_definition_id = (
        db.Column(
            db.Integer,
            db.ForeignKey(
                'collection_unit_metric_definition.collection_unit_metric_definition_id'
            ),
            nullable=False,
        )
    )
    metric_value: metric_value = db.Column(db.Double, nullable=False)
    confidence_level: confidence_level = db.Column(db.String(255))
    date_from: date_from = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_to: date_to = db.Column(
        db.DateTime, nullable=False, default=datetime(9999, 12, 31, 23, 59, 59)
    )
    current: current = db.Column(db.Enum(BooleanEnum), nullable=False, default='yes')
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='collection_unit_metric'
    )
    collection_unit_metric_definition = db.relationship(
        'CollectionUnitMetricDefinition', back_populates='collection_unit_metric'
    )


@dataclass
class CollectionUnitMetricDefinition(db.Model):
    __tablename__ = 'collection_unit_metric_definition'
    # fields
    collection_unit_metric_definition_id: collection_unit_metric_definition_id = (
        db.Column(db.Integer, primary_key=True)
    )
    metric_name: metric_name = db.Column(db.String(255), nullable=False)
    metric_definition: metric_definition = db.Column(db.String(255))
    metric_units: metric_units = db.Column(db.String(255))
    metric_datatype: metric_datatype = db.Column(db.String(255))
    # relationships
    collection_unit_metric = db.relationship(
        'CollectionUnitMetric', back_populates='collection_unit_metric_definition'
    )
    unit_metric_draft = db.relationship(
        'UnitMetricDraft', back_populates='collection_unit_metric_definition'
    )


@dataclass
class Criterion(db.Model):
    __tablename__ = 'criterion'
    # fields
    criterion_id: criterion_id = db.Column(db.Integer, primary_key=True)
    category_id: category_id = db.Column(
        db.Integer, db.ForeignKey('category.category_id')
    )
    criterion_code: criterion_code = db.Column(db.String(255))
    criterion_name: criterion_name = db.Column(db.String(255))
    definition: definition = db.Column(db.Text)
    referenced_standards: referenced_standards = db.Column(db.Text)
    # relationships
    category = db.relationship('Category', back_populates='criterion')
    rank = db.relationship('Rank', back_populates='criterion')
    unit_assessment_criterion = db.relationship(
        'UnitAssessmentCriterion', back_populates='criterion'
    )
    unit_rank_draft = db.relationship('UnitRankDraft', back_populates='criterion')


@dataclass
class CuratorialUnitDefinition(db.Model):
    __tablename__ = 'curatorial_unit_definition'
    # fields
    curatorial_unit_definition_id: curatorial_unit_definition_id = db.Column(
        db.Integer, primary_key=True
    )
    item_type_id: item_type_id = db.Column(
        db.Integer, db.ForeignKey('item_type.item_type_id'), nullable=False
    )
    preservation_method_id: preservation_method_id = db.Column(
        db.Integer,
        db.ForeignKey('preservation_method.preservation_method_id'),
        nullable=False,
    )
    bibliographic_level_id: bibliographic_level_id = db.Column(
        db.Integer,
        db.ForeignKey('bibliographic_level.bibliographic_level_id'),
        nullable=False,
    )
    description: description = db.Column(db.String(255))
    typical_item_count: typical_item_count = db.Column(db.String(255))
    typical_item_count_range: typical_item_count_range = db.Column(db.String(255))
    items_unestimatable_flag: items_unestimatable_flag = db.Column(db.Enum(BooleanEnum))
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='curatorial_unit_definition'
    )
    bibliographic_level = db.relationship(
        'BibliographicLevel', back_populates='curatorial_unit_definition'
    )
    item_type = db.relationship('ItemType', back_populates='curatorial_unit_definition')
    preservation_method = db.relationship(
        'PreservationMethod', back_populates='curatorial_unit_definition'
    )


@dataclass
class Department(db.Model):
    __tablename__ = 'department'
    # fields
    department_id: department_id = db.Column(db.Integer, primary_key=True)
    department_name: department_name = db.Column(db.String(255), nullable=False)
    # relationships
    division = db.relationship('Division', back_populates='department')
    taxon = db.relationship('Taxon', back_populates='department')


@dataclass
class Division(db.Model):
    __tablename__ = 'division'
    # fields
    division_id: division_id = db.Column(db.Integer, primary_key=True)
    department_id: department_id = db.Column(
        db.Integer, db.ForeignKey('department.department_id'), nullable=False
    )
    division_name: division_name = db.Column(db.String(255), nullable=False)
    # relationships
    department = db.relationship('Department', back_populates='division')
    section = db.relationship('Section', back_populates='division')
    users = db.relationship('Users', back_populates='division')


@dataclass
class Enhancements(db.Model):
    __tablename__ = 'enhancements'
    # fields
    enhancement_id: enhancement_id = db.Column(db.Integer, primary_key=True)
    description: description = db.Column(db.String(1000), nullable=False)
    expected_date: expected_date = db.Column(db.DateTime, nullable=False)


@dataclass
class Floor(db.Model):
    __tablename__ = 'floor'
    # fields
    floor_id: floor_id = db.Column(db.Integer, primary_key=True)
    building_id: building_id = db.Column(
        db.Integer, db.ForeignKey('building.building_id'), nullable=False
    )
    floor_name: floor_name = db.Column(db.String(255))
    # relationships
    building = db.relationship('Building', back_populates='floor')
    storage_room = db.relationship('StorageRoom', back_populates='floor')


@dataclass
class GeographicOrigin(db.Model):
    __tablename__ = 'geographic_origin'
    # fields
    geographic_origin_id: geographic_origin_id = db.Column(db.Integer, primary_key=True)
    geographic_origin_name: geographic_origin_name = db.Column(
        db.String(255), nullable=False
    )
    region_type: region_type = db.Column(db.String(255))
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='geographic_origin'
    )


@dataclass
class GeologicalTimePeriod(db.Model):
    __tablename__ = 'geological_time_period'
    # fields
    geological_time_period_id: geological_time_period_id = db.Column(
        db.Integer, primary_key=True
    )
    parent_id: parent_id = db.Column(db.Integer)
    period_name: period_name = db.Column(db.String(255), nullable=False)
    rank: rank = db.Column(db.String(255), nullable=False)
    rank_sort_order: rank_sort_order = db.Column(db.Integer)
    # relationships
    collection_unit_from = db.relationship(
        'CollectionUnit',
        foreign_keys='CollectionUnit.geological_time_period_from_id',
        back_populates='geological_time_period_from',
    )
    collection_unit_to = db.relationship(
        'CollectionUnit',
        foreign_keys='CollectionUnit.geological_time_period_to_id',
        back_populates='geological_time_period_to',
    )


@dataclass
class HelpGuidance(db.Model):
    __tablename__ = 'help_guidance'
    # fields
    guidance_id: guidance_id = db.Column(db.Integer, primary_key=True)
    header: header = db.Column(db.String(50), nullable=False)
    guidance: guidance = db.Column(db.Text)
    recording_url: recording_url = db.Column(db.String(500))


@dataclass
class Issues(db.Model):
    __tablename__ = 'issues'
    # fields
    issue_id: issue_id = db.Column(db.Integer, primary_key=True)
    issue: issue = db.Column(db.Text, nullable=False)
    user_id: user_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False
    )
    date_added: date_added = db.Column(db.DateTime, nullable=False)
    status: status = db.Column(db.String(25), nullable=False, default='raised')
    visible: visible = db.Column(db.Boolean, nullable=False, default=0)
    date_resolved: date_resolved = db.Column(db.DateTime)
    # relationships
    users = db.relationship('Users', back_populates='issues')


@dataclass
class ItemType(db.Model):
    __tablename__ = 'item_type'
    # fields
    item_type_id: item_type_id = db.Column(db.Integer, primary_key=True)
    item_type: item_type = db.Column(db.String(255), nullable=False)
    # relationships
    curatorial_unit_definition = db.relationship(
        'CuratorialUnitDefinition', back_populates='item_type'
    )


@dataclass
class LibraryAndArchivesFunction(db.Model):
    __tablename__ = 'library_and_archives_function'
    # fields
    library_and_archives_function_id: library_and_archives_function_id = db.Column(
        db.Integer, primary_key=True
    )
    function_name: function_name = db.Column(db.String(255), nullable=False)
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='library_and_archives_function'
    )


@dataclass
class Person(db.Model):
    __tablename__ = 'person'
    # fields
    person_id: person_id = db.Column(db.Integer, primary_key=True)
    first_name: first_name = db.Column(db.String(255))
    last_name: last_name = db.Column(db.String(255))
    job_title: job_title = db.Column(db.String(255))
    # relationships
    users = db.relationship('Users', back_populates='person')
    unit_assessment_criterion = db.relationship(
        'UnitAssessmentCriterion', back_populates='person'
    )


@dataclass
class PreservationMethod(db.Model):
    __tablename__ = 'preservation_method'
    # fields
    preservation_method_id: preservation_method_id = db.Column(
        db.Integer, primary_key=True
    )
    preservation_method: preservation_method = db.Column(db.String(255), nullable=False)
    # relationships
    curatorial_unit_definition = db.relationship(
        'CuratorialUnitDefinition', back_populates='preservation_method'
    )


@dataclass
class Rank(db.Model):
    __tablename__ = 'rank'
    # fields
    rank_id: rank_id = db.Column(db.Integer, primary_key=True)
    criterion_id: criterion_id = db.Column(
        db.Integer, db.ForeignKey('criterion.criterion_id'), nullable=False
    )
    rank_value: rank_value = db.Column(db.Integer, nullable=False)
    definition: definition = db.Column(db.Text)
    assessment: assessment = db.Column(db.String(255))
    # relationships
    criterion = db.relationship('Criterion', back_populates='rank')
    unit_assessment_rank = db.relationship('UnitAssessmentRank', back_populates='rank')
    unit_rank_draft = db.relationship('UnitRankDraft', back_populates='rank')


@dataclass
class RescoreSession(db.Model):
    __tablename__ = 'rescore_session'
    # fields
    rescore_session_id: rescore_session_id = db.Column(db.Integer, primary_key=True)
    user_id: user_id = db.Column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False
    )
    status: status = db.Column(db.Enum(StatusEnum), default='in_progress')
    created_at: created_at = db.Column(db.DateTime, default=datetime.now)
    completed_at: completed_at = db.Column(db.DateTime)
    # relationships
    rescore_session_units = db.relationship(
        'RescoreSessionUnits', back_populates='rescore_session'
    )
    users = db.relationship('Users', back_populates='rescore_session')


@dataclass
class RescoreSessionUnits(db.Model):
    __tablename__ = 'rescore_session_units'
    # fields
    rescore_session_units_id: rescore_session_units_id = db.Column(
        db.Integer, primary_key=True
    )
    rescore_session_id: rescore_session_id = db.Column(
        db.Integer, db.ForeignKey('rescore_session.rescore_session_id'), nullable=False
    )
    collection_unit_id: collection_unit_id = db.Column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    # relationships
    rescore_session = db.relationship(
        'RescoreSession', back_populates='rescore_session_units'
    )
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='rescore_session_units'
    )
    unit_category_draft = db.relationship(
        'UnitCategoryDraft', back_populates='rescore_session_units'
    )
    unit_comment_draft = db.relationship(
        'UnitCommentDraft', back_populates='rescore_session_units'
    )
    unit_metric_draft = db.relationship(
        'UnitMetricDraft', back_populates='rescore_session_units'
    )


@dataclass
class Roles(db.Model):
    __tablename__ = 'roles'
    # fields
    role_id: role_id = db.Column(db.Integer, primary_key=True)
    role: role = db.Column(db.String(45), nullable=False)
    level: level = db.Column(db.Integer, nullable=False)
    # relationships
    users = db.relationship('Users', back_populates='roles')


@dataclass
class Section(db.Model):
    __tablename__ = 'section'
    # fields
    section_id: section_id = db.Column(db.Integer, primary_key=True)
    division_id: division_id = db.Column(
        db.Integer, db.ForeignKey('division.division_id'), nullable=False
    )
    section_name: section_name = db.Column(db.String(255), nullable=False)
    # relationships
    division = db.relationship('Division', back_populates='section')
    collection_unit = db.relationship('CollectionUnit', back_populates='section')


@dataclass
class Site(db.Model):
    __tablename__ = 'site'
    # fields
    site_id: site_id = db.Column(db.Integer, primary_key=True)
    site_name: site_name = db.Column(db.String(255))
    # relationships
    building = db.relationship('Building', back_populates='site')


@dataclass
class StorageContainer(db.Model):
    __tablename__ = 'storage_container'
    # fields
    storage_container_id: storage_container_id = db.Column(db.Integer, primary_key=True)
    container_name: container_name = db.Column(db.String(255))
    temperature: temperature = db.Column(db.Integer)
    relative_humidity: relative_humidity = db.Column(db.Integer)
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='storage_container'
    )


@dataclass
class StorageRoom(db.Model):
    __tablename__ = 'storage_room'
    # fields
    storage_room_id: storage_room_id = db.Column(db.Integer, primary_key=True)
    floor_id: floor_id = db.Column(
        db.Integer, db.ForeignKey('floor.floor_id'), nullable=False
    )
    room_name: room_name = db.Column(db.String(255))
    room_code: room_code = db.Column(db.String(255))
    estates_room_type: estates_room_type = db.Column(db.String(50))
    estates_division_code: estates_division_code = db.Column(db.String(50))
    estates_room_area: estates_room_area = db.Column(db.Float)
    floorplan_area: floorplan_area = db.Column(db.Float)
    storage_footprint: storage_footprint = db.Column(db.Float)
    typical_height: typical_height = db.Column(db.Float)
    volume: volume = db.Column(db.Float)
    circulation: circulation = db.Column(db.Float)
    multi_room_split: multi_room_split = db.Column(db.Enum(BooleanEnum))
    threshold_temp_min: threshold_temp_min = db.Column(db.Integer)
    threshold_temp_max: threshold_temp_max = db.Column(db.Integer)
    threshold_rh_min: threshold_rh_min = db.Column(db.Integer)
    threshold_rh_max: threshold_rh_max = db.Column(db.Integer)
    # relationships
    floor = db.relationship('Floor', back_populates='storage_room')
    collection_unit = db.relationship('CollectionUnit', back_populates='storage_room')


@dataclass
class StructuralChangesBasic(db.Model):
    __tablename__ = 'structural_changes_basic'
    # fields
    structural_changes_basic_id: structural_changes_basic_id = db.Column(
        db.Integer, primary_key=True
    )
    structural_changes_higher_id: structural_changes_higher_id = db.Column(db.Integer)
    collection_unit_id: collection_unit_id = db.Column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    operation: operation = db.Column(db.Enum(OperationEnum))
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='structural_changes_basic'
    )


@dataclass
class StructuralChangesComments(db.Model):
    __tablename__ = 'structural_changes_comments'
    # fields
    structural_changes_comment_id: structural_changes_comment_id = db.Column(
        db.Integer, primary_key=True
    )
    structural_changes_higher_id: structural_changes_higher_id = db.Column(
        db.Integer,
        db.ForeignKey('structural_changes_higher.structural_changes_higher_id'),
        nullable=False,
    )
    comment: comment = db.Column(db.Text, nullable=False)
    date_added: date_added = db.Column(db.DateTime)
    # relationships
    structural_changes_higher = db.relationship(
        'StructuralChangesHigher', back_populates='structural_changes_comments'
    )


@dataclass
class StructuralChangesHigher(db.Model):
    __tablename__ = 'structural_changes_higher'
    # fields
    structural_changes_higher_id: structural_changes_higher_id = db.Column(
        db.Integer, primary_key=True
    )
    higher_operation: higher_operation = db.Column(db.Enum(HigherOperationEnum))
    effective_date: effective_date = db.Column(db.DateTime)
    change_agent_id: change_agent_id = db.Column(db.Integer)
    cause: cause = db.Column(db.String(50))
    # relationships
    structural_changes_comments = db.relationship(
        'StructuralChangesComments', back_populates='structural_changes_higher'
    )


@dataclass
class Taxon(db.Model):
    __tablename__ = 'taxon'
    # fields
    taxon_id: taxon_id = db.Column(db.Integer, primary_key=True)
    taxon_name: taxon_name = db.Column(db.String(255), nullable=False)
    taxon_rank: taxon_rank = db.Column(db.String(255), nullable=False)
    external_ref_name: external_ref_name = db.Column(db.String(255))
    external_ref_id: external_ref_id = db.Column(db.String(255))
    department_id: department_id = db.Column(
        db.Integer, db.ForeignKey('department.department_id'), nullable=False
    )
    taxon_life_science_id: taxon_life_science_id = db.Column(db.Integer)
    taxon_palaeontology_id: taxon_palaeontology_id = db.Column(db.Integer)
    # relationships
    department = db.relationship('Department', back_populates='taxon')
    collection_unit = db.relationship('CollectionUnit', back_populates='taxon')


@dataclass
class UnitAssessmentCriterion(db.Model):
    __tablename__ = 'unit_assessment_criterion'
    # fields
    unit_assessment_criterion_id: unit_assessment_criterion_id = db.Column(
        db.Integer, primary_key=True
    )
    collection_unit_id: collection_unit_id = db.Column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    criterion_id: criterion_id = db.Column(
        db.Integer, db.ForeignKey('criterion.criterion_id'), nullable=False
    )
    assessor_id: assessor_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    criteria_assessment: criteria_assessment = db.Column(
        db.Enum(CriteriaAssessmentEnum), nullable=False, default='known'
    )
    date_assessed: date_assessed = db.Column(db.Date)
    date_from: date_from = db.Column(db.DateTime, nullable=False, default=datetime.now)
    date_to: date_to = db.Column(
        db.DateTime, nullable=False, default=datetime(9999, 12, 31, 23, 59, 59)
    )
    current: current = db.Column(db.Enum(BooleanEnum), nullable=False, default='yes')
    # relationships
    criterion = db.relationship('Criterion', back_populates='unit_assessment_criterion')
    person = db.relationship('Person', back_populates='unit_assessment_criterion')
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='unit_assessment_criterion'
    )
    unit_assessment_rank = db.relationship(
        'UnitAssessmentRank', back_populates='unit_assessment_criterion'
    )


@dataclass
class UnitAssessmentRank(db.Model):
    __tablename__ = 'unit_assessment_rank'
    # fields
    unit_assessment_rank_id: unit_assessment_rank_id = db.Column(
        db.Integer, primary_key=True
    )
    unit_assessment_criterion_id: unit_assessment_criterion_id = db.Column(
        db.Integer,
        db.ForeignKey('unit_assessment_criterion.unit_assessment_criterion_id'),
        nullable=False,
    )
    rank_id: rank_id = db.Column(
        db.Integer, db.ForeignKey('rank.rank_id'), nullable=False
    )
    percentage: percentage = db.Column(db.Float, nullable=False)
    comment: comment = db.Column(db.String(1000))
    # relationships
    rank = db.relationship('Rank', back_populates='unit_assessment_rank')
    unit_assessment_criterion = db.relationship(
        'UnitAssessmentCriterion', back_populates='unit_assessment_rank'
    )


@dataclass
class UnitCategoryDraft(db.Model):
    __tablename__ = 'unit_category_draft'
    # fields
    category_draft_id: category_draft_id = db.Column(db.Integer, primary_key=True)
    rescore_session_units_id: rescore_session_units_id = db.Column(
        db.Integer,
        db.ForeignKey('rescore_session_units.rescore_session_units_id'),
        nullable=False,
    )
    category_id: category_id = db.Column(
        db.Integer, db.ForeignKey('category.category_id'), nullable=False
    )
    complete: complete = db.Column(db.Boolean, nullable=False)
    updated_at: updated_at = db.Column(db.DateTime, default=datetime.now)
    # relationships
    rescore_session_units = db.relationship(
        'RescoreSessionUnits', back_populates='unit_category_draft'
    )
    unit_rank_draft = db.relationship(
        'UnitRankDraft', back_populates='unit_category_draft'
    )


@dataclass
class UnitComment(db.Model):
    __tablename__ = 'unit_comment'
    # fields
    unit_comment_id: unit_comment_id = db.Column(db.Integer, primary_key=True)
    collection_unit_id: collection_unit_id = db.Column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    unit_comment: unit_comment = db.Column(db.Text)
    date_added: date_added = db.Column(
        db.DateTime, nullable=False, default=datetime.now
    )
    # relationships
    collection_unit = db.relationship('CollectionUnit', back_populates='unit_comment')


@dataclass
class UnitCommentDraft(db.Model):
    __tablename__ = 'unit_comment_draft'
    # fields
    unit_comment_draft_id: unit_comment_draft_id = db.Column(
        db.Integer, primary_key=True
    )
    rescore_session_units_id: rescore_session_units_id = db.Column(
        db.Integer,
        db.ForeignKey('rescore_session_units.rescore_session_units_id'),
        nullable=False,
    )
    unit_comment: unit_comment = db.Column(db.Text, nullable=False)
    created_at: created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at: updated_at = db.Column(db.DateTime, default=datetime.now)
    # relationships
    rescore_session_units = db.relationship(
        'RescoreSessionUnits', back_populates='unit_comment_draft'
    )


@dataclass
class UnitMetricDraft(db.Model):
    __tablename__ = 'unit_metric_draft'
    # fields
    unit_metric_draft_id: unit_metric_draft_id = db.Column(db.Integer, primary_key=True)
    rescore_session_units_id: rescore_session_units_id = db.Column(
        db.Integer,
        db.ForeignKey('rescore_session_units.rescore_session_units_id'),
        nullable=False,
    )
    collection_unit_metric_definition_id: collection_unit_metric_definition_id = (
        db.Column(
            db.Integer,
            db.ForeignKey(
                'collection_unit_metric_definition.collection_unit_metric_definition_id'
            ),
            nullable=False,
        )
    )
    metric_value: metric_value = db.Column(db.Double, nullable=False)
    confidence_level: confidence_level = db.Column(db.String(1000), nullable=False)
    created_at: created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at: updated_at = db.Column(db.DateTime, default=datetime.now)
    # relationships
    rescore_session_units = db.relationship(
        'RescoreSessionUnits', back_populates='unit_metric_draft'
    )
    collection_unit_metric_definition = db.relationship(
        'CollectionUnitMetricDefinition', back_populates='unit_metric_draft'
    )


@dataclass
class UnitRankDraft(db.Model):
    __tablename__ = 'unit_rank_draft'
    # fields
    rank_draft_id: rank_draft_id = db.Column(db.Integer, primary_key=True)
    category_draft_id: category_draft_id = db.Column(
        db.Integer,
        db.ForeignKey('unit_category_draft.category_draft_id'),
        nullable=False,
    )
    criterion_id: criterion_id = db.Column(
        db.Integer, db.ForeignKey('criterion.criterion_id'), nullable=False
    )
    rank_id: rank_id = db.Column(
        db.Integer, db.ForeignKey('rank.rank_id'), nullable=False
    )
    percentage: percentage = db.Column(db.Float, nullable=False)
    comment: comment = db.Column(db.String(1000))
    created_at: created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at: updated_at = db.Column(db.DateTime, default=datetime.now)
    # relationships
    unit_category_draft = db.relationship(
        'UnitCategoryDraft', back_populates='unit_rank_draft'
    )
    criterion = db.relationship('Criterion', back_populates='unit_rank_draft')
    rank = db.relationship('Rank', back_populates='unit_rank_draft')


@dataclass
class Users(db.Model):
    __tablename__ = 'users'
    # fields
    user_id: user_id = db.Column(db.Integer, primary_key=True)
    email: email = db.Column(db.String(45), unique=True, nullable=False)
    azure_id = db.Column(db.String(45), unique=True, nullable=False)
    role_id: role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    division_id: division_id = db.Column(
        db.Integer, db.ForeignKey('division.division_id')
    )
    person_id: person_id = db.Column(db.Integer, db.ForeignKey('person.person_id'))
    display_name: display_name = db.Column(db.String(100))
    user_active = db.Column(db.SmallInteger, nullable=False)
    # relationships
    roles = db.relationship('Roles', back_populates='users')
    person = db.relationship('Person', back_populates='users')
    issues = db.relationship('Issues', back_populates='users')
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='responsible_curator'
    )
    assigned_units = db.relationship('AssignedUnits', back_populates='users')
    division = db.relationship('Division', back_populates='users')
    rescore_session = db.relationship('RescoreSession', back_populates='users')
