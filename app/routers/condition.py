"""
Condition Resource Router Template
FHIR R6 Condition resource endpoints

INSTRUCTIONS:
1. Replace Condition with the actual resource name (e.g., Practitioner, Device)
2. Replace condition with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.condition import Condition
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.condition import Condition
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Condition", response_model=Condition, status_code=status.HTTP_201_CREATED)
async def create_condition(
    condition: Condition,
    current_user = Depends(get_current_active_user)
):
    """Create a new Condition resource"""
    db = get_database()
    
    if not condition.id:
        condition.id = f"condition-{uuid.uuid4()}"
    
    existing = await db.Condition.find_one({"id": condition.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Condition with id {condition.id} already exists"
        )
    
    condition_dict = condition.dict()
    await db.Condition.insert_one(condition_dict)
    
    return condition


@router.get("/Condition/{condition_id}", response_model=Condition)
async def get_condition(
    condition_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Condition resource by ID"""
    db = get_database()
    
    condition = await db.Condition.find_one({"id": condition_id}, {"_id": 0})
    
    if not condition:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Condition with id {condition_id} not found"
        )
    
    return Condition(**condition)


@router.get("/Condition", response_model=List[Condition])
async def search_conditions(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Condition resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Condition.find(query, {"_id": 0}).skip(_offset).limit(_count)
    conditions = await cursor.to_list(length=_count)
    
    return [Condition(**r) for r in conditions]


@router.put("/Condition/{condition_id}", response_model=Condition)
async def update_condition(
    condition_id: str,
    condition: Condition,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Condition resource"""
    db = get_database()
    
    existing = await db.Condition.find_one({"id": condition_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Condition with id {condition_id} not found"
        )
    
    condition.id = condition_id
    condition_dict = condition.dict()
    
    await db.Condition.replace_one({"id": condition_id}, condition_dict)
    
    return condition


@router.delete("/Condition/{condition_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_condition(
    condition_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Condition resource"""
    db = get_database()
    
    result = await db.Condition.delete_one({"id": condition_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Condition with id {condition_id} not found"
        )
    
    return None
