from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class DocumentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: Optional[str] = None

    is_public: bool = Field(default=False, description="Documento es publico o no")

class DocumentCreate(DocumentBase):
    organization_id: str
    owner_id: Optional[str] = None

class DocumentUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = None
    is_public: Optional[bool] = None

class Document(DocumentBase):
    id: str
    organization_id: str  
    created_at: datetime

    class Config:
        from_attributes = True

class DocumentRoleAssignment(BaseModel):
    user_id: str = Field(..., description="User ID to assign role to")
    role: str = Field(..., description="Role: 'owner', 'editor', or 'viewer'")

class DocumentPermissions(BaseModel):
    user_id: str
    document_id: str
    can_read: bool
    can_write: bool