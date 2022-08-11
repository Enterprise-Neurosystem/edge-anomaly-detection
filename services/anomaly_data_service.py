import pandas as pd
import psycopg2

from services.connection_pool_singleton import ConnectionPoolSingleton


class AnomalyDataService:
    """Executes and returns queries from a Postgres database"""

    @staticmethod
    def get_all_data():
        """Returns all rows from table and reads it into a pandas dataframe"""
        GET_ALL_ROWS_SQL = "SELECT * FROM prediction"
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        cursor = conn.cursor()
        try:
            cursor.execute(GET_ALL_ROWS_SQL)
            anomaly = pd.read_sql_query(GET_ALL_ROWS_SQL, conn)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            return anomaly
        finally:
            cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_sensor_25():
        """Returns values from sensor 25 and reads them into a pandas dataframe"""
        GET_SENSOR_25_SQL = "SELECT sensor_25 FROM anomaly"
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        cursor = conn.cursor()
        try:
            cursor.execute(GET_SENSOR_25_SQL)
            sensor_25 = pd.read_sql_query(GET_SENSOR_25_SQL, conn)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            return sensor_25
        finally:
            cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_sensor_11():
        """Returns values from sensor 11 and reads them into a pandas dataframe"""
        GET_SENSOR_11_SQL = "SELECT sensor_11 FROM anomaly"
        pool = ConnectionPoolSingleton.getConnectionPool()
        conn = pool.getconn()
        cursor = conn.cursor()
        try:
            cursor.execute(GET_SENSOR_11_SQL)
            sensor_11 = pd.read_sql_query(GET_SENSOR_11_SQL, conn)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            return sensor_11
        finally:
            cursor.close()
            pool.putconn(conn)

    @staticmethod
    def get_min_max(col_name, groupname):
        """Returns the minimum and maximum value of a sensor for a given value of groupname"""
        GET_MIN_SQL = "SELECT MIN({}) FROM anomaly WHERE groupname = {}".format(
            col_name, groupname
        )
        GET_MAX_SQL = "SELECT MAX({}) FROM anomaly WHERE groupname = {}".format(
            col_name, groupname
        )
        pool = ConnectionPoolSingleton().getConnectionPool()
        conn = pool.getconn()
        cursor = conn.cursor()
        try:
            cursor.execute(GET_MIN_SQL)
            min_value = cursor.fetchone()
            cursor.execute(GET_MAX_SQL)
            max_value = cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
        else:
            print("The minimum value is:{}".format(min_value[0]))
            print("The maximum value is:{}".format(max_value[0]))
        finally:
            cursor.close()
            pool.putconn(conn)
