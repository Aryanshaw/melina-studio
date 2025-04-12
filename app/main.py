from fastapi import FastAPI
import sys
import os
from contextlib import asynccontextmanager

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import __init__ as project_root

from .config.db import MongoDB
from apis.node_routes import node_router
from apis.graph_routes import graph_router
from apis.edge_routes import edge_router
from scripts.script import test_runner

@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDB.connect()
    init_routes()
    # await test_runner()
    yield
    await MongoDB.close()

app = FastAPI(lifespan=lifespan)

def init_routes():
    print("Initializing routes")
    app.include_router(node_router, prefix="/node")
    app.include_router(graph_router, prefix="/graph")
    app.include_router(edge_router, prefix="/edge")
    
if __name__ == "main":
    project_root.init()
