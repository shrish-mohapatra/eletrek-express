from ..simulate.passenger import pythagoreanDistance
from ..simulate.station import Station

class TestPassenger:
    def test_pythagoreanDistance(self):
        s1 = Station(1, 1, 100, 100)
        s2 = Station(2, 2, 100, 200)

        assert not pythagoreanDistance(s1, s2) < 1