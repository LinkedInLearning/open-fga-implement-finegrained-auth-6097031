import asyncio
from openfga_sdk import OpenFgaClient
from openfga_sdk.client import ClientConfiguration
from openfga_sdk.client.models import (
    ClientWriteRequest, 
    ClientTuple)
from dotenv import load_dotenv
import os
import yaml 

def load_tuples(path: str) -> list[ClientTuple]:
  with open(path, "r") as f:
    tuples_data = yaml.safe_load(f)

  tuples_to_write = list()
  for item in tuples_data:
    tuples_to_write.append(
      ClientTuple(
        user=item["user"],
        relation=item["relation"],
        object=item["object"]
      )
    )
  return tuples_to_write

async def main():
  load_dotenv()

  configuration = ClientConfiguration(
      api_url=os.getenv("OPENFGA_API_URL"),
      store_id=os.getenv("OPENFGA_STORE_ID"),
      authorization_model_id=os.getenv("OPENFGA_AUTHORIZATION_MODEL_ID"),
  )

  print(f"Connecting to OpenFGA at {os.getenv("OPENFGA_API_URL")} with store ID {os.getenv("OPENFGA_STORE_ID")}")

  tuples_to_write = load_tuples("app/openfga/backups/tuples_to_migrate.yaml")

  body = ClientWriteRequest(writes=tuples_to_write)

  tuples_to_delete = load_tuples("app/openfga/backups/old_tuples.yaml")
  
  async with OpenFgaClient(configuration) as fga_client:
    try:
      await fga_client.write(body)
      print(f"Write new tuples successful!")

      await fga_client.write(ClientWriteRequest(deletes=tuples_to_delete))
      print(f"Delete old tuples successful!")

      await fga_client.close()
    except Exception as e:
      print(f"Error writing tuples: {e}")

asyncio.run(main())