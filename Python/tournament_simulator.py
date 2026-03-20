import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestClassifier

# ============================================================
# 1. CORE SETUP AND MODEL TRAINING
# ============================================================
def load_and_train_model():
    print("⚙️  Booting up the UCL Tournament Engine...")
    print("⚙️  Training Random Forest on full match dataset...")
    print("=" * 60)

    db_url = "postgresql+psycopg2://postgres:Student%40123@127.0.0.1:1234/ucl_predictor"
    engine = create_engine(db_url)

    df = pd.read_sql("SELECT * FROM final_ml_dataset;", engine).dropna()

    y = df['actual_result']
    X = df.drop(columns=['home_team', 'away_team', 'actual_result',
                          'actual_home_goals', 'actual_away_goals', 'result_id'])

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    print("✅  Model trained successfully.\n")
    return model, X.columns, engine


# ============================================================
# 2. MATCH FEATURE EXTRACTOR
# ============================================================
def get_match_features(home_team, away_team, engine, feature_columns):
    query = f"""
    SELECT
        htp.total_goals          AS h_season_goals,
        htp.total_shots          AS h_season_shots,
        htp.avg_plus_minus       AS h_squad_plus_minus,
        hpp.fw_avg_goals         AS h_fw_rating,
        hpp.fw_avg_shots         AS h_fw_shots,
        hpp.mf_avg_assists       AS h_mf_creative_score,
        hpp.mf_avg_crosses       AS h_mf_control_score,
        hpp.df_avg_tackles_won   AS h_df_tackles,
        hpp.df_avg_interceptions AS h_df_solidity,

        atp.total_goals          AS a_season_goals,
        atp.total_shots          AS a_season_shots,
        atp.avg_plus_minus       AS a_squad_plus_minus,
        app.fw_avg_goals         AS a_fw_rating,
        app.fw_avg_shots         AS a_fw_shots,
        app.mf_avg_assists       AS a_mf_creative_score,
        app.mf_avg_crosses       AS a_mf_control_score,
        app.df_avg_tackles_won   AS a_df_tackles,
        app.df_avg_interceptions AS a_df_solidity

    FROM raw_team_power htp
    JOIN positional_power hpp ON htp.team_name = hpp.team_name
    CROSS JOIN raw_team_power atp
    JOIN positional_power app ON atp.team_name = app.team_name
    WHERE htp.team_name = '{home_team}'
      AND atp.team_name = '{away_team}';
    """
    try:
        match_data = pd.read_sql(query, engine)
        if match_data.empty:
            return None
        return match_data[feature_columns]
    except Exception as e:
        print(f"   ❌ Data extraction failed: {e}")
        return None


# ============================================================
# 3. HOME ADVANTAGE INJECTOR
# Applies realistic home and away modifiers to raw probabilities
# so Leg 1 and Leg 2 produce genuinely different results.
#
# Football analytics research shows home teams win ~46% of
# top-flight matches vs ~30% for away sides. We encode this
# by boosting the home team probability by a scaling factor
# and compressing the away team's probability accordingly.
# ============================================================
HOME_BOOST  = 1.18   # Home team gets an 18% probability boost
AWAY_DAMPEN = 0.82   # Away team's probability is dampened by 18%

# Competitiveness floor — prevents any team from dropping
# below this probability regardless of quality gap.
# Set to 0.15 so even Galatasaray vs Bayern shows 15% minimum.
FLOOR = 0.15

def apply_home_advantage(raw_home_prob, raw_away_prob):
    boosted_home = raw_home_prob * HOME_BOOST
    dampened_away = raw_away_prob * AWAY_DAMPEN

    # Re-normalise so they sum to 1.0
    total = boosted_home + dampened_away
    home_adj = boosted_home / total
    away_adj = dampened_away / total

    # Apply competitiveness floor — no team below 15%
    if home_adj < FLOOR:
        home_adj = FLOOR
        away_adj = 1 - FLOOR
    if away_adj < FLOOR:
        away_adj = FLOOR
        home_adj = 1 - FLOOR

    return round(home_adj * 100, 1), round(away_adj * 100, 1)


# ============================================================
# 4. TWO-LEGGED AGGREGATE LOGIC
# Leg 1: team_1 at home (team_1 gets home boost)
# Leg 2: team_2 at home (team_2 gets home boost)
# This means each leg produces DIFFERENT percentages,
# creating genuine tension across the two matches.
# ============================================================
def simulate_two_legs(team_1, team_2, model, features, engine,
                      match_num, round_name):
    classes = list(model.classes_)

    print(f"  Match {match_num}")
    print(f"  {team_1}  vs  {team_2}")
    print(f"  {'─' * 44}")

    if team_1 not in classes or team_2 not in classes:
        print(f"  ⚠️  One or both teams not found in training data.\n")
        return team_1

    idx_1 = classes.index(team_1)
    idx_2 = classes.index(team_2)

    # ── Leg 1: team_1 is at home ──────────────────────────
    leg1_features = get_match_features(team_1, team_2, engine, features)
    leg1_probs    = model.predict_proba(leg1_features)[0]

    raw_home_1 = leg1_probs[idx_1]   # team_1 raw home probability
    raw_away_2 = leg1_probs[idx_2]   # team_2 raw away probability

    leg1_team1_pct, leg1_team2_pct = apply_home_advantage(
        raw_home_1, raw_away_2
    )

    # ── Leg 2: team_2 is at home ──────────────────────────
    leg2_features = get_match_features(team_2, team_1, engine, features)
    leg2_probs    = model.predict_proba(leg2_features)[0]

    raw_home_2 = leg2_probs[idx_2]   # team_2 raw home probability
    raw_away_1 = leg2_probs[idx_1]   # team_1 raw away probability

    leg2_team2_pct, leg2_team1_pct = apply_home_advantage(
        raw_home_2, raw_away_1
    )

    # ── Aggregate: sum adjusted probabilities across both legs
    aggregate_1 = leg1_team1_pct + leg2_team1_pct
    aggregate_2 = leg1_team2_pct + leg2_team2_pct

    # Normalise aggregate to percentage
    total_agg   = aggregate_1 + aggregate_2
    agg_pct_1   = round(aggregate_1 / total_agg * 100, 1)
    agg_pct_2   = round(100 - agg_pct_1, 1)

    # ── Print leg-by-leg breakdown ─────────────────────────
    print(f"  Leg 1  ({team_1} at home)")
    print(f"    {team_1:<30} {leg1_team1_pct}%")
    print(f"    {team_2:<30} {leg1_team2_pct}%")
    print()
    print(f"  Leg 2  ({team_2} at home)")
    print(f"    {team_2:<30} {leg2_team2_pct}%")
    print(f"    {team_1:<30} {leg2_team1_pct}%")
    print()
    print(f"  Aggregate over 180 minutes:")
    print(f"    {team_1:<30} {agg_pct_1}%")
    print(f"    {team_2:<30} {agg_pct_2}%")
    print()

    if aggregate_1 > aggregate_2:
        winner = team_1
        loser  = team_2
        w_pct  = agg_pct_1
        l_pct  = agg_pct_2
    else:
        winner = team_2
        loser  = team_1
        w_pct  = agg_pct_2
        l_pct  = agg_pct_1

    next_round_map = {
        "Round of 16"   : "Quarter Finals",
        "Quarter Finals" : "Semi Finals",
        "Semi Finals"    : "the Final",
    }
    next_round = next_round_map.get(round_name, "the next round")

    print(f"  🏅  {winner} wins on aggregate  ({w_pct}% vs {l_pct}%)")
    print(f"  ✅  {winner} progresses to the {next_round}!")
    print()

    return winner


# ============================================================
# 5. NEUTRAL VENUE FINAL
# Neither team gets home advantage — both are visitors.
# We average both home/away permutations to find true strength.
# Competitiveness floor still applies.
# ============================================================
def simulate_final(team_1, team_2, model, features, engine):
    classes = list(model.classes_)
    idx_1   = classes.index(team_1)
    idx_2   = classes.index(team_2)

    var1_features = get_match_features(team_1, team_2, engine, features)
    var2_features = get_match_features(team_2, team_1, engine, features)

    # Average both permutations — no home boost applied
    raw_1 = (
        model.predict_proba(var1_features)[0][idx_1]
      + model.predict_proba(var2_features)[0][idx_1]
    ) / 2

    raw_2 = (
        model.predict_proba(var1_features)[0][idx_2]
      + model.predict_proba(var2_features)[0][idx_2]
    ) / 2

    # Normalise
    total  = raw_1 + raw_2
    pct_1  = raw_1 / total
    pct_2  = raw_2 / total

    # Apply competitiveness floor for the final too
    if pct_1 < FLOOR:
        pct_1 = FLOOR
        pct_2 = 1 - FLOOR
    if pct_2 < FLOOR:
        pct_2 = FLOOR
        pct_1 = 1 - FLOOR

    pct_1 = round(pct_1 * 100, 1)
    pct_2 = round(100 - pct_1, 1)

    print("=" * 60)
    print("🏟️   THE UEFA CHAMPIONS LEAGUE FINAL")
    print("     Neutral venue · No home advantage")
    print("=" * 60)
    print(f"  {team_1}  vs  {team_2}")
    print(f"  {'─' * 44}")
    print(f"    {team_1:<30} {pct_1}%  win probability")
    print(f"    {team_2:<30} {pct_2}%  win probability")
    print()

    if pct_1 > pct_2:
        champion  = team_1
        runner_up = team_2
        dom       = pct_1
    else:
        champion  = team_2
        runner_up = team_1
        dom       = pct_2

    print("=" * 60)
    print(f"🏆  {champion.upper()} ARE CHAMPIONS OF EUROPE!")
    print(f"    Winning probability : {dom}%")
    print(f"    Runner-up           : {runner_up}")
    print("=" * 60)


# ============================================================
# 6. ROUND RUNNER
# ============================================================
def run_round(teams, model, features, engine, round_name):
    print()
    print("=" * 60)
    print(f"  🔥  {round_name.upper()}")
    print("=" * 60)
    print()

    winners   = []
    match_num = 1

    for i in range(0, len(teams), 2):
        winner = simulate_two_legs(
            teams[i], teams[i + 1],
            model, features, engine,
            match_num, round_name
        )
        winners.append(winner)
        match_num += 1

    print(f"  {'─' * 44}")
    print(f"  {round_name} complete. Teams advancing:")
    for idx, team in enumerate(winners, 1):
        print(f"    {idx}.  {team}")
    print()

    return winners


# ============================================================
# 7. MAIN TOURNAMENT RUNNER
# ============================================================
def run_tournament(matchups, model, features, engine):
    r16_teams = [team for tie in matchups for team in tie]

    quarter_finalists = run_round(
        r16_teams, model, features, engine, "Round of 16"
    )
    semi_finalists = run_round(
        quarter_finalists, model, features, engine, "Quarter Finals"
    )
    finalists = run_round(
        semi_finalists, model, features, engine, "Semi Finals"
    )

    simulate_final(finalists[0], finalists[1], model, features, engine)


# ============================================================
# 8. ENTRY POINT
# ============================================================
if __name__ == "__main__":

    trained_model, feature_cols, db_engine = load_and_train_model()

    round_of_16_draw = [
        ('Chelsea',           'Paris Saint-Germain'),
        ('Liverpool',         'Galatasaray'),
        ('Manchester City',   'Real Madrid'),
        ('Bayern Munich',     'Atalanta'),
        ('Barcelona',         'Newcastle United'),
        ('Tottenham Hotspur', 'Atlético Madrid'),
        ('Sporting CP',       'Bodø/Glimt'),
        ('Arsenal',           'Leverkusen'),
    ]

    run_tournament(round_of_16_draw, trained_model, feature_cols, db_engine)