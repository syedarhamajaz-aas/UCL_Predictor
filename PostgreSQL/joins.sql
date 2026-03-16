DROP TABLE IF EXISTS ml_master_dataset CASCADE;

CREATE TABLE ml_master_dataset AS
SELECT 
    m.match_id,
    m.league,
    m.match_date,
    m.home_team,
    m.away_team,
    m.home_goals,
    m.away_goals,
    m.winning_team,
    
    h.total_goals AS home_power_goals,
    h.total_shots AS home_power_shots,
    h.total_shots_on_target AS home_power_sot,
    h.tackles_won AS home_power_tackles,
    h.interceptions AS home_power_interceptions,
    h.avg_plus_minus AS home_power_plus_minus,
    
    a.total_goals AS away_power_goals,
    a.total_shots AS away_power_shots,
    a.total_shots_on_target AS away_power_sot,
    a.tackles_won AS away_power_tackles,
    a.interceptions AS away_power_interceptions,
    a.avg_plus_minus AS away_power_plus_minus

FROM raw_matches m
-- Join 1: Match the home team to the power table
LEFT JOIN raw_team_power h ON m.home_team = h.team_name
-- Join 2: Match the away team to the power table
LEFT JOIN raw_team_power a ON m.away_team = a.team_name;