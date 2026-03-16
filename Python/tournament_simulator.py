import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier

# --- 1. CORE SETUP AND MODEL TRAINING ---
def load_and_train_model():
    print("⚙️ Booting up the Tournament Engine and training the Random Forest...")
    db_url = "postgresql+psycopg2://postgres:Student%40123@127.0.0.1:1234/ucl_predictor"
    engine = create_engine(db_url)
    
    # Pull the exact same master dataset
    df = pd.read_sql("SELECT * FROM final_ml_dataset;", engine).dropna()
    y = df['winning_team']
    X = df.drop(columns=['home_team', 'away_team', 'winning_team'])
    
    # Train the model on the FULL dataset for maximum tournament accuracy
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    return model, X.columns, engine

# --- 2. MATCH FEATURE EXTRACTOR ---
def get_match_features(home_team, away_team, engine, feature_columns):
    # This dynamically builds the flat table for ANY two teams you give it
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
    try:
        match_data = pd.read_sql(query, engine)
        if match_data.empty:
            return None
        return match_data[feature_columns]
    except:
        return None

# --- 3. TWO-LEGGED AGGREGATE LOGIC ---
def simulate_two_legs(team_1, team_2, model, features, engine):
    classes = list(model.classes_)
    
    # Check if teams are in the model's brain to avoid crashing
    if team_1 not in classes or team_2 not in classes:
        print(f"⚠️ Error: {team_1} or {team_2} not found in training data.")
        return team_1 # Default fallback
        
    idx_1 = classes.index(team_1)
    idx_2 = classes.index(team_2)

    # Leg 1: Team 1 is Home
    leg1_features = get_match_features(team_1, team_2, engine, features)
    leg1_probs = model.predict_proba(leg1_features)[0]
    
    # Leg 2: Team 2 is Home
    leg2_features = get_match_features(team_2, team_1, engine, features)
    leg2_probs = model.predict_proba(leg2_features)[0]

    # Combine tactical dominance across 180 minutes
    total_prob_team_1 = leg1_probs[idx_1] + leg2_probs[idx_1]
    total_prob_team_2 = leg1_probs[idx_2] + leg2_probs[idx_2]

    if total_prob_team_1 > total_prob_team_2:
        print(f"   ⚔️ {team_1} ({total_prob_team_1:.2f}) defeats {team_2} ({total_prob_team_2:.2f}) on aggregate.")
        return team_1
    else:
        print(f"   ⚔️ {team_2} ({total_prob_team_2:.2f}) defeats {team_1} ({total_prob_team_1:.2f}) on aggregate.")
        return team_2

# --- 4. NEUTRAL FINAL LOGIC ---
def simulate_final(team_1, team_2, model, features, engine):
    classes = list(model.classes_)
    idx_1 = classes.index(team_1)
    idx_2 = classes.index(team_2)

    # Simulate both variations to completely remove Home-Field advantage
    var1_features = get_match_features(team_1, team_2, engine, features)
    var2_features = get_match_features(team_2, team_1, engine, features)

    neutral_prob_1 = (model.predict_proba(var1_features)[0][idx_1] + model.predict_proba(var2_features)[0][idx_1]) / 2
    neutral_prob_2 = (model.predict_proba(var1_features)[0][idx_2] + model.predict_proba(var2_features)[0][idx_2]) / 2

    print(f"\n🏟️ THE CHAMPIONS LEAGUE FINAL 🏟️")
    print(f"   {team_1} vs {team_2}")
    
    if neutral_prob_1 > neutral_prob_2:
        print(f"\n🏆 {team_1.upper()} WINS THE CHAMPIONS LEAGUE! (Dominance: {neutral_prob_1*100:.1f}%)")
    else:
        print(f"\n🏆 {team_2.upper()} WINS THE CHAMPIONS LEAGUE! (Dominance: {neutral_prob_2*100:.1f}%)")

# --- 5. THE TOURNAMENT BRACKET RUNNER ---
def run_tournament(matchups, model, features, engine):
    print("\n" + "="*50)
    print("🔥 COMMENCING ROUND OF 16 🔥")
    print("="*50)
    quarter_finalists = []
    for tie in matchups:
        winner = simulate_two_legs(tie[0], tie[1], model, features, engine)
        quarter_finalists.append(winner)

    print("\n" + "="*50)
    print("🔥 COMMENCING QUARTER-FINALS 🔥")
    print("="*50)
    semi_finalists = []
    # Pair them up consecutively (1v2, 3v4, 5v6, 7v8)
    for i in range(0, 8, 2):
        winner = simulate_two_legs(quarter_finalists[i], quarter_finalists[i+1], model, features, engine)
        semi_finalists.append(winner)

    print("\n" + "="*50)
    print("🔥 COMMENCING SEMI-FINALS 🔥")
    print("="*50)
    finalists = []
    for i in range(0, 4, 2):
        winner = simulate_two_legs(semi_finalists[i], semi_finalists[i+1], model, features, engine)
        finalists.append(winner)

    # The Grand Final
    simulate_final(finalists[0], finalists[1], model, features, engine)


if __name__ == "__main__":
    trained_model, feature_cols, db_engine = load_and_train_model()
    round_of_16_draw = [
        ('Chelsea', 'Paris Saint-Germain'),
        ('Liverpool', 'PROXY_FOR_GALATASARAY'), 
        ('Manchester City', 'Real Madrid'),
        ('Bayern Munich', 'Atalanta'),
        ('Barcelona', 'Newcastle United'),
        ('Tottenham Hotspur', 'Atlético Madrid'),
        ('PROXY_FOR_SPORTING', 'PROXY_FOR_BODO'), 
        ('Arsenal', 'Bayer Leverkusen')
    ]
    
    # Run the simulation!
    run_tournament(round_of_16_draw, trained_model, feature_cols, db_engine)