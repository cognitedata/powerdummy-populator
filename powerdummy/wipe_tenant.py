from powerdummy.utils.cdf import connect

client = connect()

for api in [client.assets, client.events, client.time_series, client.relationships]:
    ids = [x.external_id for x in api() if x.external_id]
    api.delete(external_id=ids)
    print(f"deleted {len(ids)} resources in {api}")
