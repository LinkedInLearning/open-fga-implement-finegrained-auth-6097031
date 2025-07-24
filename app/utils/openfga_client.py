import asyncio
from typing import Optional, Dict, Any

# Paso 3: importar el cliente de OpenFGA y las clases necesarias

from openfga_sdk import OpenFgaClient
from openfga_sdk.client import ClientConfiguration
from openfga_sdk.client.models import (
    ClientCheckRequest, 
    ClientWriteRequest, 
    ClientTuple, 
    ClientBatchCheckRequest, ClientListObjectsRequest)

from openfga_sdk.client.models.list_users_request import ClientListUsersRequest
from dotenv import load_dotenv
import os

# Paso 4: Crear un cliente OpenFGA
# esta clase se encargará de interactuar con OpenFGA directamente
# usando el SDK de OpenFGA
class OpenFGAClient:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        configuration = ClientConfiguration(
            api_url=os.getenv("OPENFGA_API_URL"),
            store_id=os.getenv("OPENFGA_STORE_ID"),
            authorization_model_id=os.getenv("OPENFGA_AUTHORIZATION_MODEL_ID"),
        )
        print(f"Connecting to OpenFGA at {os.getenv("OPENFGA_API_URL")} with store ID {os.getenv("OPENFGA_STORE_ID")}")
        self.client = OpenFgaClient(configuration)

    # Paso 1: agregar un método para verificar permisos
    # usando el endpoint check de OpenFGA mediante el SDK
    # https://openfga.dev/api/service#/Relationship%20Queries/Check
    async def check_permission(self, user: str, relation: str, object_id: str) -> bool:
        """Check if a user has a specific relation to an object."""
        try:
            response = await self.client.check(ClientCheckRequest(
                user=user,
                relation=relation,
                object=object_id
            ))
            return response.allowed
        except Exception as e:
            print(f"Error checking permission: {e}")
            return False

    async def batch_check_permission(self, requests: ClientBatchCheckRequest) -> list[str]:
        """Check multiple permissions at once.
            
        Returns:
            A list of object IDs for which the permission check was allowed.
        """
        try:
            response = await self.client.batch_check(requests)
            results = []
            for result in response.result:
                if result.allowed:
                    results.append(result.request.object)
            return results

        except Exception as e:
            print(f"Error performing batch check: {e}")
            return []
    async def write_tuples(self, tuples: list[ClientTuple]) -> bool:
        """Write relationship tuples to OpenFGA."""
        try:
            write_request = ClientWriteRequest(
                writes=tuples
            )
            
            await self.client.write(write_request)
            return True
        except Exception as e:
            print(f"Error writing tuples: {e}")
            return False

    async def delete_tuples(self, tuples: list[ClientTuple]) -> bool:
        """Delete relationship tuples from OpenFGA."""
        try:
            write_request = ClientWriteRequest(
                deletes=tuples
            )
            await self.client.write(write_request)
            return True
        except Exception as e:
            print(f"Error deleting tuples: {e}")
            return False

    async def list_objects(self, request: ClientListObjectsRequest) -> list[str]:
        """List all objects of a type that the user has the specified relation to.
        
        Args:
            request: A ClientListObjectsRequest containing the query parameters
            
        Returns:
            A list of object IDs that the user has the specified relation to
        """
        try:
            response = await self.client.list_objects(request)
            return response.objects
            
        except Exception as e:
            print(f"Error listing objects: {e}")
            return []

    async def list_users(self, request: ClientListUsersRequest) -> list[str]:
        """List all users that have a specific relation to an object.
        
        Args:
            request: A ClientListUsersRequest containing:
                - object: FgaObject with type and id of the target object
                - relation: The relation to check
                - user_filters: Optional list of UserTypeFilter to filter users by type
                - context: Optional context dictionary
                - contextual_tuples: Optional list of additional tuples to consider
            
        Returns:
            A list of user IDs that have the specified relation to the object
        """
        try:
            response = await self.client.list_users(request)
            return response.users
            
        except Exception as e:
            print(f"Error listing users: {e}")
            return []

# Global client instance
openfga_client = OpenFGAClient()