from datetime import datetime

from powerdummy.utils.time_series import generate_time_series


class TestTimeSeries:
    def test_const(self):
        dpt = generate_time_series(
            type="const",
            parameters={"baseline": 100, "noise": 0.0},
            start=datetime(2018, 1, 1),
            end=datetime(2018, 1, 2),
            frequency=1 / 3600,
        )
        dpt = list(dpt)
        assert all([x == 100 for t, x in dpt])
        assert 24 == len(dpt)
