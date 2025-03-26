LTC_EXPORT = """
                        WITH item_count_data AS (
	SELECT cu.collection_unit_id as collection_unit_id, (
			SELECT cum.metric_value FROM jtd_live.collection_unit_metric cum WHERE ((cum.collection_unit_id = cu.collection_unit_id) 
				and (cum.current = 'yes')
				and (cum.collection_unit_metric_definition_id = 1))
		) AS item_count, (
			SELECT cum.confidence_level FROM jtd_live.collection_unit_metric cum WHERE ((cum.collection_unit_id = cu.collection_unit_id) 
				and (cum.current = 'yes')
				and (cum.collection_unit_metric_definition_id = 1))
		) AS item_count_confidence_level
	FROM jtd_live.collection_unit cu
),
unit_count_data AS (
	SELECT cu.collection_unit_id as collection_unit_id, (
			SELECT cum.metric_value FROM jtd_live.collection_unit_metric cum WHERE ((cum.collection_unit_id = cu.collection_unit_id) 
				and (cum.current = 'yes')
				and (cum.collection_unit_metric_definition_id = 2))
		) AS curatorial_unit_count, (
			SELECT cum.confidence_level FROM jtd_live.collection_unit_metric cum WHERE ((cum.collection_unit_id = cu.collection_unit_id) 
				and (cum.current = 'yes')
				and (cum.collection_unit_metric_definition_id = 2))
		) AS curatorial_unit_count_confidence_level
	FROM jtd_live.collection_unit cu
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
	--     									METHOD FOR FINDING WEIGHTED AVERAGE - IS SLOW!
	--     									IF(
	--     										(SELECT 
	-- 												MAX(vwar.weighted_average) 
	-- 												FROM jtd_live.vw_weighted_average_review vwar 
	-- 												WHERE vwar.collection_unit_id = cu.collection_unit_id AND vwar.criterion_code = "C1"
	-- 											) IS NOT NULL,
	-- 											JSON_OBJECT(
	-- 	    										'ltc:measurementDerivation', '',
	-- 	    										'dwc:measurementMethod', 'Curator assessment',
	-- 	    										'dwc:measurementType', 'C1: Physical accessibility',
	-- 	    										'dwc:measurementValue', 
	-- 	    											(SELECT 
	-- 	    												MAX(vwar.weighted_average) 
	-- 	    												FROM jtd_live.vw_weighted_average_review vwar 
	-- 	    												WHERE vwar.collection_unit_id = cu.collection_unit_id AND vwar.criterion_code = "C1"
	-- 	    											)
	-- 	    									)
	-- 	    								, JSON_OBJECT())
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
				                                FROM jtd_live.unit_assessment_criterion uac
				                                JOIN jtd_live.unit_assessment_rank uar ON uac.unit_assessment_criterion_id = uar.unit_assessment_criterion_id
				                                JOIN jtd_live.rank r ON r.rank_id = uar.rank_id
				                                RIGHT JOIN jtd_live.criterion c ON r.criterion_id = c.criterion_id
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
				                                ORDER BY r.rank_id
				                            )
    									, JSON_ARRAY())
    								)
    							)
    					, JSON_OBJECT())
	    			) 
	    		) 
	    		FROM jtd_live.collection_unit cu
	    		LEFT JOIN jtd_live.section s ON s.section_id = cu.section_id 
                LEFT JOIN jtd_live.division d ON d.division_id = s.division_id 
                LEFT JOIN jtd_live.department d2 ON d2.department_id = d.department_id 
	    		LEFT JOIN jtd_live.curatorial_unit_definition cud ON cud.curatorial_unit_definition_id = cu.curatorial_unit_definition_id 
                LEFT JOIN jtd_live.item_type it ON it.item_type_id = cud.item_type_id
                LEFT JOIN jtd_live.preservation_method pm ON pm.preservation_method_id = cud.preservation_method_id 
                LEFT JOIN jtd_live.geographic_origin go2 ON go2.geographic_origin_id = cu.geographic_origin_id
                LEFT JOIN jtd_live.taxon_palaeontology tp ON tp.taxon_palaeontology_id = cu.taxon_palaeontology_id 
               	LEFT JOIN jtd_live.taxon_life_science tls ON tls.taxon_life_science_id = cu.taxon_life_science_id 
               	JOIN item_count_data on item_count_data.collection_unit_id = cu.collection_unit_id
               	JOIN unit_count_data on unit_count_data.collection_unit_id = cu.collection_unit_id
                --	WHERE cu.collection_unit_id = 1
            )
    	)
    )
AS ltc_export;

                        """


SECTION_UNITS = """
					SELECT
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
                   """