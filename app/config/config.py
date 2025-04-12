import os
from dotenv import load_dotenv

load_dotenv()

def config_load():
    return {
        "MONGO_URI": os.getenv("MONGO_URI"),
        "MONGO_PASSWORD": os.getenv("MONGO_PASSWORD"),
        "DB_TYPE": os.getenv("DB_TYPE"),
    }
