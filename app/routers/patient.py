"""
Patient Resource Router
FHIR R6 Patient resource endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends, Body
from typing import List, Optional
from fhir.resources.patient import Patient
from fhir.resources.bundle import Bundle, BundleEntry
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Patient", status_code=status.HTTP_201_CREATED)
async def create_patient(
    patient_data: dict = Body(...),
    current_user = Depends(get_current_active_user)
):
    """
    Create a new Patient resource

    Creates a new patient record in the system.
    """
    db = get_database()

    # Generate ID if not provided
    if not patient_data.get("id"):
        patient_data["id"] = f"patient-{uuid.uuid4()}"

    # Check if patient already exists
    existing = await db.Patient.find_one({"id": patient_data["id"]})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Patient with id {patient_data['id']} already exists"
        )

    # Insert the patient data
    await db.Patient.insert_one(patient_data)

    return patient_data


@router.get("/Patient/{patient_id}", response_model=Patient)
async def get_patient(
    patient_id: str,
    current_user = Depends(get_current_active_user)
):
    """
    Retrieve a Patient resource by ID
    
    Returns a single patient resource.
    """
    db = get_database()
    
    patient = await db.Patient.find_one({"id": patient_id}, {"_id": 0})
    
    if not patient:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )
    
    return Patient(**patient)


@router.get("/Patient", response_model=List[Patient])
async def search_patients(
    name: Optional[str] = Query(None, description="Search by patient name"),
    family: Optional[str] = Query(None, description="Search by family name"),
    given: Optional[str] = Query(None, description="Search by given name"),
    identifier: Optional[str] = Query(None, description="Search by identifier value"),
    birthdate: Optional[str] = Query(None, description="Search by birth date (YYYY-MM-DD)"),
    gender: Optional[str] = Query(None, description="Search by gender"),
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """
    Search for Patient resources
    
    Supports multiple search parameters based on FHIR specification.
    """
    db = get_database()
    
    # Build search query
    query = {}
    
    if name or family:
        # Search in family name
        search_name = name or family
        query["name.family"] = {"$regex": search_name, "$options": "i"}
    
    if given:
        query["name.given"] = {"$regex": given, "$options": "i"}
    
    if identifier:
        query["identifier.value"] = identifier
    
    if birthdate:
        query["birthDate"] = birthdate
    
    if gender:
        query["gender"] = gender
    
    # Execute search with pagination
    cursor = db.Patient.find(query, {"_id": 0}).skip(_offset).limit(_count)
    patients = await cursor.to_list(length=_count)
    
    return [Patient(**p) for p in patients]


@router.put("/Patient/{patient_id}")
async def update_patient(
    patient_id: str,
    patient_data: dict = Body(...),
    current_user = Depends(get_current_active_user)
):
    """
    Update an existing Patient resource

    Replaces the entire patient resource with the provided data.
    """
    db = get_database()

    # Check if patient exists
    existing = await db.Patient.find_one({"id": patient_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )

    # Update patient
    patient_data["id"] = patient_id  # Ensure ID matches

    await db.Patient.replace_one({"id": patient_id}, patient_data)

    return patient_data


@router.delete("/Patient/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(
    patient_id: str,
    current_user = Depends(get_current_active_user)
):
    """
    Delete a Patient resource
    
    Permanently removes a patient record from the system.
    """
    db = get_database()
    
    result = await db.Patient.delete_one({"id": patient_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Patient with id {patient_id} not found"
        )
    
    return None
