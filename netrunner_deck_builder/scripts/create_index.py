import json
import numpy as np
import faiss

DATA_DIR = "netrunner_deck_builder/data/"

EMBEDDING_FILES = {
    "corp": f"{DATA_DIR}corp-card-embeddings.json",
    "runner": f"{DATA_DIR}runner-card-embeddings.json"
}

INDEX_FILES = {
    "corp": f"{DATA_DIR}corp-card-embeddings.faiss",
    "runner": f"{DATA_DIR}runner-card-embeddings.faiss"
}

CODE_FILES = {
    "corp": f"{DATA_DIR}corp-card-codes.json",
    "runner": f"{DATA_DIR}runner-card-codes.json"
}

def build_index(embedding_json_path, index_path, codes_path):
    with open(embedding_json_path, "r") as f:
        data = json.load(f)
    codes = [item[0] for item in data]
    embeddings = np.array([item[1] for item in data], dtype=np.float32)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)
    faiss.write_index(index, index_path)
    with open(codes_path, "w") as f:
        json.dump(codes, f, indent=2)

if __name__ == "__main__":
    for key in EMBEDDING_FILES:
        build_index(EMBEDDING_FILES[key], INDEX_FILES[key], CODE_FILES[key])
