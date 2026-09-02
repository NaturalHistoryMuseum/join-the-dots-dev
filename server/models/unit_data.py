from sqlalchemy.orm import Mapped, mapped_column

from server.database import db


class GeographicOrigin(db.Model):
    __tablename__ = 'geographic_origin'
    # fields
    geographic_origin_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    geographic_origin_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    region_type: Mapped[str] = mapped_column(db.String(255))
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='geographic_origin'
    )


class GeologicalTimePeriod(db.Model):
    __tablename__ = 'geological_time_period'
    # fields
    geological_time_period_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    parent_id: Mapped[int] = mapped_column(db.Integer)
    period_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    rank: Mapped[str] = mapped_column(db.String(255), nullable=False)
    rank_sort_order: Mapped[int] = mapped_column(db.Integer)
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


class LibraryAndArchivesFunction(db.Model):
    __tablename__ = 'library_and_archives_function'
    # fields
    library_and_archives_function_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    function_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='library_and_archives_function'
    )


class Taxon(db.Model):
    __tablename__ = 'taxon'
    # fields
    taxon_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    taxon_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    taxon_rank: Mapped[str] = mapped_column(db.String(255), nullable=False)
    external_ref_name: Mapped[str] = mapped_column(db.String(255))
    external_ref_id: Mapped[str] = mapped_column(db.String(255))
    department_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('department.department_id'), nullable=False
    )
    taxon_life_science_id: Mapped[int] = mapped_column(db.Integer)
    taxon_palaeontology_id: Mapped[int] = mapped_column(db.Integer)
    # relationships
    department = db.relationship('Department', back_populates='taxon')
    collection_unit = db.relationship('CollectionUnit', back_populates='taxon')
