import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy import text, select
from sqlalchemy.ext.asyncio import AsyncSession

# Explicitly use absolute imports
from app.database import engine, Base, get_db
from app import models, schemas

@asynccontextmanager
async def lifespan(app: FastAPI):
    # This now forces the creation of tables using the unified Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
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
        raise HTTPException(status_code=503, detail="Database unavailable please check back later")


@app.post("/tasks/", response_model=schemas.TaskResponse)
async def create_task(task: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    # 1. Create a new database model using the data from the browser
    new_task = models.Task(
        title=task.title,
        description=task.description,
        status="Pending"  # Default status when a task is first created
    )
    # 2. Add it to the vault and save (commit) the changes
    db.add(new_task)
    await db.commit()
    await db.refresh(new_task)

    # 3. Return the newly created task back to the browser
    return new_task

@app.get("/tasks/", response_model=list[schemas.TaskResponse])
async def read_tasks(db: AsyncSession = Depends(get_db)):
    query = select(models.Task)
    result = await db.execute(query)
    tasks = result.scalars().all()
    return tasks

@app.put("/tasks/{task_id}", response_model=schemas.TaskResponse)
async def update_task(task_id: int, task_update: schemas.TaskCreate, db: AsyncSession = Depends(get_db)):
    query = select(models.Task).where(models.Task.id == task_id)
    result = await db.execute(query)

    db_task = result.scalar_one_or_none()

    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.title = task_update.title
    db_task.description = task_update.description
    db_task.status = task_update.status

    await db.commit()
    await db.refresh(db_task)

    return db_task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)):
    query = select(models.Task).where(models.Task.id == task_id)
    result = await db.execute(query)

    db_task = result.scalar_one_or_none()
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(db_task)
    await db.commit()

    return {"status": "success", "message": "Task deleted"}