DROP TABLE IF EXISTS final_ml_dataset CASCADE;

CREATE TABLE final_ml_dataset AS
WITH all_matches AS (
    SELECT home_team, away_team, winning_team FROM ucl_matches
    UNION ALL
    SELECT home_team, away_team, winning_team FROM raw_matches
)
SELECT 
    m.home_team, m.away_team, m.winning_team,
    
    htp.total_goals AS home_squad_goals, htp.total_assists AS home_squad_assists,
    htp.total_shots AS home_squad_shots, htp.total_shots_on_target AS home_squad_sot,
    htp.tackles_won AS home_squad_tackles, htp.interceptions AS home_squad_interceptions,
    htp.avg_plus_minus AS home_squad_plus_minus,
    
    hpp.fw_avg_goals AS home_fw_goals, hpp.fw_avg_shots AS home_fw_shots,
    hpp.fw_avg_sot AS home_fw_sot, hpp.mf_avg_assists AS home_mf_assists,
    hpp.mf_avg_crosses AS home_mf_crosses, hpp.mf_avg_plus_minus AS home_mf_plus_minus,
    hpp.df_avg_tackles_won AS home_df_tackles, hpp.df_avg_interceptions AS home_df_interceptions,
    hpp.df_avg_plus_minus AS home_df_plus_minus,

    atp.total_goals AS away_squad_goals, atp.total_assists AS away_squad_assists,
    atp.total_shots AS away_squad_shots, atp.total_shots_on_target AS away_squad_sot,
    atp.tackles_won AS away_squad_tackles, atp.interceptions AS away_squad_interceptions,
    atp.avg_plus_minus AS away_squad_plus_minus,
    
    app.fw_avg_goals AS away_fw_goals, app.fw_avg_shots AS away_fw_shots,
    app.fw_avg_sot AS away_fw_sot, app.mf_avg_assists AS away_mf_assists,
    app.mf_avg_crosses AS away_mf_crosses, app.mf_avg_plus_minus AS away_mf_plus_minus,
    app.df_avg_tackles_won AS away_df_tackles, app.df_avg_interceptions AS away_df_interceptions,
    app.df_avg_plus_minus AS away_df_plus_minus

FROM all_matches m
LEFT JOIN raw_team_power htp ON m.home_team = htp.team_name
LEFT JOIN positional_power hpp ON m.home_team = hpp.team_name
LEFT JOIN raw_team_power atp ON m.away_team = atp.team_name
LEFT JOIN positional_power app ON m.away_team = app.team_name;