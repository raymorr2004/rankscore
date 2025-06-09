import requests
import subprocess

def get_rank_info(api_url):
    try:
        resp = requests.get(api_url)
        data = resp.json()

        if "data" in data and isinstance(data["data"], list) and data["data"]:
            player = data["data"][0]
            score = player.get("rankScore")
            rank = player.get("rank")
            return score, rank
    except Exception as e:
        print("Error:", e)
    return None, None

def log_player(api_url, file_path):
    score, rank = get_rank_info(api_url)
    if score and rank:
        message = f"Rank Score: {score:,} | Rank: #{rank}"
        with open(file_path, "w") as f:
            f.write(message)
        print("Updated:", message)
        subprocess.run(["git", "add", file_path])
        return True
    else:
        print("Rank or score not found.")
        return False

if __name__ == "__main__":
    updated = False

    # First player
    impieux_url = "https://api.the-finals-leaderboard.com/v1/leaderboard/s6/crossplay?name=TTV-Impieux%234861".replace("#", "%23")
    if log_player(impieux_url, "docs/latest_rank.txt"):
        updated = True

    # Second player
    rae_url = "https://api.the-finals-leaderboard.com/v1/leaderboard/s6/crossplay?name=RaeRaeeeTTV%232538".replace("#", "%23")
    if log_player(rae_url, "docs/rae_latest_rank.txt"):
        updated = True

    if updated:
        subprocess.run(["git", "commit", "-m", "Update rank info for both players"])
        subprocess.run(["git", "push"])

