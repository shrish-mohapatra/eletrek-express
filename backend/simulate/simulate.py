from .station import Station
from .passenger import Passenger
from .graphtools import graph_network


class Simulate:
    def __init__(self, station_matrix, lines):
        self.lines = lines
        self.stations = []
        self.passengers = []

        self.total_passengers = 0
        self.num_passengers = 0
        self.total_passenger_path_cost = 0
        self.total_line_length = 0

        self.load_station_matrix(station_matrix)

    def load_station_matrix(self, station_matrix):
        """
        Load station and passengers instances from station_matrix
        """
        for id, row in enumerate(station_matrix):
            # Create station
            station = Station(id, row[0], row[1], row[2])
            self.stations.append(station)

            # Create passengers
            for shape_i in range(3):
                passenger_count = row[shape_i+3]

                if not passenger_count:
                    continue

                passenger = Passenger(shape_i+1, station, passenger_count)
                self.total_passengers += passenger_count
                self.passengers.append(passenger)

    def compute_network_cost(self):
        """
        Calculate line and passenger costs
        """
        expanded_lines = []

        # Create expanded array of lines
        # ex. [ [1,2] ] -> [ [1,2], [2,1] ]
        for line in self.lines:
            expanded_lines.append([line[0], line[1]])
            expanded_lines.append([line[1], line[0]])

        # Calculate line cost
        for line in self.lines:
            st1 = self.stations[line[0]]
            st2 = self.stations[line[1]]
            line_length = ((st1.x - st2.x)**2 + (st1.y - st2.y)**2)**0.5
            self.total_line_length += line_length

        # Calculate passenger cost
        for passenger in self.passengers:
            passenger.get_path(self.stations, expanded_lines)

            if passenger.path:
                self.num_passengers += passenger.count
                self.total_passenger_path_cost += passenger.count * passenger.path_cost

    def visualize(self, name):
        """
        Visualize subway network configuration
        """
        graph_network(self, name)

    def missed_passengers(self):
        return self.total_passengers - self.num_passengers

    def to_dict(self):
        """
        Return dict representation of stations & lines
        ```
        {
            nodes: [
                {
                    shape: <shape str>,
                    x: <x>,
                    y: <y>,
                    passengers: [<shape_index>,...],
                },
                ...
            ],
            lines: [
                [<station_id_1>, <station_id_2>],
                ...
            ]
        }
        ```
        """
        nodes = [
            {
                "shape": station.shape_str(),
                "x": int(station.x),
                "y": int(station.y),
                "passengers": [
                    passenger.shape - 1
                    for passenger in self.passengers
                    for _ in range(passenger.count)
                    if passenger.start_station.id == station.id
                ]
            }
            for station in self.stations
        ]

        return {
            "nodes": nodes,
            "lines": self.lines
        }