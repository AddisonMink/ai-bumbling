import requests
import json
from openai import OpenAI
client = OpenAI()

INITIAL_PROMPT = """
# Netrunner Deck Construction
This is an example of a valid Netrunner deck using Null Signal's
System Gateway set. We will making a runner deck using Zahya.

Here is a list of cards in the deck:
```
"""

ZAYHA_JSON = """
{
      "base_link": 0,
      "code": "30010",
      "deck_limit": 1,
      "faction_code": "criminal",
      "faction_cost": 0,
      "flavor": "I obtain your desire.",
      "illustrator": "Benjamin Giletti",
      "influence_limit": 15,
      "keywords": "Cyborg",
      "minimum_deck_size": 40,
      "pack_code": "sg",
      "position": 10,
      "quantity": 1,
      "side_code": "runner",
      "stripped_text": "Once per turn -> When a run on HQ or R&D ends, you may gain 1[credit] for each time you accessed a card during that run.",
      "stripped_title": "Zahya Sadeghi: Versatile Smuggler",
      "text": "Once per turn \u2192 When a run on HQ or R&D ends, you may gain 1[credit] for each time you accessed a card during that run.",
      "title": "Zahya Sadeghi: Versatile Smuggler",
      "type_code": "identity",
      "uniqueness": false
    }
"""

def main():
    cards = load_cards()
    print(f"Loaded {len(cards)} cards from System Gateway.")
    prompt = assemble_prompt(json.dumps(cards, indent=2))
    result = query_api(prompt)
    print()
    print(result.strip())
    
def assemble_prompt(cards):
    return f"""
    # Drafting a Netrunner Deck
    This is an example of a valid Netrunner deck using Null Signal's
    System Gateway set. We will making a runner deck using Zahya.

    Her is the JSON data for Zayha:
    ```json
    {ZAYHA_JSON}
    ```
    Here are the cards available to us:
    ```json
    {cards}
    ```
    
    Next, we will think about what we want to accomplish with a Zahya deck.
    Then we will conclude with a deck list in the following format:
    ```
    card_name xquantity
    ```
    Finally, we will provide a brief explanation of how to play the deck and its strategy.
    """


def load_cards():
    with open('system-gateway-cards.json', 'r') as file:
        data = json.load(file)
        filtered_cards = [
            card for card in data
            if (
                card['side_code'] == 'runner'
                and card['type_code'] != 'identity'
                and (card['faction_code'] == 'criminal' or card['faction_code'] == 'neutral-runner')
            )
        ]
        return filtered_cards


def query_api(prompt):
    response = client.completions.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1.0,
        max_tokens=1028,
    )

    if not response.choices or len(response.choices) == 0:
        raise ValueError("No response from the model.")

    return response.choices[0].text

main()