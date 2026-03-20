DROP TABLE IF EXISTS final_ml_dataset CASCADE;

CREATE TABLE final_ml_dataset AS
WITH all_matches AS (
    SELECT 
        home_team, away_team, winning_team,
        home_goals, away_goals
    FROM ucl_matches
    UNION ALL
    SELECT 
        home_team, away_team, winning_team,
        home_goals, away_goals
    FROM raw_matches
)
SELECT 
    -- 1. MATCH INFO (Labels/Targets)
    m.home_team, 
    m.away_team, 
    m.home_goals AS actual_home_goals,
    m.away_goals AS actual_away_goals,
    m.winning_team AS actual_result,
    
    CASE 
        WHEN m.home_goals > m.away_goals THEN 2
        WHEN m.home_goals = m.away_goals THEN 1
        WHEN m.home_goals < m.away_goals THEN 0
        ELSE NULL 
    END AS result_id,

    -- 2. HOME TEAM FEATURES (Rounded to 2 Decimal Places)
    ROUND(htp.total_goals::numeric, 2) AS h_season_goals, 
    ROUND(htp.total_shots::numeric, 2) AS h_season_shots,
    ROUND(htp.avg_plus_minus::numeric, 2) AS h_squad_plus_minus,
    ROUND(hpp.fw_avg_goals::numeric, 2) AS h_fw_rating, 
    ROUND(hpp.fw_avg_shots::numeric, 2) AS h_fw_shots,
    ROUND(hpp.mf_avg_assists::numeric, 2) AS h_mf_creative_score,
    ROUND(hpp.mf_avg_plus_minus::numeric, 2) AS h_mf_control_score,
    ROUND(hpp.df_avg_tackles_won::numeric, 2) AS h_df_tackles,
    ROUND(hpp.df_avg_plus_minus::numeric, 2) AS h_df_solidity,

    -- 3. AWAY TEAM FEATURES (Rounded to 2 Decimal Places)
    ROUND(atp.total_goals::numeric, 2) AS a_season_goals, 
    ROUND(atp.total_shots::numeric, 2) AS a_season_shots,
    ROUND(atp.avg_plus_minus::numeric, 2) AS a_squad_plus_minus,
    ROUND(app.fw_avg_goals::numeric, 2) AS a_fw_rating, 
    ROUND(app.fw_avg_shots::numeric, 2) AS a_fw_shots,
    ROUND(app.mf_avg_assists::numeric, 2) AS a_mf_creative_score,
    ROUND(app.mf_avg_plus_minus::numeric, 2) AS a_mf_control_score,
    ROUND(app.df_avg_tackles_won::numeric, 2) AS a_df_tackles,
    ROUND(app.df_avg_plus_minus::numeric, 2) AS a_df_solidity

FROM all_matches m
LEFT JOIN raw_team_power htp ON m.home_team = htp.team_name
LEFT JOIN positional_power hpp ON m.home_team = hpp.team_name
LEFT JOIN raw_team_power atp ON m.away_team = atp.team_name
LEFT JOIN positional_power app ON m.away_team = app.team_name
WHERE htp.team_name IS NOT NULL AND atp.team_name IS NOT NULL;