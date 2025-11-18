"""
Observation Resource Router
FHIR R6 Observation resource endpoints with wearable integration
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.observation import Observation
import uuid
from datetime import datetime

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Observation", response_model=Observation, status_code=status.HTTP_201_CREATED)
async def create_observation(
    observation: Observation,
    current_user = Depends(get_current_active_user)
):
    """
    Create a new Observation resource
    
    Creates observations from wearables, lab results, or clinical assessments.
    """
    db = get_database()
    
    # Validate required fields
    if not observation.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="status is required"
        )
    
    if not observation.code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="code is required"
        )
    
    # Generate ID if not provided
    if not observation.id:
        observation.id = f"observation-{uuid.uuid4()}"
    
    # Check if observation already exists
    existing = await db.Observation.find_one({"id": observation.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Observation with id {observation.id} already exists"
        )
    
    # Convert to dict and insert
    observation_dict = observation.dict()
    await db.Observation.insert_one(observation_dict)
    
    return observation


@router.get("/Observation/{observation_id}", response_model=Observation)
async def get_observation(
    observation_id: str,
    current_user = Depends(get_current_active_user)
):
    """
    Retrieve an Observation resource by ID
    """
    db = get_database()
    
    observation = await db.Observation.find_one({"id": observation_id}, {"_id": 0})
    
    if not observation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Observation with id {observation_id} not found"
        )
    
    return Observation(**observation)


@router.get("/Observation", response_model=List[Observation])
async def search_observations(
    patient: Optional[str] = Query(None, description="Search by patient reference (e.g., Patient/123)"),
    subject: Optional[str] = Query(None, description="Search by subject reference"),
    code: Optional[str] = Query(None, description="Search by LOINC code"),
    category: Optional[str] = Query(None, description="Search by category (e.g., vital-signs)"),
    date: Optional[str] = Query(None, description="Search by date (YYYY-MM-DD)"),
    date_from: Optional[str] = Query(None, description="Search from date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="Search to date (YYYY-MM-DD)"),
    status: Optional[str] = Query(None, description="Search by status"),
    device: Optional[str] = Query(None, description="Search by device reference"),
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    _sort: Optional[str] = Query("-effectiveDateTime", description="Sort order (effectiveDateTime or -effectiveDateTime)"),
    current_user = Depends(get_current_active_user)
):
    """
    Search for Observation resources
    
    Supports searching by patient, code, category, date range, and more.
    Useful for retrieving vital signs from wearables or lab results.
    """
    db = get_database()
    
    # Build search query
    query = {}
    
    if patient or subject:
        search_subject = patient or subject
        query["subject.reference"] = search_subject
    
    if code:
        query["code.coding.code"] = code
    
    if category:
        query["category.coding.code"] = category
    
    if date:
        # Search for exact date
        query["effectiveDateTime"] = {
            "$gte": f"{date}T00:00:00Z",
            "$lt": f"{date}T23:59:59Z"
        }
    elif date_from or date_to:
        # Date range search
        date_query = {}
        if date_from:
            date_query["$gte"] = f"{date_from}T00:00:00Z"
        if date_to:
            date_query["$lt"] = f"{date_to}T23:59:59Z"
        query["effectiveDateTime"] = date_query
    
    if status:
        query["status"] = status
    
    if device:
        query["device.reference"] = device
    
    # Determine sort order
    sort_field = "effectiveDateTime"
    sort_direction = -1 if _sort.startswith("-") else 1
    
    # Execute search with pagination and sorting
    cursor = (
        db.Observation.find(query, {"_id": 0})
        .sort(sort_field, sort_direction)
        .skip(_offset)
        .limit(_count)
    )
    observations = await cursor.to_list(length=_count)
    
    return [Observation(**obs) for obs in observations]


@router.put("/Observation/{observation_id}", response_model=Observation)
async def update_observation(
    observation_id: str,
    observation: Observation,
    current_user = Depends(get_current_active_user)
):
    """
    Update an existing Observation resource
    """
    db = get_database()
    
    # Check if observation exists
    existing = await db.Observation.find_one({"id": observation_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Observation with id {observation_id} not found"
        )
    
    # Update observation
    observation.id = observation_id
    observation_dict = observation.dict()
    
    await db.Observation.replace_one({"id": observation_id}, observation_dict)
    
    return observation


@router.delete("/Observation/{observation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_observation(
    observation_id: str,
    current_user = Depends(get_current_active_user)
):
    """
    Delete an Observation resource
    """
    db = get_database()
    
    result = await db.Observation.delete_one({"id": observation_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Observation with id {observation_id} not found"
        )
    
    return None


# Special endpoint for wearable data
@router.get("/Observation/latest/{patient_id}", response_model=List[Observation])
async def get_latest_observations(
    patient_id: str,
    category: str = Query("vital-signs", description="Category of observations"),
    limit: int = Query(10, description="Number of latest observations", le=100),
    current_user = Depends(get_current_active_user)
):
    """
    Get latest observations for a patient
    
    Useful for dashboard displays showing recent vital signs from wearables.
    """
    db = get_database()
    
    query = {
        "subject.reference": f"Patient/{patient_id}",
        "category.coding.code": category
    }
    
    cursor = (
        db.Observation.find(query, {"_id": 0})
        .sort("effectiveDateTime", -1)
        .limit(limit)
    )
    observations = await cursor.to_list(length=limit)
    
    return [Observation(**obs) for obs in observations]
