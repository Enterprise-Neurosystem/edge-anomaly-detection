from flask import Flask, render_template, Response, request, session

# TODO: use dash instead of flask
# from dash import dash, html, dcc
# from dash.dependencies import Input, Output

import json
from managers.preprocess_data_manager import PreprocessDataManager
import pandas as pd

# reload
app = Flask(__name__)
app.secret_key = "my_secret_key"
# 'application' reference required for wgsi / gunicorn
# https://docs.openshift.com/container-platform/3.11/using_images/s2i_images/python.html#using-images-python-configuration
application = app


@app.route("/")
def main():
    return render_template("main.html")


@app.route("/generateData", methods=["GET", "POST"])
def generate_data():
    #  col_name, points_group_size, regress_group_size, anomaly_std_factor are all obtained
    # from the form in the user interface.

    data_source = request.form.get("radio", "synthetic")

    if data_source == "csv":
        col_name = request.form.get("col_name", "")

        uploaded_file = request.files["csv_input"]
        if uploaded_file.filename != "":
            uploaded_file.save(uploaded_file.filename)
            file_name = uploaded_file.filename
        else:
            file_name = "static/casing1.csv"
        session["file_name"] = file_name
    else:
        col_name = request.form.get("sensor_list", "")
        session["file_name"] = ""

    regression_group_size = int(request.form.get("batch", "80"))
    points_group_size = 1
    anomaly_std_factor = int(request.form.get("stds_list", "4"))
    max_window_size = request.form.get("window_size", 100)
    speed_up = request.form.get("speed_up", 1)

    print("Data Generated")

    session["data_source"] = data_source
    session["col_name"] = col_name
    session["reg_group_size"] = regression_group_size
    session["anomaly_std_threshold"] = anomaly_std_factor
    session["window_size"] = max_window_size
    session["speed_up"] = speed_up

    return Response()


@app.route("/graphData")
def graphData():
    print(session["data_source"])
    print(session["col_name"])
    print(session["reg_group_size"])
    print(session["anomaly_std_threshold"])
    print(session["window_size"])
    print(session["speed_up"])
    pdm = PreprocessDataManager(
        session["data_source"],
        session["reg_group_size"],
        1,
        session["col_name"],
        session["anomaly_std_threshold"],
        session["window_size"],
        session["speed_up"],
        csv_file_name=session["file_name"],
    )
    pdm.process_point()
    return Response(pdm.process_point(), mimetype="text/event-stream")


if __name__ == "__main__":
    app.run(debug=True, port=8080, host="0.0.0.0")  # nosec

# run gunicorn manually
# TODO: move to readme
# gunicorn wsgi:application -b 0.0.0.0:8080
