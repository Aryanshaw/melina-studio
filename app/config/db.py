from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi
from pymongo import DESCENDING, ASCENDING
import certifi
from typing import Optional

from app.config.config import config_load

class MongoDB:
    client: Optional[AsyncIOMotorClient] = None
    database = None
    
    # Collections
    node_collection = None
    graph_collection = None
    edge_collection = None

    @classmethod
    async def connect(cls):
        """Initialize MongoDB connection and collections"""
        if cls.client is not None:
            return
            
        config = config_load()
        uri = config.get('MONGO_URI')
        db_type = config.get('DB_TYPE')

        try:
            # Initialize client
            cls.client = AsyncIOMotorClient(
                uri, 
                server_api=ServerApi('1'), 
                tlsCAFile=certifi.where()
            )
            
            # Test connection
            await cls.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
            
            # Set database based on environment
            cls.database = cls.client.dev if db_type == 'dev' else cls.client.prod
            print(f"Database selected: {cls.database.name}")

            # Initialize all collections
            cls.node_collection = cls.database.node_collection
            cls.graph_collection = cls.database.graph_collection
            cls.edge_collection = cls.database.edge_collection
            
            # Create indexes
            await cls._create_indexes()

            print("All collections initialized successfully")

        except Exception as e:
            print(f"Could not connect to MongoDB: {e}")
            raise e

    @classmethod
    async def _create_indexes(cls):
        """Create all necessary indexes"""
        try:
            # User collection indexes
            pass            
            # Add other indexes as needed
            # await cls.company_collection.create_index([('name', ASCENDING)])
            # await cls.chat_collection.create_index([('created_at', DESCENDING)])
            # etc...

        except Exception as e:
            print(f"Error creating indexes: {e}")
            raise e

    @classmethod
    async def close(cls):
        """Close MongoDB connection"""
        if cls.client is not None:
            cls.client.close()
            cls.client = None
            cls.database = None
            print("MongoDB connection closed")

    @classmethod
    def get_database(cls):
        """Get database instance"""
        if cls.database is None:
            raise Exception("Database not initialized. Call connect() first.")
        return cls.database

    @classmethod
    def get_collection(cls, collection_name: str):
        """Get a specific collection by name"""
        if cls.database is None:
            raise Exception("Database not initialized. Call connect() first.")
        return getattr(cls, f"{collection_name}_collection")

    @classmethod
    async def ping(cls):
        """Test database connection"""
        if cls.client is None:
            raise Exception("Client not initialized. Call connect() first.")
        try:
            await cls.client.admin.command('ping')
            return True
        except Exception as e:
            print(f"Error pinging database: {e}")
            return False

    @classmethod
    async def get_collection_names(cls):
        """Get list of all collection names"""
        if cls.database is None:
            raise Exception("Database not initialized. Call connect() first.")
        return await cls.database.list_collection_names()

    @classmethod
    async def drop_collection(cls, collection_name: str):
        """Drop a collection (careful!)"""
        if cls.database is None:
            raise Exception("Database not initialized. Call connect() first.")
        try:
            await cls.database.drop_collection(collection_name)
            print(f"Collection {collection_name} dropped successfully")
        except Exception as e:
            print(f"Error dropping collection: {e}")
            raise e

# Export the class
__all__ = ['MongoDB']

