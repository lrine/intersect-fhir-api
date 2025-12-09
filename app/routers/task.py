"""
Task Resource Router Template
FHIR R6 Task resource endpoints
"""

from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.task import Task
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Task", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    task: Task,
    current_user = Depends(get_current_active_user)
):
    """Create a new Task resource"""
    db = get_database()
    if not task.id:
        task.id = f"task-{uuid.uuid4()}"

    existing = await db.Task.find_one({"id": task.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Task with id {task.id} already exists"
        )

    task_dict = task.dict()
    await db.Task.insert_one(task_dict)

    return task


@router.get("/Task/{task_id}", response_model=Task)
async def get_task(
    task_id: str,
    current_user = Depends(get_current_active_user)
):
    """Get a Task resource by ID"""
    db = get_database()
    task = await db.Task.find_one({"id": task_id})
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    return Task.model_construct(**{k: v for k, v in task.items() if k != "_id"})


@router.get("/Task", response_model=List[Task])
async def search_tasks(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Task resources"""
    db = get_database()

    query = {}
    # Add search parameters based on FHIR spec

    cursor = db.Task.find(query, {"_id": 0}).skip(_offset).limit(_count)
    tasks = await cursor.to_list(length=_count)

    return [Task.model_construct(**{k: v for k, v in r.items() if k != "_id"}) for r in tasks]


@router.put("/Task/{task_id}", response_model=Task)
async def update_task(
    task_id: str,
    task: Task,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Task resource"""
    db = get_database()
    existing = await db.Task.find_one({"id": task_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    task.id = task_id
    task_dict = task.dict()

    await db.Task.replace_one({"id": task_id}, task_dict)

    return task


@router.delete("/Task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Task resource"""
    db = get_database()

    result = await db.Task.delete_one({"id": task_id})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id {task_id} not found"
        )

    return None
