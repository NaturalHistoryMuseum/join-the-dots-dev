from sqlalchemy.orm import Mapped, mapped_column

from server.database import db

from .utils import BooleanEnum


class CollectionUnit(db.Model):
    __tablename__ = 'collection_unit'
    # fields
    collection_unit_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    unit_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    public_unit_name: Mapped[str] = mapped_column(db.String(255))
    section_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('section.section_id'), nullable=False
    )
    unit_active: Mapped[BooleanEnum] = mapped_column(
        db.Enum(BooleanEnum), nullable=False, default='yes'
    )
    responsible_curator_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('users.user_id')
    )
    curatorial_unit_definition_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('curatorial_unit_definition.curatorial_unit_definition_id'),
    )
    storage_room_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('storage_room.storage_room_id')
    )
    storage_container_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('storage_container.storage_container_id')
    )
    geographic_origin_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('geographic_origin.geographic_origin_id')
    )
    library_and_archives_function_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('library_and_archives_function.library_and_archives_function_id'),
    )
    geological_time_period_from_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('geological_time_period.geological_time_period_id')
    )
    geological_time_period_to_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('geological_time_period.geological_time_period_id')
    )
    type_collection_flag: Mapped[BooleanEnum] = mapped_column(db.Enum(BooleanEnum))
    publish_flag: Mapped[BooleanEnum] = mapped_column(db.Enum(BooleanEnum))
    informal_taxon: Mapped[str] = mapped_column(db.Text)
    named_collection: Mapped[str] = mapped_column(db.String(255))
    es_recent_specimen_flag: Mapped[BooleanEnum] = mapped_column(db.Enum(BooleanEnum))
    archives_fond_ref: Mapped[str] = mapped_column(db.String(255))
    count_curatorial_units_flag: Mapped[BooleanEnum] = mapped_column(
        db.Enum(BooleanEnum)
    )
    sort_order: Mapped[int] = mapped_column(db.Integer)
    taxon_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('taxon.taxon_id'))
    draft_unit: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=0)
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
