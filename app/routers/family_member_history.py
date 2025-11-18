"""
FamilyMemberHistory Resource Router Template
FHIR R6 FamilyMemberHistory resource endpoints

INSTRUCTIONS:
1. Replace FamilyMemberHistory with the actual resource name (e.g., Practitioner, Device)
2. Replace familymemberhistory with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.familymemberhistory import FamilyMemberHistory
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.familymemberhistory import FamilyMemberHistory
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/FamilyMemberHistory", response_model=FamilyMemberHistory, status_code=status.HTTP_201_CREATED)
async def create_familymemberhistory(
    familymemberhistory: FamilyMemberHistory,
    current_user = Depends(get_current_active_user)
):
    """Create a new FamilyMemberHistory resource"""
    db = get_database()
    
    if not familymemberhistory.id:
        familymemberhistory.id = f"familymemberhistory-{uuid.uuid4()}"
    
    existing = await db.FamilyMemberHistory.find_one({"id": familymemberhistory.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"FamilyMemberHistory with id {familymemberhistory.id} already exists"
        )
    
    familymemberhistory_dict = familymemberhistory.dict()
    await db.FamilyMemberHistory.insert_one(familymemberhistory_dict)
    
    return familymemberhistory


@router.get("/FamilyMemberHistory/{familymemberhistory_id}", response_model=FamilyMemberHistory)
async def get_familymemberhistory(
    familymemberhistory_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a FamilyMemberHistory resource by ID"""
    db = get_database()
    
    familymemberhistory = await db.FamilyMemberHistory.find_one({"id": familymemberhistory_id}, {"_id": 0})
    
    if not familymemberhistory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FamilyMemberHistory with id {familymemberhistory_id} not found"
        )
    
    return FamilyMemberHistory(**familymemberhistory)


@router.get("/FamilyMemberHistory", response_model=List[FamilyMemberHistory])
async def search_familymemberhistorys(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for FamilyMemberHistory resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.FamilyMemberHistory.find(query, {"_id": 0}).skip(_offset).limit(_count)
    familymemberhistorys = await cursor.to_list(length=_count)
    
    return [FamilyMemberHistory(**r) for r in familymemberhistorys]


@router.put("/FamilyMemberHistory/{familymemberhistory_id}", response_model=FamilyMemberHistory)
async def update_familymemberhistory(
    familymemberhistory_id: str,
    familymemberhistory: FamilyMemberHistory,
    current_user = Depends(get_current_active_user)
):
    """Update an existing FamilyMemberHistory resource"""
    db = get_database()
    
    existing = await db.FamilyMemberHistory.find_one({"id": familymemberhistory_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FamilyMemberHistory with id {familymemberhistory_id} not found"
        )
    
    familymemberhistory.id = familymemberhistory_id
    familymemberhistory_dict = familymemberhistory.dict()
    
    await db.FamilyMemberHistory.replace_one({"id": familymemberhistory_id}, familymemberhistory_dict)
    
    return familymemberhistory


@router.delete("/FamilyMemberHistory/{familymemberhistory_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_familymemberhistory(
    familymemberhistory_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a FamilyMemberHistory resource"""
    db = get_database()
    
    result = await db.FamilyMemberHistory.delete_one({"id": familymemberhistory_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"FamilyMemberHistory with id {familymemberhistory_id} not found"
        )
    
    return None
