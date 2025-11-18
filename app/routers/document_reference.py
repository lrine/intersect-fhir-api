"""
DocumentReference Resource Router Template
FHIR R6 DocumentReference resource endpoints

INSTRUCTIONS:
1. Replace DocumentReference with the actual resource name (e.g., Practitioner, Device)
2. Replace documentreference with lowercase version (e.g., practitioner, device)
3. Update search parameters based on FHIR spec for that resource
4. Import: from fhir.resources.documentreference import DocumentReference
"""
from fastapi import APIRouter, HTTPException, status, Query, Depends
from typing import List, Optional
from fhir.resources.documentreference import DocumentReference
import uuid

from app.database import get_database
from app.services.auth_service import get_current_active_user

router = APIRouter()


@router.post("/DocumentReference", response_model=DocumentReference, status_code=status.HTTP_201_CREATED)
async def create_documentreference(
    documentreference: DocumentReference,
    current_user = Depends(get_current_active_user)
):
    """Create a new DocumentReference resource"""
    db = get_database()
    
    if not documentreference.id:
        documentreference.id = f"documentreference-{uuid.uuid4()}"
    
    existing = await db.DocumentReference.find_one({"id": documentreference.id})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"DocumentReference with id {documentreference.id} already exists"
        )
    
    documentreference_dict = documentreference.dict()
    await db.DocumentReference.insert_one(documentreference_dict)
    
    return documentreference


@router.get("/DocumentReference/{documentreference_id}", response_model=DocumentReference)
async def get_documentreference(
    documentreference_id: str,
    current_user = Depends(get_current_active_user)
):
    """Retrieve a DocumentReference resource by ID"""
    db = get_database()
    
    documentreference = await db.DocumentReference.find_one({"id": documentreference_id}, {"_id": 0})
    
    if not documentreference:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentReference with id {documentreference_id} not found"
        )
    
    return DocumentReference(**documentreference)


@router.get("/DocumentReference", response_model=List[DocumentReference])
async def search_documentreferences(
    _count: Optional[int] = Query(100, description="Number of results", le=1000),
    _offset: Optional[int] = Query(0, description="Offset for pagination"),
    current_user = Depends(get_current_active_user)
):
    """Search for DocumentReference resources"""
    db = get_database()
    
    query = {}
    # Add search parameters based on FHIR spec
    
    cursor = db.DocumentReference.find(query, {"_id": 0}).skip(_offset).limit(_count)
    documentreferences = await cursor.to_list(length=_count)
    
    return [DocumentReference(**r) for r in documentreferences]


@router.put("/DocumentReference/{documentreference_id}", response_model=DocumentReference)
async def update_documentreference(
    documentreference_id: str,
    documentreference: DocumentReference,
    current_user = Depends(get_current_active_user)
):
    """Update an existing DocumentReference resource"""
    db = get_database()
    
    existing = await db.DocumentReference.find_one({"id": documentreference_id})
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentReference with id {documentreference_id} not found"
        )
    
    documentreference.id = documentreference_id
    documentreference_dict = documentreference.dict()
    
    await db.DocumentReference.replace_one({"id": documentreference_id}, documentreference_dict)
    
    return documentreference


@router.delete("/DocumentReference/{documentreference_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_documentreference(
    documentreference_id: str,
    current_user = Depends(get_current_active_user)
):
    """Delete a DocumentReference resource"""
    db = get_database()
    
    result = await db.DocumentReference.delete_one({"id": documentreference_id})
    
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"DocumentReference with id {documentreference_id} not found"
        )
    
    return None
