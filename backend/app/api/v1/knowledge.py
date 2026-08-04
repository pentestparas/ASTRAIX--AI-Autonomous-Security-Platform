from fastapi import APIRouter, HTTPException, Query
from pathlib import Path
from typing import Optional

from app.schemas.base import ResponseSchema
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

KB_PATH = "/app/knowledge-base"
KB_DIR = Path(KB_PATH)

try:
    import sys
    sys.path.insert(0, KB_PATH)
    from search import get_knowledge_base
    _kb = get_knowledge_base()
    _loaded = True
    logger.info("Knowledge base loaded: %s", _kb.stats())
except Exception as e:
    _kb = None
    _loaded = False
    logger.warning("Knowledge base not available: %s", e)


@router.get("/knowledge/search")
async def search_knowledge(
    q: str = Query(..., description="Search query"),
    top_k: int = Query(10, ge=1, le=50),
):
    """Search the cybersecurity knowledge base."""
    if not _loaded or not _kb:
        return ResponseSchema(data={"results": [], "total": 0})
    results = _kb.search(q, top_k=top_k)
    return ResponseSchema(data={"results": results, "total": len(results)})


@router.get("/knowledge/stats")
async def knowledge_stats():
    """Get knowledge base statistics."""
    if not _loaded or not _kb:
        return ResponseSchema(data={"loaded": False})
    stats = _kb.stats()
    stats["loaded"] = True
    return ResponseSchema(data=stats)


@router.post("/knowledge/rebuild")
async def rebuild_knowledge_index():
    """Rebuild FAISS vector index from chunks.json."""
    if not _loaded or not _kb:
        return ResponseSchema(success=False, message="Knowledge base not loaded")
    success = _kb.rebuild_faiss()
    if success:
        return ResponseSchema(message="FAISS index rebuilt successfully")
    return ResponseSchema(success=False, message="FAISS rebuild failed (check dependencies)")


@router.get("/knowledge/sources")
async def list_kb_sources():
    """List all source documents stored on disk inside the knowledge base."""
    src_root = KB_DIR / "sources"
    if not src_root.exists():
        return ResponseSchema(data={"sources": [], "total": 0})
    sources = []
    for p in src_root.rglob("*"):
        if p.is_file():
            try:
                rel = p.relative_to(KB_DIR)
            except ValueError:
                rel = p
            sources.append({
                "path": str(rel),
                "size": p.stat().st_size,
            })
    return ResponseSchema(data={"sources": sources, "total": len(sources)})


@router.get("/knowledge/source")
async def get_kb_source(
    path: str = Query(..., description="Relative path inside knowledge-base, e.g. sources/.../file.md"),
):
    """Read a single source document from the knowledge base (path-traversal safe)."""
    if not KB_DIR.exists():
        raise HTTPException(status_code=404, detail="Knowledge base not found")
    resolved = (KB_DIR / path).resolve()
    root = KB_DIR.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise HTTPException(status_code=400, detail="Path escapes the knowledge base")
    if not resolved.is_file():
        raise HTTPException(status_code=404, detail="Source not found")
    text = resolved.read_text(encoding="utf-8", errors="replace")
    return ResponseSchema(data={
        "path": str(resolved.relative_to(root)),
        "size": resolved.stat().st_size,
        "content": text,
    })
