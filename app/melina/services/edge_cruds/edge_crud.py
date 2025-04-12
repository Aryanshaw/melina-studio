from bson import ObjectId
from app.config.db import MongoDB
from app.melina.graph.edges.edge import Edge

class EdgeCrud:
    def __init__(self):
        self.edge_collection = MongoDB.edge_collection

    async def create_edge(self, edge: Edge):
        try:
            output = await self.edge_collection.insert_one(edge.model_dump())
            return str(output.inserted_id)
        except Exception as e:
            print(f"Error creating edge: {e}")
            return None

    async def get_edge(self, edge_id: str):
        try:
            output = await self.edge_collection.find_one({"_id": ObjectId(edge_id)})
            return Edge(**output)
        except Exception as e:
            print(f"Error getting edge: {e}")
            return None