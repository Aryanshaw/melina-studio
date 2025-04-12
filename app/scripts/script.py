import asyncio
from typing import TypedDict

from app.melina.graph.edges.edge import Edge
from app.melina.graph.nodes.llm_node import LLMNode
from app.melina.graph.graph import Graph
from app.melina.core.executor import GraphExecutor

print("Starting test runner")

async def test_runner():
    llm_node_1 = LLMNode(
        id="1234",
        name="Test LLM Node",
        type="llm",
        provider="groq",
        model_name="llama3-8b-8192",
        prompt="Your task is to generate a list of 10 random words. Return the list in a JSON array format.",
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        api_key="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"
    )

    llm_node_2 = LLMNode(
        id="1235",
        name="Test LLM Node 2",
        type="llm",
        provider="groq",
        model_name="llama3-8b-8192",
        prompt="Take this list of words: {output} and create a short story using them. Return the story as a string.",
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        api_key="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"
    )

    edge_1 = Edge(
        id="1236",
        source_id=llm_node_1.id,
        target_id=llm_node_2.id,
        label="Test Edge 1"
    )

    state = {
        "input": any,
        "output": any
    }
    g = Graph(
        name="Test Graph",
        description="Test Graph",
        nodes=[llm_node_1, llm_node_2],
        edges=[edge_1],
        state=state
    )

    executor = GraphExecutor(g)
    result = await executor.aexecute({"input": "Do what i said!"})

    print(result)
    return result
