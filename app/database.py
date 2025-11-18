"""
Database Connection and Utilities
Handles MongoDB/Cosmos DB connection with connection pooling
"""
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Global database client
_client: AsyncIOMotorClient = None
_database: AsyncIOMotorDatabase = None


async def connect_to_database():
    """
    Connect to MongoDB/Cosmos DB
    Called on application startup
    """
    global _client, _database
    
    try:
        logger.info(f"Connecting to MongoDB: {settings.mongodb_database}")
        
        _client = AsyncIOMotorClient(
            settings.mongodb_url,
            minPoolSize=settings.mongodb_min_pool_size,
            maxPoolSize=settings.mongodb_max_pool_size,
        )
        
        _database = _client[settings.mongodb_database]
        
        # Test connection
        await _client.admin.command('ping')
        logger.info("✅ Successfully connected to MongoDB")
        
        # Create indexes
        await create_indexes()
        
    except ConnectionFailure as e:
        logger.error(f"❌ Failed to connect to MongoDB: {e}")
        raise


async def close_database_connection():
    """
    Close MongoDB connection
    Called on application shutdown
    """
    global _client
    
    if _client:
        _client.close()
        logger.info("Closed MongoDB connection")


def get_database() -> AsyncIOMotorDatabase:
    """
    Get database instance
    
    Returns:
        AsyncIOMotorDatabase: Database instance
    """
    return _database


async def create_indexes():
    """
    Create database indexes for better query performance
    """
    try:
        db = get_database()
        
        # Patient indexes
        await db.Patient.create_index("id", unique=True)
        await db.Patient.create_index("identifier.value")
        await db.Patient.create_index([("name.family", 1), ("name.given", 1)])
        await db.Patient.create_index("birthDate")
        
        # Observation indexes
        await db.Observation.create_index("id", unique=True)
        await db.Observation.create_index("subject.reference")
        await db.Observation.create_index("code.coding.code")
        await db.Observation.create_index("effectiveDateTime")
        await db.Observation.create_index("category.coding.code")
        
        # Practitioner indexes
        await db.Practitioner.create_index("id", unique=True)
        await db.Practitioner.create_index("identifier.value")
        
        # Organization indexes
        await db.Organization.create_index("id", unique=True)
        await db.Organization.create_index("identifier.value")
        await db.Organization.create_index("name")
        
        # Device indexes
        await db.Device.create_index("id", unique=True)
        await db.Device.create_index("identifier.value")
        
        # Encounter indexes
        await db.Encounter.create_index("id", unique=True)
        await db.Encounter.create_index("subject.reference")
        await db.Encounter.create_index("period.start")
        
        # DiagnosticReport indexes
        await db.DiagnosticReport.create_index("id", unique=True)
        await db.DiagnosticReport.create_index("subject.reference")
        await db.DiagnosticReport.create_index("code.coding.code")
        
        logger.info("✅ Created database indexes")
        
    except Exception as e:
        logger.warning(f"⚠️ Could not create indexes: {e}")


# Synchronous database client for testing
def get_sync_database():
    """
    Get synchronous database client (for testing/scripts)
    """
    client = MongoClient(settings.mongodb_url)
    return client[settings.mongodb_database]
