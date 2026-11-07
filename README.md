# 🏏 Cricket Data Analysis & Match Prediction System

## 📌 Project Overview

The Cricket Data Analysis & Match Prediction System is a Data Science project developed using Python and Machine Learning.

The project analyzes international T20 cricket matches from 2005 to 2025. It explores team performance, match venues, and toss results. It also uses a Random Forest machine learning model to estimate possible match winners.

## 🎯 Project Objectives

- Analyze international T20 cricket match data.
- Perform data cleaning and preprocessing.
- Explore team performance and venue statistics.
- Analyze the impact of toss results.
- Build a Machine Learning model for match winner prediction.
- Develop an interactive web dashboard using Streamlit.

## 📂 Dataset

- Dataset: International T20 Cricket Dataset (2005–2025)
- Total valid matches: 4,656
- Data format: CSV and YAML

## 🛠️ Technologies & Libraries

- Python
- Pandas
- Matplotlib
- Seaborn
- Scikit-learn
- Streamlit
- Joblib
- PyYAML

## 🤖 Machine Learning Model

**Algorithm:** Random Forest Classifier

**Input Features:**
- Team 1
- Team 2
- Venue
- Toss Winner
- Toss Decision

**Data Split:**
- Training: 80%
- Testing: 20%

**Model Accuracy: 61.48%**

OneHotEncoder is used for categorical data preprocessing.

## 📊 Data Analysis

The project includes visualizations for:

1. Top 10 teams by match wins.
2. Top 10 cricket venues.
3. Toss winner analysis.
4. Confusion matrix.

## 🌐 Web Application

The interactive Streamlit dashboard provides:

- Dataset overview.
- Cricket statistics and visualizations.
- Match winner prediction.
- Machine Learning model performance.

## ▶️ How to Run the Project

**1. Clone the repository**

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

**2. Open the project folder**

```bash
cd Cricket_Data_Science
```

**3. Install required libraries**

```bash
pip install -r requirements.txt
```

**4. Run the Streamlit application**

```bash
python -m streamlit run app.py
```

## ⚠️ Limitations

- The dataset contains an imbalanced number of matches across teams.
- Some teams have limited historical records.
- The model uses only five input features.
- Predictions are estimates and are not guaranteed match results.

## 🔮 Future Improvements

- Include recent team performance.
- Add head-to-head statistics.
- Improve model evaluation.
- Add more match-related features.
- Improve prediction accuracy.

## 👨‍🎓 Academic Project

**Project Name:** Cricket Data Analysis & Match Prediction System

**Degree:** BS Information Technology

**Course:** Data Science

**Developed using:** Python, Machine Learning and Streamlit
