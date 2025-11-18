"""
CareTeam Resource Router Template
FHIR R6 CareTeam resource endpoints

INSTRUCTIONS:
1. Replace CareTeam with the actual resource name (e.g., Practitioner, Device)
2. Replace careteam with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.careteam import CareTeam
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.careteam import CareTeam
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/CareTeam", response_model=CareTeam, status_code=status.HTTP_201_CREATED)
async def create_careteam(
    careteam: CareTeam,
    current_user = Depends(get_current_active_user)
):
    """Create a new CareTeam resource"""
    db = get_database()
    
    if not careteam.id:
        careteam.id = f"careteam-{uuid.uuid4()}"
    
    existing = await db.CareTeam.find_one({"id": careteam.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"CareTeam with id {careteam.id} already exists"
        )
    
    careteam_dict = careteam.dict()
    await db.CareTeam.insert_one(careteam_dict)
    
    return careteam


@router.get("/CareTeam/{careteam_id}", response_model=CareTeam)
async def get_careteam(
    careteam_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a CareTeam resource by ID"""
    db = get_database()
    
    careteam = await db.CareTeam.find_one({"id": careteam_id}, {"_id": 0})
    
    if not careteam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CareTeam with id {careteam_id} not found"
        )
    
    return CareTeam(**careteam)


@router.get("/CareTeam", response_model=List[CareTeam])
async def search_careteams(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for CareTeam resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.CareTeam.find(query, {"_id": 0}).skip(_offset).limit(_count)
    careteams = await cursor.to_list(length=_count)
    
    return [CareTeam(**r) for r in careteams]


@router.put("/CareTeam/{careteam_id}", response_model=CareTeam)
async def update_careteam(
    careteam_id: str,
    careteam: CareTeam,
    current_user = Depends(get_current_active_user)
):
    """Update an existing CareTeam resource"""
    db = get_database()
    
    existing = await db.CareTeam.find_one({"id": careteam_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CareTeam with id {careteam_id} not found"
        )
    
    careteam.id = careteam_id
    careteam_dict = careteam.dict()
    
    await db.CareTeam.replace_one({"id": careteam_id}, careteam_dict)
    
    return careteam


@router.delete("/CareTeam/{careteam_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_careteam(
    careteam_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a CareTeam resource"""
    db = get_database()
    
    result = await db.CareTeam.delete_one({"id": careteam_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"CareTeam with id {careteam_id} not found"
        )
    
    return None
