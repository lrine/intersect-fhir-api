"""
Specimen Resource Router Template
FHIR R6 Specimen resource endpoints

INSTRUCTIONS:
1. Replace Specimen with the actual resource name (e.g., Practitioner, Device)
2. Replace specimen with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.specimen import Specimen
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.specimen import Specimen
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Specimen", response_model=Specimen, status_code=status.HTTP_201_CREATED)
async def create_specimen(
    specimen: Specimen,
    current_user = Depends(get_current_active_user)
):
    """Create a new Specimen resource"""
    db = get_database()
    
    if not specimen.id:
        specimen.id = f"specimen-{uuid.uuid4()}"
    
    existing = await db.Specimen.find_one({"id": specimen.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Specimen with id {specimen.id} already exists"
        )
    
    specimen_dict = specimen.dict()
    await db.Specimen.insert_one(specimen_dict)
    
    return specimen


@router.get("/Specimen/{specimen_id}", response_model=Specimen)
async def get_specimen(
    specimen_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Specimen resource by ID"""
    db = get_database()
    
    specimen = await db.Specimen.find_one({"id": specimen_id}, {"_id": 0})
    
    if not specimen:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specimen with id {specimen_id} not found"
        )
    
    return Specimen(**specimen)


@router.get("/Specimen", response_model=List[Specimen])
async def search_specimens(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Specimen resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Specimen.find(query, {"_id": 0}).skip(_offset).limit(_count)
    specimens = await cursor.to_list(length=_count)
    
    return [Specimen(**r) for r in specimens]


@router.put("/Specimen/{specimen_id}", response_model=Specimen)
async def update_specimen(
    specimen_id: str,
    specimen: Specimen,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Specimen resource"""
    db = get_database()
    
    existing = await db.Specimen.find_one({"id": specimen_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specimen with id {specimen_id} not found"
        )
    
    specimen.id = specimen_id
    specimen_dict = specimen.dict()
    
    await db.Specimen.replace_one({"id": specimen_id}, specimen_dict)
    
    return specimen


@router.delete("/Specimen/{specimen_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specimen(
    specimen_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Specimen resource"""
    db = get_database()
    
    result = await db.Specimen.delete_one({"id": specimen_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Specimen with id {specimen_id} not found"
        )
    
    return None
