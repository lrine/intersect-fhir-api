"""
ServiceRequest Resource Router Template
FHIR R6 ServiceRequest resource endpoints

INSTRUCTIONS:
1. Replace ServiceRequest with the actual resource name (e.g., Practitioner, Device)
2. Replace servicerequest with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.servicerequest import ServiceRequest
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.servicerequest import ServiceRequest
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/ServiceRequest", response_model=ServiceRequest, status_code=status.HTTP_201_CREATED)
async def create_servicerequest(
    servicerequest: ServiceRequest,
    current_user = Depends(get_current_active_user)
):
    """Create a new ServiceRequest resource"""
    db = get_database()
    
    if not servicerequest.id:
        servicerequest.id = f"servicerequest-{uuid.uuid4()}"
    
    existing = await db.ServiceRequest.find_one({"id": servicerequest.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"ServiceRequest with id {servicerequest.id} already exists"
        )
    
    servicerequest_dict = servicerequest.dict()
    await db.ServiceRequest.insert_one(servicerequest_dict)
    
    return servicerequest


@router.get("/ServiceRequest/{servicerequest_id}", response_model=ServiceRequest)
async def get_servicerequest(
    servicerequest_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a ServiceRequest resource by ID"""
    db = get_database()
    
    servicerequest = await db.ServiceRequest.find_one({"id": servicerequest_id}, {"_id": 0})
    
    if not servicerequest:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ServiceRequest with id {servicerequest_id} not found"
        )
    
    return ServiceRequest(**servicerequest)


@router.get("/ServiceRequest", response_model=List[ServiceRequest])
async def search_servicerequests(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for ServiceRequest resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.ServiceRequest.find(query, {"_id": 0}).skip(_offset).limit(_count)
    servicerequests = await cursor.to_list(length=_count)
    
    return [ServiceRequest(**r) for r in servicerequests]


@router.put("/ServiceRequest/{servicerequest_id}", response_model=ServiceRequest)
async def update_servicerequest(
    servicerequest_id: str,
    servicerequest: ServiceRequest,
    current_user = Depends(get_current_active_user)
):
    """Update an existing ServiceRequest resource"""
    db = get_database()
    
    existing = await db.ServiceRequest.find_one({"id": servicerequest_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ServiceRequest with id {servicerequest_id} not found"
        )
    
    servicerequest.id = servicerequest_id
    servicerequest_dict = servicerequest.dict()
    
    await db.ServiceRequest.replace_one({"id": servicerequest_id}, servicerequest_dict)
    
    return servicerequest


@router.delete("/ServiceRequest/{servicerequest_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_servicerequest(
    servicerequest_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a ServiceRequest resource"""
    db = get_database()
    
    result = await db.ServiceRequest.delete_one({"id": servicerequest_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"ServiceRequest with id {servicerequest_id} not found"
        )
    
    return None
