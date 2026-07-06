from sqlalchemy.orm import Mapped, mapped_column

from server.database import db


class Category(db.Model):
    __tablename__ = 'category'
    # fields
    category_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    category_code: Mapped[str] = mapped_column(db.String(255))
    description: Mapped[str] = mapped_column(db.String(255))
    # relationships
    criterion = db.relationship('Criterion', back_populates='category')


class Criterion(db.Model):
    __tablename__ = 'criterion'
    # fields
    criterion_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    category_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('category.category_id')
    )
    criterion_code: Mapped[str] = mapped_column(db.String(255))
    criterion_name: Mapped[str] = mapped_column(db.String(255))
    definition: Mapped[str] = mapped_column(db.Text)
    referenced_standards: Mapped[str] = mapped_column(db.Text)
    # relationships
    category = db.relationship('Category', back_populates='criterion')
    rank = db.relationship('Rank', back_populates='criterion')
    unit_assessment_criterion = db.relationship(
        'UnitAssessmentCriterion', back_populates='criterion'
    )
    unit_rank_draft = db.relationship('UnitRankDraft', back_populates='criterion')


class Rank(db.Model):
    __tablename__ = 'rank'
    # fields
    rank_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    criterion_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('criterion.criterion_id'), nullable=False
    )
    rank_value: Mapped[int] = mapped_column(db.Integer, nullable=False)
    definition: Mapped[str] = mapped_column(db.Text)
    assessment: Mapped[str] = mapped_column(db.String(255))
    # relationships
    criterion = db.relationship('Criterion', back_populates='rank')
    unit_assessment_rank = db.relationship('UnitAssessmentRank', back_populates='rank')
    unit_rank_draft = db.relationship('UnitRankDraft', back_populates='rank')
