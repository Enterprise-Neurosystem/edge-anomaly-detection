from csv import DictReader
import time
import sys

class SynthesizeDataManager:
    """Used as a  data source that periodically yields timeseries data points
    """
    @staticmethod
    def csv_line_reader(file_name, col_name, points_per_sec):
        """Use data from a csv to periodically yield a row of data
        :param file_name: Name of csv file as source of data
        :param col_name:  Name of column to extract
        :return: none
        ..notes:: This static method has no return.  Instead, it yields a row of data that has been read from
        a data source.
        """
        try:
            with open(file_name, 'r') as read_obj:
                dict_reader = DictReader(read_obj)
                for row in dict_reader:
                    #print("row in reader: {}".format(row))
                    time.sleep(1 / points_per_sec)
                    yield [row['timestamp'], row[col_name]]
        except KeyError as ex:
            print("Key error in row: {}".format(row))
            print("Data file must have a first column with name: 'timestamp' and a second column named '{}'".format(col_name))

