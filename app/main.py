from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager
import os

from app.database import engine, Base, get_db
import app.models  # We import this so SQLAlchemy knows your tables exist before creating them

# Lifecycle Management (The Boot Sequence)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # What happens when you turn the server ON:
    # We securely log into PostgreSQL and tell it to build your 7 tables.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # What happens when you turn the server OFF:
    await engine.dispose()

# App Initialization
app = FastAPI(
    title="Bookr Compliance API",
    description="Enterprise-grade regulatory compliance tracker",
    version="1.0.0",
    lifespan=lifespan
)

# Frontend Integration (Working with the HTML)
# Find the absolute path to your 'static' folder
STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")

# Tell FastAPI to allow the browser to load your CSS, JS, and Images
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def serve_dashboard():
    # This routes users to your actual UI when they visit localhost:8000
    index_path = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "API is live, but index.html was not found in app/static."}

# Diagnostics & Routes
@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # A diagnostic route to verify database connectivity
    try:
        # The app tries to "ping" the database
        await db.execute(text("SELECT 1"))
        return {
            "status": "secure",
            "database": "connected",
            "environment": "production-ready"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database connection failed")