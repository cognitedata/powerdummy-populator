from datetime import datetime

import numpy as np
from cognite.client.utils._time import timestamp_to_ms


def generate_time_series(
    type="const", parameters={}, start=datetime(2018, 1, 1), end="now", frequency=0.1
):
    timestamps = np.arange(timestamp_to_ms(start), timestamp_to_ms(end), 1000 / frequency).astype(
        int
    )
    if type == "sine":
        return generate_sine(timestamps, parameters)
    elif type == "const":
        return generate_const(timestamps, parameters)
    elif type == "switch":  # 0-1
        return generate_switch(timestamps, parameters)
    else:
        raise ValueError("unknown time series type")


def generate_sine(timestamps, parameters):
    ampl = parameters.get("amplitude", 1)
    baseline = parameters.get("baseline", 0)
    freq = parameters.get("frequency", 1)
    sine = np.sin(timestamps * (2 * np.pi * freq / 1000)) * ampl + baseline
    return zip(timestamps, sine)


def generate_const(timestamps, parameters):
    baseline = parameters.get("baseline", 1)
    noise = parameters.get("noise", 0.01)
    const = np.random.randn(*timestamps.shape) * noise + baseline
    return zip(timestamps, const)


def generate_switch(timestamps, parameters):
    switch_freq = parameters.get("switch_freq", 1 / 3600)  # 1/hr
    switch_freq_dpt = np.mean(np.diff(timestamps)) * switch_freq / 1000
    switch = np.cumsum(np.random.rand(*timestamps.shape) < switch_freq_dpt) % 2
    return zip(timestamps, switch)
