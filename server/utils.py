from datetime import datetime, timedelta, timezone

from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    set_access_cookies,
)
from sqlalchemy import select, text

from server.config import Config
from server.database import db
from server.models import Users

database_name = Config.MYSQL_DB


def refresh_jwt_token(response):
    """
    Refresh the JWT token in the response if it is about to expire.
    """
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
    """
    Return the full users details.
    """
    query = f"""SELECT u.*, r.role, r.`level`, p.*,
            COALESCE(CONCAT(p.first_name, ' ', p.last_name), u.display_name) AS name,
            (
                SELECT JSON_ARRAYAGG( au.collection_unit_id )
                FROM {database_name}.assigned_units au
                JOIN {database_name}.collection_unit cu
                    ON au.collection_unit_id = cu.collection_unit_id
                WHERE au.user_id = u.user_id AND cu.unit_active = 'yes'
            ) AS assigned_units,
            (
                SELECT JSON_ARRAYAGG(
                    cu.collection_unit_id
                )
                FROM {database_name}.collection_unit cu
                WHERE cu.responsible_curator_id = u.user_id AND cu.unit_active = 'yes'
            ) AS responsible_units
            FROM {database_name}.users u
            LEFT JOIN {database_name}.roles r ON u.role_id = r.role_id
            LEFT JOIN {database_name}.person p ON u.person_id = p.person_id
            WHERE user_id = :user_id;"""

    data = db.session.execute(text(query), {'user_id': user_id}).fetchone()
    if not data:
        return None
    return dict(data._mapping)


def get_person_id(user_id):
    """
    Return only the person_id for a user.
    """
    user = db.session.execute(select(Users).where(Users.user_id == user_id)).scalar()
    if not user:
        return None
    person_id = user.person_id
    return person_id
