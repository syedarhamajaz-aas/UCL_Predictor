DROP TABLE IF EXISTS ucl_ml_dataset CASCADE;

CREATE TABLE ucl_ml_dataset AS
SELECT 
    m.home_team,
    m.away_team,
    m.winning_team,
    
    -- Injecting the Home Team's Tactical Power
    h.total_goals AS home_power_goals,
    h.total_shots AS home_power_shots,
    h.total_shots_on_target AS home_power_sot,
    h.tackles_won AS home_power_tackles,
    h.interceptions AS home_power_interceptions,
    h.avg_plus_minus AS home_power_plus_minus,
    
    -- Injecting the Away Team's Tactical Power
    a.total_goals AS away_power_goals,
    a.total_shots AS away_power_shots,
    a.total_shots_on_target AS away_power_sot,
    a.tackles_won AS away_power_tackles,
    a.interceptions AS away_power_interceptions,
    a.avg_plus_minus AS away_power_plus_minus

FROM ucl_matches m
-- Match the home team to their domestic power ratings
LEFT JOIN raw_team_power h ON m.home_team = h.team_name
-- Match the away team to their domestic power ratings
LEFT JOIN raw_team_power a ON m.away_team = a.team_name;