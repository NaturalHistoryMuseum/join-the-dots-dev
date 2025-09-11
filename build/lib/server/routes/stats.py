from flask import Blueprint, jsonify, session
from flask_jwt_extended import jwt_required

from server.routes.queries.data_queries import *
from server.utils import fetch_data, refreshJWTToken

stats_bp = Blueprint("stats", __name__)


# After a request, refresh the JWT token if it is about to expire
@stats_bp.after_request
def refresh_expiring_jwts(response):
    return refreshJWTToken(response)


@stats_bp.route("/home-stats", methods=["GET"])
@jwt_required()
def get_home_stats():
    user = session.get("user")
    if not user:
        return jsonify({"error": "Unauthorized"}), 401
    user_level = user["level"]
    match user_level:
        case 1:
            category_percent_query = """

WITH ranked_data AS (
    SELECT
        cat.description,
        crit.criterion_name,
        rnk.rank_value,
        (uar.percentage * cum.metric_value) AS rank_curatorial_units
    FROM {database_name}.unit_assessment_rank uar
    JOIN {database_name}.unit_assessment_criterion uac
        ON uar.unit_assessment_criterion_id = uac.unit_assessment_criterion_id
    JOIN {database_name}.collection_unit cu
        ON uac.collection_unit_id = cu.collection_unit_id
    JOIN {database_name}.rank rnk
        ON uar.rank_id = rnk.rank_id
    JOIN {database_name}.criterion crit
        ON rnk.criterion_id = crit.criterion_id
    JOIN {database_name}.category cat
        ON crit.category_id = cat.category_id
    JOIN {database_name}.collection_unit_metric cum
        ON cu.collection_unit_id = cum.collection_unit_id
        AND cum.current = 'yes'
        AND cum.collection_unit_metric_definition_id = 2
    WHERE
        uac.current = 'yes'
        AND uac.assessor_id IS NOT NULL
        AND uac.assessor_id <> ''
        AND cu.unit_active = 'yes'
        and crit.criterion_id <> 3
),
aggregated_raw AS (
    SELECT
        description,
        criterion_name,
        rank_value,
        SUM(rank_curatorial_units) AS rank_total
    FROM ranked_data
    GROUP BY description, criterion_name, rank_value
),
category_totals AS (
    SELECT
        description,
        criterion_name,
        SUM(rank_total) AS criterion_total
    FROM aggregated_raw
    GROUP BY description, criterion_name
)
SELECT
    a.description AS Category,
    a.criterion_name AS Criterion,
    ROUND(SUM(CASE WHEN a.rank_value = 1 THEN a.rank_total ELSE 0 END) / ct.criterion_total * 100, 1) AS rank_1,
    ROUND(SUM(CASE WHEN a.rank_value = 2 THEN a.rank_total ELSE 0 END) / ct.criterion_total * 100, 1) AS rank_2,
    ROUND(SUM(CASE WHEN a.rank_value = 3 THEN a.rank_total ELSE 0 END) / ct.criterion_total * 100, 1) AS rank_3,
    ROUND(SUM(CASE WHEN a.rank_value = 4 THEN a.rank_total ELSE 0 END) / ct.criterion_total * 100, 1) AS rank_4,
    ROUND(SUM(CASE WHEN a.rank_value = 5 THEN a.rank_total ELSE 0 END) / ct.criterion_total * 100, 1) AS rank_5
FROM aggregated_raw a
JOIN category_totals ct
    ON a.description = ct.description AND a.criterion_name = ct.criterion_name
GROUP BY a.description, a.criterion_name, ct.criterion_total
ORDER BY a.description, a.criterion_name;

 """

            category_percent = fetch_data(category_percent_query)

            total_units_query = """SELECT COUNT(cu.collection_unit_id)
                        FROM {database_name}.collection_unit cu
                        WHERE cu.unit_active = 'yes';"""
            total_units = fetch_data(total_units_query)[0][
                "COUNT(cu.collection_unit_id)"
            ]

            data = {"category_percent": category_percent, "total_units": total_units}
        case 2:
            last_rescored_query = """SELECT  (
                            SELECT MAX(DATE(rs.completed_at))
                            FROM {database_name}.rescore_session_units rsu
                            JOIN {database_name}.rescore_session rs on rs.rescore_session_id = rsu.rescore_session_id
                            WHERE rsu.collection_unit_id = cu.collection_unit_id
                        ) AS last_rescored
                        FROM {database_name}.collection_unit cu
                        JOIN {database_name}.assigned_units au ON au.collection_unit_id = cu.collection_unit_id
                        WHERE au.user_id = %s AND cu.unit_active = 'yes';"""
            last_rescored = fetch_data(last_rescored_query, (user["user_id"],))[0][
                "last_rescored"
            ]

            unit_count_query = """SELECT COUNT(cu.collection_unit_id) as unit_count
                        FROM {database_name}.collection_unit cu
                        JOIN {database_name}.assigned_units au ON au.collection_unit_id = cu.collection_unit_id
                        WHERE au.user_id = %s AND cu.unit_active = 'yes';"""
            unit_count = fetch_data(unit_count_query, (user["user_id"],))[0][
                "unit_count"
            ]

            scored_in_last_year_query = """SELECT
  SUM(CASE
        WHEN latest_completed_at >= CURDATE() - INTERVAL 1 YEAR THEN 1
        ELSE 0
      END) AS less_than_year,
  SUM(CASE
        WHEN latest_completed_at < CURDATE() - INTERVAL 1 YEAR THEN 1
        ELSE 0
      END) AS older_than_year
FROM (
  SELECT cu.collection_unit_id, MAX(DATE(rs.completed_at)) AS latest_completed_at
  FROM {database_name}.collection_unit cu
  JOIN {database_name}.rescore_session_units rsu ON rsu.collection_unit_id = cu.collection_unit_id
  JOIN {database_name}.rescore_session rs ON rs.rescore_session_id = rsu.rescore_session_id
  JOIN {database_name}.assigned_units au ON au.collection_unit_id = cu.collection_unit_id
  WHERE au.user_id = %s AND cu.unit_active = 'yes'
  GROUP BY cu.collection_unit_id
) AS latest_per_unit;
"""
            scored_in_last_year = fetch_data(
                scored_in_last_year_query, (user["user_id"],)
            )
            data = {
                "last_rescored": last_rescored,
                "unit_count": unit_count,
                "scored_in_last_year": scored_in_last_year,
            }
        case 3:
            data = {"message": "User Level 3"}
        case 4:
            data = {"message": "User Level 4"}
        case _:
            data = {"message": "Unknown User Level"}
    return jsonify(data), 200
