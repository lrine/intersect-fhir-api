"""
Practitioner Resource Router Template
FHIR R6 Practitioner resource endpoints

INSTRUCTIONS:
1. Replace Practitioner with the actual resource name (e.g., Practitioner, Device)
2. Replace practitioner with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.practitioner import Practitioner
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends, Body
from typing import List, Optional
from fhir.resources.practitioner import Practitioner
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Practitioner", status_code=status.HTTP_201_CREATED)
async def create_practitioner(
    practitioner_data: dict = Body(...),
    current_user = Depends(get_current_active_user)
):
    """Create a new Practitioner resource"""
    db = get_database()

    if not practitioner_data.get("id"):
        practitioner_data["id"] = f"practitioner-{uuid.uuid4()}"

    existing = await db.Practitioner.find_one({"id": practitioner_data["id"]})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Practitioner with id {practitioner_data['id']} already exists"
        )

    await db.Practitioner.insert_one(practitioner_data)

    # Remove MongoDB's _id field to avoid ObjectId serialization issues
    practitioner_data.pop("_id", None)

    return practitioner_data


@router.get("/Practitioner/{practitioner_id}", response_model=Practitioner)
async def get_practitioner(
    practitioner_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Practitioner resource by ID"""
    db = get_database()
    
    practitioner = await db.Practitioner.find_one({"id": practitioner_id}, {"_id": 0})
    
    if not practitioner:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Practitioner with id {practitioner_id} not found"
        )
    
    return Practitioner(**practitioner)


@router.get("/Practitioner", response_model=List[Practitioner])
async def search_practitioners(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Practitioner resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Practitioner.find(query, {"_id": 0}).skip(_offset).limit(_count)
    practitioners = await cursor.to_list(length=_count)
    
    return [Practitioner(**r) for r in practitioners]


@router.put("/Practitioner/{practitioner_id}")
async def update_practitioner(
    practitioner_id: str,
    practitioner_data: dict = Body(...),
    current_user = Depends(get_current_active_user)
):
    """Update an existing Practitioner resource"""
    db = get_database()

    existing = await db.Practitioner.find_one({"id": practitioner_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Practitioner with id {practitioner_id} not found"
        )

    practitioner_data["id"] = practitioner_id

    await db.Practitioner.replace_one({"id": practitioner_id}, practitioner_data)

    return practitioner_data


@router.delete("/Practitioner/{practitioner_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_practitioner(
    practitioner_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Practitioner resource"""
    db = get_database()
    
    result = await db.Practitioner.delete_one({"id": practitioner_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Practitioner with id {practitioner_id} not found"
        )
    
    return None
