"""
migrations/env.py

Alembic environment file.
Loads .env, wires up SQLAlchemy URL, exposes Base.metadata to Alembic,
and runs migrations in online/offline modes.
"""
import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- Make sure we can import the `app` package (project root = parent of migrations/) ---
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# --- Load environment variables from .env in project root ---
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# Alembic Config object (reads alembic.ini)
config = context.config

# If we got DATABASE_URL from .env, override alembic.ini's sqlalchemy.url
if DATABASE_URL:
    config.set_main_option("sqlalchemy.url", DATABASE_URL)

# Configure logging per alembic.ini
fileConfig(config.config_file_name)

# Import Base (declarative base only; models are imported separately)
from app.db.base import Base  # noqa: E402

# Ensure all models are imported so Base.metadata is populated for Alembic
import app.models  # noqa: F401,E402

# Tell Alembic which metadata to autogenerate from
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode (emit SQL without a DB connection)."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode (connect to DB and execute)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
