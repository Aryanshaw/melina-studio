from fastapi import FastAPI
import sys
import os
from contextlib import asynccontextmanager

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
import __init__ as project_root

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_routes()
    yield

app = FastAPI(lifespan=lifespan)

def init_routes():
    print("Initializing routes")

if __name__ == "main":
    project_root.init()
