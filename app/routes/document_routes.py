from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List
import uuid
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document import *
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
                title=document.title,
                description=document.description,
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
        title=document_db.title,
        description=document_db.description,
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
        title=document.title,
        organization_id=document.organization_id,
        created_at=datetime.now()
    )
    
    db.add(document_db)
    await db.commit()
    await db.refresh(document_db)
    
    # Link document to organization in OpenFGA
    await authz_service.assign_document_to_organization(document_id, document.organization_id)
    
    success = await authz_service.assign_document_role(
        user_id, 
        document_id, 
        "owner"
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to assign role")

    return Document(
        id=document_db.id,
        title=document_db.title,
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
        title=document_db.title,
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

@router.post("/{document_id}/roles")
async def assign_document_role(
    document_id: str,
    role_assignment: DocumentRoleAssignment,
    user_id: str = Query(..., description="User ID for authorization"),
    db: AsyncSession = Depends(get_db)
):
    """Assign a role to a user on a specific document (requires can_share permission)."""
    if not await authz_service.can_share_document(user_id, document_id):
        raise HTTPException(status_code=403, detail="Share access required")
    
    # Check if document exists
    result = await db.execute(select(DocumentDB).where(DocumentDB.id == document_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Document not found")
    
    success = await authz_service.assign_document_role(
        role_assignment.user_id, 
        document_id, 
        role_assignment.role
    )
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to assign role")
    
    return {
        "message": f"User {role_assignment.user_id} assigned as {role_assignment.role}",
        "document_id": document_id,
        "user_id": role_assignment.user_id,
        "role": role_assignment.role
    }

@router.delete("/{document_id}/roles/{target_user_id}")
async def remove_document_role(
    document_id: str,
    target_user_id: str,
    role: str = Query(..., description="Role to remove ('owner', 'editor', or 'viewer')"),
    user_id: str = Query(..., description="User ID for authorization"),
    db: AsyncSession = Depends(get_db)
):
    """Remove a role from a user on a specific document (requires can_share permission)."""
    if not await authz_service.can_share_document(user_id, document_id):
        raise HTTPException(status_code=403, detail="Share access required")
    
    # Check if document exists
    result = await db.execute(select(DocumentDB).where(DocumentDB.id == document_id))
    if not result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Document not found")
    
    success = await authz_service.remove_document_role(target_user_id, document_id, role)
    
    if not success:
        raise HTTPException(status_code=500, detail="Failed to remove role")
    
    return {"message": f"User {target_user_id} removed from {role} role"}

@router.get("/{document_id}/permissions", response_model=DocumentPermissions)
async def check_document_permissions(
    document_id: str,
    user_id: str = Query(..., description="User ID to check permissions for"),
    db: AsyncSession = Depends(get_db)
):
    """Check what permissions a user has on a specific document."""
    result = await db.execute(select(DocumentDB).where(DocumentDB.id == document_id))
    document_db = result.scalar_one_or_none()
    
    if not document_db:
        raise HTTPException(status_code=404, detail="Document not found")
    
    permissions = DocumentPermissions(
        user_id=user_id,
        document_id=document_id,
        can_read=await authz_service.can_read_document(user_id, document_id),
        can_write=await authz_service.can_write_document(user_id, document_id),
        can_delete=await authz_service.can_delete_document(user_id, document_id)
    )
    
    return permissions
