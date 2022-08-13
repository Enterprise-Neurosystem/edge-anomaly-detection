from flask import Flask, render_template, Response, request
from managers.preprocess_data_manager import PreprocessDataManager
from utilities.data_file_manager import DataFileManager
from os.path import join
app = Flask(__name__)

# 'application' reference required for wgsi / gunicorn
# https://docs.openshift.com/container-platform/3.11/using_images/s2i_images/python.html#using-images-python-configuration
application = app

@app.route('/')
def main():
    file_names = DataFileManager.get_file_names_in_path('static/data')
    return render_template('main.html', filenames=file_names)


@app.route('/generateData')
def generate_data():
    """
    regress_group_size, anomaly_std_factor, plot_scrolling_size are all obtained
    from the  URL parameters appended to '/generateData' (The parameters are
    appended to the base url in the messageHandler.js
    """

    regression_group_size = request.args.get('regression_size')
    anomaly_std_factor = request.args.get('std_threshold')
    plot_scrolling_size = request.args.get('plot_scrolling_size')
    file_name_only = request.args.get('filename')
    points_per_sec = int(request.args.get('points_per_sec'))
    col_name = 'pressure'
    path = 'static/data'
    file_name = join(path, file_name_only)

    pdm = PreprocessDataManager(regression_group_size,
                                plot_scrolling_size, col_name, anomaly_std_factor, points_per_sec,
                                csv_file_name=file_name)
    pdm.process_point()
    return Response(pdm.process_point(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")  # nosec

# run gunicorn manually
# TODO: move to readme
# gunicorn wsgi:application -b 0.0.0.0:8080
