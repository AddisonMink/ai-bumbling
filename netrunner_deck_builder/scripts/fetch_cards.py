"""Fetch Netrunner cards from the NetrunnerDB API and save them to a JSON file."""
import requests
import json


PACK_CODES = ["sg", "elev"] # System Gateway and Elevation pack codes
URL = "https://netrunnerdb.com/api/2.0/public/cards"
OUTPUT_DIR = "netrunner_deck_builder/data/"

response = requests.get(URL)

if not response.ok:
    raise Exception(f"Failed to fetch cards: {response.status_code} {response.reason}")

cards = response.json().get("data", [])
filtered_cards = [card for card in cards if card.get("pack_code") in PACK_CODES]

for card in filtered_cards:
    card.pop("title", None)
    card.pop("text", None)
    card.pop("pack_code", None)
    card.pop("position", None)
    card.pop("illustrator", None)
    card.pop("flavor_text", None)
    card.pop("keywords", None)
    card.pop("flavor", None)
    

identity_cards = [card for card in filtered_cards if card.get("type_code") == "identity"]
runner_cards = [card for card in filtered_cards if card.get("side_code") == "runner" and card.get("type_code") != "identity"]
corp_cards = [card for card in filtered_cards if card.get("side_code") == "corp" and card.get("type_code") != "identity"]

with open(f"{OUTPUT_DIR}identity-cards.json", "w") as f:
    json.dump(identity_cards, f, indent=2)
with open(f"{OUTPUT_DIR}runner-cards.json", "w") as f:
    json.dump(runner_cards, f, indent=2)
with open(f"{OUTPUT_DIR}corp-cards.json", "w") as f:
    json.dump(corp_cards, f, indent=2)
