from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from sqlalchemy import literal, select, update

from server.database import db
from server.models import Roles, Users

user_bp = Blueprint('user', __name__)


@user_bp.route('/edit-user-role', methods=['POST'])
@jwt_required()
def edit_user_role():
    data = request.get_json()
    role_id = data.get('role_id')
    user_id = data.get('user_id')

    if not role_id:
        return jsonify({'error': 'Role is required'}), 400

    # Update role and commit changes
    try:
        db.session.execute(
            update(Users).where(Users.user_id == user_id).values(role_id=role_id)
        )
        db.session.commit()
        return jsonify({'message': 'Role successfully changed', 'success': True}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@user_bp.route('/update-division', methods=['POST'])
@jwt_required()
def edit_user_division():
    data = request.get_json()
    division_id = data.get('division_id')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()

    db.session.execute(
        update(Users).where(Users.user_id == user_id).values(division_id=division_id)
    )
    db.session.commit()
    return jsonify({'success': True}), 201


@user_bp.route('/upgrade-viewer', methods=['POST'])
@jwt_required()
def upgrade_viewer():
    data = request.get_json()
    user_id = data.get('user_id')
    division_id = data.get('division_id')

    db.session.execute(
        update(Users)
        .where(Users.user_id == user_id)
        .values(division_id=division_id, role_id=2)
    )
    db.session.commit()
    return jsonify({'success': True}), 201


@user_bp.route('/all-viewers', methods=['GET'])
@jwt_required()
def all_viewers():
    query = (
        select(*Users.__table__.columns, Roles.role, literal(False).label('selected'))
        .join(Roles, Roles.role_id == Users.role_id)
        .where(Users.role_id == 1)
    )

    data = db.session.execute(query).mappings().all()
    return jsonify([dict(row) for row in data])
