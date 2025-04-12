
from app.config.db import MongoDB
from bson import ObjectId
from typing import Dict, Any

from app.melina.models.node import BaseNode
from app.melina.models.node import NodeType

class NodeCrud:
    def __init__(self):
        self.node_collection = MongoDB.node_collection

    async def create_node(self, node: BaseNode):
        try:
            node_data = node.model_dump()
            node_data.pop("id", None)  # Remove "_id" if it exists

            result = await self.node_collection.insert_one(node_data)
            return str(result.inserted_id)
        except Exception as e:
            print(f"Error creating node: {e}")
            raise e

    async def get_node(self, node_id: str):
        try:
            node = await self.node_collection.find_one({"_id": ObjectId(node_id)})

            if not node:
                return None
            
            return self._create_node_instance(node)
        except Exception as e:
            print(f"Error getting node: {e}")
            raise e

    async def update_node(self, node_id: str, node: BaseNode):
        try:
            await self.node_collection.update_one({"_id": ObjectId(node_id)}, {"$set": node.model_dump()})
        except Exception as e:
            print(f"Error updating node: {e}")
            raise e

    async def delete_node(self, node_id: str):
        try:
            await self.node_collection.delete_one({"_id": ObjectId(node_id)})
        except Exception as e:
            print(f"Error deleting node: {e}")
            raise e
        
    def _create_node_instance(self, node_data: Dict[str, Any]) -> BaseNode:
        """Create a node instance based on the node type."""
        node_type = node_data.get("type")
        
        if node_type == NodeType.LLM:
            # Import here to avoid circular import
            from app.melina.graph.nodes.llm_node import LLMNode, LLMConfig
            
            llm_config_data = node_data.get("llm_config", {})
            llm_config = LLMConfig(**llm_config_data)
            
            # Create LLM node with the config
            node = LLMNode(
                name=node_data.get("name", ""),
                type=node_data.get("type", ""),
                provider=llm_config.provider,
                model_name=llm_config.model_name,
                prompt=node_data.get("prompt", ""),
                temperature=llm_config.temperature,
                max_tokens=llm_config.max_tokens,
                top_p=llm_config.top_p,
                frequency_penalty=llm_config.frequency_penalty,
                api_key=llm_config.api_key
            )
            # Set the ID explicitly
            node.id = str(node_data.get("_id"))
            return node
        else:
            # For other node types, use the base class
            # Create a copy of the data so we can modify it
            node_dict = dict(node_data)
            # Convert ObjectId to string for the ID
            node_dict["id"] = str(node_dict.pop("_id"))
            return BaseNode(**node_dict)