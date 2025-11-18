"""
MedicationRequest Resource Router Template
FHIR R6 MedicationRequest resource endpoints

INSTRUCTIONS:
1. Replace MedicationRequest with the actual resource name (e.g., Practitioner, Device)
2. Replace medicationrequest with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.medicationrequest import MedicationRequest
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.medicationrequest import MedicationRequest
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/MedicationRequest", response_model=MedicationRequest, status_code=status.HTTP_201_CREATED)
async def create_medicationrequest(
    medicationrequest: MedicationRequest,
    current_user = Depends(get_current_active_user)
):
    """Create a new MedicationRequest resource"""
    db = get_database()
    
    if not medicationrequest.id:
        medicationrequest.id = f"medicationrequest-{uuid.uuid4()}"
    
    existing = await db.MedicationRequest.find_one({"id": medicationrequest.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"MedicationRequest with id {medicationrequest.id} already exists"
        )
    
    medicationrequest_dict = medicationrequest.dict()
    await db.MedicationRequest.insert_one(medicationrequest_dict)
    
    return medicationrequest


@router.get("/MedicationRequest/{medicationrequest_id}", response_model=MedicationRequest)
async def get_medicationrequest(
    medicationrequest_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a MedicationRequest resource by ID"""
    db = get_database()
    
    medicationrequest = await db.MedicationRequest.find_one({"id": medicationrequest_id}, {"_id": 0})
    
    if not medicationrequest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MedicationRequest with id {medicationrequest_id} not found"
        )
    
    return MedicationRequest(**medicationrequest)


@router.get("/MedicationRequest", response_model=List[MedicationRequest])
async def search_medicationrequests(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for MedicationRequest resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.MedicationRequest.find(query, {"_id": 0}).skip(_offset).limit(_count)
    medicationrequests = await cursor.to_list(length=_count)
    
    return [MedicationRequest(**r) for r in medicationrequests]


@router.put("/MedicationRequest/{medicationrequest_id}", response_model=MedicationRequest)
async def update_medicationrequest(
    medicationrequest_id: str,
    medicationrequest: MedicationRequest,
    current_user = Depends(get_current_active_user)
):
    """Update an existing MedicationRequest resource"""
    db = get_database()
    
    existing = await db.MedicationRequest.find_one({"id": medicationrequest_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MedicationRequest with id {medicationrequest_id} not found"
        )
    
    medicationrequest.id = medicationrequest_id
    medicationrequest_dict = medicationrequest.dict()
    
    await db.MedicationRequest.replace_one({"id": medicationrequest_id}, medicationrequest_dict)
    
    return medicationrequest


@router.delete("/MedicationRequest/{medicationrequest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medicationrequest(
    medicationrequest_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a MedicationRequest resource"""
    db = get_database()
    
    result = await db.MedicationRequest.delete_one({"id": medicationrequest_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"MedicationRequest with id {medicationrequest_id} not found"
        )
    
    return None
