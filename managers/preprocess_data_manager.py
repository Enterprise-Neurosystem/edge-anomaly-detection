import numpy as np
import json
from managers.synthesize_data_manager import SynthesizeDataManager


class PreprocessDataManager:
    """Prepares a timeseries data point for graphing
    The class uses a generator that it receives from a data source.  A timeseries data point is received
    and the method, process_point() is used to process the point.   When the point has been processed, it
    yields a message that contains json data that will be consumed.

    """

    def __init__(
        self,
        data_source,
        regress_group_size,
        points_group_size,
        col_name,
        anomaly_std_factor,
        max_window_size,
        speed_up,
        csv_file_name=None,
    ):
        """
        :param regress_group_size:  Size in data points of how many points will be included in the linear regression
        calculation.
        :type regress_group_size: int
        :param points_group_size: How many data points should be consumed in one batch.  Currently only the value
        of 1 is used.
        :param col_name: Name of data column that holds the data to be processed
        :type: string
        :param anomaly_std_factor: Used to define the threshold that defines an anomaly.  This factor will
        be multiplied by the data's STD to define the threshold.
        :type: int
        :param csv_file_name: Name of csv file to be used as the data source
        :type: string
        """
        self.row_counter = 0
        self.data_source = data_source
        self.regress_plot_size = regress_group_size  # Number of points used to calculate linear regression line
        self.points_group_size = points_group_size  # Not used in this first version
        self.col_name = col_name  # col name of feature to plot
        self.file_name = csv_file_name
        self.regress_buffX = (
            []
        )  # Fixed size buffer.  Size is limited to value of self.regress_plot_size
        self.regress_buffY = []
        self.anomaly_std_factor = (
            anomaly_std_factor  # Defines how many STD that determine an anomaly
        )
        self.speed_up = speed_up
        self.max_window_size = max_window_size

    def process_point(self):
        """Process one point and put calculated data into a json format.
        This function uses a generator that yields a timeseries data point from a data source.  When the data source
        yields a timeseries data point in the form of the pair: (timestamp, value), the data point is put into a buffer
        that consists of two parallel arrays: self.regress_buffX and self.regress_buffY. This buffer's size is maintained
        at the size specified by self.regress_plot_size.  If the buffer is filled, the oldest by timestamp is removed,
        and the new data point is appended, thereby maintaining a fixed size buffer.  When the buffer is filled, the
        following process is put into action:
        (1)  Calculate the linear regression line for the points currently in the buffer.
        (2)  Calculate the coordinates of the two endpoints of the regression line.  The starting endpoint corresponds
             to the oldest point in the buffer, while the ending endpoint corresponds to the newest point in the buffer.
        (3)  Calculate the STD and MEAN for the points in the buffer.
        (4)  For the newest endpoint in the buffer, calculate the y difference between the data point and the regression
             line.  This y difference will be used in the plot.
        (5)  Compare the y difference with the value (self.anomaly_std_factor * STD).  If the value is outside
             this calculation, set the plot color to 'red'.

        The above calculated data is wrapped into a Dictionary and is converted to JSON.  This JSON is then yielded
        to the listener on the browser side, where it is plotted.

        :return: none
        ..notes:: This function has no return.  Instead, it yields events that allow the listener (in this case, a
        javascript EventSource object) to consume the data in the messages.
        ..notes::  The yielded JSON from this function is generic so that any renderer can make the plots.

        """
        x_old_idx = 0
        y_percent_diff_old = 0
        plot_color = "green"
        graphRange = [0, 1]

        sdm = SynthesizeDataManager()
        # This generator yields when one point is available from the data source
        if self.data_source == "csv":
            gen = sdm.csv_line_reader(
                self.file_name, self.col_name, self.speed_up
            )  # this is a generator
        elif self.data_source == "postgres":
            gen = sdm.load_sensor(self.col_name, self.speed_up)
        else:
            gen = sdm.synthesize_data(self.col_name, self.speed_up)

        row = next(gen, None)  # list of two strings
        graphRange = sdm.return_range()
        json_data = {"range": graphRange}

        yield "event: initialize\ndata: " + json.dumps(
            json_data
        ) + "\n\n"  # Initialize plot

        while True:
            # print("rowcounter: {}".format(self.row_counter))
            # Use the generator's next() with a param of None.  If the generator is out of data, next() will
            # return None.
            row = next(gen, None)  # list of two strings
            if row is None:
                print("row is none")
                # print("Job Finished")
                # Generator is exhausted, yield message "jobfinished"
                yield "event: jobfinished\ndata: " + "none" + "\n\n"
                break
            else:
                timestamp = row[0]
                sensor_val = row[1]
                self.regress_buffX.append(timestamp)  # append new pt into buffer
                self.regress_buffY.append(sensor_val)
                if self.row_counter >= self.regress_plot_size:
                    self.regress_buffX.pop(0)  # if buffer is full, pop oldest val
                    self.regress_buffY.pop(0)
                    # Get linear regression line based on points in regress buffer (regress_buffX, regress_buffY)
                    fit = self.get_fit_function(self.regress_buffX, self.regress_buffY)

                    regress_start_idx = len(self.regress_buffX) - self.regress_plot_size
                    # Get endpoints of regression line for plotting
                    (
                        x_start_p,
                        x_end_p,
                        y_start_p,
                        y_end_p,
                    ) = self.__get_endpoints_for_regr_line(fit, regress_start_idx)

                    y_percent_diffs = self.__calc_percent_diffs(
                        fit
                    )  # Get all percent diffs for all points in regress buffer
                    std_for_buffer = np.std(
                        y_percent_diffs
                    )  # STD of percent diffs in regress buffer
                    mean_for_buffer = np.mean(
                        y_percent_diffs
                    )  # mean of percent diffs in regress buffer

                    # Get percent diff for the current point, which is at the end of the regress_buffX
                    y_percent_diff = self.calculate_percent_diff_for_curr_point(
                        (len(self.regress_buffX) - 1), fit
                    )
                    if y_percent_diff < (
                        mean_for_buffer - self.anomaly_std_factor * std_for_buffer
                    ) or (
                        y_percent_diff
                        > (mean_for_buffer + self.anomaly_std_factor * std_for_buffer)
                    ):
                        plot_color = "red"
                    y_percent_diff_new = y_percent_diff

                    # add [x_old_point, x_new_point] and [y_percent_diff_old, y_percent_diff_new] and plot_color to json
                    x_old_p = self.regress_buffX[len(self.regress_buffX) - 2]
                    x_new_p = self.regress_buffX[len(self.regress_buffX) - 1]
                    json_data = self.create_json(
                        timestamp,
                        sensor_val,
                        x_start_p,
                        x_end_p,
                        y_start_p,
                        y_end_p,
                        x_old_p,
                        x_new_p,
                        y_percent_diff_old,
                        y_percent_diff,
                        plot_color,
                        self.row_counter,
                        self.max_window_size,
                    )
                    # print("Regress slope: {}   Regress intspt: {}".format(fit[0],fit[1]))
                    print("Server json data: {} ".format(json_data))
                    y_percent_diff_old = y_percent_diff_new
                    plot_color = "green"
                    self.row_counter = self.row_counter + self.points_group_size
                    yield "event: update\ndata: " + json.dumps(json_data) + "\n\n"
                else:
                    # We are here because the buffer window is not yet full.  The buffer window consists of
                    # self.regress_buffX and self.regress_buffY.  This condition only happens
                    # when the app starts.  The buffer window is used to calculate the running
                    # regression line.  So while we are waiting for the buffer window to fill, we still plot
                    # the sensor data as points.
                    self.row_counter = self.row_counter + self.points_group_size
                    json_data = self.create_json(
                        timestamp,
                        sensor_val,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        max_window_size=self.max_window_size,
                    )
                    yield "event: update\ndata: " + json.dumps(json_data) + "\n\n"
                    next(gen)

    def __get_endpoints_for_regr_line(self, regr_fit, regress_start_index):
        """Private function for calculating endpoints of a regression line

        :param regr_fit: The linear regression object
        :type: ndarray as returned from numpy.polyfit()
        :param regress_start_index: index of starting point in buffer,  usually 0
        :return: x and y values of start and end point of regression line as constrained by the buffer size.
        :type: tuple
        """
        x_start_idx = regress_start_index
        x_start_p = self.regress_buffX[x_start_idx]
        y_start_p = regr_fit[0] * x_start_idx + regr_fit[1]
        x_end_idx = len(self.regress_buffX) - 1
        x_end_p = self.regress_buffX[x_end_idx]
        y_end_p = x_end_idx * regr_fit[0] + regr_fit[1]
        return x_start_p, x_end_p, y_start_p, y_end_p

    def __calc_percent_diffs(self, regr_fit):
        """Calculate y diffs between data points and regression line for all points in the buffer

        :param regr_fit: The numpy.polyfit()
        :return: Array of errors, where error is the difference between each point's y value and the corresponding
        y value of the regression line
        :type:  ndarray
        """
        y_errors = []
        point_counter = 0
        for point in self.regress_buffY:
            regress_Y = point_counter * regr_fit[0] + regr_fit[1]
            # Make the difference calculation dimensionless by dividing by regress_Y
            y_errors.append((float(point) - regress_Y) / regress_Y)
            point_counter += 1
        return np.array(y_errors)

    def calculate_percent_diff_for_curr_point(self, x_index, regr_fit):
        """Calculate y diff at the x value (x_index) between the data point and the regression line

        :param x_index: Index of the current point ( Index is relative the points in the buffer).  This index ranges
        from 0 to len(self.regress_buffX) -1
        :param regr_fit: regr_fit: The numpy.polyfit()
        :return: The ratio of the y distance between the data point and the regression line and the y value of the
        regression line.
        :type:: float
        """
        regress_Y = regr_fit[0] * x_index + regr_fit[1]

        return 100 * (float(self.regress_buffY[x_index]) - regress_Y) / regress_Y

    def get_fit_function(self, xarr, yarr):  # pass regress_buffX and regress_buffY
        """Get the numpy.polyfit() as calculated by the data currently in the buffer

        :param xarr: array of x values of points in the buffer
        :param yarr: array of y values of points in the buffer
        :return: numpy.polyfit()
        :type:: ndarray
        """
        xarr_temp = xarr.copy()
        yarr_temp = yarr.copy()  # list of strings representing floats

        xarr_temp.pop()  # Remove current point since it may be an anomaly.
        yarr_temp.pop()
        float_list = []  # Must convert yarr_temp to numpy array of floats.
        for item in yarr_temp:
            float_list.append(float(item))
        yarr_converted = np.array(float_list)
        # Make temp array of integers that serve as x index for points in the buffer.
        numericX = np.arange(len(xarr_temp))
        fit = np.polyfit(numericX, yarr_converted, 1)  # deg of 1

        return fit

    def create_json(
        self,
        timestamp,
        sensor_val,
        x1,
        x2,
        y1,
        y2,
        x_old_p,
        x_new_p,
        y_percent_diff_old,
        y_percent_diff,
        plot_color,
        row_counter,
        max_window_size,
    ):
        """Put all parameters into a JSON string

        :param timestamp:
        :param sensor_val:
        :param x1:
        :param x2:
        :param y1:
        :param y2:
        :param x_old_p:
        :param x_new_p:
        :param y_percent_diff_old:
        :param y_percent_diff:
        :param plot_color:
        :param row_counter:
        :return: Json string
        """
        plot_dict = {
            "plotpoint": [timestamp, sensor_val],
            "regress": {"xs": [x1, x2], "ys": [y1, y2]},
            "calc": {
                "x1": x_old_p,
                "x2": x_new_p,
                "y_diff1": y_percent_diff_old,
                "y_diff2": y_percent_diff,
                "plot_color": plot_color,
                "row_counter": row_counter,
                "max_window_size": max_window_size,
            },
        }
        return plot_dict

    def init_plot(self, graphRange):
        """Currently not used"""
        print("PreprocessDataManager.init_plot()")
        json_data = self.create_json(graphRange)
        yield "event: initialize\ndata: " + json.dumps(json_data) + "\n\n"

    def stop_plot(self):
        """Currently not used"""
        print("PreprocessDataManager.stop_plot()")
        yield "event: stop\ndata: " + "none" + "\n\n"
