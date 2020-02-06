from powerdummy.populate_assets import populate_assets
from powerdummy.populate_time_series import populate_time_series
from powerdummy.utils.cdf import connect, wipe_tenant

client = connect()
wipe_tenant(client)
populate_assets(client)
populate_time_series(client)
