from bson import ObjectId
import json
from app.melina.models.graph import Graph, UpdateGraph
from app.melina.services.edge_cruds.edge_crud import EdgeCrud
from app.melina.services.node_cruds.node_crud import NodeCrud
from app.melina.graph.edges.edge import Edge
from datetime import datetime

from app.config.db import MongoDB

class GraphCRUD:
    def __init__(self):
        self.graph_collection = MongoDB.graph_collection

    async def create_graph(self, graph: Graph):
        try:
            # If graph is None, create a default graph
            graph = graph or Graph(
                name="Untitled Graph",
                description="",
                nodes=[],
                edges=[]
            )
                
            output = await self.graph_collection.insert_one(graph.model_dump())
            return str(output.inserted_id)
        except Exception as e:
            print(f"Error creating graph: {e}")
            return None
        
    async def get_graph(self, graph_id: str):
        try:
            output = await self.graph_collection.find_one({"_id": ObjectId(graph_id)})
            if output is None:
                return None

            graph = Graph(**output)
            
            if graph.nodes is not None:
                temp_nodes = []
                for node_id in graph.nodes:
                    node = await NodeCrud().get_node(node_id)
                    temp_nodes.append(node)
                graph.nodes = []
                graph.nodes = temp_nodes

            if graph.edges is not None:
                temp_edges = []
                for edge_id in graph.edges:
                    edge = await EdgeCrud().get_edge(edge_id)
                    temp_edges.append(edge)
                graph.edges = []
                graph.edges = temp_edges

            if graph.state is not None:
                # convert the values of the state to a dictionary
                for key, value in graph.state.items():
                    if value == 'str':
                        graph.state[key] = str
                    elif value == 'int':
                        graph.state[key] = int
                    elif value == 'float':
                        graph.state[key] = float
                    elif value == 'bool':
                        graph.state[key] = bool
                    elif value == 'list':
                        graph.state[key] = list
                    elif value == 'dict':
                        graph.state[key] = dict
                    else:
                        graph.state[key] = any

            # if graph.metadata is not None:
            #     graph.metadata = {}

            return graph
        except Exception as e:
            print(f"Error getting graph: {e}")
            return None
        
    async def update_graph(self, graph_id: str, graph: UpdateGraph):
        try:
            # Get only fields that have values (not None)
            update_data = {k: v for k, v in graph.model_dump().items() 
                          if v is not None and k not in ["nodes", "edges"]}
            
            # Add nodes one by one
            if graph.nodes is not None:
                for node in graph.nodes:
                    await self.graph_collection.update_one(
                        {"_id": ObjectId(graph_id)},
                        {"$push": {"nodes": node.node_id}}  # Use node_id instead of the object
                    )
            
            # Add edges one by one
            if graph.edges is not None:
                for edge in graph.edges:
                    await self.graph_collection.update_one(
                        {"_id": ObjectId(graph_id)},
                        {"$push": {"edges": edge.edge_id}}  # Use edge_id instead of the object
                    )
            
            # Update state if provided
            if graph.state is not None:
                update_data["state"] = graph.state
            
            # Update timestamp
            update_data["updated_at"] = datetime.now()
            
            # Only update if there are fields to update
            if update_data:
                result = await self.graph_collection.update_one(
                    {"_id": ObjectId(graph_id)},
                    {"$set": update_data}
                )
                return result.modified_count > 0
            
            # If only nodes/edges were added but no other fields updated
            return True
            
        except Exception as e:
            print(f"Error updating graph: {e}")
            return False