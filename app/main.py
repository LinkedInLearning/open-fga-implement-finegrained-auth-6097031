from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import settings
from app.database import init_db
from app.routes import organization_routes, document_routes

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f"Starting {settings.app_title} v{settings.app_version}")
    print(f"OpenFGA API URL: {settings.openfga_api_url}")
    print("Initializing database...")
    await init_db()
    print("Database initialized successfully!")
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="FastAPI OpenFGA RBAC Demo",
    version=settings.app_version,
    debug=settings.debug,
    lifespan=lifespan,
    description="""
    A simple FastAPI application demonstrating RBAC (Role-Based Access Control) using OpenFGA.
    
    This demo showcases:
    - Organizations with admin/member roles
    - Documents owned by organizations
    - Permission inheritance from organization roles to document permissions
    
    ## RBAC Model
    - **admin**: Can manage organization members and delete documents
    - **member**: Can view organization members and documents, create new documents
    - **viewer**: Can view organization members and documents, create new documents
    - **Documents**: Inherit permissions from their owning organization
    
    All authorization is handled through OpenFGA using a simple, coarse-grained access control model.
    """
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    organization_routes.router, 
    prefix="/organizations", 
    tags=["organizations"]
)
app.include_router(
    document_routes.router, 
    prefix="/documents", 
    tags=["documents"]
)

@app.get("/")
async def read_root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to the FastAPI OpenFGA RBAC Demo!",
        "version": settings.app_version,
        "docs": "/docs",
        "redoc": "/redoc",
        "model": "Simple RBAC with organizations and documents",
        "roles": ["admin", "member", "viewer"],
        "example_usage": {
            "1": "Create an organization (user becomes admin)",
            "2": "Add members to the organization",
            "3": "Create documents in the organization",
            "4": "Check permissions on documents"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "version": settings.app_version}

@app.get("/info")
async def info():
    """Information about the RBAC model implementation."""
    return {
        "model": "OpenFGA RBAC Implementation",
        "pattern": "Coarse-grained access control",
        "types": {
            "user": "Individual users in the system",
            "organization": "Groups that contain users with roles",
            "document": "Assets owned by organizations"
        },
        "roles": {
            "admin": {
                "description": "Full control over organization and its documents",
                "permissions": [
                    "can_add_member",
                    "can_delete_member", 
                    "can_view_member",
                    "can_add_document",
                    "can_delete_document",
                    "can_view_document"
                ]
            },
            "member": {
                "description": "Basic access to organization and documents",
                "permissions": [
                    "can_view_member",
                    "can_add_document", 
                    "can_view_document"
                ]
            }
        },
        "inheritance": "Resource permissions inherit from organization roles via 'admin from organization' and 'member from organization' patterns"
    }