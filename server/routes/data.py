from flask import Blueprint, jsonify, Response, stream_with_context
from server.database import get_db_connection
import json

import csv

from server.routes.queries.data_queries import *

data_bp = Blueprint('data', __name__)

database_name = 'jtd_test'

def fetch_data(query, params=None):
    """Helper function to execute a database query."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    # Format the query with the database name
    formatted_query = query.format(database_name=database_name)
    cursor.execute(formatted_query, params or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

@data_bp.route('/unit-department', methods=['GET'])
def get_units_and_departments():
    print("get_units_and_departments")
    data = fetch_data("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, department.department_name, unit.unit_active
                   FROM {database_name}.collection_unit AS unit 
                    LEFT JOIN {database_name}.section AS section ON unit.section_id = section.section_id
                    LEFT JOIN {database_name}.division AS division ON section.division_id = division.division_id
                    LEFT JOIN {database_name}.department AS department ON division.department_id = department.department_id
                   """)
    return jsonify(data)

@data_bp.route('/unit/<unit_id>', methods=['GET'])
def get_unit(unit_id):
    data = fetch_data("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, department.department_name, unit.*
                   FROM {database_name}.collection_unit AS unit 
                    LEFT JOIN {database_name}.section AS section ON unit.section_id = section.section_id
                    LEFT JOIN {database_name}.division AS division ON section.division_id = division.division_id
                    LEFT JOIN {database_name}.department AS department ON division.department_id = department.department_id
                    WHERE  unit.collection_unit_id = %u
                   """ % int(unit_id))
    return jsonify(data)

@data_bp.route('/full-unit/<unit_id>', methods=['GET'])
def get_full_unit(unit_id):
    data = fetch_data("""SELECT  cu.*, concat(p.first_name, ' ', p.last_name) AS responsible_curator,
                    uc.unit_comment, DATE(uc.date_added) AS date_comment_added
                    FROM {database_name}.collection_unit cu 
                    LEFT JOIN {database_name}.person p ON p.person_id = cu.responsible_curator_id 
                    LEFT JOIN {database_name}.unit_comment uc ON uc.collection_unit_id = cu.collection_unit_id
                    WHERE cu.collection_unit_id = %u
                   """ % int(unit_id))
    return jsonify(data)

@data_bp.route('/criterion', methods=['GET'])
def get_criterion():
    data = fetch_data("""SELECT cat.*, crit.criterion_id, crit.criterion_name, crit.criterion_code, crit.definition
                   FROM {database_name}.criterion crit
                    LEFT JOIN {database_name}.category cat ON crit.category_id = cat.category_id
                   """)
    return jsonify(data)

@data_bp.route('/category', methods=['GET'])
def get_category():
    data = fetch_data("""SELECT cat.*
                   FROM {database_name}.category cat
                   """)
    return jsonify(data)

@data_bp.route('/all-sections', methods=['GET'])
def get_all_sections():
    data = fetch_data("""SELECT sect.*, divis.department_id, divis.division_name, dept.department_name
                   FROM {database_name}.section sect 
                    LEFT JOIN {database_name}.division divis ON divis.division_id = sect.division_id
                    LEFT JOIN {database_name}.department dept ON dept.department_id = divis.department_id
                   """)
    return jsonify(data)

@data_bp.route('/all-geographic-origin', methods=['GET'])
def get_all_geographic_origin():
    data = fetch_data("""SELECT *
                   FROM {database_name}.geographic_origin
                   """)
    return jsonify(data)

@data_bp.route('/all-geological-time-period', methods=['GET'])
def get_all_geological_time_period():
    data = fetch_data("""SELECT *
                   FROM {database_name}.geological_time_period
                   """)
    return jsonify(data)


@data_bp.route('/all-divisions', methods=['GET'])
def get_all_divisions():
    data = fetch_data("""SELECT divis.*
                   FROM {database_name}.division divis
                   
                   """)
    return jsonify(data)

@data_bp.route('/all-departments', methods=['GET'])
def get_all_departments():
    data = fetch_data("""SELECT *
                   FROM {database_name}.department 
                   """)
    return jsonify(data)

@data_bp.route('/container-data', methods=['GET'])
def get_all_containers():
    data = fetch_data("""SELECT *
                   FROM {database_name}.storage_container 
                   """)
    return jsonify(data)

@data_bp.route('/all-taxon', methods=['GET'])
def get_all_taxon():
    data = fetch_data("""SELECT *
                   FROM {database_name}.taxon 
                   """)
    return jsonify(data)

@data_bp.route('/all-curtorial-definition', methods=['GET'])
def get_all_curtorial_definition():
    data = fetch_data("""SELECT cud.*, bl.*, it.*, pm.*
                    FROM {database_name}.curatorial_unit_definition cud 
                    LEFT JOIN {database_name}.bibliographic_level bl ON bl.bibliographic_level_id = cud.bibliographic_level_id 
                    LEFT JOIN {database_name}.item_type it ON it.item_type_id = cud.item_type_id 
                    LEFT JOIN {database_name}.preservation_method pm ON pm.preservation_method_id = cud.preservation_method_id  
                   """)
    return jsonify(data)

@data_bp.route('/room-data', methods=['GET'])
def get_all_rooms():
    data = fetch_data("""SELECT sr.*, f.*, b.*, s.*
                        FROM {database_name}.storage_room sr
                        JOIN {database_name}.floor f ON f.floor_id = sr.floor_id 
                        JOIN {database_name}.building b ON b.building_id = f.building_id 
                        JOIN {database_name}.site s ON s.site_id = b.site_id 
                   """)
    return jsonify(data)

@data_bp.route('/all-lib-function', methods=['GET'])
def get_all_lib_function():
    data = fetch_data("""SELECT *
                        FROM {database_name}.library_and_archives_function
                   """)
    return jsonify(data)


@data_bp.route('/export-view/<view>', methods=['GET'])
def get_view(view):
    try:
        # Connect to db
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        query = """SELECT * 
                        FROM {database_name}.%s
                        """ % str(view,)
        # Format the query with the database name
        formatted_query = query.format(database_name=database_name)
        # Execute query
        cursor.execute(formatted_query)
        # Fetch rows
        data = cursor.fetchall()

        # Get the column names
        col_names = [desc[0] for desc in cursor.description]
        # Create CSV response
        def generate():
            # Make headers
            header = ",".join(col_names)
            # Convert JSON objects to a comma-separated string
            rows = "\n".join(",".join(str(row[col]) for col in col_names) for row in data)
            # Return both
            return f"{header}\n{rows}"

        # Create Response with CSV MIME type
        response = Response(generate(), mimetype="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename="+view+".csv"

        return response
    
    except Exception as e:
        return str(e)

    finally:
        cursor.close()
        connection.close()

def generate_json():
    data = fetch_data(LTC_EXPORT)
    if data:
        try:
            # Extract JSON 
            json_data = json.loads(data[0]['ltc_export']) 
        except json.JSONDecodeError as e:
            yield '{"error": "Invalid JSON format"}'
            return
        # Stream the JSON array directly
        yield '[\n'
        for i, item in enumerate(json_data):
            comma = ',' if i < len(json_data) - 1 else ''
            yield f'  {json.dumps(item)}{comma}\n'
        yield ']\n'

@data_bp.route('/export-ltc-json', methods=['GET'])
def get_ltc_json():
    return Response(stream_with_context(generate_json()), 
                content_type="application/json",
                headers={'Content-Disposition': 'attachment; filename=data.json'})

# Old section get with no ranking data
# @data_bp.route('/section-units/<sectionId>', methods=['GET'])
# def get_section_units(sectionId):
#     data = fetch_data("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, section.section_name, unit.*
#                    FROM {database_name}.collection_unit AS unit 
#                     LEFT JOIN {database_name}.section AS section ON unit.section_id = section.section_id
#                     LEFT JOIN {database_name}.division AS division ON section.division_id = division.division_id
#                     LEFT JOIN {database_name}.department AS department ON division.department_id = department.department_id
#                     WHERE  section.section_id = %i
#                    """ % int(sectionId))
#     return jsonify(data)


@data_bp.route('/section-units/<sectionId>', methods=['GET'])
def get_section_units(sectionId):
    data = fetch_data(SECTION_UNITS % int(sectionId))
    return jsonify(data)


@data_bp.route('/unit-scores/<unitId>', methods=['GET'])
def get_unit_scores(unitId):
    data = fetch_data(UNIT_SCORES % int(unitId))
    return jsonify(data)