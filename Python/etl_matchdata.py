import pandas as pd
from sqlalchemy import create_engine

def extract_and_transform_data():
    print("--- STEP 1: EXTRACTING DATA ---")
    
    urls = {
        "Premier League": "https://www.football-data.co.uk/mmz4281/2526/E0.csv",
        "La Liga":        "https://www.football-data.co.uk/mmz4281/2526/SP1.csv",
        "Serie A":        "https://www.football-data.co.uk/mmz4281/2526/I1.csv",
        "Bundesliga":     "https://www.football-data.co.uk/mmz4281/2526/D1.csv",
        "Ligue 1":        "https://www.football-data.co.uk/mmz4281/2526/F1.csv"
    }
    
    raw_dataframes = []
    
    for league, url in urls.items():
        try:
            df = pd.read_csv(url)
            df['League'] = league 
            raw_dataframes.append(df)
            print(f"✅ Loaded {league}")
        except Exception as e:
            print(f"❌ Error loading {league}: {e}")
            
    master_df = pd.concat(raw_dataframes, ignore_index=True)
    
    print("\n--- STEP 2: TRANSFORMING & CLEANING DATA ---")
    
    # 1. Define exactly which columns to keep and what to rename them to
    columns_to_keep = {
        'League': 'league',
        'Div': 'division',
        'Date': 'match_date',
        'Time': 'match_time',
        'HomeTeam': 'home_team',
        'AwayTeam': 'away_team',
        'FTHG': 'home_goals',
        'FTAG': 'away_goals',
        'FTR': 'full_time_result', # Keeping H/D/A for the ML Model
        'HTHG': 'ht_home_goals',
        'HTAG': 'ht_away_goals',
        'HTR': 'ht_result',
        'HS': 'home_shots',
        'AS': 'away_shots',
        'HST': 'home_shots_target',
        'AST': 'away_shots_target',
        'HC': 'home_corners',
        'AC': 'away_corners',
        'HF': 'home_fouls',
        'AF': 'away_fouls',
        'HY': 'home_yellow_cards',
        'AY': 'away_yellow_cards',
        'HR': 'home_red_cards',
        'AR': 'away_red_cards',
    }

    # 2. Filter out all the betting junk by only keeping the columns in our dictionary
    clean_df = master_df[list(columns_to_keep.keys())].copy()
    
    # 3. Rename the columns to our clean, readable SQL formats
    clean_df = clean_df.rename(columns=columns_to_keep)
    
    # 4. Feature Engineering: Create the 'winning_team' column for Power BI
    def determine_winner(row):
        if row['full_time_result'] == 'H':
            return row['home_team']
        elif row['full_time_result'] == 'A':
            return row['away_team']
        else:
            return 'Draw'

    clean_df['winning_team'] = clean_df.apply(determine_winner, axis=1)
    
    # 5. Fix the date format so PostgreSQL and Power BI can read it easily
    clean_df['match_date'] = pd.to_datetime(clean_df['match_date'], format='%d/%m/%Y', errors='coerce')
    
    # THIS WAS THE MISSING LINE!
    return clean_df
    
def load_to_postgres(df):
    print("\n--- STEP 3: LOADING TO POSTGRESQL ---")
    
    # Format: postgresql+psycopg2://username:password@localhost:port/database_name
    db_url = "postgresql+psycopg2://postgres:Student%40123@127.0.0.1:1234/ucl_predictor"
    
    try:
        # Create the connection engine
        engine = create_engine(db_url)
        
        # Inject the data into the 'raw_matches' table
        rows_inserted = df.to_sql('raw_matches', engine, if_exists='append', index=False)
        
        print(f"🎉 Success! Injected {len(df)} rows securely into the 'raw_matches' table.")
        
    except Exception as e:
        print(f"❌ Failed to load data to PostgreSQL: {e}")

if __name__ == "__main__":
    # Run the extraction and cleaning phase
    final_clean_df = extract_and_transform_data()
    
    # Run the loading phase
    load_to_postgres(final_clean_df)