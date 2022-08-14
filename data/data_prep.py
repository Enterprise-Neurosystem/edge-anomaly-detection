from services.anomaly_data_service import AnomalyDataService
from io import BytesIO
import base64
import pandas as pd
import matplotlib.dates as mdates
import numpy as np


def calculatePerCentDiffs(xDataVals, yDataVals, regSlope, regIntersept):
    yErrors = []
    for point in zip(xDataVals, yDataVals):
        regY = regSlope * point[0] + regIntersept
        yErrors.append(100 * (point[1] - regY) / (point[1] + 0.01))

    return np.array(yErrors)


# Calculate the per cent difference between one data value and its corresponding
# value as predicted by the regression line given by regSlope and regIntersept
def calculatePerCentDiff(xDataVal, yDataVal, regSlope, regIntersept):
    regY = regSlope * xDataVal + regIntersept
    return 100 * (yDataVal - regY) / regY


def find_anomalies(df):
    # Define anomaly as greater than anomalyDtdDevFactor * StandardDev
    anomalyStdDevFactor = 4
    # Define datetime window size
    datetimeWindowSize = 43
    # Get data as two numpy arrays: xvals and yvals
    xStrDates = df.iloc[:, 0]
    yVals = df.iloc[:, 1]

    # Convert dates as strings to dates as datetime.datetime values
    # dates_list = [dt.datetime.strptime(date, '%Y-%m-%d %H:%M:%S') for date in xStrDates]
    # Convert list of datetime.datetime values to ndarray of
    xVals = mdates.date2num(df.iloc[:, 0])

    fit = np.polyfit(np.array(xVals), np.array(yVals), deg=1)

    # Calculate std and mean
    yPerCentDiffs = calculatePerCentDiffs(xVals, yVals, fit[0], fit[1])
    std = np.std(yPerCentDiffs)
    mean = np.mean(yPerCentDiffs)

    anomalies = list()
    for diff, index in zip(yPerCentDiffs, df.index.values):
        if (diff < mean - anomalyStdDevFactor * std) or (
            diff > mean + anomalyStdDevFactor * std
        ):
            anomalies.append(index)

    print("**********************************")
    print(len(anomalies))
    print("**********************************")
    return anomalies


def load_sensor(sensor="sensor_25"):
    query = AnomalyDataService
    df_data = query.get_all_data()
    df_sensor = df_data[["sensortimestamp", sensor]]
    return df_sensor, find_anomalies(df_sensor)
