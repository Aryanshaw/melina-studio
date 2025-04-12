import uuid
import json
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field

from ..models.node import BaseNode
from .edges.edge import Edge
from app.melina.services.graph_cruds.graph_crud import GraphCRUD

class Graph(BaseModel):
    """Represents a workflow graph with nodes and edges."""
    id: str
    name: Optional[str] = None
    description: Optional[str] = None
    nodes: Optional[List[BaseNode]] = None
    edges: Optional[List[Edge]] = None
    state: Optional[Dict[str, Any]] = None
    metadata: Optional[Dict[str, Any]] = None
    
    def add_node(self, node: BaseNode) -> None:
        """Add a node to the graph."""
        self.nodes.append(node)
    
    def add_edge(self, edge: Edge) -> None:
        """Add an edge to the graph."""
        self.edges.append(edge)
    
    def get_node(self, node_id: str) -> Optional[BaseNode]:
        """Get a node by its ID."""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None
    
    def get_edge(self, edge_id: str) -> Optional[Edge]:
        """Get an edge by its ID."""
        for edge in self.edges:
            if edge.id == edge_id:
                return edge
        return None
    
    async def run_node(self, node_id: str, inputs: dict):
        node = self.get_node(node_id)
        if node:
            return await node.process(inputs)
        raise ValueError("Node not found")
    
    async def execute_graph(self, inputs: dict):
        """Execute the graph."""
        try:
            """get the graph id and graph"""
            graph_id = self.id
            graph = await GraphCRUD().get_graph(graph_id)

            """Now that we have the graph, we can execute it"""
            from app.melina.core.executor import GraphExecutor

            executor = GraphExecutor(graph)
            result = await executor.aexecute(inputs)
            
            """Attempt to parse in case if response is a json string"""
            try:
                result = json.loads(result)
            except:
                pass

            return result
        except Exception as e:
            print(f"Error executing graph: {e}")
            raise e