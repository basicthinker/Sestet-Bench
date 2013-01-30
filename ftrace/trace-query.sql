USE sestet;

SET @num_cores = 4;
SET @trial_id = 1;

SELECT @num_cores * (MAX(time) - MIN(time)) AS 'CPU Time (s)' FROM functions
WHERE trial_id=@trial_id;

SELECT SUM(duration)/1000000 AS 'Syscall Time (s)' FROM functions
WHERE parent='root' AND trial_id=@trial_id AND name LIKE 'sys_%';

-- Calculate time portion of profiled functions over all functions

DROP TABLE IF EXISTS func_duration_aggr;
CREATE TEMPORARY TABLE func_duration_aggr(
	func_name char(63) NOT NULL,
	duration_ms double NOT NULL
);

INSERT INTO func_duration_aggr
SELECT `name`, SUM(duration)/1000 AS duration_ms FROM functions
WHERE parent='root' AND trial_id=@trial_id
GROUP BY `name` ORDER BY `duration_ms` DESC;

SELECT SUM(duration_ms) INTO @total_duration FROM func_duration_aggr;
SELECT SUM(duration_ms)/@total_duration FROM func_duration_aggr
WHERE duration_ms > 1000;

SELECT func_name, duration_ms FROM func_duration_aggr
WHERE duration_ms > 100;

DELIMITER //

DROP PROCEDURE IF EXISTS stat_event_func //
CREATE PROCEDURE stat_event_func (
	IN trial SMALLINT,
	IN cpu_num TINYINT,
	IN threshold DOUBLE -- (ms)
)
BEGIN
	DECLARE event_time DOUBLE DEFAULT 0;
	DECLARE event_cur CURSOR FOR SELECT `begin_time` FROM event_time_stat;

	DECLARE CONTINUE HANDLER FOR NOT FOUND SET event_time=0;

	OPEN event_cur;
    FETCH event_cur INTO event_time;
	WHILE event_time > 0 DO
		INSERT INTO event_func_stat
		SELECT NULL, event_time, threshold, cpu_num, `name`,
			SUM(duration)/1000, trial
		FROM functions
		WHERE `cpu`=cpu_num AND `trial_id`=trial AND
			`time` > event_time AND `time` < (event_time + threshold/1000) AND	
			`parent`='root'
		GROUP BY `name`;
		FETCH event_cur INTO event_time;
	END WHILE;
END //

DELIMITER ;
