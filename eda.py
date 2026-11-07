import matplotlib.pyplot as plt
import pandas as pd

# Load the prepared dataset
df = pd.read_csv("data/matches.csv")

# Display basic dataset information
print("\nCRICKET DATA ANALYSIS")
print("---------------------")

print("\nTotal Matches:", len(df))

# Count wins by each team
team_wins = df["winner"].value_counts()

print("\nTOP 10 TEAMS BY MATCH WINS")
print("--------------------------")
print(team_wins.head(10))

# Find the most frequently used venues
venue_counts = df["venue"].value_counts()

print("\nTOP 10 MATCH VENUES")
print("-------------------")
print(venue_counts.head(10))

# Check how often the toss winner also won
toss_match_wins = (
    df["toss_winner"] == df["winner"]
).sum()

print("\nTOSS WINNER ANALYSIS")
print("--------------------")
print("Toss winner also won:", toss_match_wins)
print(
    "Percentage:",
    round((toss_match_wins / len(df)) * 100, 2),
    "%"
)

# CHART 1: Top 10 Teams by Wins

plt.figure(figsize=(10, 6))

team_wins.head(10).plot(
    kind="bar",
    title="Top 10 Teams by Match Wins"
)

plt.xlabel("Teams")
plt.ylabel("Number of Wins")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig("charts/top_10_teams.png")
plt.show()


# CHART 2: Top 10 Match Venues

plt.figure(figsize=(10, 6))

venue_counts.head(10).plot(
    kind="bar",
    title="Top 10 Cricket Match Venues"
)

plt.xlabel("Venues")
plt.ylabel("Number of Matches")
plt.xticks(rotation=45, ha="right")
plt.tight_layout()

plt.savefig("charts/top_10_venues.png")
plt.show()


# CHART 3: Toss Winner Analysis

toss_results = pd.Series({
    "Toss Winner Also Won": toss_match_wins,
    "Toss Winner Lost": len(df) - toss_match_wins
})

plt.figure(figsize=(7, 7))

toss_results.plot(
    kind="pie",
    autopct="%1.1f%%",
    title="Does Winning the Toss Help?"
)

plt.ylabel("")
plt.tight_layout()

plt.savefig("charts/toss_analysis.png")
plt.show()

print("\nAll charts saved successfully in the charts folder!")