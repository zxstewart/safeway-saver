from flask import Flask, render_template, request
from utils.scraper import scrape_safeway_deals
from utils.recommender import update_history, recommend_from_history
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    deals = scrape_safeway_deals()

    recommendations = []
    matched_items = []
    user_list = []

    if request.method == "POST":
        raw_input = request.form["shopping_list"]
        user_list = [item.strip().lower() for item in raw_input.split("\n") if item.strip()]
        update_history(user_list)

        with open("data/safeway_deals.json") as f:
            deals = json.load(f)
        matched_items = [d for d in deals if d["item"] in user_list]
        recommendations = recommend_from_history(deals)

    return render_template("index.html",
                           shopping_list=user_list,
                           matched_items=matched_items,
                           recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
