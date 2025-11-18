"""
Encounter Resource Router Template
FHIR R6 Encounter resource endpoints

INSTRUCTIONS:
1. Replace Encounter with the actual resource name (e.g., Practitioner, Device)
2. Replace encounter with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.encounter import Encounter
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.encounter import Encounter
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Encounter", response_model=Encounter, status_code=status.HTTP_201_CREATED)
async def create_encounter(
    encounter: Encounter,
    current_user = Depends(get_current_active_user)
):
    """Create a new Encounter resource"""
    db = get_database()
    
    if not encounter.id:
        encounter.id = f"encounter-{uuid.uuid4()}"
    
    existing = await db.Encounter.find_one({"id": encounter.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Encounter with id {encounter.id} already exists"
        )
    
    encounter_dict = encounter.dict()
    await db.Encounter.insert_one(encounter_dict)
    
    return encounter


@router.get("/Encounter/{encounter_id}", response_model=Encounter)
async def get_encounter(
    encounter_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Encounter resource by ID"""
    db = get_database()
    
    encounter = await db.Encounter.find_one({"id": encounter_id}, {"_id": 0})
    
    if not encounter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Encounter with id {encounter_id} not found"
        )
    
    return Encounter(**encounter)


@router.get("/Encounter", response_model=List[Encounter])
async def search_encounters(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Encounter resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Encounter.find(query, {"_id": 0}).skip(_offset).limit(_count)
    encounters = await cursor.to_list(length=_count)
    
    return [Encounter(**r) for r in encounters]


@router.put("/Encounter/{encounter_id}", response_model=Encounter)
async def update_encounter(
    encounter_id: str,
    encounter: Encounter,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Encounter resource"""
    db = get_database()
    
    existing = await db.Encounter.find_one({"id": encounter_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Encounter with id {encounter_id} not found"
        )
    
    encounter.id = encounter_id
    encounter_dict = encounter.dict()
    
    await db.Encounter.replace_one({"id": encounter_id}, encounter_dict)
    
    return encounter


@router.delete("/Encounter/{encounter_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_encounter(
    encounter_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Encounter resource"""
    db = get_database()
    
    result = await db.Encounter.delete_one({"id": encounter_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Encounter with id {encounter_id} not found"
        )
    
    return None
