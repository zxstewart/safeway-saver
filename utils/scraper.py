import json

def scrape_safeway_deals():
    # Placeholder data; replace with real scraping logic
    deals = [
        {"item": "milk", "price": "2 for $5"},
        {"item": "eggs", "price": "$1.99"},
        {"item": "chicken thighs", "price": "$3.49/lb"}
    ]
    with open("data/safeway_deals.json", "w") as f:
        json.dump(deals, f, indent=2)
    return deals
