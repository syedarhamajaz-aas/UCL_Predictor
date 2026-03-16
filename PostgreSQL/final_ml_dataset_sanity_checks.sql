SELECT DISTINCT team_name
FROM (
    SELECT home_team AS team_name FROM final_ml_dataset WHERE home_squad_goals IS NULL
    UNION
    SELECT away_team AS team_name FROM final_ml_dataset WHERE away_squad_goals IS NULL
) AS missing_teams
ORDER BY team_name;
