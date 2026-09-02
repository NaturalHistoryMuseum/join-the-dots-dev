from datetime import datetime, timedelta, timezone

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
)
from sqlalchemy import func, select

from server.config import Config
from server.database import db
from server.models import AssignedUnits, CollectionUnit, Roles, Users

database_name = Config.MYSQL_DB


def refresh_jwt_token(response):
    """Refresh the JWT token in the response if it is about to expire."""
    try:
        exp_timestamp = get_jwt()['exp']
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=10))
        # if the token is about to expire in 10 mins, create a new one
        if target_timestamp > exp_timestamp:
            user_id = get_jwt_identity()
            # Generate a new access token
            new_access_token = create_access_token(identity=user_id)
            set_access_cookies(response, new_access_token)
            return response
        # Return if token is not about to expire
        else:
            return response

    except (RuntimeError, KeyError):
        # Case where there is not a valid JWT. Just return the original response
        return response


def get_user_by_id(user_id):
    """Return the full users details."""
    au_subquery = (
        select(func.JSON_ARRAYAGG(AssignedUnits.collection_unit_id))
        .join(
            CollectionUnit,
            CollectionUnit.collection_unit_id == AssignedUnits.collection_unit_id,
        )
        .where(
            AssignedUnits.user_id == Users.user_id,
            CollectionUnit.unit_active == 'yes',
        )
        .correlate(Users)
        .scalar_subquery()
    )

    ru_subquery = (
        select(func.JSON_ARRAYAGG(CollectionUnit.collection_unit_id))
        .where(
            CollectionUnit.responsible_curator_id == Users.user_id,
            CollectionUnit.unit_active == 'yes',
        )
        .correlate(Users)
        .scalar_subquery()
    )

    data = db.session.execute(
        select(
            Users,
            Roles,
            au_subquery.label('assigned_units'),
            ru_subquery.label('responsible_units'),
        )
        .join(Roles, Users.role_id == Roles.role_id)
        .where(Users.user_id == user_id)
    ).one_or_none()

    if data is None:
        return None

    return {
        **{c.name: getattr(data.Users, c.name) for c in Users.__table__.columns},
        **{c.name: getattr(data.Roles, c.name) for c in Roles.__table__.columns},
        'name': data.Users.display_name,
        'assigned_units': data.assigned_units,
        'responsible_units': data.responsible_units,
    }


def get_person_id(user_id):
    """Return only the person_id for a user."""
    user = db.session.execute(select(Users).where(Users.user_id == user_id)).scalar()
    if not user:
        return None
    person_id = user.person_id
    return person_id
