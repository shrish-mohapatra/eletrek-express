from queue import PriorityQueue
import math
from loguru import logger

from .node import Node
from .shape import Shape


class Passenger(Shape):
    def __init__(self, shape, start_station, count=1):
        self.shape = shape
        self.start_station = start_station
        self.count = count
        self.path = None
        self.path_cost = 0

    def __str__(self):
        return f'P {self.shape_str()} x {self.count} ({self.path})'

    def get_path(self, stations, lines):
        """
        Compute path from start station to matching shape
        If path exists, save to self.path
        Otherwise, self.path = None
        - stations: array of Station instances
        - lines: expanded list of lines (ex. [[1,2],[2,1]])
        """
        frontier = PriorityQueue()
        reached = {}

        start = Node(self.start_station, 0.0, [self.start_station.id])

        if self.is_goal(start.station):
            logger.error("Started at goal")

        frontier.put((0.0, start))

        while not frontier.empty():
            node = frontier.get()[1]

            # If we reached the goal, we return the path
            if self.is_goal(node.station):
                self.path = node.path
                self.path_cost = node.priority

                if (self.path_cost == 0):
                    logger.error("Zero path cost")

                return

            children = self.expand(node, lines, stations)

            for c in children:
                child = c.station
                # for each candidate, replace old priorities with new shorter ones
                # put it into the frontier
                if (child.id not in reached) or (c.priority < reached[child.id]):
                    reached[child.id] = c.priority
                    frontier.put((c.priority, c))

        # No solution
        self.path = None
        self.path_cost = 0
        return

    def is_goal(self, node):
        return node.shape == self.shape

    def expand(self, node, lines, stations):
        children = []
        nextStations = self.getAdjecentNodes(node.station, lines, stations)

        # for each candidate, change them into proper pqnodes
        for s in nextStations:
            pathCost = node.priority + pythagoreanDistance(node.station, s)
            children.append(Node(s, pathCost, node.path + [s.id]))

        return children

    # assume each line only has 2 stations
    # assume station id = index in stations array
    def getAdjecentNodes(self, station, lines, stations):
        adjacent = []
        for line in lines:
            for i, s in enumerate(line):
                if s == station.id:
                    adjacent.append(stations[line[i-1]])
        return adjacent

def pythagoreanDistance(station1, station2):
    xSq = (station2.x - station1.x)**2
    ySq = (station2.y - station1.y)**2
    return math.sqrt(xSq+ySq)
