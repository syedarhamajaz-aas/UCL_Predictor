-- SPAIN
UPDATE ucl_matches SET home_team = 'Atlético Madrid' WHERE home_team IN ('Atletico Madrid', 'Ath Madrid');
UPDATE ucl_matches SET away_team = 'Atlético Madrid' WHERE away_team IN ('Atletico Madrid', 'Ath Madrid');
UPDATE raw_matches SET home_team = 'Atlético Madrid' WHERE home_team IN ('Atletico Madrid', 'Ath Madrid');
UPDATE raw_matches SET away_team = 'Atlético Madrid' WHERE away_team IN ('Atletico Madrid', 'Ath Madrid');

UPDATE ucl_matches SET home_team = 'Athletic Club' WHERE home_team = 'Ath Bilbao';
UPDATE ucl_matches SET away_team = 'Athletic Club' WHERE away_team = 'Ath Bilbao';
UPDATE raw_matches SET home_team = 'Athletic Club' WHERE home_team = 'Ath Bilbao';
UPDATE raw_matches SET away_team = 'Athletic Club' WHERE away_team = 'Ath Bilbao';

UPDATE ucl_matches SET home_team = 'Real Betis' WHERE home_team = 'Betis';
UPDATE ucl_matches SET away_team = 'Real Betis' WHERE away_team = 'Betis';
UPDATE raw_matches SET home_team = 'Real Betis' WHERE home_team = 'Betis';
UPDATE raw_matches SET away_team = 'Real Betis' WHERE away_team = 'Betis';

UPDATE ucl_matches SET home_team = 'Celta Vigo' WHERE home_team = 'Celta';
UPDATE ucl_matches SET away_team = 'Celta Vigo' WHERE away_team = 'Celta';
UPDATE raw_matches SET home_team = 'Celta Vigo' WHERE home_team = 'Celta';
UPDATE raw_matches SET away_team = 'Celta Vigo' WHERE away_team = 'Celta';

UPDATE ucl_matches SET home_team = 'Espanyol' WHERE home_team = 'Espanol';
UPDATE ucl_matches SET away_team = 'Espanyol' WHERE away_team = 'Espanol';
UPDATE raw_matches SET home_team = 'Espanyol' WHERE home_team = 'Espanol';
UPDATE raw_matches SET away_team = 'Espanyol' WHERE away_team = 'Espanol';

UPDATE ucl_matches SET home_team = 'Rayo Vallecano' WHERE home_team = 'Vallecano';
UPDATE ucl_matches SET away_team = 'Rayo Vallecano' WHERE away_team = 'Vallecano';
UPDATE raw_matches SET home_team = 'Rayo Vallecano' WHERE home_team = 'Vallecano';
UPDATE raw_matches SET away_team = 'Rayo Vallecano' WHERE away_team = 'Vallecano';

-- FRANCE
UPDATE ucl_matches SET home_team = 'Paris Saint-Germain' WHERE home_team = 'Paris SG';
UPDATE ucl_matches SET away_team = 'Paris Saint-Germain' WHERE away_team = 'Paris SG';
UPDATE raw_matches SET home_team = 'Paris Saint-Germain' WHERE home_team = 'Paris SG';
UPDATE raw_matches SET away_team = 'Paris Saint-Germain' WHERE away_team = 'Paris SG';

-- ENGLAND
UPDATE ucl_matches SET home_team = 'Tottenham Hotspur' WHERE home_team = 'Tottenham';
UPDATE ucl_matches SET away_team = 'Tottenham Hotspur' WHERE away_team = 'Tottenham';
UPDATE raw_matches SET home_team = 'Tottenham Hotspur' WHERE home_team = 'Tottenham';
UPDATE raw_matches SET away_team = 'Tottenham Hotspur' WHERE away_team = 'Tottenham';

UPDATE ucl_matches SET home_team = 'Nottingham Forest' WHERE home_team = 'Nott''m Forest';
UPDATE ucl_matches SET away_team = 'Nottingham Forest' WHERE away_team = 'Nott''m Forest';
UPDATE raw_matches SET home_team = 'Nottingham Forest' WHERE home_team = 'Nott''m Forest';
UPDATE raw_matches SET away_team = 'Nottingham Forest' WHERE away_team = 'Nott''m Forest';

-- GERMANY
UPDATE ucl_matches SET home_team = 'Eintracht Frankfurt' WHERE home_team = 'Ein Frankfurt';
UPDATE ucl_matches SET away_team = 'Eintracht Frankfurt' WHERE away_team = 'Ein Frankfurt';
UPDATE raw_matches SET home_team = 'Eintracht Frankfurt' WHERE home_team = 'Ein Frankfurt';
UPDATE raw_matches SET away_team = 'Eintracht Frankfurt' WHERE away_team = 'Ein Frankfurt';

UPDATE ucl_matches SET home_team = 'Mönchengladbach' WHERE home_team = 'M''gladbach';
UPDATE ucl_matches SET away_team = 'Mönchengladbach' WHERE away_team = 'M''gladbach';
UPDATE raw_matches SET home_team = 'Mönchengladbach' WHERE home_team = 'M''gladbach';
UPDATE raw_matches SET away_team = 'Mönchengladbach' WHERE away_team = 'M''gladbach';

UPDATE ucl_matches SET home_team = 'Mainz 05' WHERE home_team = 'Mainz';
UPDATE ucl_matches SET away_team = 'Mainz 05' WHERE away_team = 'Mainz';
UPDATE raw_matches SET home_team = 'Mainz 05' WHERE home_team = 'Mainz';
UPDATE raw_matches SET away_team = 'Mainz 05' WHERE away_team = 'Mainz';

UPDATE ucl_matches SET home_team = 'Köln' WHERE home_team = 'FC Koln';
UPDATE ucl_matches SET away_team = 'Köln' WHERE away_team = 'FC Koln';
UPDATE raw_matches SET home_team = 'Köln' WHERE home_team = 'FC Koln';
UPDATE raw_matches SET away_team = 'Köln' WHERE away_team = 'FC Koln';

-- ITALY
UPDATE ucl_matches SET home_team = 'Hellas Verona' WHERE home_team = 'Verona';
UPDATE ucl_matches SET away_team = 'Hellas Verona' WHERE away_team = 'Verona';
UPDATE raw_matches SET home_team = 'Hellas Verona' WHERE home_team = 'Verona';
UPDATE raw_matches SET away_team = 'Hellas Verona' WHERE away_team = 'Verona';

-- ==========================================
-- FIXING MANCHESTER CITY
-- ==========================================
UPDATE ucl_matches SET home_team = 'Manchester City' WHERE home_team = 'Man City';
UPDATE ucl_matches SET away_team = 'Manchester City' WHERE away_team = 'Man City';
UPDATE raw_matches SET home_team = 'Manchester City' WHERE home_team = 'Man City';
UPDATE raw_matches SET away_team = 'Manchester City' WHERE away_team = 'Man City';

-- ==========================================
-- FIXING MANCHESTER UNITED
-- ==========================================
UPDATE ucl_matches SET home_team = 'Manchester United' WHERE home_team IN ('Man United', 'Man Utd');
UPDATE ucl_matches SET away_team = 'Manchester United' WHERE away_team IN ('Man United', 'Man Utd');
UPDATE raw_matches SET home_team = 'Manchester United' WHERE home_team IN ('Man United', 'Man Utd');
UPDATE raw_matches SET away_team = 'Manchester United' WHERE away_team IN ('Man United', 'Man Utd');

-- ==========================================
-- FIXING ATLETICO MADRID (The Missing Accent)
-- ==========================================
UPDATE ucl_matches SET home_team = 'Atlético Madrid' WHERE home_team = 'Atletico Madrid';
UPDATE ucl_matches SET away_team = 'Atlético Madrid' WHERE away_team = 'Atletico Madrid';
UPDATE raw_matches SET home_team = 'Atlético Madrid' WHERE home_team = 'Atletico Madrid';
UPDATE raw_matches SET away_team = 'Atlético Madrid' WHERE away_team = 'Atletico Madrid';

-- ==========================================
-- FIXING NEWCASTLE, LEEDS & WEST HAM
-- ==========================================
UPDATE ucl_matches SET home_team = 'Newcastle United' WHERE home_team = 'Newcastle';
UPDATE ucl_matches SET away_team = 'Newcastle United' WHERE away_team = 'Newcastle';
UPDATE raw_matches SET home_team = 'Newcastle United' WHERE home_team = 'Newcastle';
UPDATE raw_matches SET away_team = 'Newcastle United' WHERE away_team = 'Newcastle';

UPDATE ucl_matches SET home_team = 'Leeds United' WHERE home_team = 'Leeds';
UPDATE ucl_matches SET away_team = 'Leeds United' WHERE away_team = 'Leeds';
UPDATE raw_matches SET home_team = 'Leeds United' WHERE home_team = 'Leeds';
UPDATE raw_matches SET away_team = 'Leeds United' WHERE away_team = 'Leeds';

UPDATE ucl_matches SET home_team = 'West Ham United' WHERE home_team = 'West Ham';
UPDATE ucl_matches SET away_team = 'West Ham United' WHERE away_team = 'West Ham';
UPDATE raw_matches SET home_team = 'West Ham United' WHERE home_team = 'West Ham';
UPDATE raw_matches SET away_team = 'West Ham United' WHERE away_team = 'West Ham';

-- ==========================================
-- FIXING SOCIEDAD
-- ==========================================
UPDATE ucl_matches SET home_team = 'Real Sociedad' WHERE home_team = 'Sociedad';
UPDATE ucl_matches SET away_team = 'Real Sociedad' WHERE away_team = 'Sociedad';
UPDATE raw_matches SET home_team = 'Real Sociedad' WHERE home_team = 'Sociedad';
UPDATE raw_matches SET away_team = 'Real Sociedad' WHERE away_team = 'Sociedad';

-- Fix Alaves (adding the accent)
UPDATE ucl_matches SET home_team = 'Alavés' WHERE home_team = 'Alaves';
UPDATE ucl_matches SET away_team = 'Alavés' WHERE away_team = 'Alaves';
UPDATE raw_matches SET home_team = 'Alavés' WHERE home_team = 'Alaves';
UPDATE raw_matches SET away_team = 'Alavés' WHERE away_team = 'Alaves';

-- Fix Manchester United (changing to FBref's 'Utd' shorthand)
UPDATE ucl_matches SET home_team = 'Manchester Utd' WHERE home_team = 'Manchester United';
UPDATE ucl_matches SET away_team = 'Manchester Utd' WHERE away_team = 'Manchester United';
UPDATE raw_matches SET home_team = 'Manchester Utd' WHERE home_team = 'Manchester United';
UPDATE raw_matches SET away_team = 'Manchester Utd' WHERE away_team = 'Manchester United';

-- Fix Mönchengladbach (changing to FBref's shorthand)
UPDATE ucl_matches SET home_team = 'Gladbach' WHERE home_team IN ('M''Gladbach', 'Mönchengladbach');
UPDATE ucl_matches SET away_team = 'Gladbach' WHERE away_team IN ('M''Gladbach', 'Mönchengladbach');
UPDATE raw_matches SET home_team = 'Gladbach' WHERE home_team IN ('M''Gladbach', 'Mönchengladbach');
UPDATE raw_matches SET away_team = 'Gladbach' WHERE away_team IN ('M''Gladbach', 'Mönchengladbach');

-- Fixing Winning Team Names (for consistency in the target variable)
-- Convert "Home" and "Away" into the actual team names
UPDATE ucl_matches SET winning_team = home_team WHERE winning_team ILIKE 'Home';
UPDATE ucl_matches SET winning_team = away_team WHERE winning_team ILIKE 'Away';

UPDATE raw_matches SET winning_team = home_team WHERE winning_team ILIKE 'Home';
UPDATE raw_matches SET winning_team = away_team WHERE winning_team ILIKE 'Away';
