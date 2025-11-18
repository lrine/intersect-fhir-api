"""
Medication Resource Router Template
FHIR R6 Medication resource endpoints

INSTRUCTIONS:
1. Replace Medication with the actual resource name (e.g., Practitioner, Device)
2. Replace medication with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.medication import Medication
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.medication import Medication
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Medication", response_model=Medication, status_code=status.HTTP_201_CREATED)
async def create_medication(
    medication: Medication,
    current_user = Depends(get_current_active_user)
):
    """Create a new Medication resource"""
    db = get_database()
    
    if not medication.id:
        medication.id = f"medication-{uuid.uuid4()}"
    
    existing = await db.Medication.find_one({"id": medication.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Medication with id {medication.id} already exists"
        )
    
    medication_dict = medication.dict()
    await db.Medication.insert_one(medication_dict)
    
    return medication


@router.get("/Medication/{medication_id}", response_model=Medication)
async def get_medication(
    medication_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Medication resource by ID"""
    db = get_database()
    
    medication = await db.Medication.find_one({"id": medication_id}, {"_id": 0})
    
    if not medication:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medication with id {medication_id} not found"
        )
    
    return Medication(**medication)


@router.get("/Medication", response_model=List[Medication])
async def search_medications(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Medication resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Medication.find(query, {"_id": 0}).skip(_offset).limit(_count)
    medications = await cursor.to_list(length=_count)
    
    return [Medication(**r) for r in medications]


@router.put("/Medication/{medication_id}", response_model=Medication)
async def update_medication(
    medication_id: str,
    medication: Medication,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Medication resource"""
    db = get_database()
    
    existing = await db.Medication.find_one({"id": medication_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medication with id {medication_id} not found"
        )
    
    medication.id = medication_id
    medication_dict = medication.dict()
    
    await db.Medication.replace_one({"id": medication_id}, medication_dict)
    
    return medication


@router.delete("/Medication/{medication_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_medication(
    medication_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Medication resource"""
    db = get_database()
    
    result = await db.Medication.delete_one({"id": medication_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Medication with id {medication_id} not found"
        )
    
    return None
