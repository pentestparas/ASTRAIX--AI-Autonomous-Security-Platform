"""Hybrid search engine: FAISS vector (fastembed) + TF-IDF fallback."""
import json
import math
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Optional
from collections import Counter

KB_DIR = Path(__file__).parent
CHUNKS_FILE = KB_DIR / "embeddings" / "chunks.json"
INDEX_FILE = KB_DIR / "embeddings" / "faiss_index.bin"
MAPPING_FILE = KB_DIR / "embeddings" / "index_mapping.json"


class KnowledgeBase:
    def __init__(self):
        self.chunks: List[Dict] = []
        self.doc_freq: Dict[str, int] = {}
        self.num_docs = 0
        self._faiss_index = None
        self._faiss_mapping = None
        self._has_faiss = False
        self._embedder = None
        self._load()
        self._try_load_faiss()

    def _load(self):
        if not CHUNKS_FILE.exists():
            return
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            self.chunks = json.load(f)
        self.num_docs = len(self.chunks)
        for chunk in self.chunks:
            terms = set(self._tokenize(chunk["text"]))
            for term in terms:
                self.doc_freq[term] = self.doc_freq.get(term, 0) + 1

    def _try_load_faiss(self):
        if not INDEX_FILE.exists() or not MAPPING_FILE.exists():
            return
        try:
            import faiss
            import numpy as np
            self._faiss_index = faiss.read_index(str(INDEX_FILE))
            with open(MAPPING_FILE, "r") as f:
                self._faiss_mapping = json.load(f)
            self._has_faiss = True
        except Exception:
            self._has_faiss = False

    def _get_embedder(self):
        if self._embedder is None and self._has_faiss:
            try:
                import concurrent.futures
                from fastembed import TextEmbedding
                model_name = self._faiss_mapping.get("model", "BAAI/bge-small-en-v1.5")
                # The model may need downloading on first use. Bound it so a slow
                # or offline HF Hub cannot block a scan; fall back to TF-IDF.
                executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
                fut = executor.submit(TextEmbedding, model_name=model_name)
                try:
                    self._embedder = fut.result(timeout=int(os.environ.get("KB_EMBEDDER_TIMEOUT", "25")))
                except concurrent.futures.TimeoutError:
                    import logging
                    logging.getLogger("knowledge_base").warning(
                        "fastembed model load timed out - using TF-IDF fallback"
                    )
                    self._has_faiss = False
                    self._embedder = None
                except Exception:
                    self._has_faiss = False
                    self._embedder = None
                finally:
                    executor.shutdown(wait=False)
            except Exception:
                self._has_faiss = False
        return self._embedder

    def _tokenize(self, text: str) -> List[str]:
        text = text.lower()
        tokens = re.findall(r"[a-zA-Z][a-zA-Z0-9_#+.-]{1,50}", text)
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "have", "has", "had", "do", "does", "did", "will", "would",
            "could", "should", "may", "might", "can", "shall", "to",
            "of", "in", "for", "on", "with", "at", "by", "from", "as",
            "into", "through", "during", "before", "after", "above",
            "below", "between", "out", "off", "over", "under", "again",
            "further", "then", "once", "here", "there", "when", "where",
            "why", "how", "all", "each", "every", "both", "few", "more",
            "most", "other", "some", "such", "no", "nor", "not", "only",
            "own", "same", "so", "than", "too", "very", "just", "because",
            "and", "but", "or", "if", "while", "that", "this", "these",
            "those", "it", "its", "what", "which", "who", "whom",
        }
        return [t for t in tokens if t not in stopwords and len(t) > 2]

    def search(self, query: str, top_k: int = 10) -> List[Dict]:
        if not query.strip() or not self.chunks:
            return []

        if self._has_faiss:
            result = self._search_faiss(query, top_k)
            if result:
                return result
        return self._search_tfidf(query, top_k)

    def _search_faiss(self, query: str, top_k: int) -> List[Dict]:
        embedder = self._get_embedder()
        if embedder is None:
            return []
        try:
            import numpy as np
            import faiss
            embeddings = list(embedder.query_embed(query))
            q_vec = np.array(embeddings, dtype=np.float32).reshape(1, -1)
            faiss.normalize_L2(q_vec)
            scores, indices = self._faiss_index.search(q_vec, min(top_k, len(self.chunks)))
            results = []
            for score, idx in zip(scores[0], indices[0]):
                if idx < 0 or idx >= len(self.chunks):
                    continue
                chunk = dict(self.chunks[idx])
                chunk["relevance"] = round(float(score), 4)
                results.append(chunk)
            return results
        except Exception:
            return []

    def _search_tfidf(self, query: str, top_k: int) -> List[Dict]:
        query_terms = self._tokenize(query)
        if not query_terms:
            return []

        scores = []
        for i, chunk in enumerate(self.chunks):
            terms = self._tokenize(chunk["text"])
            if not terms:
                continue
            term_freq = Counter(terms)
            score = 0.0
            for qt in query_terms:
                if qt in term_freq:
                    tf = term_freq[qt] / len(terms)
                    idf = math.log((self.num_docs + 1) / (self.doc_freq.get(qt, 1) + 1)) + 1
                    score += tf * idf
            if score > 0:
                scores.append((score, i))

        scores.sort(key=lambda x: -x[0])
        results = []
        for score, idx in scores[:top_k]:
            chunk = dict(self.chunks[idx])
            chunk["relevance"] = round(score, 4)
            results.append(chunk)
        return results

    def stats(self) -> dict:
        return {
            "total_chunks": len(self.chunks),
            "total_sources": len(set(c["source"] for c in self.chunks)),
            "vocab_size": len(self.doc_freq),
            "semantic_search": self._has_faiss,
        }


_kb: Optional[KnowledgeBase] = None


def get_knowledge_base() -> KnowledgeBase:
    global _kb
    if _kb is None:
        _kb = KnowledgeBase()
    return _kb


if __name__ == "__main__":
    kb = get_knowledge_base()
    print(f"Knowledge Base: {kb.stats()}")
    while True:
        q = input("\nQuery (or 'quit'): ").strip()
        if q.lower() in ("quit", "exit", "q"):
            break
        results = kb.search(q, top_k=5)
        print(f"\nTop {len(results)} results:")
        for r in results:
            print(f"  [{r['relevance']:.3f}] {r['source']} - {r['title']}")
            snippet = r['text'][:200].replace("\n", " ")
            print(f"      {snippet}...")
