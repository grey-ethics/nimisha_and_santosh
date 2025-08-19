"""
create_tables.py
----------------
Utility script to create all database tables for the FastAPI app
without using Alembic migrations.

This script:
1. Loads environment variables from `.env`
2. Uses SQLAlchemy engine defined in app/db/session.py
3. Imports Base (from app/db/base.py), which automatically registers all models
4. Calls Base.metadata.create_all() to create the tables in PostgreSQL

Usage:
    python create_tables.py
"""

import os
from dotenv import load_dotenv
from app.db.session import engine
from app.db.base import Base  # ensures all models are imported

def create_all_tables():
    print("🔄 Creating all tables in the database...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully!")

if __name__ == "__main__":
    # Load environment variables (ensures DATABASE_URL is available)
    load_dotenv()
    create_all_tables()
