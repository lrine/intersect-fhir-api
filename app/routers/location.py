"""
Location Resource Router Template
FHIR R6 Location resource endpoints

INSTRUCTIONS:
1. Replace Location with the actual resource name (e.g., Practitioner, Device)
2. Replace location with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.location import Location
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.location import Location
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Location", response_model=Location, status_code=status.HTTP_201_CREATED)
async def create_location(
    location: Location,
    current_user = Depends(get_current_active_user)
):
    """Create a new Location resource"""
    db = get_database()
    
    if not location.id:
        location.id = f"location-{uuid.uuid4()}"
    
    existing = await db.Location.find_one({"id": location.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Location with id {location.id} already exists"
        )
    
    location_dict = location.dict()
    await db.Location.insert_one(location_dict)
    
    return location


@router.get("/Location/{location_id}", response_model=Location)
async def get_location(
    location_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Location resource by ID"""
    db = get_database()
    
    location = await db.Location.find_one({"id": location_id}, {"_id": 0})
    
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    
    return Location(**location)


@router.get("/Location", response_model=List[Location])
async def search_locations(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Location resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Location.find(query, {"_id": 0}).skip(_offset).limit(_count)
    locations = await cursor.to_list(length=_count)
    
    return [Location(**r) for r in locations]


@router.put("/Location/{location_id}", response_model=Location)
async def update_location(
    location_id: str,
    location: Location,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Location resource"""
    db = get_database()
    
    existing = await db.Location.find_one({"id": location_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    
    location.id = location_id
    location_dict = location.dict()
    
    await db.Location.replace_one({"id": location_id}, location_dict)
    
    return location


@router.delete("/Location/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_location(
    location_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Location resource"""
    db = get_database()
    
    result = await db.Location.delete_one({"id": location_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with id {location_id} not found"
        )
    
    return None
