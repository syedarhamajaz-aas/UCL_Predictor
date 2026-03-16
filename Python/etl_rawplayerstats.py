import os
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi
from sqlalchemy import create_engine

def build_star_power():
    print("--- 1. DOWNLOADING PLAYER DATA FROM KAGGLE ---")
    api = KaggleApi()
    api.authenticate()
    
    dataset_slug = "hubertsidorowicz/football-players-stats-2025-2026" 
    download_folder = "./fbref_raw_data"
    api.dataset_download_files(dataset_slug, path=download_folder, unzip=True)
    
    # Locate the CSV
    csv_file = os.path.join(download_folder, "players_data-2025_2026.csv")
    df = pd.read_csv(csv_file, low_memory=False)
    
    print(f"✅ Loaded {len(df)} players.")
# Locate the CSV
    csv_file = os.path.join(download_folder, "players_data-2025_2026.csv")
    df = pd.read_csv(csv_file, low_memory=False)
    
    print(f"✅ Loaded {len(df)} players.")

    # --- ADD THESE TWO LINES TO FIND THE REAL NAMES ---
    print("\n--- ACTUAL COLUMN NAMES ---")
    print(df.columns.tolist())
    
    print("\n--- 2. CLEANING POSITIONS & NUMBERS ---")
    # Grab only the first two letters of the position (e.g., 'MF,FW' becomes 'MF')
    df['Primary_Pos'] = df['Pos'].astype(str).str[:2]
    
    # Filter down to the core outfield positions
    df = df[df['Primary_Pos'].isin(['FW', 'MF', 'DF'])]
    
    # The columns we ACTUALLY have in this specific dataset
    power_cols = ['Starts', 'Gls', 'Ast', 'Sh', 'SoT', 'Crs', 'TklW', 'Int', '+/-']
    
    # Convert them to numeric, dropping any weird commas or blanks
    for col in power_cols:
        df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce').fillna(0)

    print("\n--- 3. EXTRACTING THE TOP 3 STARTERS PER POSITION ---")
    # Sort by Team, then Position, then by amount of 'Starts' (highest to lowest)
    sorted_df = df.sort_values(by=['Squad', 'Primary_Pos', 'Starts'], ascending=[True, True, False])
    
    # Snag the top 3 players for each position on each team
    top_starters = sorted_df.groupby(['Squad', 'Primary_Pos']).head(3)

    print("\n--- 4. CALCULATING POSITIONAL LETHALITY ---")
    # Average the stats of those 3 elite players
    team_averages = top_starters.groupby(['Squad', 'Primary_Pos'])[power_cols].mean().reset_index()

    # 1. Attack Power (FW)
    fw_power = team_averages[team_averages['Primary_Pos'] == 'FW'][['Squad', 'Gls', 'Sh', 'SoT']]
    fw_power.columns = ['team_name', 'fw_avg_goals', 'fw_avg_shots', 'fw_avg_sot']
    
    # 2. Midfield Power (MF)
    mf_power = team_averages[team_averages['Primary_Pos'] == 'MF'][['Squad', 'Ast', 'Crs', '+/-']]
    mf_power.columns = ['team_name', 'mf_avg_assists', 'mf_avg_crosses', 'mf_avg_plus_minus']
    
    # 3. Defense Power (DF)
    df_power = team_averages[team_averages['Primary_Pos'] == 'DF'][['Squad', 'TklW', 'Int', '+/-']]
    df_power.columns = ['team_name', 'df_avg_tackles_won', 'df_avg_interceptions', 'df_avg_plus_minus']

    # Merge them all together into one flat table
    final_power_df = pd.merge(fw_power, mf_power, on='team_name', how='outer')
    final_power_df = pd.merge(final_power_df, df_power, on='team_name', how='outer').fillna(0)

    print("\n✅ STAR POWER MATRIX GENERATED!")
    print(final_power_df.head())
    
    return final_power_df

def load_to_postgres(df):
    print("\n--- 5. LOADING STAR POWER TO POSTGRESQL ---")
    db_url = "postgresql+psycopg2://postgres:Student%40123@127.0.0.1:1234/ucl_predictor"
    engine = create_engine(db_url)
    
    df.to_sql('positional_power', engine, if_exists='replace', index=False)
    print("🎉 Success! The Star Power ratings are securely locked in the database.")

if __name__ == "__main__":
    power_df = build_star_power()
    load_to_postgres(power_df)