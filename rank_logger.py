import requests
from datetime import datetime
import subprocess

API_URL = "https://api.the-finals-leaderboard.com/v1/leaderboard/s6/crossplay?name=TTV-Impieux%234861".replace("#", "%23")
FILE_PATH = "docs/latest_rank.txt"

def get_rank_score():
    try:
        resp = requests.get(API_URL)
        data = resp.json()

        if "data" in data and isinstance(data["data"], list) and data["data"]:
            return data["data"][0].get("rankScore")
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

