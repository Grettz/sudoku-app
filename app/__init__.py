import os
import json
import random
from flask import Flask, render_template, jsonify, send_file, current_app

# create and configure the app
app = Flask(__name__)
# app.config.from_mapping(
#     SECRET_KEY='dev',
#     # DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
# )

"""     if test_config is None:
    # load the instance config, if it exists, when not testing
    app.config.from_pyfile('config.py', silent=True)
else:
    # load the test config if passed in
    app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass """
    
from .config import Config

@app.route('/')
def home():
    dist_dir = current_app.config['DIST_DIR']
    entry = os.path.join(dist_dir, 'index.html')
    return send_file(entry)

@app.route('/sudoku')
def sudoku():
    return render_template('sudoku.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/data/sudokus')
def data_sudokus():
    with open('sudokus.json') as jsonfile:
        sudokus = []
        for line in jsonfile:
            data = {}
            data['sudoku'] = json.loads(line)
            sudokus.append(data)

        sudoku = random.choice(sudokus)
        return jsonify(sudoku)

#    return app