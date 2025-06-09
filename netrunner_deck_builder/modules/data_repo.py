import json
import os
import faiss
import numpy as np

DATA_DIR = "netrunner_deck_builder/data/"

class DataRepo:
    def __init__(self, data_dir=DATA_DIR):
        pass

    def _load_json(self, filename):
        path = os.path.join(DATA_DIR, filename)
        with open(path, "r") as f:
            return json.load(f)
    
    def get_identity_card_by_code(self, code):
        identity_cards = self._load_json("identity-cards.json")
        return next((card for card in identity_cards if card.get("code") == code), None)
    
    def get_identity_embedding_by_code(self, code):
        embedding_file = "identity-card-embeddings.json"
        embeddings = self._load_json(embedding_file)
        for item in embeddings:
            if item[0] == code:
                return item[1]
        return None
    
    def get_cards_by_filter(self, side_code, filter_func):
        if side_code not in ["runner", "corp"]:
            raise ValueError("side_code must be 'runner' or 'corp'")
        file = "runner" if side_code == "runner" else "corp"
        cards_file = f"{file}-cards.json"
        cards = self._load_json(cards_file)
        return [card for card in cards if filter_func(card)]
    
    def get_top_n_cards_by_embedding(self, embedding, cards, n):
        # Build an in-memory FAISS index from the provided cards only
        embeddings = []
        codes = []
        for card in cards:
            code = card["code"]
            # Find the embedding for this card
            side_code = card["side_code"]
            emb_file = f"{side_code}-card-embeddings.json"
            all_embeddings = self._load_json(emb_file)
            emb_dict = {item[0]: item[1] for item in all_embeddings}
            if code in emb_dict:
                embeddings.append(emb_dict[code])
                codes.append(code)
        if not embeddings:
            return []
        embeddings_np = np.array(embeddings, dtype=np.float32)
        index = faiss.IndexFlatL2(embeddings_np.shape[1])
        index.add(embeddings_np)
        embedding_np = np.array(embedding, dtype=np.float32).reshape(1, -1)
        D, I = index.search(embedding_np, min(n, len(codes)))
        top_codes = [codes[i] for i in I[0]]
        code_to_card = {card["code"]: card for card in cards}
        top_cards = [code_to_card[code] for code in top_codes if code in code_to_card]
        return top_cards
    

# Example usage:
# repo = DataRepo()
# corp_cards = repo.get_corp_cards()
# runner_embeddings = repo.get_embeddings("runner")
