import asyncio
from typing import TypedDict

from app.melina.graph.nodes.llm_node import LLMNode
from app.melina.graph.graph import Graph
from app.melina.core.executor import GraphExecutor

print("Starting test runner")

async def test_runner():
    llm_node = LLMNode(
        id="12345",
        name="Test LLM Node",
        type="llm",
        provider="openai",
        model_name="gpt-4o-mini",
        prompt="Your task is to generate a list of 10 random words. Return the list in a JSON array format.",
        temperature=0.7,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.0,
        api_key="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"
    )
    # result = await llm_node.process({"input": "Hello, world!"})
    # print(result)
    state = {
        "input": str,
        "output": str
    }
    g = Graph(
        name="Test Graph",
        description="Test Graph",
        nodes=[llm_node],
        edges=[],
        state=state
    )
    # result = await g.run_node(llm_node.id, {"input": "Do what i said!"})
    # print(result)
    executor = GraphExecutor(g)
    result = await executor.aexecute({"input": "Do what i said!"})

    print(result)
    return result
