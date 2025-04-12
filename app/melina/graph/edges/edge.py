from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class Edge(BaseModel):
    """Base class for edges connecting nodes in the graph."""
    id: str
    source_id: str  # ID of the source node
    target_id: str  # ID of the target node
    label: Optional[str] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the edge to a dictionary."""
        return self.model_dump()
    
    def to_code(self) -> str:
        """Generate code representation of this edge."""
        return f"graph.add_edge(\"{self.source_id}\", \"{self.target_id}\")"