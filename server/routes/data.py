from flask import Blueprint, jsonify
from server.database import get_db_connection

data_bp = Blueprint('data', __name__)

def fetch_data(query, params=None):
    """Helper function to execute a database query."""
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result

@data_bp.route('/unit-department', methods=['GET'])
def get_units_and_departments():
    print("get_units_and_departments")
    data = fetch_data("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, department.department_name
                   FROM jtd_live.collection_unit AS unit 
                    LEFT JOIN jtd_live.section AS section ON unit.section_id = section.section_id
                    LEFT JOIN jtd_live.division AS division ON section.division_id = division.division_id
                    LEFT JOIN jtd_live.department AS department ON division.department_id = department.department_id
                   """)
    return jsonify(data)

@data_bp.route('/unit/<unit_id>', methods=['GET'])
def get_unit(unit_id):
    data = fetch_data("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, department.department_name, unit.*
                   FROM jtd_live.collection_unit AS unit 
                    LEFT JOIN jtd_live.section AS section ON unit.section_id = section.section_id
                    LEFT JOIN jtd_live.division AS division ON section.division_id = division.division_id
                    LEFT JOIN jtd_live.department AS department ON division.department_id = department.department_id
                    WHERE  unit.collection_unit_id = %u
                   """ % int(unit_id))
    return jsonify(data)

@data_bp.route('/criterion', methods=['GET'])
def get_criterion():
    data = fetch_data("""SELECT cat.*, crit.criterion_id, crit.criterion_name, crit.criterion_code, crit.definition
                   FROM jtd_live.criterion crit
                    LEFT JOIN jtd_live.category cat ON crit.category_id = cat.category_id
                   """)
    return jsonify(data)

@data_bp.route('/category', methods=['GET'])
def get_category():
    data = fetch_data("""SELECT cat.*
                   FROM jtd_live.category cat
                   """)
    return jsonify(data)


# Old section get with no ranking data
# @data_bp.route('/section-units/<sectionId>', methods=['GET'])
# def get_section_units(sectionId):
#     data = fetch_data("""SELECT unit.collection_unit_id, unit.unit_name, unit.named_collection, section.section_name, division.division_name, section.section_name, unit.*
#                    FROM jtd_live.collection_unit AS unit 
#                     LEFT JOIN jtd_live.section AS section ON unit.section_id = section.section_id
#                     LEFT JOIN jtd_live.division AS division ON section.division_id = division.division_id
#                     LEFT JOIN jtd_live.department AS department ON division.department_id = department.department_id
#                     WHERE  section.section_id = %i
#                    """ % int(sectionId))
#     return jsonify(data)


@data_bp.route('/section-units/<sectionId>', methods=['GET'])
def get_section_units(sectionId):
    data = fetch_data("""select
                            `cu`.`collection_unit_id` AS `collection_unit_id`,
                            `di`.`division_name` AS `division_name`,
                            `se`.`section_name` AS `section_name`,
                            concat(`pe`.`first_name`, ' ', `pe`.`last_name`) AS `responsible_curator`,
                            `cud`.`description` AS `curatorial_unit_type`,
                            `cu`.`unit_name` AS `unit_name`,
                            `cu`.`sort_order` AS `sort_order`,
                            (
                            select
                                concat(`jtd_live`.`person`.`first_name`, ' ', `jtd_live`.`person`.`last_name`)
                            from
                                `jtd_live`.`person`
                            where
                                (`jtd_live`.`person`.`person_id` in (
                                select
                                    distinct `jtd_live`.`unit_assessment_criterion`.`assessor_id`
                                from
                                    `jtd_live`.`unit_assessment_criterion`
                                where
                                    ((`jtd_live`.`unit_assessment_criterion`.`collection_unit_id` = `cu`.`collection_unit_id`)
                                        and (`jtd_live`.`unit_assessment_criterion`.`current` = 'yes')))
                                    and (`jtd_live`.`person`.`person_id` <> 113))
                            limit 1) AS `assessor`,
                            `jtd_live`.`vmc`.`curatorial_unit_count` AS `curatorial_unit_count`,
                            `jtd_live`.`vmc`.`curatorial_unit_count_confidence` AS `curatorial_unit_count_confidence`,
                            `jtd_live`.`vmc`.`item_count` AS `item_count`,
                            `jtd_live`.`vmc`.`item_count_confidence` AS `item_count_confidence`,
                            `jtd_live`.`vmc`.`barcoded_percentage` AS `barcoded_percentage`,
                            `jtd_live`.`vmc`.`barcoded_percentage_confidence` AS `barcoded_percentage_confidence`,
                            (
                            select
                                `uc`.`unit_comment`
                            from
                                `jtd_live`.`unit_comment` `uc`
                            where
                                (`uc`.`collection_unit_id` = `cu`.`collection_unit_id`)
                            order by
                                `uc`.`date_added` desc
                            limit 1) AS `unit_comment`,
                            (
                                SELECT JSON_ARRAYAGG(
                                    JSON_OBJECT(
                                        'percentage', IF(uar.percentage = 0, NULL, uar.percentage),
                                        'rank_id', uar.rank_id,
                                        'rank_value', r.rank_value,
                                        'definition', r.definition,
                                        'criterion_id', r.criterion_id
                                    )
                                ) AS percentages_json
                                FROM jtd_live.unit_assessment_criterion uac
                                JOIN jtd_live.unit_assessment_rank uar ON uac.unit_assessment_criterion_id = uar.unit_assessment_criterion_id
                                JOIN jtd_live.rank r ON r.rank_id = uar.rank_id
                                WHERE ((uac.collection_unit_id = cu.collection_unit_id) 
                                AND uar.unit_assessment_criterion_id IN (
                                    SELECT uac.unit_assessment_criterion_id
                                    FROM jtd_live.unit_assessment_criterion uac
                                    JOIN jtd_live.collection_unit cu ON cu.collection_unit_id = uac.collection_unit_id
                                    WHERE uac.current = 'yes'
                                )
                                AND uar.rank_id IN (
                                    SELECT r.rank_id FROM jtd_live.rank r
                                ))
                            ) AS ranks_json
                        from
                            (((((`jtd_live`.`collection_unit` `cu`
                        left join `jtd_live`.`section` `se` on
                            ((`se`.`section_id` = `cu`.`section_id`)))
                        left join `jtd_live`.`division` `di` on
                            ((`di`.`division_id` = `se`.`division_id`)))
                        left join `jtd_live`.`person` `pe` on
                            ((`pe`.`person_id` = `cu`.`responsible_curator_id`)))
                        left join `jtd_live`.`curatorial_unit_definition` `cud` on
                            ((`cud`.`curatorial_unit_definition_id` = `cu`.`curatorial_unit_definition_id`)))
                        left join `jtd_live`.`vw_metrics_current` `vmc` on
                            ((`jtd_live`.`vmc`.`collection_unit_id` = `cu`.`collection_unit_id`)))
                        where
                            (`cu`.`unit_active` = 'yes') AND se.section_id = %i
                        order by
                            `se`.`section_name`,
                            `cu`.`sort_order`,
                            `cu`.`collection_unit_id`;
                   """ % int(sectionId))
    return jsonify(data)