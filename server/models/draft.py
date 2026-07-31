from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from server.database import db


class UnitCategoryDraft(db.Model):
    __tablename__ = 'unit_category_draft'
    # fields
    category_draft_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    rescore_session_units_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('rescore_session_units.rescore_session_units_id'),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('category.category_id'), nullable=False
    )
    complete: Mapped[bool] = mapped_column(db.Boolean, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime, default_factory=datetime.now
    )
    # relationships
    rescore_session_units = db.relationship(
        'RescoreSessionUnits', back_populates='unit_category_draft'
    )
    unit_rank_draft = db.relationship(
        'UnitRankDraft', back_populates='unit_category_draft'
    )


class UnitCommentDraft(db.Model):
    __tablename__ = 'unit_comment_draft'
    # fields
    unit_comment_draft_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    rescore_session_units_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('rescore_session_units.rescore_session_units_id'),
        nullable=False,
    )
    unit_comment: Mapped[str] = mapped_column(db.Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime, default_factory=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime, default_factory=datetime.now
    )
    # relationships
    rescore_session_units = db.relationship(
        'RescoreSessionUnits', back_populates='unit_comment_draft'
    )


class UnitMetricDraft(db.Model):
    __tablename__ = 'unit_metric_draft'
    # fields
    unit_metric_draft_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    rescore_session_units_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('rescore_session_units.rescore_session_units_id'),
        nullable=False,
    )
    collection_unit_metric_definition_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey(
            'collection_unit_metric_definition.collection_unit_metric_definition_id'
        ),
        nullable=False,
    )
    metric_value: Mapped[float] = mapped_column(db.Double, nullable=False)
    confidence_level: Mapped[str] = mapped_column(db.String(1000), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime, default_factory=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime, default_factory=datetime.now
    )
    # relationships
    rescore_session_units = db.relationship(
        'RescoreSessionUnits', back_populates='unit_metric_draft'
    )
    collection_unit_metric_definition = db.relationship(
        'CollectionUnitMetricDefinition', back_populates='unit_metric_draft'
    )


class UnitRankDraft(db.Model):
    __tablename__ = 'unit_rank_draft'
    # fields
    rank_draft_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    category_draft_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('unit_category_draft.category_draft_id'),
        nullable=False,
    )
    criterion_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('criterion.criterion_id'), nullable=False
    )
    rank_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('rank.rank_id'), nullable=False
    )
    percentage: Mapped[float] = mapped_column(db.Float, nullable=False)
    comment: Mapped[str] = mapped_column(db.String(1000))
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime, default_factory=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        db.DateTime, default_factory=datetime.now
    )
    # relationships
    unit_category_draft = db.relationship(
        'UnitCategoryDraft', back_populates='unit_rank_draft'
    )
    criterion = db.relationship('Criterion', back_populates='unit_rank_draft')
    rank = db.relationship('Rank', back_populates='unit_rank_draft')
