from powerdummy.utils.cdf import connect, create_time_series
from powerdummy.utils.time_series import generate_time_series

client = connect()

create_time_series(client, "example_sine", generate_time_series(type="sine"))
create_time_series(
    client, "example_const", generate_time_series(type="const", parameters={"baseline": 100, "noise": 0.1})
)
create_time_series(
    client,
    "example_switch",
    generate_time_series(type="switch", frequency=0.01, parameters={"switch_freq": 1 / (12 * 3600)}),
)
