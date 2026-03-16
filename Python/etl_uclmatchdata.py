import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def process_ucl_data():
    print("--- CONNECTING TO KAGGLE ---")
    api = KaggleApi()
    api.authenticate()

    dataset_slug = "johntocci/champions-league-matches-2025-2026"
    download_folder = "./ucl_raw_data"
    
    print(f"\n--- DOWNLOADING UCL DATASET ---")
    api.dataset_download_files(dataset_slug, path=download_folder, unzip=True)
    
    # Find the downloaded CSV file automatically
    csv_files = [f for f in os.listdir(download_folder) if f.endswith('.csv')]
    if not csv_files:
        print("❌ No CSV found in the downloaded files.")
        return None
        
    file_path = os.path.join(download_folder, csv_files[0])
    df = pd.read_csv(file_path)
    
    print(f"✅ Loaded raw UCL data. Found {len(df)} matches.")

    print("\n--- ACTUAL COLUMN NAMES ---")
    print(df.columns.tolist())
    
    # --- THE CLEANING PHASE ---
    print("\n--- CLEANING THE SCORE COLUMN ---")
    
    # 1. Drop any unplayed matches where the 'score' might be blank (LOWERCASE 's')
    df = df.dropna(subset=['score'])
    
    # 2. Split the 'score' column into two separate columns (e.g., '2-1' -> '2' and '1')
    score_split = df['score'].str.split(r'-|–', expand=True)
    
    # 3. Assign to new columns and convert to numbers
    df['home_goals'] = pd.to_numeric(score_split[0].str.strip(), errors='coerce')
    df['away_goals'] = pd.to_numeric(score_split[1].str.strip(), errors='coerce')
    
    # 4. Calculate the winning team for our Machine Learning Target!
    def determine_winner(row):
        if row['home_goals'] > row['away_goals']:
            return 'Home'
        elif row['home_goals'] < row['away_goals']:
            return 'Away'
        else:
            return 'Draw'
            
    df['winning_team'] = df.apply(determine_winner, axis=1)
    
    # Show the cleaned results using the correct lowercase column names
    print("\n--- PREVIEW OF CLEANED ML TARGETS ---")
    print(df[['home_team', 'away_team', 'score', 'home_goals', 'away_goals', 'winning_team']].head(10))
    
    return df

if __name__ == "__main__":
    clean_ucl_df = process_ucl_data()

def load_to_postgres(df):
    print("\n--- STEP 3: LOADING UCL DATA TO POSTGRESQL ---")
    
    # Pointing directly to your ucl_predictor database!
    db_url = "postgresql+psycopg2://postgres:Student%40123@127.0.0.1:1234/ucl_predictor"
    
    try:
        from sqlalchemy import create_engine
        engine = create_engine(db_url)
        
        # Inject the data into the 'ucl_matches' table
        df.to_sql('ucl_matches', engine, if_exists='replace', index=False)
        
        print(f"Success! Injected {len(df)} historical UCL matches into the database.")
        
    except Exception as e:
        print(f"Failed to load data to PostgreSQL: {e}")

if __name__ == "__main__":
    clean_ucl_df = process_ucl_data()
    
    if clean_ucl_df is not None:
        load_to_postgres(clean_ucl_df)