from modules.data_repo import DataRepo
import json
from openai import OpenAI

IDENTITY_CODE = "30010"
NON_FACTION_CARD_LIMIT = 3

if __name__ == "__main__":
    repo = DataRepo()
    identity_card = repo.get_identity_card_by_code(IDENTITY_CODE)
    identity_embedding = repo.get_identity_embedding_by_code(IDENTITY_CODE)

    faction_cards = repo.get_cards_by_filter(
        side_code=identity_card["side_code"],
        filter_func=lambda card: card["faction_code"] == identity_card["faction_code"]
    )

    non_faction_cards = repo.get_cards_by_filter(
        side_code=identity_card["side_code"],
        filter_func=lambda card: card["faction_code"] != identity_card["faction_code"]
    )

    relevant_non_faction_cards = repo.get_top_n_cards_by_embedding(
        embedding=identity_embedding,
        cards=non_faction_cards,
        n=NON_FACTION_CARD_LIMIT
    )

    cards_to_consider = faction_cards + relevant_non_faction_cards

    stripped_cards = []
    for card in cards_to_consider:
        card_name = card.get("stripped_title")
        card_text = card.get("stripped_text")
        stripped_cards.append({
            "name": card_name,
            "text": card_text
        })

    cards_input = json.dumps(stripped_cards)

    # Prepare prompt for GPT-3.5-turbo-instruct
    prompt = f"""
You are a Netrunner deckbuilding assistant. Given the following identity card and a list of cards, build a legal and fun deck for the identity. Output the deck as a list of card codes and quantities, and explain your choices.

Identity card:
{json.dumps(identity_card, indent=2)}

Cards to consider:
{json.dumps(cards_to_consider, indent=2)}
"""

    client = OpenAI()
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1024,
    )
    print(response.choices[0].text)


