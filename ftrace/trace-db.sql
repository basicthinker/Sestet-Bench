
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
	`pid` int NOT NULL,
	`name` char(63) NOT NULL,
	`spec` char(255),
	`trial_id` smallint NOT NULL,
	PRIMARY KEY (`pid`, `trial_id`),
	FOREIGN KEY (`trial_id`) REFERENCES `trials`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `functions` (
	`id` bigint NOT NULL auto_increment,
	`name` char(63) NOT NULL,
	`parent` char(63) NOT NULL,
	`time` double NOT NULL,
	`cpu` smallint NOT NULL,
	`pid` int NOT NULL,
	`duration` double NOT NULL,
	`depth` tinyint NOT NULL,
	`trial_id` smallint NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`pid`, `trial_id`)
	REFERENCES `processes`(`pid`, `trial_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `event_time_stat` (
	`id` bigint NOT NULL auto_increment,
	`begin_time` double NOT NULL,
	`trial_id` smallint NOT NULL,
	`func_id` bigint NOT NULL,
	PRIMARY KEY (`id`),
	FOREIGN KEY (`func_id`) REFERENCES `functions`(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `event_func_stat` (
	`id` bigint NOT NULL auto_increment,
	`begin_time` double NOT NULL,
	`interval` double NOT NULL,
	`cpu` tinyint NOT NULL,
	`func_name` char(63) NOT NULL,
	`duration_ms` double NOT NULL,
	`trial_id` smallint NOT NULL,
	PRIMARY KEY (`id`),
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
	IN pid INT,
	IN proc_name CHAR(63),
	IN proc_spec CHAR(255),
	IN trial_id INT
)
BEGIN
	INSERT INTO `processes`(`pid`, `name`, `spec`, `trial_id`)
	VALUES (
		pid,
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
	IN pid INT,
	IN duration DOUBLE,
	IN depth TINYINT,
	IN trial_id SMALLINT
)
BEGIN
	INSERT INTO `functions` VALUES (
		NULL, func_name, parent,
		func_time, cpu_num, pid,
		duration, depth, trial_id
	);
END //

DROP PROCEDURE IF EXISTS stat_event_times //
CREATE PROCEDURE stat_event_times (IN trial TINYINT)
BEGIN
	DROP TABLE IF EXISTS floor_times;
	CREATE TEMPORARY TABLE floor_times (
		`time` decimal(10,1) NOT NULL,
		`func_id` bigint NOT NULL
	);
	
	INSERT INTO floor_times
	SELECT `time`, `id` FROM functions
	WHERE `trial_id`=@trial AND `name`='input_event';

	INSERT INTO event_time_stat
	SELECT NULL, `time`, `trial_id`, `func_id` FROM (
		SELECT MIN(`func_id`) AS func_id FROM floor_times GROUP BY `time`
	) AS floor_func LEFT JOIN `functions` ON floor_func.func_id = `functions`.`id`;
END //

DELIMITER ;

