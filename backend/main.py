from datetime import datetime
import pandas as pd
import joblib
from pydantic import BaseModel
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Load trained Machine Learning model
model = joblib.load("models/cricket_model.pkl")

app = FastAPI(title="Cricket Analytics API")

# Frontend configuration
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Database configuration

import os
from pathlib import Path
from dotenv import load_dotenv

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load Neon environment variables locally
load_dotenv(BASE_DIR / ".env.neon")

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASE_URL = DATABASE_URL.replace(
        "postgresql://", "postgresql+psycopg://", 1
    )
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )
else:
    DATABASE_URL = f"sqlite:///{BASE_DIR / 'cricket.db'}"
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()


# Match database table
class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    team1 = Column(String)
    team2 = Column(String)
    venue = Column(String)
    toss_winner = Column(String)
    toss_decision = Column(String)
    winner = Column(String)

# Prediction history database table
class PredictionHistory(Base):
    __tablename__ = "prediction_history"

    id = Column(Integer, primary_key=True, index=True)
    team1 = Column(String)
    team2 = Column(String)
    venue = Column(String)
    toss_winner = Column(String)
    toss_decision = Column(String)
    predicted_winner = Column(String)
    created_at = Column(String, default=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

Base.metadata.create_all(bind=engine)


# Website homepage
@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)



# Get options for dropdowns
@app.get("/api/db-check")
def db_check():
    db = SessionLocal()
    try:
        return {
            "database": engine.url.database,
            "host": engine.url.host,
            "total_matches": db.query(Match).count()
        }
    except Exception as e:
        return {"error": str(e)}
    finally:
        db.close()
@app.get("/api/options")
def get_options():
    db = SessionLocal()

    try:
        team1_list = db.query(Match.team1).distinct().all()
        team2_list = db.query(Match.team2).distinct().all()
        venue_list = db.query(Match.venue).distinct().all()

        teams = set()

        for team in team1_list + team2_list:
            if team[0]:
                teams.add(team[0])

        venues = sorted({
            venue[0]
            for venue in venue_list
            if venue[0]
        })

        return {
            "teams": sorted(teams),
            "venues": venues,
            "total_matches": db.query(Match).count()
        }

    finally:
        db.close()


# Get matches
@app.get("/api/matches")
def get_matches():
    db = SessionLocal()

    try:
        matches = db.query(Match).limit(10).all()

        return [
            {
                "id": match.id,
                "team1": match.team1,
                "team2": match.team2,
                "venue": match.venue,
                "winner": match.winner
            }
            for match in matches
        ]

    finally:
        db.close()


# Prediction request format


       
class PredictionInput(BaseModel):
    team1: str
    team2: str
    venue: str
    toss_winner: str
    toss_decision: str


# Predict match winner
@app.post("/api/predict")
def predict_match(data: PredictionInput):

    if data.team1 == data.team2:
        return {"error": "Please select two different teams."}

    if data.toss_winner not in [data.team1, data.team2]:
        return {"error": "Toss winner must be one of the selected teams."}

    input_data = pd.DataFrame([{
    "team1": data.team1,
    "team2": data.team2,
    "venue": data.venue,
    "toss_winner": data.toss_winner,
    "toss_decision": data.toss_decision
    }])

    prediction = model.predict(input_data)[0]
    db = SessionLocal()
    try:
        history = PredictionHistory(
            team1=data.team1,
            team2=data.team2,
            venue=data.venue,
            toss_winner=data.toss_winner,
            toss_decision=data.toss_decision,
            predicted_winner=str(prediction)
        )

        db.add(history)
        db.commit()

    finally:
        db.close()

    return {
        "predicted_winner": str(prediction),
        "message": "Prediction generated successfully."
    }

        # Get prediction history
@app.get("/api/history")
def get_prediction_history():
    db = SessionLocal()

    try:
        history = (
            db.query(PredictionHistory)
            .order_by(PredictionHistory.id.desc())
            .all()
        )

        return [
            {
                "id": item.id,
                "team1": item.team1,
                "team2": item.team2,
                "venue": item.venue,
                "toss_winner": item.toss_winner,
                "toss_decision": item.toss_decision,
                "predicted_winner": item.predicted_winner,
                "created_at": item.created_at
            }
            for item in history
        ]

    finally:
        db.close()
