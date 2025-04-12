import uuid
from typing import Dict, Any, List, Optional, Union
from pydantic import BaseModel, Field

from ..models.node import BaseNode
from .edges.edge import Edge

class Graph(BaseModel):
    """Represents a workflow graph with nodes and edges."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    nodes: List[BaseNode] = Field(default_factory=list)
    edges: List[Edge] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
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
    
    def remove_node(self, node_id: str) -> bool:
        """Remove a node by its ID."""
        for i, node in enumerate(self.nodes):
            if node.id == node_id:
                self.nodes.pop(i)
                # Also remove any edges connected to this node
                self.edges = [e for e in self.edges 
                             if e.source_id != node_id and e.target_id != node_id]
                return True
        return False
    
    def remove_edge(self, edge_id: str) -> bool:
        """Remove an edge by its ID."""
        for i, edge in enumerate(self.edges):
            if edge.id == edge_id:
                self.edges.pop(i)
                return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the graph to a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "metadata": self.metadata
        }