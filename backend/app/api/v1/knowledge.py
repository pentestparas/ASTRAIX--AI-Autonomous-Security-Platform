from fastapi import APIRouter, Query
from typing import Optional

from app.schemas.base import ResponseSchema
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

KB_PATH = "/app/knowledge-base"

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
