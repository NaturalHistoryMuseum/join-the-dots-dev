from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from server.database import db

from .utils import BooleanEnum


class CollectionUnitMetric(db.Model):
    __tablename__ = 'collection_unit_metric'
    # fields
    collection_unit_metric_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    collection_unit_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    collection_unit_metric_definition_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey(
            'collection_unit_metric_definition.collection_unit_metric_definition_id'
        ),
        nullable=False,
    )
    metric_value: Mapped[int] = mapped_column(db.Double, nullable=False)
    confidence_level: Mapped[str] = mapped_column(db.String(255))
    date_from: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=False, default_factory=datetime.now
    )
    date_to: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=False, default=datetime(9999, 12, 31, 23, 59, 59)
    )
    current: Mapped[BooleanEnum] = mapped_column(
        db.Enum(BooleanEnum), nullable=False, default='yes'
    )
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='collection_unit_metric'
    )
    collection_unit_metric_definition = db.relationship(
        'CollectionUnitMetricDefinition', back_populates='collection_unit_metric'
    )


class CollectionUnitMetricDefinition(db.Model):
    __tablename__ = 'collection_unit_metric_definition'
    # fields
    collection_unit_metric_definition_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    metric_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    metric_definition: Mapped[str] = mapped_column(db.String(255))
    metric_units: Mapped[str] = mapped_column(db.String(255))
    metric_datatype: Mapped[str] = mapped_column(db.String(255))
    # relationships
    collection_unit_metric = db.relationship(
        'CollectionUnitMetric', back_populates='collection_unit_metric_definition'
    )
    unit_metric_draft = db.relationship(
        'UnitMetricDraft', back_populates='collection_unit_metric_definition'
    )
