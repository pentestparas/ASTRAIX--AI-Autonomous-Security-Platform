from fastapi import APIRouter, Query

from app.recon_orchestrator.graph_db import get_knowledge_graph
from app.schemas.base import ResponseSchema

router = APIRouter()


@router.get("/graph")
async def get_graph(scan_id: str = Query("", description="Filter graph by scan ID")):
    kg = get_knowledge_graph()
    data = await kg.fetch_graph(scan_id=scan_id)
    return ResponseSchema(data=data)
