from flask import Blueprint, request
from flask_jwt_extended import (
    get_jwt_identity,
    verify_jwt_in_request,
)

from server.utils import (
    get_person_id,
    refreshJWTToken,
)

# Create data blueprint
data_bp = Blueprint('data', __name__)

# Import subfiles
from sqlalchemy import text

from server.database import db
from server.models import Person

from . import rescore, support, unit_actions, unit_data


# After a request, refresh the JWT token if it is about to expire
@data_bp.after_request
def refresh_expiring_jwts(response):
    return refreshJWTToken(response)


# Before request - set the current person_id for the audit log
@data_bp.before_request
def set_current_user():
    try:
        verify_jwt_in_request()
        user_id = get_jwt_identity()
        if user_id:
            person_id = get_person_id(user_id)
        else:
            person_id = None

    except Exception:
        person_id = None

    db.session.execute(
        text('SET @current_person_id = :person_id'), {'person_id': person_id}
    )
