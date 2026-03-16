SELECT DISTINCT team_name
FROM (
    SELECT home_team AS team_name FROM ucl_ml_dataset WHERE home_power_goals IS NULL
    UNION
    SELECT away_team AS team_name FROM ucl_ml_dataset WHERE away_power_goals IS NULL
) AS missing_teams
ORDER BY team_name;