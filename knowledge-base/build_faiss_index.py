"""Build FAISS vector index from chunks.json using fastembed.
Lightweight ONNX-based embedding (no PyTorch needed).

Parallel mode: chunks are split across N worker processes (one per CPU),
each embedding its slice with its own model instance loaded from the
shared disk cache. Merges the parts and writes the final index.
"""
import argparse
import json
import multiprocessing
import sys
import time
from pathlib import Path

KB_DIR = Path(__file__).parent
CHUNKS_FILE = KB_DIR / "embeddings" / "chunks.json"
INDEX_FILE = KB_DIR / "embeddings" / "faiss_index.bin"
MAPPING_FILE = KB_DIR / "embeddings" / "index_mapping.json"

_MODEL = None


def _get_model(model_name):
    """Return the shared model. With fork, children inherit the parent's instance,
    so each worker avoids fastembed's cache-lock contention."""
    global _MODEL
    if _MODEL is None:
        from fastembed import TextEmbedding

        _MODEL = TextEmbedding(model_name=model_name, threads=1)
    return _MODEL


def _embed_slice(args):
    """Worker: embed one slice of texts. Top-level fn required for pickling."""
    slice_idx, texts, model_name = args
    import numpy as np

    model = _get_model(model_name)
    t0 = time.time()
    vecs = list(model.embed(texts, batch_size=64, parallel=None))
    arr = np.array(vecs, dtype=np.float32)
    print(f"[worker {slice_idx}] embedded {len(arr)} chunks in {time.time() - t0:.1f}s", flush=True)
    return arr


def main():
    if not CHUNKS_FILE.exists():
        print(f"ERROR: {CHUNKS_FILE} not found. Run ingest.py first.")
        sys.exit(1)

    parser = argparse.ArgumentParser()
    parser.add_argument("--workers", type=int, default=multiprocessing.cpu_count())
    args = parser.parse_args()
    n_workers = max(1, args.workers)

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
    model_name = "BAAI/bge-small-en-v1.5"

    if n_workers > 1 and len(texts) > 1000:
        # Warm the model ONCE in the parent; fork children inherit the loaded
        # instance, so workers never hit fastembed's cache-lock contention.
        print("Warming model cache (single load)...", flush=True)
        _get_model(model_name)

        # Split into contiguous slices so chunk ids stay ordered.
        step = (len(texts) + n_workers - 1) // n_workers
        slices = [texts[i : i + step] for i in range(0, len(texts), step)]
        slices = [s for s in slices if s]

        print(f"Generating embeddings with {len(slices)} parallel workers...", flush=True)
        t0 = time.time()
        ctx = multiprocessing.get_context("fork")
        with ctx.Pool(len(slices)) as pool:
            parts = pool.map(
                _embed_slice,
                [(i, sl, model_name) for i, sl in enumerate(slices)],
            )
        embeddings = np.concatenate(parts, axis=0)
        print(
            f"Generated {len(embeddings)} embeddings in {time.time() - t0:.1f}s, dim={embeddings.shape[1]}",
            flush=True,
        )
    else:
        print(f"Generating embeddings (single process)...", flush=True)
        model = TextEmbedding(model_name=model_name)
        embeddings_list = list(model.embed(texts, batch_size=64, parallel=None))
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
