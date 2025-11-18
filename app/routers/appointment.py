"""
Appointment Resource Router Template
FHIR R6 Appointment resource endpoints

INSTRUCTIONS:
1. Replace Appointment with the actual resource name (e.g., Practitioner, Device)
2. Replace appointment with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.appointment import Appointment
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.appointment import Appointment
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Appointment", response_model=Appointment, status_code=status.HTTP_201_CREATED)
async def create_appointment(
    appointment: Appointment,
    current_user = Depends(get_current_active_user)
):
    """Create a new Appointment resource"""
    db = get_database()
    
    if not appointment.id:
        appointment.id = f"appointment-{uuid.uuid4()}"
    
    existing = await db.Appointment.find_one({"id": appointment.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Appointment with id {appointment.id} already exists"
        )
    
    appointment_dict = appointment.dict()
    await db.Appointment.insert_one(appointment_dict)
    
    return appointment


@router.get("/Appointment/{appointment_id}", response_model=Appointment)
async def get_appointment(
    appointment_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Appointment resource by ID"""
    db = get_database()
    
    appointment = await db.Appointment.find_one({"id": appointment_id}, {"_id": 0})
    
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with id {appointment_id} not found"
        )
    
    return Appointment(**appointment)


@router.get("/Appointment", response_model=List[Appointment])
async def search_appointments(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Appointment resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Appointment.find(query, {"_id": 0}).skip(_offset).limit(_count)
    appointments = await cursor.to_list(length=_count)
    
    return [Appointment(**r) for r in appointments]


@router.put("/Appointment/{appointment_id}", response_model=Appointment)
async def update_appointment(
    appointment_id: str,
    appointment: Appointment,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Appointment resource"""
    db = get_database()
    
    existing = await db.Appointment.find_one({"id": appointment_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with id {appointment_id} not found"
        )
    
    appointment.id = appointment_id
    appointment_dict = appointment.dict()
    
    await db.Appointment.replace_one({"id": appointment_id}, appointment_dict)
    
    return appointment


@router.delete("/Appointment/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_appointment(
    appointment_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Appointment resource"""
    db = get_database()
    
    result = await db.Appointment.delete_one({"id": appointment_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Appointment with id {appointment_id} not found"
        )
    
    return None
