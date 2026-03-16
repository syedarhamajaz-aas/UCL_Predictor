import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def download_player_data():
    print("--- CONNECTING TO KAGGLE ---")
    
    try:
        api = KaggleApi()
        api.authenticate()
        print("✅ Successfully authenticated with Kaggle!")
    except Exception as e:
        print(f"❌ Authentication failed. Check your kaggle.json path. Error: {e}")
        return None

    dataset_slug = "hubertsidorowicz/football-players-stats-2025-2026" 
    download_folder = "./fbref_raw_data"
    
    print(f"\n--- DOWNLOADING DATASET: {dataset_slug} ---")
    try:
        api.dataset_download_files(dataset_slug, path=download_folder, unzip=True)
        print(f"✅ Download complete! Files saved to {download_folder}")
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

    print("\n--- AGGREGATING PLAYER DATA INTO TEAM POWER RATINGS ---")
    main_file_path = os.path.join(download_folder, "players_data-2025_2026.csv")
    
    if os.path.exists(main_file_path):
        df = pd.read_csv(main_file_path, low_memory=False)
        
        # 1. Select only the columns we need for our Machine Learning model
        columns_to_keep = ['Squad', 'Min', 'Gls', 'Ast', 'Sh', 'SoT', 'TklW', 'Int', '+/-']
        df_filtered = df[columns_to_keep].copy()
        
        # 2. Clean the data (convert strings to numbers, replace commas, fill blanks with 0)
        numeric_cols = ['Min', 'Gls', 'Ast', 'Sh', 'SoT', 'TklW', 'Int', '+/-']
        for col in numeric_cols:
            df_filtered[col] = pd.to_numeric(df_filtered[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)
            
        # 3. Smash the players together to create Team Profiles!
        team_power_df = df_filtered.groupby('Squad')[['Gls', 'Ast', 'Sh', 'SoT', 'TklW', 'Int']].sum().reset_index()
        team_power_df['avg_plus_minus'] = df_filtered.groupby('Squad')['+/-'].mean().round(2).values
        
        # 4. RENAME COLUMNS to beautiful, readable formats
        readable_names = {
            'Squad': 'team_name',
            'Gls': 'total_goals',
            'Ast': 'total_assists',
            'Sh': 'total_shots',
            'SoT': 'total_shots_on_target',
            'TklW': 'tackles_won',
            'Int': 'interceptions'
        }
        team_power_df = team_power_df.rename(columns=readable_names)
        
        print("✅ Successfully generated Team Power Ratings from individual player data!")
        print("\n--- PREVIEW OF CLEAN TEAM ML FEATURES ---")
        print(team_power_df.head(10))
        
        return team_power_df
    else:
        print("❌ Could not find the extracted CSV file.")
        return None
    
def load_to_postgres(df):
    print("\n--- STEP 3: LOADING TEAM POWER TO POSTGRESQL ---")
    
    # Using your exact credentials from the first script
    db_url = "postgresql+psycopg2://postgres:Student%40123@127.0.0.1:1234/ucl_predictor"
    
    try:
        from sqlalchemy import create_engine
        engine = create_engine(db_url)
        
        # Inject the data into the new 'raw_team_power' table
        df.to_sql('raw_team_power', engine, if_exists='replace', index=False)
        
        print(f"🎉 Success! Injected {len(df)} teams securely into the 'raw_team_power' table.")
        
    except Exception as e:
        print(f"❌ Failed to load data to PostgreSQL: {e}")

if __name__ == "__main__":
    # 1. Download and transform the player data
    final_team_power_df = download_player_data()
    
    # 2. If it worked, load it into the database
    if final_team_power_df is not None:
        load_to_postgres(final_team_power_df)
