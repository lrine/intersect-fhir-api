"""
Procedure Resource Router Template
FHIR R6 Procedure resource endpoints

INSTRUCTIONS:
1. Replace Procedure with the actual resource name (e.g., Practitioner, Device)
2. Replace procedure with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.procedure import Procedure
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.procedure import Procedure
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Procedure", response_model=Procedure, status_code=status.HTTP_201_CREATED)
async def create_procedure(
    procedure: Procedure,
    current_user = Depends(get_current_active_user)
):
    """Create a new Procedure resource"""
    db = get_database()
    
    if not procedure.id:
        procedure.id = f"procedure-{uuid.uuid4()}"
    
    existing = await db.Procedure.find_one({"id": procedure.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Procedure with id {procedure.id} already exists"
        )
    
    procedure_dict = procedure.dict()
    await db.Procedure.insert_one(procedure_dict)
    
    return procedure


@router.get("/Procedure/{procedure_id}", response_model=Procedure)
async def get_procedure(
    procedure_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Procedure resource by ID"""
    db = get_database()
    
    procedure = await db.Procedure.find_one({"id": procedure_id}, {"_id": 0})
    
    if not procedure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Procedure with id {procedure_id} not found"
        )
    
    return Procedure(**procedure)


@router.get("/Procedure", response_model=List[Procedure])
async def search_procedures(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Procedure resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Procedure.find(query, {"_id": 0}).skip(_offset).limit(_count)
    procedures = await cursor.to_list(length=_count)
    
    return [Procedure(**r) for r in procedures]


@router.put("/Procedure/{procedure_id}", response_model=Procedure)
async def update_procedure(
    procedure_id: str,
    procedure: Procedure,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Procedure resource"""
    db = get_database()
    
    existing = await db.Procedure.find_one({"id": procedure_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Procedure with id {procedure_id} not found"
        )
    
    procedure.id = procedure_id
    procedure_dict = procedure.dict()
    
    await db.Procedure.replace_one({"id": procedure_id}, procedure_dict)
    
    return procedure


@router.delete("/Procedure/{procedure_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_procedure(
    procedure_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Procedure resource"""
    db = get_database()
    
    result = await db.Procedure.delete_one({"id": procedure_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Procedure with id {procedure_id} not found"
        )
    
    return None
