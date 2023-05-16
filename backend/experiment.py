"""

Experiment different NN configurations

"""

import matplotlib.pyplot as plt
import numpy as np
from loguru import logger
import tensorflow as tf

from backend.model import Model

EXPERIMENT_FOLDER = 'backend/experiments'

class Experiment:
    def __init__(self, test_epochs=5):
        """
        Experiment NN configurations
        - test_epochs: Number of iterations to rerun test config
        """
        self.test_epochs = test_epochs

    # Tests ---
    def test_layers(self):
        """
        Test different Tensorflow layers
        """
        logger.info("Testing layers")

        sample_model = Model()
        return self.root_test(
            test_key='layers',
            tests={
                "dense-1": [
                    tf.keras.layers.InputLayer(input_shape=(
                        sample_model.num_stations, sample_model.num_features)),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(
                        sample_model.calc_num_lines(), activation='sigmoid'),
                ],
                "dense-3": [
                    tf.keras.layers.InputLayer(input_shape=(
                        sample_model.num_stations, sample_model.num_features)),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(18, activation='relu'),
                    tf.keras.layers.Dense(12, activation='relu'),
                    tf.keras.layers.Dense(
                        sample_model.calc_num_lines(), activation='sigmoid'),
                ],
                "cnn": [
                    tf.keras.layers.InputLayer(input_shape=(
                        sample_model.num_stations, sample_model.num_features)),
                    tf.keras.layers.Conv1D(
                        filters=12, kernel_size=3, activation='relu'),
                    tf.keras.layers.AveragePooling1D(pool_size=2),
                    tf.keras.layers.Flatten(),
                    tf.keras.layers.Dense(18, activation='relu'),
                    tf.keras.layers.Dense(12, activation='relu'),
                    tf.keras.layers.Dense(
                        sample_model.calc_num_lines(), activation='sigmoid'),
                ],
            },
        )

    def test_scoring(self):
        def positive_sum(
            passengers,
            missed_passengers,
            lines,
            path_length,
            line_length,
            map_unit,
        ):
            factors = [
                [10, passengers],
                [-1, lines],
                [-2*map_unit, path_length],
                [-1*map_unit, line_length],
            ]
            return sum([f[0] * f[1] for f in factors])

        def negative_sum(
            passengers,
            missed_passengers,
            lines,
            path_length,
            line_length,
            map_unit,
        ):
            factors = [
                [10, missed_passengers],
                [1, lines],
                [2/map_unit, path_length],
                [1/map_unit, line_length],
            ]
            return sum([-1 * f[0] * f[1] for f in factors])

        def negative_reciprocal(
            passengers,
            missed_passengers,
            lines,
            path_length,
            line_length,
            map_unit,
        ):
            factors = [
                [10, missed_passengers],
                [1, lines],
                [2/map_unit, path_length],
                [1/map_unit, line_length],
            ]
            return 1/sum([1 * f[0] * f[1] for f in factors])

        self.root_test(
            test_key='score_func',
            tests={
                'positive sum': positive_sum,
                'negative sum': negative_sum,
                'negative reciprocal': negative_reciprocal,
            },
        )

    # Helpers ---
    def root_test(
        self,
        test_key,
        tests,

        num_samples=10,
        num_generations=10,
        num_parents_mating=10,
        num_solutions=20,
        seed=68,
    ):
        """
        Run tests based on configs
        - test_key: GA Model param to modify
        - tests: dictionary with (key=test label, value=argument to supply)
        """
        results = {
            test_label: [0 for _ in range(4)]
            for test_label in tests.keys()
        }

        # Run tests
        for test_label, test in tests.items():
            logger.info(f"Testing config {test_label}")
            for _ in range(self.test_epochs):
                model_args = {
                    "num_samples": num_samples,
                    "num_generations": num_generations,
                    "num_parents_mating": num_parents_mating,
                    "num_solutions": num_solutions,
                    "seed": seed,

                    test_key: test
                }

                model = Model(**model_args)
                model.load_data()
                model.create_model()
                model.train()
                result = model.visualize_solution()

                # Add results to corresponding entry in dict
                results[test_label] = [
                    sum(i) for i in zip(results[test_label], result)]

        # Calculate average results
        results = {
            test_label: [metric/self.test_epochs for metric in result]
            for test_label, result in results.items()
        }

        self.graph_results(test_key, results)

    def graph_results(self, test_key, results):
        """
        Graph results using Matplotlib
        - test_key: GA Model param to modify (used to create title)
        - results: Results generated from `root_test()`

        Results are formatted like so:
        ```
        {
            'test_label1': [
                <num missed passengers>,
                <num lines>,
                <total path length>,
                <total line length>
            ],
            ...
        }
        ```
        """
        plt.clf()

        xaxis = np.array(list(results.keys()))
        line_colors = [
            ('missed passengers', '#9400D3'),
            ('num lines', '#228B22'),
            ('path length', '#8B0000'),
            ('line length', '#008080'),
        ]

        # Plot results
        for i, lc in enumerate(line_colors):
            new_results = [
                results[test_label][i]
                for test_label in results.keys()
            ]
            plt.plot(
                xaxis,
                new_results,
                label=lc[0],
                color=lc[1]
            )
        
        plt.legend()
        plt.xlabel(test_key)

        title = f"Testing different {test_key}"
        filename = title.replace(' ', '_')
        plt.title(title)
        plt.savefig(f'{EXPERIMENT_FOLDER}/{filename}.png')
        logger.info(f"Generated {filename}")


if __name__ == "__main__":
    exp = Experiment(1)
    exp.test_layers()
    exp.test_scoring()
    # results = {
    #     't1': [10,20,30,40],
    #     't2': [10,20,30,40],
    #     't3': [10,20,30,40],
    # }
    # results = {
    #     test_label: [metric/10 for metric in result]
    #     for test_label, result in results.items()
    # }
    # exp.graph_results("layers", results)