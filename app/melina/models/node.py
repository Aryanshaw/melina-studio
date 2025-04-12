from datetime import datetime
from enum import Enum
from typing import Dict, Any, Optional, List, Union
from pydantic import BaseModel, Field, ConfigDict

class NodeType(str, Enum):
    LLM = "llm"
    TOOL = "tool"
    ROUTER = "router"
    CONDITION = "condition"
    INPUT = "input"
    OUTPUT = "output"

class Position(BaseModel):
    x: float = 0
    y: float = 0
    
class BaseNode(BaseModel):
    """Base class for all node types in the graph."""
    model_config = ConfigDict(extra="allow")
    
    id: Optional[str] = None
    name: str 
    type: NodeType
    description: Optional[str] = None
    graph_template_id: Optional[str] = None
    position: Position = Field(default_factory=Position)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def update_timestamp(self):
        self.updated_at = datetime.now()
    
    async def process(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Process the node with the given inputs.
        
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the node to a dictionary."""
        return self.model_dump()
    
    def to_code(self) -> str:
        """Generate code representation of this node.
        
        This method should be implemented by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")