import json

HISTORY_PATH = "data/user_history.json"

def load_user_history():
    try:
        with open(HISTORY_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_user_history(history):
    with open(HISTORY_PATH, "w") as f:
        json.dump(history, f, indent=2)

def update_history(new_items):
    history = load_user_history()
    for item in new_items:
        history[item] = history.get(item, 0) + 1
    save_user_history(history)

def recommend_from_history(deals):
    history = load_user_history()
    recommended = []
    for deal in deals:
        if deal["item"] in history:
            recommended.append(deal)
    return recommended
