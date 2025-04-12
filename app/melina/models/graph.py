from typing import List, Optional, Dict, Any
from pydantic import Field
from datetime import datetime
from pydantic import BaseModel

class Graph(BaseModel):
    name: str
    description: str
    nodes: Optional[List[str]] = None
    edges: Optional[List[str]] = None
    state: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    def update_timestamp(self):
        self.updated_at = datetime.now()

class AddNode(BaseModel):
    node_id: str

class AddEdge(BaseModel):
    edge_id: str

class UpdateGraph(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    nodes: Optional[List[AddNode]] = None
    edges: Optional[List[AddEdge]] = None
    state: Optional[Dict[str, Any]] = None
    updated_at: Optional[datetime] = None

    def update_timestamp(self):
        self.updated_at = datetime.now()
