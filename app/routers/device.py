"""
Device Resource Router Template
FHIR R6 Device resource endpoints

INSTRUCTIONS:
1. Replace Device with the actual resource name (e.g., Practitioner, Device)
2. Replace device with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.device import Device
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.device import Device
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Device", response_model=Device, status_code=status.HTTP_201_CREATED)
async def create_device(
    device: Device,
    current_user = Depends(get_current_active_user)
):
    """Create a new Device resource"""
    db = get_database()
    
    if not device.id:
        device.id = f"device-{uuid.uuid4()}"
    
    existing = await db.Device.find_one({"id": device.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Device with id {device.id} already exists"
        )
    
    device_dict = device.dict()
    await db.Device.insert_one(device_dict)
    
    return device


@router.get("/Device/{device_id}", response_model=Device)
async def get_device(
    device_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Device resource by ID"""
    db = get_database()
    
    device = await db.Device.find_one({"id": device_id}, {"_id": 0})
    
    if not device:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with id {device_id} not found"
        )
    
    return Device(**device)


@router.get("/Device", response_model=List[Device])
async def search_devices(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Device resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Device.find(query, {"_id": 0}).skip(_offset).limit(_count)
    devices = await cursor.to_list(length=_count)
    
    return [Device(**r) for r in devices]


@router.put("/Device/{device_id}", response_model=Device)
async def update_device(
    device_id: str,
    device: Device,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Device resource"""
    db = get_database()
    
    existing = await db.Device.find_one({"id": device_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with id {device_id} not found"
        )
    
    device.id = device_id
    device_dict = device.dict()
    
    await db.Device.replace_one({"id": device_id}, device_dict)
    
    return device


@router.delete("/Device/{device_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_device(
    device_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Device resource"""
    db = get_database()
    
    result = await db.Device.delete_one({"id": device_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Device with id {device_id} not found"
        )
    
    return None
