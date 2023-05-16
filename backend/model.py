"""

Tensorflow model trained with GA to generate optimal subway lines

"""

import os
import json
import time
from datetime import datetime as dt
from loguru import logger
import numpy as np
import tensorflow as tf
import pygad.kerasga

from backend.utils.sample import SampleGenerator
from backend.simulate.simulate import Simulate

MODELS_FOLDER = "backend/models"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'


class Model:
    """
    NN Model to generate subways lines given station and passenger data
    """

    def __init__(
        self,

        num_stations=6,
        num_features=6,
        max_passengers=10,
        map_width=500,
        map_height=500,
        space_between=70,

        seed=None,
        num_samples=100,
        num_generations=10,
        num_parents_mating=10,
        num_solutions=20,
        mutation_probability=None,
        mutation_type="random",
        parallel_processing=5,

        score_func=None,
        layers=None,
    ):
        """
        Create NN GA instance

        Subway network config
        - num_stations: Number of stations network supports
        - num_features: Number of features for each station (ex. shape, position)
        - max_passengers: Number of passengers per network
        - map_width: Width of subway network (in pixels)
        - map_height: Height of subway network (in pixels)
        - space_between: Minimum distance between stations (in pixels)

        NN Config
        - seed: Seed for data input generation
        - num_samples: Number of samples to train NN
        - num_generations: Number of generations to train GA
        - num_parents_mating: Number of solutions to be selected in mating pool
        - num_solutions: Number of solutions in population
        - mutation_probability: Disable Pygad dynamic mutation with fixed probability
        - mutation_type: Pygad mutation type
        - parallel_processing: Number of threads

        Experiment config
        - score_func: Lambda function to take metrics from simulation and determine network score
        - layers: Tensorflow layers for sequential model
        """
        self.seed = seed
        self.num_stations = num_stations
        self.num_features = num_features
        self.max_passengers = max_passengers
        self.map_width = map_width
        self.map_height = map_height
        self.space_between = space_between

        self.num_samples = num_samples
        self.num_generations = num_generations
        self.num_parents_mating = num_parents_mating
        self.num_solutions = num_solutions
        self.mutation_probability = mutation_probability
        self.mutation_type = mutation_type
        self.parallel_processing = parallel_processing

        self.score_func = score_func
        self.layers = layers

        self.data_inputs = None
        """Matrices representing stations & passengers"""

        self.ga_instance = None
        """Pygad instance"""

        self.model = None
        """Tensorflow model"""

        self.keras_ga = None
        """Pygad model"""

        logger.info("Initialized model class instance")

    def load_data(self):
        """
        Create samples for data_inputs

        Each sample instance is represented as follows:
        ```
        # station_shape, x, y, triangles, squares, circles
        data_input = [
            [1, 120, 80,  0, 2, 0,],
            [1, 100, 350, 0, 1, 1,],
            [2, 250, 200, 0, 0, 0,],
            [3, 500, 100, 0, 0, 0,],
            [3, 300, 470, 1, 1, 0,],
            [1, 450, 450, 0, 0, 1,],
        ],
        ```
        - space_between: minimum distance (in pixels) between stations
        """
        sample_gen = SampleGenerator(
            self.num_stations,
            self.max_passengers,
            self.map_width,
            self.map_height,
            self.space_between,
        )

        self.data_inputs = np.array(
            sample_gen.create_samples(self.num_samples, seed=self.seed)
        )

        logger.info("Loaded data inputs")

    def create_model(self):
        """
        Create tensorflow & pygad models
        """
        # Create Tensorflow model
        if self.layers:
            self.model = tf.keras.Sequential(self.layers)
        else:
            self.model = tf.keras.Sequential([
                tf.keras.layers.InputLayer(input_shape=(self.num_stations, self.num_features)),
                tf.keras.layers.Conv1D(filters=12, kernel_size=3, activation='relu'),
                tf.keras.layers.AveragePooling1D(pool_size=2),
                tf.keras.layers.Flatten(),
                tf.keras.layers.Dense(18, activation='relu'),
                tf.keras.layers.Dense(12, activation='relu'),
                tf.keras.layers.Dense(18, activation='relu'),
                tf.keras.layers.Dense(self.calc_num_lines(), activation='sigmoid'),
            ])

        # Create Pygad model
        self.keras_ga = pygad.kerasga.KerasGA(
            self.model,
            self.num_solutions
        )

        logger.info("Created TF & KerasGA models")

    def train(self, save=False):
        """
        Train NN with genetic algorithm, save best solution
        """
        initial_population = self.keras_ga.population_weights
        self.ga_instance = pygad.GA(
            self.num_generations,
            self.num_parents_mating,
            initial_population=initial_population,
            fitness_func=self.fitness,
            on_generation=self.report_generation,
            mutation_probability=self.mutation_probability,
            mutation_type=self.mutation_type,
            parallel_processing=self.parallel_processing,
        )

        start = time.time()
        self.ga_instance.run()
        logger.info(f'Training took {time.time() - start} seconds')

        # Save ga_instance to file
        if save:
            timestamp = dt.now().strftime("%d-%m-%Y_%H-%M-%S")
            self.ga_instance.save(f'{MODELS_FOLDER}/{timestamp}_ga_instance')

        logger.info('Trained GA model')

    def load_instance_file(self, filename):
        self.ga_instance = pygad.load(filename)
        logger.info(f'Loaded pygad model from {filename}')

    # HELPERS ---
    def calc_num_lines(self):
        """
        Determine number of all possible lines.

        Using handshake theorem, if there are `n` nodes, there is at most
        `n(n-1)/2` edges (complete connected graph).
        """
        n = self.num_stations
        return n * (n-1) // 2

    def create_lines(self, predictions):
        """
        Generate lines based on predictions
        If probability >0.5, create line

        ex. `[ 0.2, 0.12, 0.6, ...]`
        Create lines `[1->4]`
        """
        lines = []

        for i in range(self.num_stations):
            for j in range(i+1, self.num_stations):
                p_index = i + j - 1

                # Create lines
                if (predictions[p_index] > 0.5):
                    lines.append([i, j])

        return lines

    def score(self, predictions, data_input, cur_lines=None):
        """
        Determine score of predictions based on passengers delivered
        and number of lines used
        - predictions: NN predicted lines (ex. [1,2])
        - data_input: matrix with station & passenger data

        Bad things
        1 miss alot of passengers *
        2 make alot of lines
        3 high line lengths
        4 high passenger path cost
        """
        if not cur_lines: cur_lines = self.create_lines(predictions)
        sim = Simulate(data_input, cur_lines)
        sim.compute_network_cost()
        map_unit = 1 / ((self.map_height + self.map_width)/2)  

        if self.score_func:
            return self.score_func(
                sim.num_passengers,
                sim.missed_passengers(),
                len(cur_lines),
                sim.total_passenger_path_cost,
                sim.total_line_length,
                map_unit,
            )

        factors = [
            [10, sim.num_passengers],
            [-1, len(cur_lines)],
            [-2*map_unit, sim.total_passenger_path_cost],
            [-1*map_unit, sim.total_line_length],
        ]
        
        # return 1/sum([f[0] * f[1] for f in factors])
        return sum([f[0] * f[1] for f in factors])

    def fitness(self, solution, sol_id):
        """
        Determine fitness of given solution for all data inputs
        - solution: pygad solution
        - sol_id: pygad solution ID
        Return fitness over all data inputs
        """
        # Generate predictions
        model_weights_matrix = pygad.kerasga.model_weights_as_matrix(
            model=self.model,
            weights_vector=solution
        )
        self.model.set_weights(weights=model_weights_matrix)
        predictions = self.model.predict(self.data_inputs, verbose=0)

        # Sum scores for all data inputs
        total_score = 0
        for p, prediction in enumerate(predictions):
            total_score += self.score(prediction, self.data_inputs[p])

        return total_score

    def report_generation(self, ga_instance):
        """
        Report fitness results for each generation
        - ga_instance: pygad instance
        """
        generation = ga_instance.generations_completed
        fitness = ga_instance.best_solution()[1]
        logger.info(f'Generation = {generation}, Fitness = {fitness}')
    
    def predict_single(self):
        """
        Make predictions for single data input
        """
        solution, _, _ = self.ga_instance.best_solution()
        model_weights_matrix = pygad.kerasga.model_weights_as_matrix(
            model=self.model,
            weights_vector=solution
        )
        self.model.set_weights(weights=model_weights_matrix)
        prediction = self.model.predict(
            self.data_inputs,
            verbose=0
        )[0]

        logger.debug('Prediction')
        logger.debug(prediction)

        best_line = self.create_lines(prediction)
        sim = Simulate(self.data_inputs[0], best_line)
        sim.compute_network_cost()
        sim_result = sim.to_dict()
        sim_result.update({
            "metrics": {
                "score": int(self.score(prediction, self.data_inputs[0])),
                "total_passengers": int(sim.total_passengers),
                "missed_passengers": int(sim.missed_passengers()),
                "num_lines": len(best_line),
                "line_length": sim.total_line_length,
                "path_length": sim.total_passenger_path_cost
            }
        })

        return sim_result

    def visualize_solution(self, max_visualizations=10):
        """
        Visualize subway networks generated from best solution
        - max_visualizations: Max graphs to generate
        """
        # Generate predictions from best solution
        solution, solution_fitness, solution_idx = self.ga_instance.best_solution()
        model_weights_matrix = pygad.kerasga.model_weights_as_matrix(
            model=self.model,
            weights_vector=solution
        )
        self.model.set_weights(weights=model_weights_matrix)
        predictions = self.model.predict(self.data_inputs, verbose=0)

        logger.info(f'Best Fitness = {solution_fitness}')
        total_missed_passengers = 0
        total_lines = 0
        total_line_length = 0
        total_path_length = 0

        # Visualize subway networks
        for p, prediction in enumerate(predictions):
            best_line = self.create_lines(prediction)
            sim = Simulate(self.data_inputs[p], best_line)
            sim.compute_network_cost()

            total_missed_passengers += sim.missed_passengers()
            total_lines += len(best_line)
            total_line_length += sim.total_line_length
            total_path_length += sim.total_passenger_path_cost

            if p != 4: continue

            sim.visualize(f'NN_solution_{p+1}')

            metrics = {
                "desc": "NN prediction",
                "network": p+1,
                "lines": str(sim.lines),
                "stations": [st.__str__() for st in sim.stations],
                "score": int(self.score(prediction, self.data_inputs[p])),
                "missed_passengers": int(sim.missed_passengers()),
                "num_lines": len(best_line),
                "line_length": sim.total_line_length,
                "path_length": sim.total_passenger_path_cost
            }
            logger.debug(json.dumps(metrics, indent=4))

            best_line = [[1,5],[2,3],[2,0],[3,0],[3,4],[3,5],[4,5]]
            sim = Simulate(self.data_inputs[p], best_line)
            sim.compute_network_cost()

            sim.visualize(f'josh_rajykins_solution_{p+1}')

            metrics = {
                "desc": "Josh/rajykins prediction",
                "network": p+1,
                "lines": str(sim.lines),
                "stations": [st.__str__() for st in sim.stations],
                "score": int(self.score(None, self.data_inputs[p], best_line)),
                "missed_passengers": int(sim.missed_passengers()),
                "num_lines": len(best_line),
                "line_length": sim.total_line_length,
                "path_length": sim.total_passenger_path_cost
            }
            logger.debug(json.dumps(metrics, indent=4))

        map_unit = (self.map_width + self.map_height) / 2

        avg_missed = total_missed_passengers/len(self.data_inputs)
        avg_lines = total_lines/len(self.data_inputs)
        avg_line_length = total_line_length/len(self.data_inputs)/map_unit
        avg_path_length = total_path_length/len(self.data_inputs)/map_unit

        logger.info(f'Average missed passengers = {avg_missed}')
        logger.info(f'Average num lines = {avg_lines}')
        logger.info(f'Average total line length = {avg_line_length}')
        logger.info(f'Average path length = {avg_path_length}')

        return [avg_missed, avg_lines, avg_line_length, avg_path_length]


if __name__ == "__main__":
    model = Model()
    model.load_data()
    model.create_model()
    model.train(save=True)
    model.visualize_solution()
