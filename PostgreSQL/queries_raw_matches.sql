WITH RankedMatches AS (
    SELECT 
        league,
        match_date,
        home_team,
        away_team,
        home_goals,
        away_goals,
        winning_team,
        ROW_NUMBER() OVER(PARTITION BY league ORDER BY match_date ASC, match_time ASC) as game_number
    FROM raw_matches
)
-- Query to get the first 5 matches of each league
SELECT * FROM RankedMatches
WHERE game_number <= 5
ORDER BY league, match_date;

