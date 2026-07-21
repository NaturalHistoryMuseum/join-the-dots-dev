from server.config import Config

database_name = Config.MYSQL_DB

LTC_EXPORT = f"""
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
    					),
    					IF (item_count IS NOT NULL AND item_count IS NOT NULL,
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
    									),
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
            )
    	)
    )
AS ltc_export;
"""
