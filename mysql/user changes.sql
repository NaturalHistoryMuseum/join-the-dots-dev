
CREATE TABLE `roles` (
  `role_id` int NOT NULL UNIQUE AUTO_INCREMENT,
  `role` varchar(45) NOT NULL,
  PRIMARY KEY (`role_id`)
  UNIQUE KEY `role_id_UNIQUE` (`role_id`),
) ;

INSERT INTO `roles` (`role`)
VALUES ('viewer'), ('editor'), ('manager'), ('admin');

CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(45) NOT NULL,
  `email` varchar(45) NOT NULL,
  `azure_id` varchar(45) NOT NULL,
  `role_id` int DEFAULT 1,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id_UNIQUE` (`user_id`),
  UNIQUE KEY `azure_id_UNIQUE` (`azure_id`),
  UNIQUE KEY `email_UNIQUE` (`email`),
  FOREIGN KEY (`role_id`) REFERENCES `roles`(`role_id`)
) ;

CREATE TABLE `assigned_units` (
	`assigned_unit_id` int NOT NULL AUTO_INCREMENT,
	`user_id` int NOT NULL,
	`collection_unit_id` int NOT NULL,
	PRIMARY KEY (`assigned_unit_id`),
	FOREIGN KEY (`user_id`) REFERENCES `users`(`user_id`),
	FOREIGN KEY (`collection_unit_id`) REFERENCES `collection_unit`(`collection_unit_id`)
);