from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# We pull this from environment variables so we don't hardcode secrets into GitHub
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@db:5432/compliance_db")

# SQL echo logging is useful in dev but noisy (and can leak query params into
# logs) in production. Off by default; opt in with SQL_ECHO=true.
SQL_ECHO = os.getenv("SQL_ECHO", "false").lower() == "true"

# Create the async engine (The actual engine that talks to PostgreSQL)
engine = create_async_engine(DATABASE_URL, echo=SQL_ECHO)

# Create a configured "Session" factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

# Base class for our models (This connects to the Base we used in models.py)
Base = declarative_base()


# Dependency to get a secure database session in our API routes
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session