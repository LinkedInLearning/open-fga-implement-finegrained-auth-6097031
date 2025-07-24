from typing import List, Optional
from openfga_sdk.client.models import ClientTuple, ClientBatchCheckItem, ClientBatchCheckRequest
<<<<<<< HEAD

=======
>>>>>>> 4b56674 (04_02)
from app.utils.openfga_client import openfga_client

ROLES = ["admin", "member", "viewer"]

# Paso 5: Crear un servicio de autorización 
# que maneje la lógica de permisos y relaciones
# Este servicio utilizará el cliente OpenFGA 
class AuthorizationService:
    """Simple RBAC authorization service using OpenFGA."""
    
    async def assign_user_to_organization(self, user_id: str, organization_id: str, role: str) -> bool:
        """Assign a user to an organization with a specific role (admin or member)."""
        if role not in ROLES:
            raise ValueError("Role must be 'admin' or 'member'")
            
        client_tuple = ClientTuple(
            user=f"user:{user_id}",
            relation=role,
            object=f"organization:{organization_id}"
        )
        return await openfga_client.write_tuples([client_tuple])
    
    async def remove_user_from_organization(self, user_id: str, organization_id: str, role: str) -> bool:
        """Remove a user's role from an organization."""
        if role not in ROLES:
            raise ValueError("Role must be 'admin' or 'member'")
            
        client_tuple = ClientTuple(
            user=f"user:{user_id}",
            relation=role,
            object=f"organization:{organization_id}"
        )
        return await openfga_client.delete_tuples([client_tuple])
    
    async def assign_document_to_organization(self, document_id: str, organization_id: str) -> bool:
        """Assign a document to an organization."""
        client_tuple = ClientTuple(
            user=f"organization:{organization_id}",
            relation="organization",
            object=f"document:{document_id}"
        )
        return await openfga_client.write_tuples([client_tuple])
    
    # Paso 2: llamar al metodo check_permission del cliente OpenFGA
    # en los metodos que lo requieran
    # este metodo puede sustituir a los metodos subsecuentes
    # pero por claridad y simplicidad, se mantienen los metodos individuales
    async def can_perform_action(self, user_id: str, relation: str, object_id: str) -> bool:
        """Check if a user can perform a specific action on an object."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation=relation,
            object_id=object_id
        )
    async def can_add_member(self, user_id: str, organization_id: str) -> bool:
        """Check if user can add members to organization (admin only)."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_add_member",
            object_id=f"organization:{organization_id}"
        )
    
    async def can_delete_member(self, user_id: str, organization_id: str) -> bool:
        """Check if user can delete members from organization (admin only)."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_delete_member",
            object_id=f"organization:{organization_id}"
        )
    
    async def can_view_member(self, user_id: str, organization_id: str) -> bool:
        """Check if user can view members of organization (admin or member)."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_view_member",
            object_id=f"organization:{organization_id}"
        )
    
    async def can_add_document(self, user_id: str, organization_id: str) -> bool:
        """Check if user can add documents to organization (admin or member)."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_add_document",
            object_id=f"organization:{organization_id}"
        )
    
    async def can_delete_document(self, user_id: str, document_id: str) -> bool:
        """Check if user can delete a document (admin only)."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_delete_document",
            object_id=f"document:{document_id}"
        )
    
    async def can_view_document(self, user_id: str, document_id: str) -> bool:
        """Check if user can view a document (admin or member)."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_view_document",
            object_id=f"document:{document_id}"
        )
    async def assign_document_role(self, user_id: str, document_id: str, role: str) -> bool:
            """Assign a document-specific role to a user (owner, editor, viewer)."""
            if role not in ["owner", "editor", "viewer"]:
                raise ValueError("Role must be 'owner', 'editor', or 'viewer'")
                
            client_tuple = ClientTuple(
                user=f"user:{user_id}",
                relation=role,
                object=f"document:{document_id}"
            )
            return await openfga_client.write_tuples([client_tuple])
        
    async def remove_document_role(self, user_id: str, document_id: str, role: str) -> bool:
        """Remove a document-specific role from a user."""
        if role not in ["owner", "editor", "viewer"]:
            raise ValueError("Role must be 'owner', 'editor', or 'viewer'")
            
        client_tuple = ClientTuple(
            user=f"user:{user_id}",
            relation=role,
            object=f"document:{document_id}"
        )
        return await openfga_client.delete_tuples([client_tuple])

    async def assign_document_to_organization(self, document_id: str, organization_id: str) -> bool:
        """Assign a document to an organization."""
        client_tuple = ClientTuple(
            user=f"organization:{organization_id}",
            relation="organization",
            object=f"document:{document_id}"
        )
        return await openfga_client.write_tuples([client_tuple])

    # Document permission checks
    async def can_read_document(self, user_id: str, document_id: str) -> bool:
        """Check if user can read a document."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_read",
            object_id=f"document:{document_id}"
        )

    async def can_write_document(self, user_id: str, document_id: str) -> bool:
        """Check if user can write/edit a document."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_write",
            object_id=f"document:{document_id}"
        )

    async def can_delete_document(self, user_id: str, document_id: str) -> bool:
        """Check if user can delete a document."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_delete",
            object_id=f"document:{document_id}"
        )

    async def can_share_document(self, user_id: str, document_id: str) -> bool:
        """Check if user can share a document."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_share",
            object_id=f"document:{document_id}"
        )

    # Organization document permissions  
    async def can_add_document(self, user_id: str, organization_id: str) -> bool:
        """Check if user can add documents to organization (admin or member)."""
        return await openfga_client.check_permission(
            user=f"user:{user_id}",
            relation="can_add_document",
            object_id=f"organization:{organization_id}"
        )
    
    async def set_document_public(self, document_id: str, is_public: bool) -> bool:
        """Set document as public or private using the viewer relation."""
        if is_public:
            # Añadir tupla viewer con user:* para acceso público
            client_tuple = ClientTuple(
                user="user:*",
                relation="viewer",
                object=f"document:{document_id}"
            )
            return await openfga_client.write_tuples([client_tuple])
        else:
            # Remover tupla viewer con user:*
            client_tuple = ClientTuple(
                user="user:*",
                relation="viewer", 
                object=f"document:{document_id}"
            )
            return await openfga_client.delete_tuples([client_tuple])
    
    async def is_document_public(self, document_id: str) -> bool:
        """Check if a document is marked as public by checking user:* viewer relation."""
        return await openfga_client.check_permission(
            user="user:*",
            relation="viewer",
            object_id=f"document:{document_id}"
        )

    async def can_view_documents(self, user_id: str, document_ids: List[str]) -> List[str]:
        """Check if a user has viewer access to multiple documents at once.
        
        Args:
            user_id: The ID of the user
            document_ids: List of document IDs to check permissions for
            
        Returns:
            List of document IDs that the user has permission to view
        """
        batch_request = ClientBatchCheckRequest(
            checks=[
                ClientBatchCheckItem(
                    user=f"user:{user_id}",
                    relation="can_read",
                    object=f"document:{doc_id}"
                ) for doc_id in document_ids
            ]
        )
        
        allowed_objects = await openfga_client.batch_check_permission(batch_request)
        return [obj.replace("document:", "") for obj in allowed_objects]

# Global authorization service instance
authz_service = AuthorizationService()