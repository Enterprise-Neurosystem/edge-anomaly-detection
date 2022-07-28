from flask import Flask, render_template, Response, request

# TODO: use dash instead of flask
#from dash import dash, html, dcc
#from dash.dependencies import Input, Output

import json
from graph_manager import GraphManager as GM
from data.data_prep import load_sensor
import pandas as pd


app = Flask(__name__)

# 'application' reference required for wgsi / gunicorn
# https://docs.openshift.com/container-platform/3.11/using_images/s2i_images/python.html#using-images-python-configuration
application = app

@app.route('/')
def main():
    return render_template('main.html', col_list=['sensor_25', 'sensor_11', 'sensor_36', 'sensor_34'])

@app.route('/generate-graph', methods=['GET', 'POST'])
def generate_graph():
    chosen_sensor = request.form.get('sensor_list', 'sensor_25')
    print(chosen_sensor)
    #json.loads(chosen_sensor).get('sensor')
    df, anomalies = load_sensor(chosen_sensor)
    buffer = GM.plot_data(df, anomalies)
    return buffer

if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")  # nosec

# run gunicorn manually
# TODO: move to readme
# gunicorn wsgi:application -b 0.0.0.0:8080
