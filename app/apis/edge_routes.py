from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.melina.graph.edges.edge import Edge
from app.melina.services.edge_cruds.edge_crud import EdgeCrud

edge_router = APIRouter()

@edge_router.post("/{graph_id}/create")
async def create_edge(graph_id: str, edge: Edge):

    edge.graph_template_id = graph_id
    result = await EdgeCrud().create_edge(edge)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to create edge")
    return JSONResponse(content={"message": "Edge created successfully", "edge_id": result})

@edge_router.get("/{graph_id}/get/{edge_id}")
async def get_edge(graph_id: str, edge_id: str):
    result = await EdgeCrud().get_edge(edge_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to get edge")
    return JSONResponse(content={"message": "Edge retrieved successfully", "edge": result})