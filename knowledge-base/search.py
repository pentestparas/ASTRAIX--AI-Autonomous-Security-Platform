"""Simple TF-IDF search engine for cybersecurity knowledge base."""
import json
import math
import re
import os
from pathlib import Path
from typing import List, Dict
from collections import Counter

KB_DIR = Path(__file__).parent
CHUNKS_FILE = KB_DIR / "embeddings" / "chunks.json"


class KnowledgeBase:
    def __init__(self):
        self.chunks: List[Dict] = []
        self.doc_freq: Dict[str, int] = {}
        self.num_docs = 0
        self._load()

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
        query_terms = self._tokenize(query)
        if not query_terms or not self.chunks:
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
        }


_kb: KnowledgeBase = None


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
