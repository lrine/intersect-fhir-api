"""
Communication Resource Router Template
FHIR R6 Communication resource endpoints

INSTRUCTIONS:
1. Replace Communication with the actual resource name (e.g., Practitioner, Device)
2. Replace communication with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.communication import Communication
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.communication import Communication
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Communication", response_model=Communication, status_code=status.HTTP_201_CREATED)
async def create_communication(
    communication: Communication,
    current_user = Depends(get_current_active_user)
):
    """Create a new Communication resource"""
    db = get_database()
    
    if not communication.id:
        communication.id = f"communication-{uuid.uuid4()}"
    
    existing = await db.Communication.find_one({"id": communication.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Communication with id {communication.id} already exists"
        )
    
    communication_dict = communication.dict()
    await db.Communication.insert_one(communication_dict)
    
    return communication


@router.get("/Communication/{communication_id}", response_model=Communication)
async def get_communication(
    communication_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Communication resource by ID"""
    db = get_database()
    
    communication = await db.Communication.find_one({"id": communication_id}, {"_id": 0})
    
    if not communication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Communication with id {communication_id} not found"
        )
    
    return Communication(**communication)


@router.get("/Communication", response_model=List[Communication])
async def search_communications(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Communication resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Communication.find(query, {"_id": 0}).skip(_offset).limit(_count)
    communications = await cursor.to_list(length=_count)
    
    return [Communication(**r) for r in communications]


@router.put("/Communication/{communication_id}", response_model=Communication)
async def update_communication(
    communication_id: str,
    communication: Communication,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Communication resource"""
    db = get_database()
    
    existing = await db.Communication.find_one({"id": communication_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Communication with id {communication_id} not found"
        )
    
    communication.id = communication_id
    communication_dict = communication.dict()
    
    await db.Communication.replace_one({"id": communication_id}, communication_dict)
    
    return communication


@router.delete("/Communication/{communication_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_communication(
    communication_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Communication resource"""
    db = get_database()
    
    result = await db.Communication.delete_one({"id": communication_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Communication with id {communication_id} not found"
        )
    
    return None
