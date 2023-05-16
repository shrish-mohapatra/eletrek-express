import random


class SampleGenerator():
    def __init__(self, stations, max_passengers, total_width, total_height, space_between, NUM_SHAPES=3):
        """
        SampleGenerator()
        @param num_stations: max number of stations for samples
        @param max_passengers: max number of passengers by shape
        @param total_width: total width size of environment
        @param total_height: total width size of environment
        @param space_between: space between each station
        """
        self.stations = stations
        self.max_passengers = max_passengers
        self.total_width = total_width
        self.total_height = total_height
        self.space_between = space_between
        self.NUM_SHAPES = NUM_SHAPES

    def create_samples(self, num_sample, seed=None):
        """
            create_samples(num_samples)
            @param num_sample: number of samples to return
            @return list of matrices
            [
                [3, 40, 25, 4, 2, 0],
                [1, 1, 58, 0, 2, 3],
                [3, 40, 74, 2, 3, 0],
                [1, 83, 66, 0, 2, 5],
                [3, 0, 94, 4, 1, 0],
                [2, 83, 4, 0, 0, 2]
            ],
            ...
            ]
        """
        if seed:
            random.seed(seed)

        output_arr = []

        for _ in range(num_sample):
            matrix = []

            station_shapes = self.generate_station_shapes()
            passenger_freqs = [self.random_passengers(shape, station_shapes)
                               for shape in range(self.NUM_SHAPES)]
            station_positions = self.generate_positions()

            for s in range(self.stations):
                row = [station_shapes[s]+1,
                       station_positions[s][0],
                       station_positions[s][1]]

                passenger_freq = [passenger_freqs[i][s]
                                  for i in range(self.NUM_SHAPES)]
                row.extend(passenger_freq)

                matrix.append(row)

            output_arr.append(matrix)
        return output_arr

    def generate_station_shapes(self):
        shapes = []

        while len(shapes) < self.stations:
            shape = random.randint(0, self.NUM_SHAPES-1)
            found = shape in shapes
            allFound = all(num in shapes for num in range(self.NUM_SHAPES))

            if allFound or not found:
                shapes.append(shape)

        return shapes

    def random_passengers(self, shape, station_shapes):
        m = self.stations
        n = self.max_passengers

        arr = [0] * m

        for _ in range(n):
            index = random.randint(0, n) % m
            while (station_shapes[index] == shape):
                index = random.randint(0, n) % m
            arr[index] += 1

        return arr

    def generate_positions(self):
        width = self.total_width
        height = self.total_height
        space = self.space_between
        positions = []

        while len(positions) < self.stations:
            x = random.randint(0, width)
            y = random.randint(0, height)

            too_close = False
            for pos in positions:
                distance = ((x - pos[0])**2 + (y - pos[1])**2)**0.5
                if distance < space:
                    too_close = True
                    break

            if not too_close:
                positions.append([x, y])

        return positions
