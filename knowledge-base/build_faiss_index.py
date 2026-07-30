"""Build FAISS vector index from chunks.json using fastembed.
Lightweight ONNX-based embedding (no PyTorch needed).
"""
import json
import sys
from pathlib import Path

KB_DIR = Path(__file__).parent
CHUNKS_FILE = KB_DIR / "embeddings" / "chunks.json"
INDEX_FILE = KB_DIR / "embeddings" / "faiss_index.bin"
MAPPING_FILE = KB_DIR / "embeddings" / "index_mapping.json"


def main():
    if not CHUNKS_FILE.exists():
        print(f"ERROR: {CHUNKS_FILE} not found. Run ingest.py first.")
        sys.exit(1)

    try:
        import numpy as np
        import faiss
        from fastembed import TextEmbedding
    except ImportError as e:
        print(f"ERROR: Missing dependency: {e}")
        print("pip install fastembed faiss-cpu numpy")
        sys.exit(1)

    print("Loading chunks...")
    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"Loaded {len(chunks)} chunks")

    texts = [c["text"] for c in chunks]
    print(f"Generating embeddings (BAAI/bge-small-en-v1.5)...")
    model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    embeddings_list = list(model.embed(texts))
    embeddings = np.array(embeddings_list, dtype=np.float32)
    print(f"Generated {len(embeddings)} embeddings, dim={embeddings.shape[1]}")

    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)
    faiss.normalize_L2(embeddings)
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_FILE))

    mapping = {
        "chunk_ids": [c["id"] for c in chunks],
        "dim": dim,
        "total": len(chunks),
        "model": "BAAI/bge-small-en-v1.5",
        "normalized": True,
    }
    with open(MAPPING_FILE, "w") as f:
        json.dump(mapping, f, indent=2)

    print(f"\nDone! FAISS index saved to {INDEX_FILE}")
    print(f"Total vectors: {len(chunks)}, dimension: {dim}")
    print("Semantic search is now active.")


if __name__ == "__main__":
    main()
