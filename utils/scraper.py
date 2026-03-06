import os
import requests

FLIPP_TOKEN = os.environ.get("FLIPP_TOKEN", "7749fa974b9869e8f57606ac9477decf")
BASE_URL = "https://dam.flippenterprise.net/flyerkit"


def scrape_safeway_deals():
    try:
        # Step 1: get merchant info and find current publication ID
        merchant_resp = requests.get(
            f"{BASE_URL}/merchant/safeway",
            params={"locale": "en", "access_token": FLIPP_TOKEN},
            timeout=10,
        )
        merchant_resp.raise_for_status()
        merchant_data = merchant_resp.json()

        # Publication ID may be nested differently depending on response shape
        pub_id = None
        if isinstance(merchant_data, dict):
            pub_id = (
                merchant_data.get("current_publication_id")
                or merchant_data.get("publication_id")
                or (merchant_data.get("publications") or [{}])[0].get("id")
            )
        elif isinstance(merchant_data, list) and merchant_data:
            pub_id = merchant_data[0].get("id")

        if not pub_id:
            print("Scraper: could not find publication ID in merchant response")
            print("Response:", merchant_data)
            return []

        # Step 2: fetch deal items for that publication
        items_resp = requests.get(
            f"{BASE_URL}/publication/{pub_id}/flyer_items",
            params={"locale": "en", "access_token": FLIPP_TOKEN},
            timeout=10,
        )
        items_resp.raise_for_status()
        items = items_resp.json()

        deals = []
        for item in items:
            name = item.get("name") or item.get("name_identifier", "")
            price = item.get("sale_story") or item.get("current_price", "")
            if name:
                deals.append({
                    "item": name.strip().lower(),
                    "price": str(price).strip(),
                })

        return deals

    except Exception as e:
        print(f"Scraper error: {e}")
        return []
