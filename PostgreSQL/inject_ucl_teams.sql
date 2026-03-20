-- ==========================================
-- 1. SQUAD POWER (The Macro View)
-- ==========================================
INSERT INTO raw_team_power 
(team_name, total_goals, total_assists, total_shots, total_shots_on_target, tackles_won, interceptions, avg_plus_minus)
VALUES 
('Sporting CP', 16, 10, 98, 42, 80, 66, 0.5);
INSERT INTO raw_team_power 
(team_name, total_goals, total_assists, total_shots, total_shots_on_target, tackles_won, interceptions, avg_plus_minus)
VALUES 
('Galatasaray', 16, 8, 152, 24, 63, 51, 0.5);
INSERT INTO raw_team_power 
(team_name, total_goals, total_assists, total_shots, total_shots_on_target, tackles_won, interceptions, avg_plus_minus)
VALUES 
('Bodø/Glimt', 14, 10, 90, 33, 63, 44, 1.5);

-- ==========================================
-- 2. STAR POWER (The Micro View)
-- ==========================================
INSERT INTO positional_power 
(team_name, fw_avg_goals, fw_avg_shots, fw_avg_sot, mf_avg_assists, mf_avg_crosses, mf_avg_plus_minus, df_avg_tackles_won, df_avg_interceptions, df_avg_plus_minus)
VALUES 
('Sporting CP', 2.25, 13.5, 5.5, 1.5, 8.5, 0.5, 4.75, 6.75, 0.5);
INSERT INTO positional_power 
(team_name, fw_avg_goals, fw_avg_shots, fw_avg_sot, mf_avg_assists, mf_avg_crosses, mf_avg_plus_minus, df_avg_tackles_won, df_avg_interceptions, df_avg_plus_minus)
VALUES 
('Galatasaray', 1.5, 10.0, 3.25, 1.0, 10.5, -0.5, 8.0, 8.0, -0.5);
INSERT INTO positional_power 
(team_name, fw_avg_goals, fw_avg_shots, fw_avg_sot, mf_avg_assists, mf_avg_crosses, mf_avg_plus_minus, df_avg_tackles_won, df_avg_interceptions, df_avg_plus_minus)
VALUES 
('Bodø/Glimt', 2.0, 11.6, 5.3, 1.5, 8.5, 1.5, 5.25, 4.75, 1.5);