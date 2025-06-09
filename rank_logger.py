import requests
from datetime import datetime
import subprocess

API_URL = "https://embark-discovery-leaderboard.storage.googleapis.com/leaderboard.json"
PLAYER = "TTV-Impieux#4861"
FILE_PATH = "docs/latest_rank.txt"

def get_rank_score():
    try:
        resp = requests.get(API_URL)
        data = resp.json()
        for entry in data.get("entries", []):
            if entry.get("name") == PLAYER:
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

log_and_push_score()
