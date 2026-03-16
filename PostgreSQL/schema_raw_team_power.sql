DROP TABLE IF EXISTS raw_team_power CASCADE;

CREATE TABLE raw_team_power (
    team_name VARCHAR(100) PRIMARY KEY,
    total_goals SMALLINT,
    total_assists SMALLINT,
    total_shots SMALLINT,
    total_shots_on_target SMALLINT,
    tackles_won SMALLINT,
    interceptions SMALLINT,
    avg_plus_minus NUMERIC(5,2)
);