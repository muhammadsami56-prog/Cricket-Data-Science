
import pandas as pd
from backend.main import SessionLocal, Match

# Read cricket dataset
df = pd.read_csv("data/matches.csv")

db = SessionLocal()

try:
    existing_count = db.query(Match).count()

    if existing_count == 0:
        for _, row in df.iterrows():
            match = Match(
                date=str(row["date"]),
                team1=row["team1"],
                team2=row["team2"],
                venue=row["venue"],
                toss_winner=row["toss_winner"],
                toss_decision=row["toss_decision"],
                winner=row["winner"]
            )
            db.add(match)

        db.commit()
        print(f"Successfully imported {len(df)} matches!")

    else:
        print(f"Database already contains {existing_count} matches.")

finally:
    db.close()
