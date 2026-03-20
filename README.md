# 🏆 UEFA Champions League: Tactical Match Predictor
**An End-to-End Data Science Pipeline: PostgreSQL | Python | Power BI | Random Forest**

## 📌 Project Overview
The **UCL Match Predictor** is a sophisticated analytics platform designed to move beyond surface-level football statistics. While traditional models rely on historical win-loss records, this project utilizes **granular positional data**—such as defensive solidity (interceptions and tackles) and midfield creative scores (crosses and assists)—to classify and predict match outcomes.



The result is a two-fold solution:
1.  **A Terminal-based Tournament Engine:** A Random Forest model that simulates an entire UCL bracket from the Round of 16 to the Final.
2.  **An Interactive Power BI Dashboard:** A high-level visual suite for stakeholders to perform dynamic head-to-head analysis.

---

## 🛠️ The Technical Stack
* **Database:** PostgreSQL (Relational schema design, ETL, and complex joins)
* **Programming:** Python 3.13 (Pandas, SQLAlchemy, Scikit-Learn)
* **Machine Learning:** Random Forest Classifier (Supervised Learning)
* **Data Visualization:** Power BI (DAX measures, Dynamic Slicers, UX/UI Design)
* **AI Collaboration:** Leveraged Gemini and Claude for SQL optimization and DAX debugging.

---

## 🚀 The Data Journey (The STAR Method)

### 1. Data Engineering and Processing
* **Situation:** Historical UCL data was scattered across disparate sources and often protected by anti-scraping measures. 
* **Task:** Clean and centralize 5+ seasons of match and player data into a structured relational database.
* **Action:** Engineered a PostgreSQL database with three primary tables: `final_ml_dataset` (historical), `raw_team_power` (macro stats), and `positional_power` (micro stats). 
* **Result:** A clean, normalized database that serves as the "Single Source of Truth" for both the ML model and the Power BI dashboard.

### 2. Machine Learning Implementation
* **Situation:** Standard predictors often fail to account for "tactical fit" between two specific opponents.
* **Task:** Build a classification model to predict match outcomes based on underlying performance metrics.
* **Action:** Developed a **Random Forest Classifier**. I performed specific feature engineering to remove "Data Leakage" (actual goals and result IDs) to ensure the model learned strictly from pre-match tactical indicators.
* **Result:** A robust simulation engine that calculates win probabilities for two-legged aggregate ties and neutral-ground finals.

### 3. Business Intelligence and Visualization
* **Situation:** Stakeholders need a way to interact with the data without writing Python code.
* **Task:** Design an intuitive dashboard that mirrors the prestige of the UEFA Champions League while providing deep analytical insights.
* **Action:** Created a custom Power BI theme. Developed complex **DAX measures** to scale raw stats into a 0 to 100 "Power Index," allowing for a fair comparison between teams across different seasons.
* **Result:** An interactive Head-to-Head tool where users can select any two teams and see a dynamic win probability update in real-time.



---

## 📈 Key Results and Insights
* **Feature Importance:** The model revealed that **Midfield Creative Scores** and **Defensive Solidity (Interceptions)** are stronger predictors of UCL knockout success than raw "Total Goals Scored" during the regular season.
* **Simulated Outcomes:** The tournament engine successfully simulated the bracket, identifying tactical mismatches in high-profile ties.

---

## ⚠️ Challenges and Limitations
* **The Unpredictability Factor:** Football is inherently chaotic. This model assumes historical averages translate to 90-minute performance; it does not currently account for red cards, injuries, or mid-game tactical shifts.
* **Data Latency:** The model relies on post-match aggregated stats. Future iterations could incorporate real-time "Expected Goals" (xG) data for even higher precision.

---

## 📁 Repository Structure
* `/Data`: Raw CSV files and source datasets.
* `/Scripts`: Python files including `tournament_simulator.py` and ETL pipelines.
* `/Database`: SQL schemas and table initialization queries.
* `/Dashboard`: The `.pbix` file for the Power BI Walkthrough.

---

**Contact Information**
* **Name:** [Your Name]
* **Role:** Data Science Student / Analyst
* **LinkedIn:** [Your Link]