import psycopg2
from psycopg2 import pool

class ConnectionPoolSingleton:
    """Singleton class that makes a pooled connection to a Postgres database"""
    __connection_pool = None
    __INSTANCE = None
    
    @staticmethod
    def __getInstance():
        """Checks for an instance of ConnectionPoolSingleton. If there is none, it will automatically call the __init__ method"""
        if ConnectionPoolSingleton.__INSTANCE == None:
            ConnectionPoolSingleton()
            
        return ConnectionPoolSingleton().__INSTANCE
    
    def __init__(self):
        """Enforces that there can only be one instance of ConnectionPoolSingleton"""
        if ConnectionPoolSingleton.__INSTANCE != None:
            raise Exception("Cannot create more than one instance of this class")
        else:
            ConnectionPoolSingleton.__connection_pool = psycopg2.pool.ThreadedConnectionPool(1,100, 
                                                                                             host='postgresql.test-db01.svc.cluster.local',
                                                                                             user='user82M',
                                                                                             password='q2s2gLeojWQFMkBa', 
                                                                                             database ='sampledb')
    @staticmethod
    def getConnectionPool():
        """Instantiates ConnectionPoolSingleton and returns a pooled connection"""
        ConnectionPoolSingleton.__getInstance()
        return ConnectionPoolSingleton.__connection_pool
    