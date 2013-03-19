USE sestet;

SET @num_cores = 4;
SET @trial_id = 2;

SELECT @num_cores * (MAX(time) - MIN(time)) AS 'CPU Time (s)' FROM functions
WHERE trial_id=1;

SELECT SUM(duration)/1000000 AS 'IO Time (s)' FROM functions
WHERE parent='root' AND trial_id=2;

SELECT SUM(duration)/1000000 AS 'Syscall Time (s)' FROM functions
WHERE parent='root' AND trial_id=@trial_id AND name LIKE 'sys\_%';

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


CALL stat_event_times(1);

CALL stat_event_func(1, 0, 200);
