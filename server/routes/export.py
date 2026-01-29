import csv
import io
import json

from flask import Blueprint, Response, jsonify, request, stream_with_context
from flask_jwt_extended import (
    jwt_required,
)

from server.database import get_db_connection
from server.routes.queries.data_queries import *
from server.utils import (
    database_name,
    fetch_data,
    refreshJWTToken,
)

export_bp = Blueprint('export', __name__)


# After a request, refresh the JWT token if it is about to expire
@export_bp.after_request
def refresh_expiring_jwts(response):
    return refreshJWTToken(response)


@export_bp.route('/data-export', methods=['POST'])
@jwt_required()
def make_export():
    export_config = request.get_json()
    try:
        if export_config.get('selected_data_type') == 'ltc':
            return Response(
                stream_with_context(generate_ltc_json(export_config)),
                content_type='application/json',
                headers={'Content-Disposition': 'attachment; filename=data.json'},
            )
        else:
            # Connect to db
            connection = get_db_connection()
            cursor = connection.cursor(dictionary=True)
            # Initilise query parts
            selects_query = """
                    SELECT  cu.collection_unit_id,	cu.unit_name,	cu.public_unit_name,	cu.section_id,	cu.type_collection_flag,	cu.publish_flag,	cu.informal_taxon,	cu.named_collection,	cu.es_recent_specimen_flag,	cu.archives_fond_ref,
                    cu.count_curatorial_units_flag,	cu.sort_order,	cud.curatorial_unit_definition_id,	cud.description,	bl.bibliographic_level,	it.item_type,	pm.preservation_method,	sr.storage_room_id,	sr.room_code,	sr.room_name,	f.floor_name,
                    b.building_name,	st.site_name,	sc.storage_container_id,	sc.container_name,	sc.temperature,	sc.relative_humidity,	go.geographic_origin_id,	go.geographic_origin_name,	go.region_type,	laaf.library_and_archives_function_id,	laaf.function_name,
                    gtpf.geological_time_period_id as geological_time_period_from_id,	gtpf.period_name as period_name_from,	gtpf.rank as rank_from,	gtpt.geological_time_period_id as geological_time_period_to_id,	gtpt.period_name as period_name_to,	gtpt.rank as rank_to,	t.taxon_id,	t.taxon_name,	t.taxon_rank,	t.external_ref_name,	t.external_ref_id,
                    COALESCE(CONCAT(p.first_name, ' ', p.last_name), u.display_name) AS responsible_curator,
                    uc.unit_comment, DATE(uc.date_added) AS date_comment_added
                    """
            metrics_selects_query = """
                    , (
                        SELECT JSON_ARRAYAGG(
                            JSON_OBJECT(
                                'collection_unit_metric_id', cum.collection_unit_metric_id,
                                'metric_value', cum.metric_value,
                                'confidence_level', cum.confidence_level,
                                'metric_name', cumd.metric_name
                            )
                        ) AS metric_json
                        FROM {database_name}.collection_unit_metric_definition cumd
                        LEFT JOIN {database_name}.collection_unit_metric cum
                            ON cum.collection_unit_metric_definition_id = cumd.collection_unit_metric_definition_id
                        AND cum.collection_unit_id = cu.collection_unit_id
                        AND cum.current = 'yes'
                    ) AS metric_json
                    """
            score_selects_query = """
                    ,
                    (
                        SELECT JSON_ARRAYAGG(
                            JSON_OBJECT(
                                'percentage', IF(uar.percentage = 0, NULL, uar.percentage),
                                'rank_id', uar.rank_id, 'rank_value', r.rank_value,
                                'comment', uar.comment,
                                'criterion_id', r.criterion_id,
                                'criterion_code', c.criterion_code
                            )
                        ) AS percentages_json
                        FROM {database_name}.unit_assessment_criterion uac
                        JOIN {database_name}.unit_assessment_rank uar ON uac.unit_assessment_criterion_id = uar.unit_assessment_criterion_id
                        JOIN {database_name}.rank r ON r.rank_id = uar.rank_id JOIN {database_name}.criterion c ON c.criterion_id = r.criterion_id
                        WHERE
                            uac.collection_unit_id = cu.collection_unit_id
                            AND uar.unit_assessment_criterion_id IN (
                                SELECT uac.unit_assessment_criterion_id
                                FROM {database_name}.unit_assessment_criterion uac
                                JOIN {database_name}.collection_unit cu ON cu.collection_unit_id = uac.collection_unit_id
                                WHERE uac.current = 'yes'
                            )
                            AND uar.rank_id IN (
                                SELECT r.rank_id
                                FROM {database_name}.rank r
                            )
                            AND c.criterion_id <> 3
                        ORDER BY r.rank_id
                    ) AS ranks_json"""
            average_score_query = """
                    , (
                        SELECT JSON_ARRAYAGG(
                            JSON_OBJECT(
                                'criterion_id', criterion_id,
                                'criterion_code', criterion_code,
                                'average_rank_value', avg_rank_value
                            )
                        )
                        FROM (
                            SELECT r.criterion_id, c.criterion_code, SUM(r.rank_value * uar.percentage) / NULLIF(SUM(uar.percentage), 0) AS avg_rank_value
                            FROM {database_name}.unit_assessment_rank uar
                            JOIN {database_name}.unit_assessment_criterion uac ON uac.unit_assessment_criterion_id = uar.unit_assessment_criterion_id
                            JOIN {database_name}.rank r ON r.rank_id = uar.rank_id
                            JOIN {database_name}.criterion c  ON c.criterion_id = r.criterion_id
                            WHERE uac.collection_unit_id = cu.collection_unit_id
                                AND uac.current = 'yes'
                                AND uar.percentage IS NOT NULL
                                AND uar.percentage > 0
                                AND c.criterion_id <> 3
                            GROUP BY r.criterion_id, c.criterion_code
                            ORDER BY r.criterion_id
                        ) t
                    ) AS ranks_averages_json"""
            origins_query = """
                    FROM {database_name}.collection_unit cu
                    LEFT JOIN {database_name}.users u ON u.user_id = cu.responsible_curator_id
                    LEFT JOIN {database_name}.person p ON p.person_id = u.person_id
                    LEFT JOIN {database_name}.unit_comment uc ON uc.unit_comment_id = (
				        SELECT MAX(uc2.unit_comment_id)
				        FROM {database_name}.unit_comment uc2
				        WHERE uc2.collection_unit_id = cu.collection_unit_id
				    )
                    LEFT JOIN {database_name}.geological_time_period gtpf ON gtpf.geological_time_period_id = cu.geological_time_period_from_id
                    LEFT JOIN {database_name}.geological_time_period gtpt ON gtpt.geological_time_period_id = cu.geological_time_period_to_id
                    LEFT JOIN {database_name}.geographic_origin go ON go.geographic_origin_id = cu.geographic_origin_id
                    LEFT JOIN {database_name}.library_and_archives_function laaf ON laaf.library_and_archives_function_id = cu.library_and_archives_function_id
                    LEFT JOIN {database_name}.storage_container sc ON sc.storage_container_id = cu.storage_container_id
                    LEFT JOIN {database_name}.curatorial_unit_definition cud ON cud.curatorial_unit_definition_id = cu.curatorial_unit_definition_id
                    LEFT JOIN {database_name}.bibliographic_level bl ON bl.bibliographic_level_id = cud.bibliographic_level_id
                    LEFT JOIN {database_name}.item_type it ON it.item_type_id = cud.item_type_id
                    LEFT JOIN {database_name}.preservation_method pm ON pm.preservation_method_id = cud.preservation_method_id
                    LEFT JOIN {database_name}.taxon t ON t.taxon_id = cu.taxon_id
                    LEFT JOIN {database_name}.storage_room sr ON sr.storage_room_id = cu.storage_room_id
                    LEFT JOIN {database_name}.floor f ON f.floor_id = sr.floor_id
                    LEFT JOIN {database_name}.building b ON b.building_id = f.building_id
                    LEFT JOIN {database_name}.site st ON st.site_id = b.site_id
                    LEFT JOIN {database_name}.`section` s ON s.section_id = cu.section_id
                    LEFT JOIN {database_name}.division d ON d.division_id = s.division_id
                    LEFT JOIN {database_name}.department d2 ON d2.department_id = d.department_id
                    WHERE cu.unit_active = 'yes' AND cu.draft_unit = 0
                            """

            # Build full query
            query = selects_query
            # Add metrics if requested
            if export_config.get('include_metrics'):
                query += metrics_selects_query
            # Add score if requested
            if export_config.get('include_scores'):
                query += score_selects_query
            # Add average scores if requested
            if export_config.get('include_score_averages'):
                query += average_score_query
            # Add origins and joins
            query += origins_query
            # Add to where clause to query if there are filters
            if where_claused(export_config):
                query += ' AND ' + ' AND '.join(where_claused(export_config))
            # End query
            query += ' ;'
            # Format the query with the database name
            formatted_query = query.format(database_name=database_name)
            # Execute query
            cursor.execute(formatted_query)
            # Fetch rows
            data = cursor.fetchall()
            col_names = [desc[0] for desc in cursor.description]

            if export_config.get('include_metrics'):
                if export_config.get('selected_data_type') == 'json':
                    # Parse the JSON fields for scores and ranks
                    for row in data:
                        row['metric_json'] = (
                            json.loads(row['metric_json']) if row['metric_json'] else []
                        )
                elif export_config.get('selected_data_type') == 'csv':
                    # Flatten the JSON fields for CSV export
                    for row in data:
                        # Handle metric_json
                        metrics = (
                            json.loads(row['metric_json']) if row['metric_json'] else []
                        )
                        for i, metric in enumerate(metrics):
                            # Set the new column name
                            new_col_name = f'{metric["metric_name"]}_value'
                            # Add new column to row
                            row[new_col_name] = metric['metric_value'] or ''
                            # Add to list of columns
                            if new_col_name not in col_names:
                                col_names.append(new_col_name)
                            # Set the new column name
                            new_col_name_conf = (
                                f'{metric["metric_name"]}_confidence_level'
                            )
                            # Add new column to row
                            row[new_col_name_conf] = metric['confidence_level'] or ''
                            # Add to list of columns
                            if new_col_name_conf not in col_names:
                                col_names.append(new_col_name_conf)
                        # Remove original metric_json field
                        del row['metric_json']
                    # Finally, remove the original JSON columns from col_names
                    col_names.remove('metric_json')

            if export_config.get('include_scores'):
                if export_config.get('selected_data_type') == 'json':
                    # Parse the JSON fields for scores and ranks
                    for row in data:
                        row['ranks_json'] = (
                            json.loads(row['ranks_json']) if row['ranks_json'] else []
                        )
                elif export_config.get('selected_data_type') == 'csv':
                    # Flatten the JSON fields for CSV export
                    for row in data:
                        # Handle ranks_json
                        ranks = (
                            json.loads(row['ranks_json']) if row['ranks_json'] else []
                        )
                        # Iterate over all fields in ranks
                        for rank in ranks:
                            # Set the new percentage column name
                            new_col_name = (
                                f'{rank["criterion_code"]}_rank_{rank["rank_value"]}'
                            )
                            # Add new column to row
                            row[new_col_name] = rank['percentage']
                            # Add to list of columns
                            if new_col_name not in col_names:
                                col_names.append(new_col_name)
                            # Set the new comment column name
                            comment_col_name = f'{rank["criterion_code"]}_rank_{rank["rank_value"]}_comment'
                            # Add new column to row
                            row[comment_col_name] = rank['comment']
                            # Add to list of columns
                            if comment_col_name not in col_names:
                                col_names.append(comment_col_name)
                        # Remove original ranks_json field
                        del row['ranks_json']

                    # Finally, remove the original JSON columns from
                    col_names.remove('ranks_json')

            if export_config.get('include_score_averages'):
                if export_config.get('selected_data_type') == 'json':
                    # Parse the JSON fields for scores and ranks
                    for row in data:
                        row['ranks_averages_json'] = (
                            json.loads(row['ranks_averages_json'])
                            if row['ranks_averages_json']
                            else []
                        )
                elif export_config.get('selected_data_type') == 'csv':
                    # Flatten the JSON fields for CSV export
                    for row in data:
                        # Handle ranks_averages_json
                        average_criterions = (
                            json.loads(row['ranks_averages_json'])
                            if row['ranks_averages_json']
                            else []
                        )
                        # Iterate over all fields in ranks
                        for average_criterion in average_criterions:
                            # Set the new column name
                            new_col_name = (
                                f'{average_criterion["criterion_code"]}_average_score'
                            )
                            # Add new column to row
                            row[new_col_name] = average_criterion['average_rank_value']
                            # Add to list of columns
                            if new_col_name not in col_names:
                                col_names.append(new_col_name)
                        # Remove original ranks_averages_json field
                        del row['ranks_averages_json']

                    # Finally, remove the original JSON columns from
                    col_names.remove('ranks_averages_json')

            # Return response based on selected data type
            if export_config.get('selected_data_type') == 'json':
                response = jsonify(data)
            elif export_config.get('selected_data_type') == 'csv':
                # Create Response with CSV MIME type
                response = Response(generate_csv(col_names, data), mimetype='text/csv')
                response.headers['Content-Disposition'] = (
                    'attachment; filename=test-export.csv'
                )

            cursor.close()
            connection.close()
            return response
    except Exception as e:
        return str(e)


# Create CSV response
def generate_csv(col_names, data):
    # Format column names for csv
    formatted_col_names = [col_name.replace('_', ' ').title() for col_name in col_names]
    output = io.StringIO()
    writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    # Write the headers
    writer.writerow(formatted_col_names)

    # Write the rows data
    for row in data:
        writer.writerow([row[col] for col in col_names])
    return output.getvalue()


def generate_ltc_json(export_config):
    data = fetch_data(generate_ltc_query(export_config))
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


def generate_ltc_query(export_config):
    ltc_query_start = """
    WITH item_count_data AS (
        SELECT cu.collection_unit_id as collection_unit_id, (
                SELECT cum.metric_value FROM {database_name}.collection_unit_metric cum WHERE ((cum.collection_unit_id = cu.collection_unit_id)
                    and (cum.current = 'yes')
                    and (cum.collection_unit_metric_definition_id = 1))
            ) AS item_count, (
                SELECT cum.confidence_level FROM {database_name}.collection_unit_metric cum WHERE ((cum.collection_unit_id = cu.collection_unit_id)
                    and (cum.current = 'yes')
                    and (cum.collection_unit_metric_definition_id = 1))
            ) AS item_count_confidence_level
        FROM {database_name}.collection_unit cu
    ),
    unit_count_data AS (
        SELECT cu.collection_unit_id as collection_unit_id, (
                SELECT cum.metric_value FROM {database_name}.collection_unit_metric cum WHERE ((cum.collection_unit_id = cu.collection_unit_id)
                    and (cum.current = 'yes')
                    and (cum.collection_unit_metric_definition_id = 2))
            ) AS curatorial_unit_count, (
                SELECT cum.confidence_level FROM {database_name}.collection_unit_metric cum WHERE ((cum.collection_unit_id = cu.collection_unit_id)
                    and (cum.current = 'yes')
                    and (cum.collection_unit_metric_definition_id = 2))
            ) AS curatorial_unit_count_confidence_level
        FROM {database_name}.collection_unit cu
    )
    SELECT
        JSON_ARRAY(
    -- 		LatimerScoreScheme
            JSON_OBJECT(
                'ltc:basisOfScheme', "Collections assessment",
                "ltc:isDistinctObjects", true,
                "ltc:schemeName", "Join the Dots",
                "ltc:hasObjectGroup",
                (
    --     			ObjectGroup
                    SELECT JSON_ARRAYAGG(
                        JSON_MERGE_PRESERVE(
                            JSON_OBJECT('ltc:baseTypeOfObjectGroup', JSON_ARRAY('MaterialEntity')),
    -- 	    					Collection Name
                            JSON_OBJECT('ltc:collectionName', cu.unit_name),
    --     						Scheme Name
                            JSON_OBJECT('ltc:schemeName', 'Join the Dots'),
                            IF(it.item_type IS NOT NULL,
                                JSON_OBJECT('ltc:objectType', JSON_ARRAY(it.item_type))
                            , JSON_OBJECT()),
                            IF(cud.description IS NOT NULL,
                                JSON_OBJECT('ltc:preparationType', JSON_ARRAY(cud.description))
                            , JSON_OBJECT()),
                            IF(pm.preservation_method IS NOT NULL,
                                JSON_OBJECT('ltc:preservationMethod', JSON_ARRAY(pm.preservation_method))
                            , JSON_OBJECT()),
    -- 	    					EcologicalContext
                            IF(go2.region_type IS NOT NULL,
                                JSON_OBJECT('ltc:hasEcologicalContext',
                                    JSON_ARRAY(
                                        JSON_OBJECT(
                                            'ltc:biomeType', go2.region_type
                                        )
                                    )
                                )
                            , JSON_OBJECT()),
    -- 	    					GeographicContext
                            IF(go2.geographic_origin_name IS NOT NULL,
                                JSON_OBJECT('ltc:hasGeographicContext',
                                    JSON_ARRAY(
                                        JSON_OBJECT(
                                            'ltc:region', go2.geographic_origin_name
                                        )
                                    )
                                )
                            , JSON_OBJECT()),
    -- 	    					OrganisationalUnit
                            IF(cu.section_id IS NOT NULL,
                                JSON_OBJECT('ltc:hasOrganisationalUnit',
                                    JSON_ARRAY(
                                        JSON_OBJECT(
                                            'ltc:organisationalUnitName', s.section_name,
                                            'ltc:organisationalUnitType', 'Section',
                                            'ltc:hasParentOrganisationalUnit',
                                                JSON_ARRAY(
                                                    JSON_OBJECT(
                                                        'ltc:organisationalUnitName', d.division_name,
                                                        'ltc:organisationalUnitType', 'Division',
                                                        'ltc:hasParentOrganisationalUnit',
                                                            JSON_ARRAY(
                                                                JSON_OBJECT(
                                                                    'ltc:organisationalUnitName', d2.department_name,
                                                                    'ltc:organisationalUnitType', 'Department',
                                                                    'ltc:hasParentOrganisationalUnit',
                                                                        JSON_ARRAY(
                                                                            JSON_OBJECT(
                                                                                'ltc:organisationalUnitName', 'Natural History Museum, London',
                                                                                'ltc:organisationalUnitType', 'Institution'
                                                                            )
                                                                        )
                                                                )
                                                            )
                                                    )
                                                )
                                        )
                                    )
                                )
                            , JSON_OBJECT()),
                            IF(cu.taxon_life_science_id IS NOT NULL OR cu.taxon_palaeontology_id IS NOT NULL,
                                JSON_OBJECT(
                                    'ltc:hasTaxon',
                                        JSON_ARRAY(
                                            IF(cu.taxon_life_science_id IS NOT NULL,
                                                JSON_OBJECT(
                                                    'dwc:scientificName', tls.taxon_name,
                                                    'dwc:taxonRank', tls.taxon_rank,
                                                    'ltc:hasIdentifier',
                                                        JSON_ARRAY(
                                                            JSON_OBJECT(
                                                                'ltc:identifierSource', tls.external_ref_name,
                                                                'ltc:identifierType', 'Taxon ID',
                                                                'ltc:identifierValue', tls.external_ref_id
                                                            )
                                                        )
                                                )
                                                , JSON_OBJECT(
                                                    'dwc:scientificName', tp.taxon_name,
                                                    'dwc:taxonRank', tp.taxon_rank,
                                                    'ltc:hasIdentifier',
                                                        JSON_ARRAY(
                                                            JSON_OBJECT(
                                                                'ltc:identifierSource', tp.external_ref_name,
                                                                'ltc:identifierType', 'Taxon ID',
                                                                'ltc:identifierValue', tp.external_ref_id
                                                            )
                                                        )
                                                )
                                            )
                                        )
                                )
                            , JSON_OBJECT()),
    -- 	    					Collection unit id
                            JSON_OBJECT(
                                'ltc:hasIdentifier',
                                    JSON_ARRAY(
                                        JSON_OBJECT(
                                            'ltc:identifierSource', 'Join the Dots',
                                            'ltc:identifierType', 'Collection unit ID',
                                            'ltc:identifierValue', cu.collection_unit_id
                                        )
                                    )
                            )
    """
    ltc_measures_query = """,
                            IF (item_count IS NOT NULL AND curatorial_unit_count IS NOT NULL,
                                JSON_OBJECT(
                                    'ltc:hasMeasurementOrFact',
                                        JSON_MERGE_PRESERVE(
                                            JSON_ARRAY(
        --     										Item count
                                                IF(item_count IS NOT NULL ,
                                                    JSON_OBJECT(
                                                        'ltc:measurementDerivation', 'Reported',
                                                        'dwc:measurementType', 'Reporting count',
                                                        'dwc:measurementUnit', 'Count',
                                                        'dwc:measurementAccuracy', item_count_confidence_level,
                                                        'dwc:measurementValue', item_count
                                                    )
                                                , JSON_OBJECT()),
                                                IF(curatorial_unit_count IS NOT NULL ,
                                                    JSON_OBJECT(
                                                        'ltc:measurementDerivation', 'Reported',
                                                        'dwc:measurementType', 'Curatorial unit count',
                                                        'dwc:measurementUnit', 'Count',
                                                        'dwc:measurementAccuracy', curatorial_unit_count_confidence_level,
                                                        'dwc:measurementValue', curatorial_unit_count
                                                    )
                                                , JSON_OBJECT())
                                            )
                                            ,
        --     									METHOD FOR DOING EACH RANK INDIVIDUALLY
                                            COALESCE (
                                                (
                                                    SELECT JSON_ARRAYAGG(
                                                        JSON_OBJECT(
                                                            'ltc:measurementDerivation', 'Reported',
                                                            'dwc:measurementType', CONCAT(c.criterion_code, ': ', c.criterion_name, ' - (Rank ', r.rank_value, ')'),
                                                            'dwc:measurementUnit', 'Percentage',
                                                            'dwc:measurementValue', uar.percentage
                                                        )
                                                    ) AS percentages_json
                                                    FROM {database_name}.unit_assessment_criterion uac
                                                    JOIN {database_name}.unit_assessment_rank uar ON uac.unit_assessment_criterion_id = uar.unit_assessment_criterion_id
                                                    JOIN {database_name}.rank r ON r.rank_id = uar.rank_id
                                                    RIGHT JOIN {database_name}.criterion c ON r.criterion_id = c.criterion_id
                                                    WHERE ((uac.collection_unit_id = cu.collection_unit_id)
                                                    AND uar.unit_assessment_criterion_id IN (
                                                        SELECT uac.unit_assessment_criterion_id
                                                        FROM {database_name}.unit_assessment_criterion uac
                                                        JOIN {database_name}.collection_unit cu ON cu.collection_unit_id = uac.collection_unit_id
                                                        WHERE uac.current = 'yes'
                                                    )
                                                    AND uar.rank_id IN (
                                                        SELECT r.rank_id FROM {database_name}.rank r
                                                    ))
                                                    ORDER BY r.rank_id
                                                )
                                            , JSON_ARRAY())
                                        )
                                    )
                            , JSON_OBJECT())
    """
    ltc_query_origin = """
                        )
                    )
                    FROM {database_name}.collection_unit cu
                    LEFT JOIN {database_name}.section s ON s.section_id = cu.section_id
                    LEFT JOIN {database_name}.division d ON d.division_id = s.division_id
                    LEFT JOIN {database_name}.department d2 ON d2.department_id = d.department_id
                    LEFT JOIN {database_name}.curatorial_unit_definition cud ON cud.curatorial_unit_definition_id = cu.curatorial_unit_definition_id
                    LEFT JOIN {database_name}.item_type it ON it.item_type_id = cud.item_type_id
                    LEFT JOIN {database_name}.preservation_method pm ON pm.preservation_method_id = cud.preservation_method_id
                    LEFT JOIN {database_name}.geographic_origin go2 ON go2.geographic_origin_id = cu.geographic_origin_id
                    LEFT JOIN {database_name}.taxon_palaeontology tp ON tp.taxon_palaeontology_id = cu.taxon_palaeontology_id
                    LEFT JOIN {database_name}.taxon_life_science tls ON tls.taxon_life_science_id = cu.taxon_life_science_id
                    JOIN item_count_data on item_count_data.collection_unit_id = cu.collection_unit_id
                    JOIN unit_count_data on unit_count_data.collection_unit_id = cu.collection_unit_id
    """
    ltc_query_end = """
                )
            )
        )
    AS ltc_export;
    """
    ltc_query = ltc_query_start
    # Add LtC measures if requested
    if export_config.get('include_ltc_measures'):
        ltc_query += ltc_measures_query
    # Add origins and joins
    ltc_query += ltc_query_origin
    # Add to where clause to query if there are filters
    if where_claused(export_config):
        ltc_query += ' WHERE ' + ' AND '.join(where_claused(export_config))
    ltc_query += ltc_query_end

    return ltc_query


def where_claused(export_config):
    # Init array
    where_clauses = []
    # Check filters and add if present
    if export_config.get('selected_sections'):
        where_clauses.append(
            f' cu.section_id IN ({", ".join(map(str, export_config.get("selected_sections")))})'
        )
    if export_config.get('selected_divisions'):
        where_clauses.append(
            f' d.division_id IN ({", ".join(map(str, export_config.get("selected_divisions")))})'
        )
    if export_config.get('selected_curators'):
        where_clauses.append(
            f' u.user_id IN ({", ".join(map(str, export_config.get("selected_curators")))})'
        )
    if export_config.get('selected_rooms'):
        where_clauses.append(
            f' sr.storage_room_id IN ({", ".join(map(str, export_config.get("selected_rooms")))})'
        )
    if export_config.get('selected_curatorial_definitions'):
        where_clauses.append(
            f' cud.curatorial_unit_definition_id IN ({", ".join(map(str, export_config.get("selected_curatorial_definitions")))})'
        )
    if export_config.get('selected_taxons'):
        where_clauses.append(
            f' t.taxon_id IN ({", ".join(map(str, export_config.get("selected_taxons")))})'
        )
    # Return filter query
    return where_clauses
