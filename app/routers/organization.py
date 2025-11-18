"""
Organization Resource Router Template
FHIR R6 Organization resource endpoints

INSTRUCTIONS:
1. Replace Organization with the actual resource name (e.g., Practitioner, Device)
2. Replace organization with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.organization import Organization
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.organization import Organization
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/Organization", response_model=Organization, status_code=status.HTTP_201_CREATED)
async def create_organization(
    organization: Organization,
    current_user = Depends(get_current_active_user)
):
    """Create a new Organization resource"""
    db = get_database()
    
    if not organization.id:
        organization.id = f"organization-{uuid.uuid4()}"
    
    existing = await db.Organization.find_one({"id": organization.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Organization with id {organization.id} already exists"
        )
    
    organization_dict = organization.dict()
    await db.Organization.insert_one(organization_dict)
    
    return organization


@router.get("/Organization/{organization_id}", response_model=Organization)
async def get_organization(
    organization_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a Organization resource by ID"""
    db = get_database()
    
    organization = await db.Organization.find_one({"id": organization_id}, {"_id": 0})
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {organization_id} not found"
        )
    
    return Organization(**organization)


@router.get("/Organization", response_model=List[Organization])
async def search_organizations(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for Organization resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.Organization.find(query, {"_id": 0}).skip(_offset).limit(_count)
    organizations = await cursor.to_list(length=_count)
    
    return [Organization(**r) for r in organizations]


@router.put("/Organization/{organization_id}", response_model=Organization)
async def update_organization(
    organization_id: str,
    organization: Organization,
    current_user = Depends(get_current_active_user)
):
    """Update an existing Organization resource"""
    db = get_database()
    
    existing = await db.Organization.find_one({"id": organization_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {organization_id} not found"
        )
    
    organization.id = organization_id
    organization_dict = organization.dict()
    
    await db.Organization.replace_one({"id": organization_id}, organization_dict)
    
    return organization


@router.delete("/Organization/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization(
    organization_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a Organization resource"""
    db = get_database()
    
    result = await db.Organization.delete_one({"id": organization_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organization with id {organization_id} not found"
        )
    
    return None
