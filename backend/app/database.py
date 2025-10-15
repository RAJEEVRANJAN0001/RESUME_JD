"""
Database connection and initialization for MongoDB.
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorGridFSBucket
from app.config import settings
from typing import Optional

# Global database client
mongodb_client: Optional[AsyncIOMotorClient] = None
database = None
gridfs_bucket: Optional[AsyncIOMotorGridFSBucket] = None


async def connect_to_mongo():
    """Establish connection to MongoDB Atlas."""
    global mongodb_client, database, gridfs_bucket
    
    try:
        # Add SSL certificate verification bypass for macOS
        mongodb_client = AsyncIOMotorClient(
            settings.MONGODB_URI,
            serverSelectionTimeoutMS=5000,
            tlsAllowInvalidCertificates=True  # For macOS SSL issues
        )
        # Test connection
        await mongodb_client.admin.command('ping')
        
        database = mongodb_client[settings.DATABASE_NAME]
        gridfs_bucket = AsyncIOMotorGridFSBucket(database)
        
        # Create indexes
        await database.resumes.create_index("resume_hash", unique=True)
        await database.resumes.create_index("parsed_at")
        await database.resumes.create_index([("name", "text"), ("skills", "text")])
        
        print(f"✅ Connected to MongoDB: {settings.DATABASE_NAME}")
    except Exception as e:
        print(f"❌ Failed to connect to MongoDB: {e}")
        print("⚠️  Running without database connection")
        # Don't raise - allow server to start without DB for testing
        database = None
        gridfs_bucket = None


async def close_mongo_connection():
    """Close MongoDB connection."""
    global mongodb_client
    if mongodb_client:
        mongodb_client.close()
        print("✅ MongoDB connection closed")


def get_database():
    """Get database instance."""
    return database


def get_gridfs():
    """Get GridFS bucket instance."""
    return gridfs_bucket
