import os
import sys
import json
import hashlib
import re
from pathlib import Path

KB_DIR = Path(__file__).parent
SOURCES_DIR = KB_DIR / "sources"
INGESTED_DIR = KB_DIR / "ingested"
EMBEDDINGS_DIR = KB_DIR / "embeddings"

EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", ".github", "images", "img", "assets"}
EXCLUDE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".woff", ".woff2", ".ttf", ".eot",
                ".zip", ".gz", ".tar", ".exe", ".bin", ".o", ".so", ".dll", ".pyc", ".pdf",
                ".sqlite3", ".sqlite", ".db", ".pack", ".lock", ".ipynb", ".onnx", ".joblib", ".pt", ".h5"}

SUPPORTED_EXTS = {".md", ".rst", ".txt", ".yml", ".yaml", ".json", ".html", ".htm",
                  ".py", ".js", ".ts", ".go", ".rs", ".java", ".cpp", ".h", ".c"}

MAX_FILE_BYTES = 8 * 1024 * 1024

def collect_files():
    files = []
    for root, dirs, fnames in os.walk(SOURCES_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for fname in fnames:
            ext = os.path.splitext(fname)[1].lower()
            if ext in EXCLUDE_EXTS or ext not in SUPPORTED_EXTS:
                continue
            files.append(os.path.join(root, fname))
    return files

def chunk_text(text, max_chars=2000, overlap=200):
    chunks = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        if end < n:
            break_point = max(
                text.rfind("\n\n", start, end),
                text.rfind("\n", start, end),
                text.rfind(". ", start, end),
            )
            if break_point > start:
                end = break_point + 1
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        # Clamp to guarantee forward progress: a break point at the very start
        # of the window must not push `start` backwards (infinite loop).
        start = max(end - overlap, start + 1)
    return chunks

def extract_title(filepath, content):
    stem = os.path.splitext(os.path.basename(filepath))[0]
    match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if match:
        return match.group(1).strip()
    return stem.replace("_", " ").replace("-", " ").title()

def generate_embedding_placeholder(text):
    return hashlib.sha256(text.encode()).hexdigest()[:16]

def main():
    INGESTED_DIR.mkdir(parents=True, exist_ok=True)
    EMBEDDINGS_DIR.mkdir(parents=True, exist_ok=True)

    files = collect_files()
    print(f"Found {len(files)} files to process", flush=True)

    all_chunks = []
    for idx, filepath in enumerate(files, start=1):
        print(f"  {idx}/{len(files)} {os.path.relpath(filepath, SOURCES_DIR)}", flush=True)
        if os.path.getsize(filepath) > MAX_FILE_BYTES:
            print(f"  SKIP (too large) {filepath}", flush=True)
            continue
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"  SKIP {filepath}: {e}", flush=True)
            continue

        rel_path = os.path.relpath(filepath, SOURCES_DIR)
        title = extract_title(filepath, content)
        chunks = chunk_text(content)

        doc_entry = {
            "source": rel_path,
            "title": title,
            "total_chars": len(content),
            "chunks": len(chunks),
        }

        for i, chunk in enumerate(chunks):
            chunk_id = hashlib.md5(f"{rel_path}:{i}".encode()).hexdigest()
            entry = {
                "id": chunk_id,
                "source": rel_path,
                "title": title,
                "chunk_index": i,
                "text": chunk,
                "char_count": len(chunk),
            }
            all_chunks.append(entry)

        (INGESTED_DIR / f"{hashlib.md5(rel_path.encode()).hexdigest()}.json").write_text(
            json.dumps(doc_entry, indent=2)
        )

        if idx % 100 == 0:
            _write_partial(all_chunks, {"total_sources": len({c["source"] for c in all_chunks}), "total_chunks": len(all_chunks)})
            print(f"  CHECKPOINT [{idx}/{len(files)}] {len(all_chunks)} chunks so far", flush=True)

    manifest = {
        "total_sources": len(set(c["source"] for c in all_chunks)),
        "total_chunks": len(all_chunks),
        "total_chars": sum(c["char_count"] for c in all_chunks),
    }
    (EMBEDDINGS_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))

    chunks_path = EMBEDDINGS_DIR / "chunks.json"
    with open(chunks_path, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False)

    print(f"\nDone. {manifest['total_chunks']} chunks from {manifest['total_sources']} sources", flush=True)
    print(f"Total chars: {manifest['total_chars']}", flush=True)
    print(f"Chunks saved to: {chunks_path}", flush=True)


def _write_partial(all_chunks, manifest):
    """Crash-safe incremental write so an interrupted ingest never loses progress."""
    tmp = EMBEDDINGS_DIR / "chunks.json.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False)
    tmp.replace(EMBEDDINGS_DIR / "chunks.json")
    (EMBEDDINGS_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
