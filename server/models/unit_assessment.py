from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from server.database import db

from .utils import BooleanEnum, CriteriaAssessmentEnum


class UnitAssessmentCriterion(db.Model):
    __tablename__ = 'unit_assessment_criterion'
    # fields
    unit_assessment_criterion_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    collection_unit_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    criterion_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('criterion.criterion_id'), nullable=False
    )
    assessor_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('person.person_id')
    )
    criteria_assessment: Mapped[CriteriaAssessmentEnum] = mapped_column(
        db.Enum(CriteriaAssessmentEnum), nullable=False, default='known'
    )
    date_assessed: Mapped[datetime] = mapped_column(db.Date)
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
    criterion = db.relationship('Criterion', back_populates='unit_assessment_criterion')
    person = db.relationship('Person', back_populates='unit_assessment_criterion')
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='unit_assessment_criterion'
    )
    unit_assessment_rank = db.relationship(
        'UnitAssessmentRank', back_populates='unit_assessment_criterion'
    )


class UnitAssessmentRank(db.Model):
    __tablename__ = 'unit_assessment_rank'
    # fields
    unit_assessment_rank_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    unit_assessment_criterion_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('unit_assessment_criterion.unit_assessment_criterion_id'),
        nullable=False,
    )
    rank_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('rank.rank_id'), nullable=False
    )
    percentage: Mapped[float] = mapped_column(db.Float, nullable=False)
    comment: Mapped[str] = mapped_column(db.String(1000))
    # relationships
    rank = db.relationship('Rank', back_populates='unit_assessment_rank')
    unit_assessment_criterion = db.relationship(
        'UnitAssessmentCriterion', back_populates='unit_assessment_rank'
    )


class UnitComment(db.Model):
    __tablename__ = 'unit_comment'
    # fields
    unit_comment_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    collection_unit_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    unit_comment: Mapped[str] = mapped_column(db.Text)
    date_added: Mapped[datetime] = mapped_column(
        db.DateTime, nullable=False, default_factory=datetime.now
    )
    # relationships
    collection_unit = db.relationship('CollectionUnit', back_populates='unit_comment')
