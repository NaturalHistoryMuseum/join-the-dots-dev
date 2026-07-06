from sqlalchemy.orm import Mapped, mapped_column

from server.database import db

from .utils import BooleanEnum


class Building(db.Model):
    __tablename__ = 'building'
    # fields
    building_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    site_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('site.site_id'), nullable=False
    )
    building_name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    # relationships
    site = db.relationship('Site', back_populates='building')
    floor = db.relationship('Floor', back_populates='building')


class Floor(db.Model):
    __tablename__ = 'floor'
    # fields
    floor_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    building_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('building.building_id'), nullable=False
    )
    floor_name: Mapped[str] = mapped_column(db.String(255))
    # relationships
    building = db.relationship('Building', back_populates='floor')
    storage_room = db.relationship('StorageRoom', back_populates='floor')


class Site(db.Model):
    __tablename__ = 'site'
    # fields
    site_id: Mapped[int] = mapped_column(db.Integer, primary_key=True, init=False)
    site_name: Mapped[str] = mapped_column(db.String(255))
    # relationships
    building = db.relationship('Building', back_populates='site')


class StorageContainer(db.Model):
    __tablename__ = 'storage_container'
    # fields
    storage_container_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    container_name: Mapped[str] = mapped_column(db.String(255))
    temperature: Mapped[int] = mapped_column(db.Integer)
    relative_humidity: Mapped[int] = mapped_column(db.Integer)
    # relationships
    collection_unit = db.relationship(
        'CollectionUnit', back_populates='storage_container'
    )


class StorageRoom(db.Model):
    __tablename__ = 'storage_room'
    # fields
    storage_room_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, init=False
    )
    floor_id: Mapped[int] = mapped_column(
        db.Integer, db.ForeignKey('floor.floor_id'), nullable=False
    )
    room_name: Mapped[str] = mapped_column(db.String(255))
    room_code: Mapped[str] = mapped_column(db.String(255))
    estates_room_type: Mapped[str] = mapped_column(db.String(50))
    estates_division_code: Mapped[str] = mapped_column(db.String(50))
    estates_room_area: Mapped[float] = mapped_column(db.Float)
    floorplan_area: Mapped[float] = mapped_column(db.Float)
    storage_footprint: Mapped[float] = mapped_column(db.Float)
    typical_height: Mapped[float] = mapped_column(db.Float)
    volume: Mapped[float] = mapped_column(db.Float)
    circulation: Mapped[float] = mapped_column(db.Float)
    multi_room_split: Mapped[BooleanEnum] = mapped_column(db.Enum(BooleanEnum))
    threshold_temp_min: Mapped[int] = mapped_column(db.Integer)
    threshold_temp_max: Mapped[int] = mapped_column(db.Integer)
    threshold_rh_min: Mapped[int] = mapped_column(db.Integer)
    threshold_rh_max: Mapped[int] = mapped_column(db.Integer)
    # relationships
    floor = db.relationship('Floor', back_populates='storage_room')
    collection_unit = db.relationship('CollectionUnit', back_populates='storage_room')
