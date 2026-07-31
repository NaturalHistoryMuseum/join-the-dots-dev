from datetime import datetime

from flask import jsonify, request
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
)
from sqlalchemy import delete, desc, insert, select, update

from server.database import db

# Data models
from server.models import ChangeLog, Enhancements, HelpGuidance, Issues

from . import data_bp

# Issues endpoints


@data_bp.route('/all-issues', methods=['GET'])
@jwt_required()
def get_all_issues():
    """
    Fetches all issues.
    """
    try:
        issues = db.session.execute(select(Issues)).scalars().all()
        return jsonify(issues)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/visible-issues', methods=['GET'])
@jwt_required()
def get_visible_issues():
    """
    Fetches all issues that are marked as visible to users.
    """
    try:
        issues = (
            db.session.execute(
                select(Issues)
                .where(Issues.visible == 1)
                .order_by(desc(Issues.date_added))
            )
            .scalars()
            .all()
        )
        return jsonify(issues)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/update-issue', methods=['POST'])
@jwt_required()
def update_issue():
    """
    Updates issue details.
    """
    data = request.get_json()
    issue_id = data.get('issue_id')
    visible = data.get('visible')
    status = data.get('status')
    date_resolved = data.get('date_resolved')
    if date_resolved is None:
        formatted_date_resolved = None
    else:
        formatted_date_resolved = datetime.strptime(
            date_resolved, '%a, %d %b %Y %H:%M:%S %Z'
        )
    try:
        db.session.execute(
            update(Issues)
            .where(Issues.issue_id == issue_id)
            .values(
                visible=visible,
                status=status,
                date_resolved=formatted_date_resolved,
            )
        )
        db.session.commit()
        return jsonify({'message': 'Issue updated successfully', 'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/submit-issue', methods=['POST'])
@jwt_required()
def submit_issue():
    """
    Adds a new issue.
    """
    data = request.get_json()
    issue = data.get('issue')
    # Get user_id from the jwt token
    user_id = get_jwt_identity()
    date_added = datetime.now()
    try:
        db.session.execute(
            insert(Issues).values(
                issue=issue,
                user_id=user_id,
                date_added=date_added,
                visible=0,
                status='raised',
            )
        )
        db.session.commit()
        return jsonify(
            {'message': 'Issue submitted successfully', 'success': True}
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Help guidance endpoints


@data_bp.route('/all-guidance', methods=['GET'])
@jwt_required()
def get_all_guidance():
    """
    Fetch all the help guidance.
    """
    guidance = db.session.execute(select(HelpGuidance)).scalars().all()
    return jsonify(guidance)


@data_bp.route('/update-guidance', methods=['POST'])
@jwt_required()
def update_guidance():
    """
    Update the help guidance data.
    """
    data = request.get_json()
    guidance_id = data.get('guidance_id')
    header = data.get('header')
    guidance = data.get('guidance')
    recording_url = data.get('recording_url', None)
    try:
        db.session.execute(
            update(HelpGuidance)
            .where(HelpGuidance.guidance_id == guidance_id)
            .values(
                header=header,
                guidance=guidance,
                recording_url=recording_url,
            )
        )
        db.session.commit()
        return jsonify(
            {'message': 'Guidance updated successfully', 'success': True}
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/add-guidance', methods=['POST'])
@jwt_required()
def add_guidance():
    """
    Add new help guidance data.
    """
    data = request.get_json()
    header = data.get('header')
    guidance = data.get('guidance')
    recording_url = data.get('recording_url', None)
    try:
        db.session.execute(
            insert(HelpGuidance).values(
                header=header, guidance=guidance, recording_url=recording_url
            )
        )
        db.session.commit()
        return jsonify(
            {'message': 'Guidance updated successfully', 'success': True}
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/remove-guidance', methods=['POST'])
@jwt_required()
def remove_guidance():
    """
    Remove specific help guidance.
    """
    data = request.get_json()
    guidance_id = data.get('guidance_id')
    try:
        db.session.execute(
            delete(HelpGuidance).where(HelpGuidance.guidance_id == guidance_id)
        )
        db.session.commit()
        return jsonify({'message': 'Guidance updated removed', 'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Change log endpoints


@data_bp.route('/change-log', methods=['GET'])
@jwt_required()
def get_change_log():
    """
    Fetch all change logs.
    """
    try:
        change_logs = (
            db.session.execute(select(ChangeLog).order_by(desc(ChangeLog.date_added)))
            .scalars()
            .all()
        )
        return jsonify(change_logs)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/add-change-log', methods=['POST'])
@jwt_required()
def add_change_log():
    """
    Insert new change log.
    """
    data = request.get_json()
    title = data.get('title')
    log = data.get('log')
    date_added = datetime.now()
    try:
        db.session.execute(
            insert(ChangeLog).values(title=title, log=log, date_added=date_added)
        )
        db.session.commit()
        return jsonify(
            {'message': 'Change log added successfully', 'success': True}
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/update-change-log', methods=['POST'])
@jwt_required()
def update_change_log():
    """
    Edit change log.
    """
    data = request.get_json()
    change_log_id = data.get('change_log_id')
    title = data.get('title')
    log = data.get('log')
    try:
        db.session.execute(
            update(ChangeLog)
            .where(ChangeLog.change_log_id == change_log_id)
            .values(
                title=title,
                log=log,
            )
        )
        db.session.commit()
        return jsonify(
            {'message': 'Change log updated successfully', 'success': True}
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/enhancements', methods=['GET'])
@jwt_required()
def get_enhancements():
    """
    Fetch all enhancements.
    """
    try:
        enhancements = db.session.execute(select(Enhancements)).scalars().all()
        return jsonify(enhancements)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/add-enhancements', methods=['POST'])
@jwt_required()
def add_enhancements():
    """
    Add a new enhancement.
    """
    data = request.get_json()
    description = data.get('description')
    expected_date = data.get('expected_date')
    try:
        db.session.execute(
            insert(Enhancements).values(
                description=description, expected_date=expected_date
            )
        )
        db.session.commit()
        return jsonify(
            {'message': 'Enhancement added successfully', 'success': True}
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@data_bp.route('/update-enhancements', methods=['POST'])
@jwt_required()
def update_enhancements():
    """
    Edit an enhancement.
    """
    data = request.get_json()
    enhancement_id = data.get('enhancement_id')
    description = data.get('description')
    expected_date = data.get('expected_date')
    try:
        db.session.execute(
            update(Enhancements)
            .where(Enhancements.enhancement_id == enhancement_id)
            .values(
                description=description,
                expected_date=expected_date,
            )
        )
        db.session.commit()
        return jsonify(
            {'message': 'Enhancement updated successfully', 'success': True}
        ), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
