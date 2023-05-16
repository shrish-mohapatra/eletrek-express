class Node:
    def __init__(self, station, priority, path=[]):
        self.station = station
        self.priority = priority
        self.path = path

    def __lt__(self, other):
        return self.priority < other.priority
