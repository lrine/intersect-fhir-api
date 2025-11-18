"""
Immunization Resource Router Template
FHIR R6 Immunization resource endpoints

INSTRUCTIONS:
1. Replace Immunization with the actual resource name (e.g., Practitioner, Device)
2. Replace immunization with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.immunization import Immunization
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.immunization import Immunization
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Immunization", response_model=Immunization, status_code=status.HTTP_201_CREATED)
async def create_immunization(
    immunization: Immunization,
    current_user = Depends(get_current_active_user)
):
    """Create a new Immunization resource"""
    db = get_database()
    
    if not immunization.id:
        immunization.id = f"immunization-{uuid.uuid4()}"
    
    existing = await db.Immunization.find_one({"id": immunization.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Immunization with id {immunization.id} already exists"
        )
    
    immunization_dict = immunization.dict()
    await db.Immunization.insert_one(immunization_dict)
    
    return immunization


@router.get("/Immunization/{immunization_id}", response_model=Immunization)
async def get_immunization(
    immunization_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Immunization resource by ID"""
    db = get_database()
    
    immunization = await db.Immunization.find_one({"id": immunization_id}, {"_id": 0})
    
    if not immunization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Immunization with id {immunization_id} not found"
        )
    
    return Immunization(**immunization)


@router.get("/Immunization", response_model=List[Immunization])
async def search_immunizations(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Immunization resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Immunization.find(query, {"_id": 0}).skip(_offset).limit(_count)
    immunizations = await cursor.to_list(length=_count)
    
    return [Immunization(**r) for r in immunizations]


@router.put("/Immunization/{immunization_id}", response_model=Immunization)
async def update_immunization(
    immunization_id: str,
    immunization: Immunization,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Immunization resource"""
    db = get_database()
    
    existing = await db.Immunization.find_one({"id": immunization_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Immunization with id {immunization_id} not found"
        )
    
    immunization.id = immunization_id
    immunization_dict = immunization.dict()
    
    await db.Immunization.replace_one({"id": immunization_id}, immunization_dict)
    
    return immunization


@router.delete("/Immunization/{immunization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_immunization(
    immunization_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Immunization resource"""
    db = get_database()
    
    result = await db.Immunization.delete_one({"id": immunization_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Immunization with id {immunization_id} not found"
        )
    
    return None
