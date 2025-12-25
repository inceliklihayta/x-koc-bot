import os
import json
import requests

BASE = "https://api.x.com/2"
STATE_FILE = "state.json"
QUERY = "from:InfoBurclar #koçburcu -is:retweet"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"last_reposted_id": None}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def get_latest_tweet(bearer):
    r = requests.get(
        f"{BASE}/tweets/search/recent",
        params={"query": QUERY, "max_results": 5},
        headers={"Authorization": f"Bearer {bearer}"}
    )
    r.raise_for_status()
    data = r.json().get("data", [])
    return data[0]["id"] if data else None

def repost(user_token, user_id, tweet_id):
    r = requests.post(
        f"{BASE}/users/{user_id}/retweets",
        json={"tweet_id": tweet_id},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    r.raise_for_status()

def main():
    bearer = os.environ["X_BEARER_TOKEN"]
    user_token = os.environ["X_USER_TOKEN"]
    user_id = os.environ["X_MY_USER_ID"]

    state = load_state()
    latest = get_latest_tweet(bearer)

    if not latest or latest == state["last_reposted_id"]:
        print("Yeni post yok")
        return

    repost(user_token, user_id, latest)
    state["last_reposted_id"] = latest
    save_state(state)
    print("Repost edildi")

main()
