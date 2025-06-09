import requests
from datetime import datetime
import subprocess

# ✅ Correct API that includes your player
API_URL = "https://api.the-finals-leaderboard.com/v1/leaderboard/s6/crossplay?name=TTV-Impieux%234861"
PLAYER = "ttv-impieux#4861"  # lowercase match
FILE_PATH = "docs/latest_rank.txt"

def get_rank_score():
    try:
        resp = requests.get(API_URL)
        data = resp.json()

        # Expected format: { "entries": [ { "name": ..., "rank_score": ... }, ... ] }
        if isinstance(data, dict) and "entries" in data:
            for entry in data["entries"]:
                if entry.get("name", "").lower() == PLAYER:
                    return entry.get("rank_score")
    except Exception as e:
        print("Error:", e)
    return None

def log_and_push_score():
    score = get_rank_score()
    if score:
        with open(FILE_PATH, "w") as f:
            f.write(str(score))
        print("Score updated:", score)

        subprocess.run(["git", "add", FILE_PATH])
        subprocess.run(["git", "commit", "-m", f"Update rank score"])
        subprocess.run(["git", "push"])
    else:
        print("Score not found.")

if __name__ == "__main__":
    log_and_push_score()
