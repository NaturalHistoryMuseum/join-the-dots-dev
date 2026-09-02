from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from server.database import db

from .utils import HigherOperationEnum, OperationEnum


class StructuralChangesBasic(db.Model):
    __tablename__ = 'structural_changes_basic'
    # fields
    structural_changes_basic_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    structural_changes_higher_id: Mapped[int] = mapped_column(db.Integer)
    collection_unit_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    operation: Mapped[OperationEnum] = mapped_column(db.Enum(OperationEnum))
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='structural_changes_basic'
    )


class StructuralChangesComments(db.Model):
    __tablename__ = 'structural_changes_comments'
    # fields
    structural_changes_comment_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    structural_changes_higher_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('structural_changes_higher.structural_changes_higher_id'),
        nullable=False,
    )
    comment: Mapped[str] = mapped_column(db.Text, nullable=False)
    date_added: Mapped[datetime] = mapped_column(db.DateTime)
    # relationships
    structural_changes_higher = db.relationship(
        'StructuralChangesHigher', back_populates='structural_changes_comments'
    )


class StructuralChangesHigher(db.Model):
    __tablename__ = 'structural_changes_higher'
    # fields
    structural_changes_higher_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    higher_operation: Mapped[HigherOperationEnum] = mapped_column(
        db.Enum(HigherOperationEnum)
    )
    effective_date: Mapped[datetime] = mapped_column(db.DateTime)
    change_agent_id: Mapped[int] = mapped_column(db.Integer)
    cause: Mapped[str] = mapped_column(db.String(50))
    # relationships
    structural_changes_comments = db.relationship(
        'StructuralChangesComments', back_populates='structural_changes_higher'
    )
