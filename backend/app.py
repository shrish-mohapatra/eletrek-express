"""

Flask API service to expose NN model
Uses pretrained models on randomly generated subway configs

"""

import os
from flask import Flask, request
from flask_cors import CORS

from backend.model import Model

app = Flask(
    __name__,
    static_folder='../client/dist',
    static_url_path='/',
    instance_relative_config=True,
)
cors = CORS(
    app,
    resources={r"/*": {"origins": "*"}, "/*": {"headers": "*"}}
)

best_model_file = 'models/06-04-2023_14-41-48_ga_instance'

@app.route('/')
def index():
    '''Serve static react app'''
    return app.send_static_file('index.html')


@app.route('/generate', methods=['POST'])
def create_lines():
    '''
    Generate subway lines based on station & passenger data
    1. Generate subway station based on request arg
    2. Apply pretrained model to generate lines

    ### Request Args
    - max_passengers: Number of passengers per network (default=10)
    - map_width: Width of subway network (in pixels) (default=500)
    - map_height: Height of subway network (in pixels) (default=500)
    - space_between: Minimum space between stations (in pixels) (default=70)
    - seed: Seed for data input generation

    ### Response
    - nodes: JSON rep of stations & passengers
    - lines: AI generated lines between nodes
    - metrics: {num_lines, missed_passengers, line_length, path_length}
    '''
    # Retrieve model args based on request w/ defaults
    model_args = {
        'max_passengers': 10,
        'map_width': 500,
        'map_height': 500,
        'space_between': 70,
        'seed': None,
        'num_samples': 1,
    }
    user_args = request.get_json()
    user_args = {
        label: value
        for label, value in user_args.items()
        if label in model_args
    }
    model_args.update(user_args)

    # Generate station config based on args
    model = Model(**model_args)
    model.load_data()
    model.create_model()
    model.load_instance_file(os.path.abspath(best_model_file))

    print(model.data_inputs)
    return model.predict_single()
