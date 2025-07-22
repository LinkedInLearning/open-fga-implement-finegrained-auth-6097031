from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document import Document, DocumentCreate, DocumentUpdate
from app.database import get_db, DocumentDB
from app.services.authorization_service import authz_service

router = APIRouter()

@router.get("/", response_model=List[Document])
async def list_documents(
    user_id: str = Query(..., description="User ID for authorization"),
    organization_id: str = Query(None, description="Filter by organization"),
    db: AsyncSession = Depends(get_db)
):
    """List all documents the user can view."""
    # Build query
    query = select(DocumentDB)
    if organization_id:
        query = query.where(DocumentDB.organization_id == organization_id)
    
    result = await db.execute(query)
    all_documents = result.scalars().all()
    
    accessible_documents = []
    for document in all_documents:
        if await authz_service.can_view_document(user_id, document.id):
            accessible_documents.append(Document(
                id=document.id,
                name=document.name,
                description=document.description,
                document_type=document.document_type,
                organization_id=document.organization_id,
                created_at=document.created_at
            ))
    
    return accessible_documents

@router.get("/{document_id}", response_model=Document)
async def get_document(
    document_id: str,
    user_id: str = Query(..., description="User ID for authorization"),
    db: AsyncSession = Depends(get_db)
):
    """Get a specific document."""
    if not await authz_service.can_view_document(user_id, document_id):
        raise HTTPException(status_code=403, detail="Access denied")
    
    result = await db.execute(select(DocumentDB).where(DocumentDB.id == document_id))
    document_db = result.scalar_one_or_none()
    
    if not document_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return Document(
        id=document_db.id,
        name=document_db.name,
        description=document_db.description,
        document_type=document_db.document_type,
        organization_id=document_db.organization_id,
        created_at=document_db.created_at
    )

@router.post("/", response_model=Document)
async def create_document(
    document: DocumentCreate,
    user_id: str = Query(..., description="User ID for authorization"),
    db: AsyncSession = Depends(get_db)
):
    """Create a new document (admin or member of organization)."""
    if not await authz_service.can_add_document(user_id, document.organization_id):
        raise HTTPException(status_code=403, detail="Cannot add documents to this organization")
    
    document_id = str(uuid.uuid4())
    
    # Create document in database
    document_db = DocumentDB(
        id=document_id,
        name=document.name,
        description=document.description,
        document_type=document.document_type,
        organization_id=document.organization_id,
        created_at=datetime.now()
    )
    
    db.add(document_db)
    await db.commit()
    await db.refresh(document_db)
    
    # Link document to organization in OpenFGA
    await authz_service.assign_document_to_organization(document_id, document.organization_id)
    
    return Document(
        id=document_db.id,
        name=document_db.name,
        description=document_db.description,
        document_type=document_db.document_type,
        organization_id=document_db.organization_id,
        created_at=document_db.created_at
    )

@router.put("/{document_id}", response_model=Document)
async def update_document(
    document_id: str,
    document_update: DocumentUpdate,
    user_id: str = Query(..., description="User ID for authorization"),
    db: AsyncSession = Depends(get_db)
):
    """Update a document (admin only)."""
    if not await authz_service.can_delete_document(user_id, document_id):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.execute(select(DocumentDB).where(DocumentDB.id == document_id))
    document_db = result.scalar_one_or_none()
    
    if not document_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Update fields
    update_data = document_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(document_db, field, value)
    
    await db.commit()
    await db.refresh(document_db)
    
    return Document(
        id=document_db.id,
        name=document_db.name,
        description=document_db.description,
        document_type=document_db.document_type,
        organization_id=document_db.organization_id,
        created_at=document_db.created_at
    )

@router.delete("/{document_id}")
async def delete_document(
    document_id: str,
    user_id: str = Query(..., description="User ID for authorization"),
    db: AsyncSession = Depends(get_db)
):
    """Delete a document (admin only)."""
    if not await authz_service.can_delete_document(user_id, document_id):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    result = await db.execute(select(DocumentDB).where(DocumentDB.id == document_id))
    document_db = result.scalar_one_or_none()
    
    if not document_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    await db.delete(document_db)
    await db.commit()
    
    return {"message": "Resource deleted successfully"}

@router.get("/{document_id}/permissions")
async def check_document_permissions(
    document_id: str,
    user_id: str = Query(..., description="User ID to check permissions for"),
    db: AsyncSession = Depends(get_db)
):
    """Check what permissions a user has on a specific document."""
    result = await db.execute(select(ResourceDB).where(ResourceDB.id == document_id))
    document_db = result.scalar_one_or_none()
    
    if not document_db:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    permissions = {
        "can_view": await authz_service.can_view_document(user_id, document_id),
        "can_delete": await authz_service.can_delete_document(user_id, document_id)
    }
    
    return {
        "document_id": document_id,
        "user_id": user_id,
        "permissions": permissions
    }