from sqlalchemy.orm import Mapped, mapped_column

from server.database import db


class AssignedUnits(db.Model):
    __tablename__ = 'assigned_units'
    # fields
    assigned_unit_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False
    )
    collection_unit_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('collection_unit.collection_unit_id'), nullable=False
    )
    # relationships
    users = db.relationship('Users', back_populates='assigned_units')
    collection_unit = db.relationship('CollectionUnit', back_populates='assigned_units')


class Person(db.Model):
    __tablename__ = 'person'
    # fields
    person_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    first_name: Mapped[str] = mapped_column(db.String(255))
    last_name: Mapped[str] = mapped_column(db.String(255))
    job_title: Mapped[str] = mapped_column(db.String(255))
    # relationships
    users = db.relationship('Users', back_populates='person')
    unit_assessment_criterion = db.relationship(
        'UnitAssessmentCriterion', back_populates='person'
    )


class Users(db.Model):
    __tablename__ = 'users'
    # fields
    user_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    email: Mapped[str] = mapped_column(db.String(45), unique=True, nullable=False)
    azure_id: Mapped[str] = mapped_column(db.String(45), unique=True, nullable=False)
    role_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('roles.role_id'))
    division_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('division.division_id')
    )
    person_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('person.person_id')
    )
    display_name: Mapped[str] = mapped_column(db.String(100))
    user_active: Mapped[int] = mapped_column(db.SmallInteger, nullable=False)
    # relationships
    roles = db.relationship('Roles', back_populates='users')
    person = db.relationship('Person', back_populates='users')
    issues = db.relationship('Issues', back_populates='users')
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='responsible_curator'
    )
    assigned_units = db.relationship('AssignedUnits', back_populates='users')
    division = db.relationship('Division', back_populates='users')
    rescore_session = db.relationship('RescoreSession', back_populates='users')


class Roles(db.Model):
    __tablename__ = 'roles'
    # fields
    role_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    role: Mapped[str] = mapped_column(db.String(45), nullable=False)
    level: Mapped[int] = mapped_column(db.Integer, nullable=False)
    # relationships
    users = db.relationship('Users', back_populates='roles')
