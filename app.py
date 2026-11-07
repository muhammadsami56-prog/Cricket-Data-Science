# Import required libraries
import streamlit as st
import pandas as pd
import joblib

# Page configuration
st.set_page_config(
    page_title="Cricket Data Analysis",
    page_icon="🏏",
    layout="wide"
)

# Load dataset
df = pd.read_csv("data/matches.csv")

# Load trained machine learning model
model = joblib.load("models/cricket_model.pkl")

print("Dataset and model loaded successfully!")

# Main dashboard title
st.title("🏏 Cricket Data Analysis & Match Prediction System")

# Project introduction
st.markdown("""
Welcome to the Cricket Data Analysis and Match Prediction System!

This project uses international T20 cricket data from 2005 to 2025.
Explore match statistics, analyze team performance, and predict
potential match winners using Machine Learning.
""")

# Add a horizontal divider
st.divider()

# Dataset overview
st.header("📊 Dataset Overview")

# Calculate important statistics
total_matches = len(df)
total_teams = pd.unique(
    df[["team1", "team2"]].values.ravel()
).size
total_venues = df["venue"].nunique()

# Display statistics in four columns
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Total Matches", total_matches)

with col2:
    st.metric("Total Teams", total_teams)

with col3:
    st.metric("Total Venues", total_venues)

st.divider()

# Cricket analysis charts
st.header("📈 Cricket Data Analysis")

# First row: Team and venue analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Teams")
    st.image("charts/top_10_teams.png")

with col2:
    st.subheader("Top 10 Venues")
    st.image("charts/top_10_venues.png")

# Second row: Toss analysis
st.subheader("Toss Analysis")
st.image("charts/toss_analysis.png")

st.divider()

# Match prediction section
st.header("🏆 Match Winner Prediction")

st.write("Select match details to predict the possible winner.")

# Get available options
teams = sorted(set(df["team1"]) | set(df["team2"]))
venues = sorted(df["venue"].unique())

# Select match details
col1, col2 = st.columns(2)

with col1:
    team1 = st.selectbox(
        "Select Team 1",
        teams,
        key="team1_select"
    )

    venue = st.selectbox(
        "Select Venue",
        venues,
        key="venue_select"
    )

    toss_decision = st.selectbox(
        "Toss Decision",
        ["bat", "field"],
        key="decision_select"
    )

with col2:
    available_teams = [team for team in teams if team != team1]

    team2 = st.selectbox(
        "Select Team 2",
        available_teams,
        key="team2_select"
    )

    toss_winner = st.selectbox(
        "Toss Winner",
        [team1, team2],
        key="toss_winner_select"
    )

# Prediction button
if st.button("Predict Match Winner"):

    input_data = pd.DataFrame([{
        "team1": team1,
        "team2": team2,
        "venue": venue,
        "toss_winner": toss_winner,
        "toss_decision": toss_decision
    }])

    prediction = model.predict(input_data)[0]

    st.success(f"Predicted Match Winner: {prediction}")

    st.info(
        "This is a machine learning estimate, not a guaranteed result."
    )

st.divider()
            # Model performance section
st.header(" Machine Learning Model Performance")

col1, col2 = st.columns(2)

with col1:
    st.metric("Algorithm", "Random Forest")

with col2:
    st.metric("Model Accuracy", "61.48%")

st.write("""
The Random Forest model was trained using 4,656 international T20
cricket matches.

The dataset was divided into 80% training data and 20% testing data.
OneHotEncoder was used to process categorical features.
""")

st.warning(
    "Prediction results are estimates. Model performance may vary "
    "between teams because the dataset contains an imbalanced number "
    "of matches for different teams."
)

st.divider()

st.caption("Cricket Data Analysis & Match Prediction System | BS Information Technology")