from powerdummy.populate_graph import populate_assets
from powerdummy.populate_time_series import populate_time_series
from powerdummy.utils.cdf import connect, wipe_tenant

client = connect()
wipe_tenant(client)
populate_assets(client)
populate_time_series(client)
