"""Fast knowledge base ingestion - line-based chunking."""
import os, json, hashlib, re
from pathlib import Path

KB = Path(__file__).parent
SOURCES = KB / "sources"
EMBEDDINGS = KB / "embeddings"
EXCLUDE = {".git", "node_modules", "__pycache__", ".github", "images", "img", "assets"}

def get_files():
    files = []
    for root, dirs, fnames in os.walk(SOURCES):
        dirs[:] = [d for d in dirs if d not in EXCLUDE]
        for fn in fnames:
            if fn.endswith(".md"):
                files.append(os.path.join(root, fn))
    return files

def chunk_by_lines(text, max_lines=80):
    lines = text.split("\n")
    chunks, current = [], []
    for line in lines:
        current.append(line)
        if len(current) >= max_lines:
            block = "\n".join(current).strip()
            if len(block) > 50:
                chunks.append(block)
            current = []
    if current:
        block = "\n".join(current).strip()
        if len(block) > 50:
            chunks.append(block)
    return chunks if chunks else [text[:2000]]

def extract_title(fp, content):
    m = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return Path(fp).stem.replace("_", " ").replace("-", " ").title()

def main():
    EMBEDDINGS.mkdir(parents=True, exist_ok=True)
    files = get_files()
    print(f"Files: {len(files)}", flush=True)

    all_chunks = []
    for idx, fp in enumerate(files):
        rel = str(Path(fp).relative_to(SOURCES))
        try:
            with open(fp, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except:
            continue
        if not content.strip():
            continue
        title = extract_title(fp, content)
        chunks = chunk_by_lines(content)
        for i, chunk in enumerate(chunks):
            cid = hashlib.md5(f"{rel}:{i}".encode()).hexdigest()
            all_chunks.append({"id": cid, "source": rel, "title": title, "chunk_index": i, "text": chunk, "char_count": len(chunk)})
        if (idx + 1) % 50 == 0:
            print(f"  {idx+1}/{len(files)} -> {len(all_chunks)} chunks", flush=True)

    with open(EMBEDDINGS / "chunks.json", "w", encoding="utf-8") as f:
        json.dump(all_chunks, f, ensure_ascii=False)
    manifest = {"total_sources": len(set(c["source"] for c in all_chunks)), "total_chunks": len(all_chunks)}
    with open(EMBEDDINGS / "manifest.json", "w") as f:
        json.dump(manifest, f)
    print(f"Done: {manifest['total_chunks']} chunks, {manifest['total_sources']} sources", flush=True)

if __name__ == "__main__":
    main()
