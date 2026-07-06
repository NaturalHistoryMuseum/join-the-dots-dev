from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from server.database import db

from .utils import StatusEnum


class RescoreSession(db.Model):
    __tablename__ = 'rescore_session'
    # fields
    rescore_session_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False
    )
    status: Mapped[StatusEnum] = mapped_column(
        db.Enum(StatusEnum), default='in_progress'
    )
    created_at: Mapped[datetime] = mapped_column(
        db.DateTime, default_factory=datetime.now
    )
    completed_at: Mapped[datetime] = mapped_column(db.DateTime)
    # relationships
    rescore_session_units = db.relationship(
        'RescoreSessionUnits', back_populates='rescore_session'
    )
    users = db.relationship('Users', back_populates='rescore_session')


class RescoreSessionUnits(db.Model):
    __tablename__ = 'rescore_session_units'
    # fields
    rescore_session_units_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    rescore_session_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('rescore_session.rescore_session_id'), nullable=False
    )
    collection_unit_id: Mapped[int] = mapped_column(
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
