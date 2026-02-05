"""
Todo Evolution API - FastAPI Backend
Deployed on Render with Neon PostgreSQL
"""
import os
from datetime import datetime
from contextlib import asynccontextmanager
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Import environment variables
from dotenv import load_dotenv
load_dotenv()

# Database setup
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(DATABASE_URL) if DATABASE_URL else None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) if engine else None
Base = declarative_base()

# Database Models
class UserDB(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    email_verified = Column(Boolean, default=False)
    image = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TaskDB(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String, default="pending")
    priority = Column(String, default="medium")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    due_date = Column(DateTime, nullable=True)
    user_id = Column(String, index=True)
    recursion = Column(String, nullable=True)  # daily, weekly, monthly
    category = Column(String, default="General")
    tags = Column(String, nullable=True)  # comma-separated tags
    is_deleted = Column(Boolean, default=False)  # Soft delete flag
    deleted_at = Column(DateTime, nullable=True)  # Timestamp when deleted


# Trash/Bin Model for deleted tasks
class TrashDB(Base):
    __tablename__ = "trash"
    
    id = Column(String, primary_key=True, index=True)
    task_id = Column(String, index=True)  # Original task ID
    title = Column(String, nullable=False)
    description = Column(String)
    status = Column(String)
    priority = Column(String)
    created_at = Column(DateTime)
    deleted_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, index=True)
    recursion = Column(String, nullable=True)
    category = Column(String)
    tags = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)

# Create tables
if engine:
    Base.metadata.create_all(bind=engine)
    print("Database tables ready")

# Dependency to get DB session
def get_db():
    if SessionLocal is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Health check response model
class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str = "1.0.0"
    environment: str

# Application state
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Log environment info
    environment = os.getenv("ENVIRONMENT", "development")
    print(f"Starting Todo Evolution API in {environment} mode")
    print(f"Python version: {__import__('sys').version}")
    yield
    # Shutdown
    print("Shutting down Todo Evolution API")

# Create FastAPI application
app = FastAPI(
    title="Todo Evolution API",
    description="REST API for Todo Evolution application with FastAPI and SQLModel",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/red",
)

# CORS Configuration
# Allow all localhost ports for development and specific origins for production
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "http://localhost:3002",
    "http://localhost:3003",
    "http://localhost:3004",
    "http://localhost:3005",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3005",
    # Vercel deployments - Main domain
#     "https://hackathon-2-phase-ii-full-stack-web-app.vercel.app",
#     "https://todo-evolution.vercel.app",
]

# Add custom origins from environment
extra_origins = os.getenv("CORS_ORIGINS", "")
if extra_origins:
    CORS_ORIGINS.extend(extra_origins.split(","))

# Add wildcard for Vercel preview deployments
CORS_ORIGINS.append("https://*.vercel.app")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for maximum compatibility
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH", "HEAD"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=[
        "Content-Length",
        "Content-Type",
        "Access-Control-Allow-Origin",
        "Access-Control-Allow-Credentials",
    ],
    max_age=3600,  # Cache preflight requests for 1 hour
)


# ============================================
# Health Check Endpoint (Render Health Check)
# ============================================
@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """
    Health check endpoint for Render deployment.
    Used by Render's health check system to verify the service is running.
    """
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0",
        environment=os.getenv("ENVIRONMENT", "development")
    )


# ============================================
# Root Endpoint
# ============================================
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Todo Evolution API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


# ============================================
# Example Todo Models (placeholder for future implementation)
# ============================================
class UserCreate(BaseModel):
    id: str
    name: str
    email: str
    email_verified: bool = False
    image: str | None = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    email_verified: bool
    image: str | None
    created_at: str
    updated_at: str


class TodoCreate(BaseModel):
    title: str
    description: str | None = None
    priority: str = "medium"
    status: str = "pending"
    due_date: str | None = None
    recursion: str | None = None
    category: str = "General"
    tags: List[str] = []
    user_id: str | None = None


class TodoUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    status: str | None = None
    priority: str | None = None
    due_date: str | None = None
    recursion: str | None = None
    category: str | None = None
    tags: List[str] | None = None
    is_deleted: bool | None = None


class TodoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    completed: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ============================================
# User Endpoints
# ============================================

@app.post("/users/sync", tags=["Users"], status_code=status.HTTP_200_OK)
async def sync_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """Sync user from frontend to backend database."""
    # Check if user already exists
    existing_user = db.query(UserDB).filter(UserDB.id == user_data.id).first()
    
    if existing_user:
        # Update existing user
        existing_user.name = user_data.name
        existing_user.email = user_data.email
        existing_user.email_verified = user_data.email_verified
        existing_user.image = user_data.image
        existing_user.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(existing_user)
        
        return {
            "id": existing_user.id,
            "name": existing_user.name,
            "email": existing_user.email,
            "email_verified": existing_user.email_verified,
            "image": existing_user.image,
            "created_at": existing_user.created_at.isoformat(),
            "updated_at": existing_user.updated_at.isoformat()
        }
    else:
        # Create new user
        new_user = UserDB(
            id=user_data.id,
            name=user_data.name,
            email=user_data.email,
            email_verified=user_data.email_verified,
            image=user_data.image,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        return {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email,
            "email_verified": new_user.email_verified,
            "image": new_user.image,
            "created_at": new_user.created_at.isoformat(),
            "updated_at": new_user.updated_at.isoformat()
        }


@app.get("/users/{user_id}", tags=["Users"])
async def get_user(user_id: str, db: Session = Depends(get_db)):
    """Get user details by ID."""
    user = db.query(UserDB).filter(UserDB.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "email_verified": user.email_verified,
        "image": user.image,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat()
    }


# ============================================
# Example Task Endpoints (ready for Phase 4 implementation)
# ============================================
# TODO: Implement CRUD endpoints with SQLModel and JWT authentication
# - GET /tasks/ - List all tasks
# - POST /tasks/ - Create new task
# - GET /tasks/{id} - Get specific task
# - PUT /tasks/{id} - Update task
# - DELETE /tasks/{id} - Delete task

@app.get("/tasks/", tags=["Tasks"])
async def list_tasks(
    user_id: str | None = None,
    status: str | None = None,
    priority: str | None = None,
    sort_by: str = "created_at",
    order: str = "desc",
    db: Session = Depends(get_db)
):
    """List all tasks from database with optional filters (excluding deleted)."""
    query = db.query(TaskDB).filter(TaskDB.is_deleted == False)  # Exclude deleted tasks
    
    # Filter by user_id
    if user_id:
        query = query.filter(TaskDB.user_id == user_id)
    
    # Filter by status
    if status:
        query = query.filter(TaskDB.status == status)
    
    # Filter by priority
    if priority:
        query = query.filter(TaskDB.priority == priority)
    
    # Sort
    if sort_by == "created_at":
        if order == "desc":
            query = query.order_by(TaskDB.created_at.desc())
        else:
            query = query.order_by(TaskDB.created_at.asc())
    elif sort_by == "due_date":
        if order == "desc":
            query = query.order_by(TaskDB.due_date.desc())
        else:
            query = query.order_by(TaskDB.due_date.asc())
    elif sort_by == "priority":
        # Custom priority order
        query = query.order_by(TaskDB.priority)
    
    tasks = query.all()
    
    # Convert to response format
    result = []
    for task in tasks:
        result.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "createdAt": task.created_at.isoformat() if task.created_at else None,
            "updatedAt": task.updated_at.isoformat() if task.updated_at else None,
            "dueDate": task.due_date.isoformat() if task.due_date else None,
            "userId": task.user_id,
            "recursion": task.recursion,
            "category": task.category or "General",
            "tags": task.tags.split(",") if task.tags else []
        })
    
    return result


@app.post("/tasks/", tags=["Tasks"], status_code=status.HTTP_201_CREATED)
async def create_task(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new task and save to database."""
    import uuid
    
    # Parse due_date if provided
    due_date = None
    if todo.due_date:
        try:
            due_date = datetime.fromisoformat(todo.due_date.replace('Z', '+00:00'))
        except:
            pass
    
    # Create task in database
    db_task = TaskDB(
        id=str(uuid.uuid4()),
        title=todo.title,
        description=todo.description,
        status=todo.status,
        priority=todo.priority,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        due_date=due_date,
        user_id=todo.user_id or "anonymous",
        recursion=todo.recursion,
        category=todo.category,
        tags=",".join(todo.tags) if todo.tags else None
    )
    
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Return task data
    return {
        "id": db_task.id,
        "title": db_task.title,
        "description": db_task.description,
        "status": db_task.status,
        "priority": db_task.priority,
        "createdAt": db_task.created_at.isoformat(),
        "updatedAt": db_task.updated_at.isoformat(),
        "dueDate": db_task.due_date.isoformat() if db_task.due_date else None,
        "userId": db_task.user_id,
        "recursion": db_task.recursion,
        "category": db_task.category,
        "tags": db_task.tags.split(",") if db_task.tags else []
    }


@app.get("/tasks/{task_id}", tags=["Tasks"])
async def get_task(task_id: str, user_id: str | None = None, db: Session = Depends(get_db)):
    """Get a specific task by ID."""
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Verify user ownership if user_id provided
    if user_id and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this task")
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "createdAt": task.created_at.isoformat() if task.created_at else None,
        "updatedAt": task.updated_at.isoformat() if task.updated_at else None,
        "dueDate": task.due_date.isoformat() if task.due_date else None,
        "userId": task.user_id,
        "recursion": task.recursion,
        "category": task.category,
        "tags": task.tags.split(",") if task.tags else []
    }


@app.put("/tasks/{task_id}", tags=["Tasks"])
async def update_task(task_id: str, todo: TodoUpdate, user_id: str | None = None, db: Session = Depends(get_db)):
    """Update a task."""
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Verify user ownership if user_id provided
    if user_id and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")
    
    # Update fields if provided
    if todo.title is not None:
        task.title = todo.title
    if todo.description is not None:
        task.description = todo.description
    if todo.status is not None:
        task.status = todo.status
    if todo.completed is not None:
        task.status = "completed" if todo.completed else "pending"
    if todo.priority is not None:
        task.priority = todo.priority
    if todo.due_date is not None:
        try:
            task.due_date = datetime.fromisoformat(todo.due_date.replace('Z', '+00:00'))
        except:
            pass
    if todo.recursion is not None:
        task.recursion = todo.recursion
    if todo.category is not None:
        task.category = todo.category
    if todo.tags is not None:
        task.tags = ",".join(todo.tags)
    
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    
    return {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "status": task.status,
        "priority": task.priority,
        "createdAt": task.created_at.isoformat() if task.created_at else None,
        "updatedAt": task.updated_at.isoformat() if task.updated_at else None,
        "dueDate": task.due_date.isoformat() if task.due_date else None,
        "userId": task.user_id,
        "recursion": task.recursion,
        "category": task.category,
        "tags": task.tags.split(",") if task.tags else []
    }


@app.delete("/tasks/{task_id}", tags=["Tasks"])
async def delete_task(task_id: str, user_id: str | None = None, db: Session = Depends(get_db)):
    """Move task to trash/bin (soft delete)."""
    task = db.query(TaskDB).filter(TaskDB.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Verify user ownership if user_id provided
    if user_id and task.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    # Move to trash
    import uuid
    trash_item = TrashDB(
        id=str(uuid.uuid4()),
        task_id=task.id,
        title=task.title,
        description=task.description,
        status=task.status,
        priority=task.priority,
        created_at=task.created_at,
        deleted_at=datetime.utcnow(),
        user_id=task.user_id,
        recursion=task.recursion,
        category=task.category,
        tags=task.tags,
        due_date=task.due_date
    )
    db.add(trash_item)
    
    # Soft delete the task
    task.is_deleted = True
    task.deleted_at = datetime.utcnow()
    
    db.commit()
    
    return {"message": "Task moved to trash", "id": task_id}


@app.get("/trash/", tags=["Trash"])
async def list_trash(user_id: str | None = None, db: Session = Depends(get_db)):
    """Get all items in trash/bin."""
    query = db.query(TrashDB)
    
    if user_id:
        query = query.filter(TrashDB.user_id == user_id)
    
    items = query.order_by(TrashDB.deleted_at.desc()).all()
    
    result = []
    for item in items:
        result.append({
            "id": item.id,
            "task_id": item.task_id,
            "title": item.title,
            "description": item.description,
            "status": item.status,
            "priority": item.priority,
            "created_at": item.created_at.isoformat() if item.created_at else None,
            "deleted_at": item.deleted_at.isoformat() if item.deleted_at else None,
            "user_id": item.user_id,
            "recursion": item.recursion,
            "category": item.category,
            "tags": item.tags.split(",") if item.tags else [],
            "due_date": item.due_date.isoformat() if item.due_date else None
        })
    
    return result


@app.post("/trash/{trash_id}/restore", tags=["Trash"])
async def restore_from_trash(trash_id: str, db: Session = Depends(get_db)):
    """Restore a task from trash."""
    trash_item = db.query(TrashDB).filter(TrashDB.id == trash_id).first()
    if not trash_item:
        raise HTTPException(status_code=404, detail="Trash item not found")
    
    # Find the soft-deleted task
    task = db.query(TaskDB).filter(TaskDB.id == trash_item.task_id).first()
    if task:
        # Restore the task
        task.is_deleted = False
        task.deleted_at = None
        
        # Remove from trash
        db.delete(trash_item)
        db.commit()
        
        return {"message": "Task restored successfully", "id": task.id}
    else:
        raise HTTPException(status_code=404, detail="Original task not found")


@app.delete("/trash/{trash_id}/permanent", tags=["Trash"])
async def permanent_delete(trash_id: str, db: Session = Depends(get_db)):
    """Permanently delete a task from trash."""
    trash_item = db.query(TrashDB).filter(TrashDB.id == trash_id).first()
    if not trash_item:
        raise HTTPException(status_code=404, detail="Trash item not found")
    
    # Permanently delete the task
    task = db.query(TaskDB).filter(TaskDB.id == trash_item.task_id).first()
    if task:
        db.delete(task)
    
    # Remove from trash
    db.delete(trash_item)
    db.commit()
    
    return {"message": "Task permanently deleted", "id": trash_id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8001))
    uvicorn.run(app, host="0.0.0.0", port=port)
