import pandas as pd
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

def train_model():
    print("--- 1. PULLING THE MASTER DATASET ---")
    db_url = "postgresql+psycopg2://postgres:Student%40123@127.0.0.1:1234/ucl_predictor"
    engine = create_engine(db_url)
    
    df = pd.read_sql("SELECT * FROM final_ml_dataset;", engine)
    
    # Drop the rows with missing stats (the non-Top 5 teams like Ajax/PSV)
    df = df.dropna()
    print(f"✅ Loaded {len(df)} elite matches for training.")
    
    print("\n--- 2. SETTING UP FEATURES (X) AND TARGET (y) ---")
    # y is what we want to predict (Home, Away, or Draw)
    y = df['winning_team']
    
    # X is the tactical stats. We drop the team names because algorithms only read numbers
    X = df.drop(columns=['home_team', 'away_team', 'winning_team'])
    
    # Split the data: 80% for the model to study, 20% to test it like a final exam
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    print("\n--- 3. TRAINING THE RANDOM FOREST ---")
    # We spawn 100 "decision trees" to act as our tactical analysts
    rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    
    print("\n--- 4. TESTING THE MODEL ---")
    # Force the model to guess the outcomes of the 20% of matches it hasn't seen
    predictions = rf_model.predict(X_test)
    
    # Grade the exam
    accuracy = accuracy_score(y_test, predictions)
    print(f"🎯 Model Accuracy: {accuracy * 100:.2f}%")
    
    return rf_model, X.columns

def check_feature_importance(model, feature_names):
    print("\n--- 5. INSIDE THE ALGORITHM'S BRAIN (TOP 10 STATS) ---")
    
    # Extract the importance scores and zip them with your column names
    importances = model.feature_importances_
    feature_ranking = pd.DataFrame({
        'Stat': feature_names,
        'Importance': importances
    })
    
    # Sort them from most important to least important
    feature_ranking = feature_ranking.sort_values(by='Importance', ascending=False).reset_index(drop=True)
    
    # Print the Top 10 heavyweights
    print(feature_ranking.head(10))
    
    return feature_ranking

def simulate_match(home_team, away_team, model, feature_columns):
    print(f"\n--- ⚽ SIMULATING: {home_team} (Home) vs {away_team} (Away) ---")
    db_url = "postgresql+psycopg2://postgres:Student%40123@127.0.0.1:1234/ucl_predictor"
    engine = create_engine(db_url)

    # A quick SQL query to dynamically build the exact match row for these two teams
    query = f"""
    SELECT 
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

    FROM raw_team_power htp
    JOIN positional_power hpp ON htp.team_name = hpp.team_name
    CROSS JOIN raw_team_power atp
    JOIN positional_power app ON atp.team_name = app.team_name
    WHERE htp.team_name = '{home_team}' AND atp.team_name = '{away_team}';
    """
    
    match_data = pd.read_sql(query, engine)
    
    if match_data.empty:
        print("❌ Error: One of those teams isn't in the database. Check your spelling!")
        return

    # Guarantee the columns are in the exact same order the model studied
    match_data = match_data[feature_columns]

    # Predict the outcome and grab the confidence probabilities
    prediction = model.predict(match_data)[0]
    probabilities = model.predict_proba(match_data)[0]

    print(f"🏆 Predicted Winner: {prediction}")
    print("📊 Tactical Confidence:")
    for cls, prob in zip(model.classes_, probabilities):
        print(f"   - {cls}: {prob * 100:.1f}%")

if __name__ == "__main__":
    # 1. Train the model
    trained_model, trained_features = train_model()
    
    # 2. Check the algorithm's brain
    check_feature_importance(trained_model, trained_features)
    
    # 3. THE ULTIMATE TEST
    # You can change these names to ANY two teams in your Top 5 database!
    simulate_match('Barcelona', 'Newcastle United', trained_model, trained_features)
