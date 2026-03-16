-- CREATE THE NEW STAGING TABLE
DROP TABLE IF EXISTS raw_matches CASCADE;

CREATE TABLE raw_matches (
    match_id SERIAL PRIMARY KEY,
    league VARCHAR(50),
    division VARCHAR(10),
    match_date DATE,
    match_time TIME,
    home_team VARCHAR(100),
    away_team VARCHAR(100),
    home_goals SMALLINT,
    away_goals SMALLINT,
    full_time_result VARCHAR(5),
    ht_home_goals SMALLINT,
    ht_away_goals SMALLINT,
    ht_result VARCHAR(5),
    home_shots SMALLINT,
    away_shots SMALLINT,
    home_shots_target SMALLINT,
    away_shots_target SMALLINT,
    home_corners SMALLINT,
    away_corners SMALLINT,
    home_fouls SMALLINT,
    away_fouls SMALLINT,
    home_yellow_cards SMALLINT,
    away_yellow_cards SMALLINT,
    home_red_cards SMALLINT,
    away_red_cards SMALLINT,
    winning_team VARCHAR(100)
);

-- CREATE INDEXES FOR FAST QUERYING
CREATE INDEX idx_raw_matches_date ON raw_matches(match_date);
CREATE INDEX idx_raw_matches_teams ON raw_matches(home_team, away_team);

