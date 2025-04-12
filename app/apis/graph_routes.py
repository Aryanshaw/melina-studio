from typing import Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.melina.models.graph import Graph, UpdateGraph
from app.melina.services.graph_cruds.graph_crud import GraphCRUD
from app.melina.graph.graph import Graph as GraphModel

graph_router = APIRouter()

@graph_router.post("/create")
async def create_graph(graph: Optional[Graph] = None):
    result = await GraphCRUD().create_graph(graph)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to create graph")
    return JSONResponse(content={"message": "Graph created successfully", "graph_id": result})

@graph_router.get("/get/{graph_id}")
async def get_graph(graph_id: str):
    result = await GraphCRUD().get_graph(graph_id)
    if result is None:
        raise HTTPException(status_code=400, detail="Failed to get graph")
    return JSONResponse(content={"message": "Graph retrieved successfully", "graph": result})

@graph_router.put("/update/{graph_id}")
async def update_graph(graph_id: str, graph: UpdateGraph):
    result = await GraphCRUD().update_graph(graph_id, graph)
    if result is False:
        raise HTTPException(status_code=400, detail="Failed to update graph")
    return JSONResponse(content={"message": "Graph updated successfully"})

@graph_router.post("/{graph_id}/execute")
async def execute_graph(graph_id: str, inputs: dict):
    result = await GraphModel(id=graph_id).execute_graph(inputs)
    if result is False:
        raise HTTPException(status_code=400, detail="Failed to execute graph")
    return JSONResponse(content={"message": "Graph executed successfully", "result": result})
