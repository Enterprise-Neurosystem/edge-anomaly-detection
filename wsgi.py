from flask import Flask, render_template, Response, request
from managers.preprocess_data_manager import PreprocessDataManager

app = Flask(__name__)

# 'application' reference required for wgsi / gunicorn
# https://docs.openshift.com/container-platform/3.11/using_images/s2i_images/python.html#using-images-python-configuration
application = app

@app.route('/')
def main():
    return render_template('main.html')


@app.route('/generateData')
def generate_data():
    #  col_name, points_group_size, regress_group_size, anomaly_std_factor are all obtained
    # from the form in the user interface.

    regression_group_size = request.args.get('regression_size')
    anomaly_std_factor = request.args.get('std_threshold')
    plot_scrolling_size = request.args.get('plot_scrolling_size')
    #pts_per_sec = request.args.get('pts_per_sec')

   # regression_group_size = 40
    #anomaly_std_factor = 4
    #points_group_size = 1
    col_name = 'pressure'

    file_name = 'static/data/casing1.csv'
    #file_name = 'static/slice0_scaled.csv'

    pdm = PreprocessDataManager(regression_group_size,
                                plot_scrolling_size, col_name, anomaly_std_factor,
                                csv_file_name=file_name)
    pdm.process_point()
    return Response(pdm.process_point(), mimetype='text/event-stream')


if __name__ == '__main__':
    app.run(debug=True, port=8080, host="0.0.0.0")  # nosec

# run gunicorn manually
# TODO: move to readme
# gunicorn wsgi:application -b 0.0.0.0:8080
