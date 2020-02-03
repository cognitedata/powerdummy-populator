import os

from cognite.client.experimental import CogniteClient

client = CogniteClient(
    project="powerdummy",
    api_key=os.environ["POWERDUMMY_API_KEY"],
    base_url="https://greenfield.cognitedata.com",
    client_name="powerdummy-populator",
)

for api in [client.assets, client.events, client.time_series, client.relationships]:
    ids = [x.external_id for x in api() if x.external_id]
    api.delete(external_id=ids)
    print(f"deleted {len(ids)} resources in {api}")
