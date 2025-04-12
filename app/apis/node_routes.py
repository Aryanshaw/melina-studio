from fastapi import APIRouter, HTTPException , Body
from fastapi.responses import JSONResponse
from app.melina.graph.nodes.llm_node import LLMNode
from typing import Dict, Any

from app.melina.controllers.node_cruds.node_crud import NodeCrud

node_router = APIRouter()

@node_router.post("/llm")
async def create_llm_node(node: LLMNode):
    """Create a new LLM node."""
    try:
        node_id = await node.save_node()
        return JSONResponse(status_code=200, content={"node_id": node_id , "message": "New node added successfully"})
    except Exception as e:
        print(f"Error creating LLM node: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@node_router.post("/run/{node_id}")
async def run_node(
    node_id: str,
    inputs: Dict[str, Any] = Body(...)
):
    """Run a node by ID."""
    try:
        # Fetch the node from database using node_id
        node = await NodeCrud().get_node(node_id)
        if not node:
            raise HTTPException(status_code=404, detail="Node not found")
            
        # Run the node
        result = await node.run_node(inputs)
        return JSONResponse(status_code=200, content=result)
    except Exception as e:
        print(f"Error running node: {e}")
        raise HTTPException(status_code=500, detail=str(e))
