
-- DROP DATABASE `sestet`;
CREATE DATABASE `sestet`;
USE `sestet`;

CREATE TABLE IF NOT EXISTS `trials` (
	`id` smallint NOT NULL auto_increment,
	`date` datetime NOT NULL,
	`spec` text,
	PRIMARY KEY (`id`),
	UNIQUE KEY (`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `processes` (
	`id` int NOT NULL auto_increment,
	`name` char(63) NOT NULL,
	`spec` char(255) NOT NULL,
	`trial_id` smallint NOT NULL,
	PRIMARY KEY (`id`),
	UNIQUE KEY (`name`),
	FOREIGN KEY (`trial_id`) REFERENCES `trials`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `functions` (
	`id` bigint NOT NULL auto_increment,
	`name` char(63) NOT NULL,
	`parent` char(63) NOT NULL,
	`time` double NOT NULL,
	`cpu` smallint NOT NULL,
	`proc_id` int NOT NULL,
	`duration` double NOT NULL,
	`trial_id` smallint NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`proc_id`) REFERENCES `processes`(`id`),
	FOREIGN KEY (`trial_id`) REFERENCES `trials`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

DELIMITER //

DROP FUNCTION IF EXISTS add_trial //
CREATE FUNCTION add_trial (spec TEXT)
RETURNS SMALLINT
BEGIN
	INSERT INTO `trials` VALUES (
		NULL,
		NOW(),
		spec
	);
	RETURN LAST_INSERT_ID();
END //

DROP PROCEDURE IF EXISTS add_process //
CREATE PROCEDURE add_process (
	IN proc_name CHAR(63),
	IN proc_spec CHAR(255),
	IN trial_id INT
)
BEGIN
	INSERT INTO `processes`(`name`, `spec`, `trial_id`) VALUES (
		proc_name,
		proc_spec,
		trial_id
	);
END //

DROP PROCEDURE IF EXISTS add_function //
CREATE PROCEDURE add_function (
	IN func_name CHAR(63),
	IN parent CHAR(63),
	IN func_time DOUBLE,
	IN cpu_num SMALLINT,
	IN proc CHAR(63),
	IN duration DOUBLE,
	IN trial_id SMALLINT
)
BEGIN
	SELECT `id` INTO @proc_id FROM `processes`
    WHERE `name` = proc AND `trial_id` = trial_id;

	INSERT INTO `functions` VALUES (
		NULL, func_name, parent,
		func_time, cpu_num, @proc_id,
		duration, trial_id		
	);
END //

DELIMITER ;

