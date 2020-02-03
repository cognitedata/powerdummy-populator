import itertools
import os

from cognite.client.data_classes import *
from cognite.client.experimental import CogniteClient


def iter_chunk(n, iterable):
    it = iter(iterable)
    while True:
        chunk = list(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk


def connect():
    return CogniteClient(
        project="powerdummy",
        api_key=os.environ["POWERDUMMY_API_KEY"],
        base_url="https://greenfield.cognitedata.com",
        client_name="powerdummy-populator",
    )


def create_time_series(client, external_id, data):
    DPT_CHUNK = 5_000_000
    ts = client.time_series.create(TimeSeries(external_id=external_id))
    print(f"created time series {external_id}")
    for chunk in iter_chunk(DPT_CHUNK, data):
        client.datapoints.insert(chunk, id=ts.id)
        print(f"posted {len(chunk)} datapoints to {external_id}")
    return ts
