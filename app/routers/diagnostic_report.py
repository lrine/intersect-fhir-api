"""
DiagnosticReport Resource Router Template
FHIR R6 DiagnosticReport resource endpoints

INSTRUCTIONS:
1. Replace DiagnosticReport with the actual resource name (e.g., Practitioner, Device)
2. Replace diagnosticreport with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.diagnosticreport import DiagnosticReport
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.diagnosticreport import DiagnosticReport
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/DiagnosticReport", response_model=DiagnosticReport, status_code=status.HTTP_201_CREATED)
async def create_diagnosticreport(
    diagnosticreport: DiagnosticReport,
    current_user = Depends(get_current_active_user)
):
    """Create a new DiagnosticReport resource"""
    db = get_database()
    
    if not diagnosticreport.id:
        diagnosticreport.id = f"diagnosticreport-{uuid.uuid4()}"
    
    existing = await db.DiagnosticReport.find_one({"id": diagnosticreport.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"DiagnosticReport with id {diagnosticreport.id} already exists"
        )
    
    diagnosticreport_dict = diagnosticreport.dict()
    await db.DiagnosticReport.insert_one(diagnosticreport_dict)
    
    return diagnosticreport


@router.get("/DiagnosticReport/{diagnosticreport_id}", response_model=DiagnosticReport)
async def get_diagnosticreport(
    diagnosticreport_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a DiagnosticReport resource by ID"""
    db = get_database()
    
    diagnosticreport = await db.DiagnosticReport.find_one({"id": diagnosticreport_id}, {"_id": 0})
    
    if not diagnosticreport:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DiagnosticReport with id {diagnosticreport_id} not found"
        )
    
    return DiagnosticReport(**diagnosticreport)


@router.get("/DiagnosticReport", response_model=List[DiagnosticReport])
async def search_diagnosticreports(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for DiagnosticReport resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.DiagnosticReport.find(query, {"_id": 0}).skip(_offset).limit(_count)
    diagnosticreports = await cursor.to_list(length=_count)
    
    return [DiagnosticReport(**r) for r in diagnosticreports]


@router.put("/DiagnosticReport/{diagnosticreport_id}", response_model=DiagnosticReport)
async def update_diagnosticreport(
    diagnosticreport_id: str,
    diagnosticreport: DiagnosticReport,
    current_user = Depends(get_current_active_user)
):
    """Update an existing DiagnosticReport resource"""
    db = get_database()
    
    existing = await db.DiagnosticReport.find_one({"id": diagnosticreport_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DiagnosticReport with id {diagnosticreport_id} not found"
        )
    
    diagnosticreport.id = diagnosticreport_id
    diagnosticreport_dict = diagnosticreport.dict()
    
    await db.DiagnosticReport.replace_one({"id": diagnosticreport_id}, diagnosticreport_dict)
    
    return diagnosticreport


@router.delete("/DiagnosticReport/{diagnosticreport_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_diagnosticreport(
    diagnosticreport_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a DiagnosticReport resource"""
    db = get_database()
    
    result = await db.DiagnosticReport.delete_one({"id": diagnosticreport_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DiagnosticReport with id {diagnosticreport_id} not found"
        )
    
    return None
