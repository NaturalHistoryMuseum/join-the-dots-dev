from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column

from server.database import db


class ChangeLog(db.Model):
    __tablename__ = 'change_log'
    # fields
    change_log_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    title: Mapped[str] = mapped_column(db.String(100), nullable=False)
    log: Mapped[str] = mapped_column(db.Text, nullable=False)
    date_added: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)


class Enhancements(db.Model):
    __tablename__ = 'enhancements'
    # fields
    enhancement_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    description: Mapped[str] = mapped_column(db.String(1000), nullable=False)
    expected_date: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)


class HelpGuidance(db.Model):
    __tablename__ = 'help_guidance'
    # fields
    guidance_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    header: Mapped[str] = mapped_column(db.String(50), nullable=False)
    guidance: Mapped[str] = mapped_column(db.Text)
    recording_url: Mapped[str] = mapped_column(db.String(500))


class Issues(db.Model):
    __tablename__ = 'issues'
    # fields
    issue_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    issue: Mapped[str] = mapped_column(db.Text, nullable=False)
    user_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('users.user_id'), nullable=False
    )
    date_added: Mapped[datetime] = mapped_column(db.DateTime, nullable=False)
    status: Mapped[str] = mapped_column(db.String(25), nullable=False, default='raised')
    visible: Mapped[bool] = mapped_column(db.Boolean, nullable=False, default=0)
    date_resolved: Mapped[datetime] = mapped_column(db.DateTime)
    # relationships
    users = db.relationship('Users', back_populates='issues')
