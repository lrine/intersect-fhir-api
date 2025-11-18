"""
[RESOURCE] Resource Router Template
FHIR R6 [RESOURCE] resource endpoints

INSTRUCTIONS:
1. Replace [RESOURCE] with the actual resource name (e.g., Practitioner, Device)
2. Replace [resource] with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.[resource] import [RESOURCE]
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.[resource] import [RESOURCE]
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/[RESOURCE]", response_model=[RESOURCE], status_code=status.HTTP_201_CREATED)
async def create_[resource](
    [resource]: [RESOURCE],
    current_user = Depends(get_current_active_user)
):
    """Create a new [RESOURCE] resource"""
    db = get_database()
    
    if not [resource].id:
        [resource].id = f"[resource]-{uuid.uuid4()}"
    
    existing = await db.[RESOURCE].find_one({"id": [resource].id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"[RESOURCE] with id {[resource].id} already exists"
        )
    
    [resource]_dict = [resource].dict()
    await db.[RESOURCE].insert_one([resource]_dict)
    
    return [resource]


@router.get("/[RESOURCE]/{[resource]_id}", response_model=[RESOURCE])
async def get_[resource](
    [resource]_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a [RESOURCE] resource by ID"""
    db = get_database()
    
    [resource] = await db.[RESOURCE].find_one({"id": [resource]_id}, {"_id": 0})
    
    if not [resource]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"[RESOURCE] with id {[resource]_id} not found"
        )
    
    return [RESOURCE](**[resource])


@router.get("/[RESOURCE]", response_model=List[[RESOURCE]])
async def search_[resource]s(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for [RESOURCE] resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.[RESOURCE].find(query, {"_id": 0}).skip(_offset).limit(_count)
    [resource]s = await cursor.to_list(length=_count)
    
    return [[RESOURCE](**r) for r in [resource]s]


@router.put("/[RESOURCE]/{[resource]_id}", response_model=[RESOURCE])
async def update_[resource](
    [resource]_id: str,
    [resource]: [RESOURCE],
    current_user = Depends(get_current_active_user)
):
    """Update an existing [RESOURCE] resource"""
    db = get_database()
    
    existing = await db.[RESOURCE].find_one({"id": [resource]_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"[RESOURCE] with id {[resource]_id} not found"
        )
    
    [resource].id = [resource]_id
    [resource]_dict = [resource].dict()
    
    await db.[RESOURCE].replace_one({"id": [resource]_id}, [resource]_dict)
    
    return [resource]


@router.delete("/[RESOURCE]/{[resource]_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_[resource](
    [resource]_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a [RESOURCE] resource"""
    db = get_database()
    
    result = await db.[RESOURCE].delete_one({"id": [resource]_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"[RESOURCE] with id {[resource]_id} not found"
        )
    
    return None
