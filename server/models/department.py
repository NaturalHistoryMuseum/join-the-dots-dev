from sqlalchemy.orm import Mapped, mapped_column

from server.database import db


class Department(db.Model):
    __tablename__ = 'department'
    # fields
    department_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    department_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # relationships
    division = db.relationship('Division', back_populates='department')
    taxon = db.relationship('Taxon', back_populates='department')


class Division(db.Model):
    __tablename__ = 'division'
    # fields
    division_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    department_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('department.department_id'), nullable=False
    )
    division_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # relationships
    department = db.relationship('Department', back_populates='division')
    section = db.relationship('Section', back_populates='division')
    users = db.relationship('Users', back_populates='division')


class Section(db.Model):
    __tablename__ = 'section'
    # fields
    section_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    division_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('division.division_id'), nullable=False
    )
    section_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # relationships
    division = db.relationship('Division', back_populates='section')
    collection_unit = db.relationship('CollectionUnit', back_populates='section')
