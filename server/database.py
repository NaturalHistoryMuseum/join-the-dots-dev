from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass


# Set base to be a dataclass
class Base(MappedAsDataclass, DeclarativeBase, kw_only=True):
    pass


# SqlAlchemy Connection
db = SQLAlchemy(model_class=Base)
