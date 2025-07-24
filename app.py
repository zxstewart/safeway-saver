from flask import Flask, render_template, request
from utils.scraper import scrape_safeway_deals
from models import create_tables, add_deals, add_purchases, get_all_deals, get_recommendations

app = Flask(__name__)
create_tables()

@app.route("/", methods=["GET", "POST"])
def index():
    deals = scrape_safeway_deals()
    add_deals(deals)

    user_list = []
    matched_items = []
    recommendations = []

    if request.method == "POST":
        raw_input = request.form["shopping_list"]
        user_list = [item.strip().lower() for item in raw_input.split("\n") if item.strip()]

        add_purchases(user_list)

        all_deals = get_all_deals()
        matched_items = [d for d in all_deals if d["item"] in user_list]
        recommendations = get_recommendations()

    return render_template("index.html",
                           shopping_list=user_list,
                           matched_items=matched_items,
                           recommendations=recommendations)

if __name__ == "__main__":
    app.run(debug=True)
