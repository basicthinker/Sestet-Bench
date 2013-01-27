
-- DROP DATABASE `sestet`;
CREATE DATABASE `sestet`;
USE `sestet`;

CREATE TABLE IF NOT EXISTS `processes` (
	`id` smallint NOT NULL auto_increment,
	`name` char(63) NOT NULL,
	`spec` char(255) NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `trials` (
	`id` smallint NOT NULL auto_increment,
	`date` datetime NOT NULL,
	`spec` text,
	PRIMARY KEY (`id`),
	UNIQUE KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `functions` (
	`id` bigint NOT NULL auto_increment,
	`name` char(63) NOT NULL,
	`parent_id` bigint NOT NULL,
	`time` double NOT NULL,
	`cpu` smallint NOT NULL,
	`proc_id` smallint NOT NULL,
	`duration` double NOT NULL,
	`trial_id` smallint NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`parent_id`) REFERENCES `functions`(`id`)
			ON DELETE CASCADE,
	FOREIGN KEY (`proc_id`) REFERENCES `processes`(`id`),
	FOREIGN KEY (`trial_id`) REFERENCES `trials`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DELIMITER //

DROP PROCEDURE IF EXISTS add_process //
CREATE PROCEDURE add_process (
	IN proc_name CHAR(63),
	IN proc_spec CHAR(255)
)
BEGIN
	REPLACE INTO `processes`(`name`, `spec`) VALUES (
		proc_name,
		proc_spec
	);
END //

DROP FUNCTION IF EXISTS add_trial //
CREATE FUNCTION add_trial (spec TEXT)
RETURNS SMALLINT
BEGIN
	INSERT INTO `trials` VALUES (
		NULL,
		NOW(),
		spec
	);
	RETURN MYSQL_INSERT_ID();
END //

DROP PROCEDURE IF EXISTS add_function //
CREATE PROCEDURE add_function (
	IN `name` CHAR(63),
	IN `parent` CHAR(63),
	IN `time` DOUBLE,
	IN `cpu` SMALLINT,
	IN `proc` CHAR(63),
	IN `duration` DOUBLE,
	IN `trial_id` SMALLINT
)
BEGIN
END //

DELIMITER ;

