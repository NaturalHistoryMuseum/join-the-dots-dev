CREATE TABLE `taxon` (
  `taxon_id` int NOT NULL AUTO_INCREMENT,
  `taxon_name` varchar(255) NOT NULL,
  `taxon_rank` varchar(255) NOT NULL,
  `external_ref_name` varchar(255) DEFAULT NULL,
  `external_ref_id` varchar(255) DEFAULT NULL,
  `department_id` int NOT NULL,
  `taxon_life_science_id` int DEFAULT NULL,
  `taxon_palaeontology_id` int DEFAULT NULL,
  PRIMARY KEY (`taxon_id`)
);

INSERT INTO jtd_live.taxon
(taxon_name, taxon_rank, external_ref_name, external_ref_id, department_id, taxon_palaeontology_id)
SELECT taxon_name, taxon_rank, external_ref_name, external_ref_id, 1, taxon_palaeontology_id
FROM jtd_live.taxon_palaeontology ;

INSERT INTO jtd_live.taxon
(taxon_name, taxon_rank, external_ref_name, external_ref_id, department_id, taxon_life_science_id)
SELECT taxon_name, taxon_rank, external_ref_name, external_ref_id, 3, taxon_life_science_id
FROM jtd_live.taxon_life_science ; 


ALTER TABLE jtd_live.collection_unit ADD COLUMN taxon_id INT ;


UPDATE jtd_live.collection_unit cu 
JOIN jtd_live.taxon t ON cu.taxon_life_science_id = t.taxon_life_science_id 
SET cu.taxon_id = t.taxon_id 
WHERE cu.taxon_life_science_id IS NOT NULL;

UPDATE jtd_live.collection_unit cu 
JOIN jtd_live.taxon t ON cu.taxon_palaeontology_id = t.taxon_palaeontology_id 
SET cu.taxon_id = t.taxon_id 
WHERE cu.taxon_palaeontology_id IS NOT NULL;