import json
from openai import OpenAI

client = OpenAI()

DATA_DIR = "netrunner_deck_builder/data/"

CARD_FILES = {
    "corp": f"{DATA_DIR}corp-cards.json",
    "runner": f"{DATA_DIR}runner-cards.json",
    "identity": f"{DATA_DIR}identity-cards.json"
}

OUTPUT_FILES = {
    "corp": f"{DATA_DIR}corp-card-embeddings.json",
    "runner": f"{DATA_DIR}runner-card-embeddings.json",
    "identity": f"{DATA_DIR}identity-card-embeddings.json"
}

def embed_cards(card_file, output_file):
    with open(card_file, "r") as f:
        cards = json.load(f)
    embeddings = []
    for card in cards:
        card_code = card.get("code")
        text = card.get("stripped_text")
        if not text or not card_code:
            continue
        response = client.embeddings.create(
            input=text,
            model="text-embedding-ada-002"
        )
        embedding = response.data[0].embedding
        embeddings.append((card_code, embedding))
    with open(output_file, "w") as f:
        json.dump(embeddings, f)

if __name__ == "__main__":
    for key in CARD_FILES:
        embed_cards(CARD_FILES[key], OUTPUT_FILES[key])
