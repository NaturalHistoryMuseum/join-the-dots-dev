CREATE TABLE jtd_test.rescore_session (
    rescore_session_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    status ENUM('in_progress', 'complete') DEFAULT 'in_progress',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at DATETIME null,
    CONSTRAINT `FK_users` FOREIGN KEY (user_id) REFERENCES jtd_test.users(user_id)
);
CREATE TABLE jtd_test.`rescore_session_units` (
  `rescore_session_units_id` int NOT NULL AUTO_INCREMENT,
   rescore_session_id INT not null,
   `collection_unit_id` int NOT NULL,
  PRIMARY KEY (`rescore_session_units_id`),
  FOREIGN KEY (rescore_session_id) REFERENCES jtd_test.rescore_session(rescore_session_id),
  FOREIGN KEY (collection_unit_id) REFERENCES jtd_test.collection_unit(collection_unit_id)
);
CREATE TABLE jtd_test.unit_category_draft (
    category_draft_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    rescore_session_units_id INT NOT null, 
    category_id INT NOT NULL,
    complete tinyint not null,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (rescore_session_units_id) REFERENCES jtd_test.rescore_session_units(rescore_session_units_id),
    FOREIGN KEY (category_id) REFERENCES jtd_test.category(category_id)
);
CREATE TABLE jtd_test.unit_rank_draft (
    rank_draft_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    category_draft_id INT NOT NULL,
    criterion_id INT NOT NULL,
    rank_id INT NOT NULL,
    percentage DECIMAL(8,7) not null,
    `comment` varchar(1000) DEFAULT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_draft_id) REFERENCES jtd_test.unit_category_draft(category_draft_id),
    FOREIGN KEY (criterion_id) REFERENCES jtd_test.criterion(criterion_id)
    FOREIGN KEY (rank_id) REFERENCES jtd_test.rank(rank_id)
);