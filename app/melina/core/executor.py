from typing import TypedDict, Dict, Any, Callable, Awaitable
from langgraph.graph import StateGraph
import functools

from app.melina.graph.graph import Graph


def create_node_processor(node) -> Callable[[Dict[str, Any]], Awaitable[Dict[str, Any]]]:
    """Create a processor function for a node that LangGraph can use."""
    async def process_node(state: Dict[str, Any]) -> Dict[str, Any]:
        result = await node.process(state)
        return result
    
    # Set a name for better debugging
    process_node.__name__ = f"process_{node.id}"
    
    return process_node

class GraphExecutor:
    def __init__(self, graph: Graph):
        self.graph = graph

    async def build_graph(self):
        state_type = TypedDict('GraphState', self.graph.state)
        
        # Use this TypedDict with StateGraph
        state_graph = StateGraph(state_type)

        # Add nodes to the graph
        print("Adding nodes to the graph")
        for node in self.graph.nodes:
            # Create a processor function for this node
            node_processor = create_node_processor(node)
            print(f"Adding node {node.id} to the graph")
            print(f"Node processor: {node_processor}")
            state_graph.add_node(node.id, node_processor)

        # Add edges to the graph
        print("Adding edges to the graph")
        for edge in self.graph.edges:
            state_graph.add_edge(edge.source_id, edge.target_id)

        # Set entry point if not already set
        # Find nodes with no incoming edges
        entry_nodes = self._find_entry_nodes()
        if entry_nodes and len(entry_nodes) > 0:
            state_graph.set_entry_point(entry_nodes[0].id)

        print("Compiling graph")
        return state_graph.compile()
    
    def _find_entry_nodes(self):
        """Find nodes with no incoming edges."""
        # Get all target node IDs
        target_ids = set(edge.target_id for edge in self.graph.edges)
        
        # Entry nodes are those that are not targets
        entry_nodes = [node for node in self.graph.nodes if node.id not in target_ids]
        
        # If no entry nodes found, return the first node as default
        if not entry_nodes and self.graph.nodes:
            return [self.graph.nodes[0]]
            
        return entry_nodes

    async def execute(self, start_input):
        compiled_graph = await self.build_graph()
        return compiled_graph.invoke(start_input)

    async def aexecute(self, start_input):
        compiled_graph = await self.build_graph()
        return await compiled_graph.ainvoke(start_input)
