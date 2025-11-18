"""
AllergyIntolerance Resource Router Template
FHIR R6 AllergyIntolerance resource endpoints

INSTRUCTIONS:
1. Replace AllergyIntolerance with the actual resource name (e.g., Practitioner, Device)
2. Replace allergyintolerance with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.allergyintolerance import AllergyIntolerance
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.allergyintolerance import AllergyIntolerance
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/AllergyIntolerance", response_model=AllergyIntolerance, status_code=status.HTTP_201_CREATED)
async def create_allergyintolerance(
    allergyintolerance: AllergyIntolerance,
    current_user = Depends(get_current_active_user)
):
    """Create a new AllergyIntolerance resource"""
    db = get_database()
    
    if not allergyintolerance.id:
        allergyintolerance.id = f"allergyintolerance-{uuid.uuid4()}"
    
    existing = await db.AllergyIntolerance.find_one({"id": allergyintolerance.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"AllergyIntolerance with id {allergyintolerance.id} already exists"
        )
    
    allergyintolerance_dict = allergyintolerance.dict()
    await db.AllergyIntolerance.insert_one(allergyintolerance_dict)
    
    return allergyintolerance


@router.get("/AllergyIntolerance/{allergyintolerance_id}", response_model=AllergyIntolerance)
async def get_allergyintolerance(
    allergyintolerance_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a AllergyIntolerance resource by ID"""
    db = get_database()
    
    allergyintolerance = await db.AllergyIntolerance.find_one({"id": allergyintolerance_id}, {"_id": 0})
    
    if not allergyintolerance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AllergyIntolerance with id {allergyintolerance_id} not found"
        )
    
    return AllergyIntolerance(**allergyintolerance)


@router.get("/AllergyIntolerance", response_model=List[AllergyIntolerance])
async def search_allergyintolerances(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for AllergyIntolerance resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.AllergyIntolerance.find(query, {"_id": 0}).skip(_offset).limit(_count)
    allergyintolerances = await cursor.to_list(length=_count)
    
    return [AllergyIntolerance(**r) for r in allergyintolerances]


@router.put("/AllergyIntolerance/{allergyintolerance_id}", response_model=AllergyIntolerance)
async def update_allergyintolerance(
    allergyintolerance_id: str,
    allergyintolerance: AllergyIntolerance,
    current_user = Depends(get_current_active_user)
):
    """Update an existing AllergyIntolerance resource"""
    db = get_database()
    
    existing = await db.AllergyIntolerance.find_one({"id": allergyintolerance_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AllergyIntolerance with id {allergyintolerance_id} not found"
        )
    
    allergyintolerance.id = allergyintolerance_id
    allergyintolerance_dict = allergyintolerance.dict()
    
    await db.AllergyIntolerance.replace_one({"id": allergyintolerance_id}, allergyintolerance_dict)
    
    return allergyintolerance


@router.delete("/AllergyIntolerance/{allergyintolerance_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_allergyintolerance(
    allergyintolerance_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a AllergyIntolerance resource"""
    db = get_database()
    
    result = await db.AllergyIntolerance.delete_one({"id": allergyintolerance_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"AllergyIntolerance with id {allergyintolerance_id} not found"
        )
    
    return None
