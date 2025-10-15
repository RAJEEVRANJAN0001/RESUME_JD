"""
Seed script to create a demo user account.
Run this script to create the default admin user.
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings
from app.auth import get_password_hash
from app.icons import WARNING_MSG, CHECK_MARK, WARNING
from datetime import datetime


async def seed_user():
    """Create default admin user."""
    print("[🌱] Seeding database with demo user...")
    
    # Connect to MongoDB
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    db = client[settings.DATABASE_NAME]
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": "admin@resumescreener.com"})
    
    if existing_user:
        print(f"{WARNING} Demo user already exists!")
        print("   Email: admin@resumescreener.com")
        return
    
    # Create user
    user_data = {
        "email": "admin@resumescreener.com",
        "hashed_password": get_password_hash("admin123"),
        "full_name": "Admin User",
        "is_active": True,
        "created_at": datetime.utcnow()
    }
    
    await db.users.insert_one(user_data)
    
    print(f"{CHECK_MARK} Demo user created successfully!")
    print("   Email: admin@resumescreener.com")
    print("   Password: admin123")
    print(f"\n{WARNING} IMPORTANT: Change this password in production!")
    
    # Close connection
    client.close()


if __name__ == "__main__":
    asyncio.run(seed_user())
