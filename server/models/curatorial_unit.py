from sqlalchemy.orm import Mapped, mapped_column

from server.database import db

from .utils import BooleanEnum


class BibliographicLevel(db.Model):
    __tablename__ = 'bibliographic_level'
    # fields
    bibliographic_level_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    bibliographic_level: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # relationships
    curatorial_unit_definition = db.relationship(
        'CuratorialUnitDefinition', back_populates='bibliographic_level'
    )


class CuratorialUnitDefinition(db.Model):
    __tablename__ = 'curatorial_unit_definition'
    # fields
    curatorial_unit_definition_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    item_type_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('item_type.item_type_id'), nullable=False
    )
    preservation_method_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('preservation_method.preservation_method_id'),
        nullable=False,
    )
    bibliographic_level_id: Mapped[int] = mapped_column(
        db.Integer,
        db.ForeignKey('bibliographic_level.bibliographic_level_id'),
        nullable=False,
    )
    description: Mapped[str] = mapped_column(db.String(255))
    typical_item_count: Mapped[str] = mapped_column(db.String(255))
    typical_item_count_range: Mapped[str] = mapped_column(db.String(255))
    items_unestimatable_flag: Mapped[BooleanEnum] = mapped_column(db.Enum(BooleanEnum))
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


class ItemType(db.Model):
    __tablename__ = 'item_type'
    # fields
    item_type_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    item_type: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # relationships
    curatorial_unit_definition = db.relationship(
        'CuratorialUnitDefinition', back_populates='item_type'
    )


class PreservationMethod(db.Model):
    __tablename__ = 'preservation_method'
    # fields
    preservation_method_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    preservation_method: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # relationships
    curatorial_unit_definition = db.relationship(
        'CuratorialUnitDefinition', back_populates='preservation_method'
    )
