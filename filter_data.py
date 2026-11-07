
import pandas as pd
from pathlib import Path
import shutil

# Load existing CSV
file_path = Path("data/matches.csv")
df = pd.read_csv(file_path)

print("Original Matches:", len(df))

# Count each team's total appearances
team_counts = pd.concat([
    df["team1"],
    df["team2"]
]).value_counts()

# Select Top 30 teams
top_30 = team_counts.head(30).index.tolist()

print("\nTOP 30 TEAMS:")
for i, team in enumerate(top_30, 1):
    print(f"{i}. {team} - {team_counts[team]} matches")

# Keep matches where both teams are in Top 30
filtered_df = df[
    df["team1"].isin(top_30) &
    df["team2"].isin(top_30)
].copy()

# Create backup before replacing original CSV
backup_path = Path("data/matches_backup.csv")
shutil.copy2(file_path, backup_path)

# Save filtered data
filtered_df.to_csv(file_path, index=False)

print("\nFiltering Completed!")
print("Original Matches:", len(df))
print("Filtered Matches:", len(filtered_df))
print("Removed Matches:", len(df) - len(filtered_df))
print("Saved to:", file_path)
print("Backup:", backup_path)
